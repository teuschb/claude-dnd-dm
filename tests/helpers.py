"""Shared test helpers: fixture projects in temp dirs, hook runners, a tiny MCP client.

Every test works on a fresh copy of tests/fixtures/project, so nothing outside
a temp dir is ever written.
"""
from __future__ import annotations

import json
import os
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugin"
SCRIPTS = PLUGIN / "scripts"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "project"
DATA_REL = Path("rpg") / "dnd"          # the fixture's data dir, set in .claude/dnd-dm.json
CAMPAIGN = "Fixture Keep"

PREFIXES = {"plugin": "mcp__plugin_dnd-dm_dm20-protocol__", "project": "mcp__dm20-protocol__"}


def clean_env(**extra: str) -> dict[str, str]:
    """The current env without anything that could point a script at a real project."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_DATA", "DND_DM_DEBUG_LOG")
           and not k.startswith("DM20_")}
    env.update(extra)
    return env


class FixtureProject:
    """A throwaway copy of the fixture project. Use as a context manager."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="dnd-dm-test-")
        self.tmp = Path(self._tmp.name).resolve()
        self.root = self.tmp / "project"
        shutil.copytree(FIXTURE, self.root, symlinks=True)
        self.data = self.root / DATA_REL
        self.campaign = self.data / "campaigns" / CAMPAIGN

    def __enter__(self) -> "FixtureProject":
        return self

    def __exit__(self, *exc) -> None:
        self._tmp.cleanup()

    # -- campaign data -------------------------------------------------------
    def characters(self) -> dict:
        return json.loads((self.campaign / "characters.json").read_text(encoding="utf-8"))

    def pc(self, name: str) -> dict:
        return next(c for c in self.characters().values() if c["name"] == name)

    def add_action(self, action_id: str, player_id: str, text: str) -> None:
        log = self.campaign / "party" / "actions.jsonl"
        log.parent.mkdir(exist_ok=True)
        with log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"id": action_id, "player_id": player_id, "text": text,
                                 "status": "pending"}) + "\n")

    def set_combat(self, in_combat: bool) -> None:
        path = self.campaign / "game_state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["in_combat"] = in_combat
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    # -- running hooks -------------------------------------------------------
    def run_hook(self, script: str, payload: dict, *args: str, via: str = "env",
                 env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
        """Run a hook script with a JSON payload on stdin.

        via="env": project found from CLAUDE_PROJECT_DIR (how Claude Code runs hooks).
        via="cwd": project found from the payload's "cwd" only.
        """
        payload = dict(payload)
        run_env = clean_env(CLAUDE_PLUGIN_DATA=str(self.tmp / "plugin_data"))
        if via == "env":
            run_env["CLAUDE_PROJECT_DIR"] = str(self.root)
        else:
            payload["cwd"] = str(self.root)
        run_env.update(env or {})
        return subprocess.run([sys.executable, str(SCRIPTS / script), *args], input=json.dumps(payload),
                              capture_output=True, text=True, env=run_env, cwd=self.tmp, timeout=60)


def tool_payload(tool: str, tool_input: dict, prefix: str = "plugin", **extra) -> dict:
    return {"hook_event_name": "PreToolUse", "tool_name": PREFIXES[prefix] + tool,
            "tool_input": tool_input, "session_id": "test-session", **extra}


class MCPClient:
    """Minimal JSON-RPC-over-stdio client for an MCP server process."""

    def __init__(self, argv: list[str], cwd: Path, env: dict[str, str], stderr_path: Path,
                 timeout: float = 600) -> None:
        self.timeout = timeout
        self._stderr = open(stderr_path, "ab")
        self.proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=self._stderr, start_new_session=True)
        self._id = 0
        self._buf = b""

    def request(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        self._write({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}})
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            while b"\n" in self._buf:
                line, self._buf = self._buf.split(b"\n", 1)
                try:
                    msg = json.loads(line)
                except ValueError:
                    continue
                if msg.get("id") == self._id:
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error']}")
                    return msg["result"]
            if select.select([self.proc.stdout], [], [], 1)[0]:
                chunk = os.read(self.proc.stdout.fileno(), 65536)
                if not chunk:
                    raise RuntimeError(f"server exited during {method} (code {self.proc.poll()})")
                self._buf += chunk
        raise TimeoutError(method)

    def notify(self, method: str, params: dict | None = None) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def initialize(self) -> dict:
        info = self.request("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                           "clientInfo": {"name": "dnd-dm-tests", "version": "0"}})
        self.notify("notifications/initialized")
        return info

    def call(self, tool: str, **arguments) -> tuple[bool, str]:
        """Returns (is_error, text)."""
        res = self.request("tools/call", {"name": tool, "arguments": arguments})
        text = "\n".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        return bool(res.get("isError")), text

    def close(self) -> None:
        try:
            os.killpg(self.proc.pid, signal.SIGTERM)
            self.proc.wait(timeout=10)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        for pipe in (self.proc.stdin, self.proc.stdout, self._stderr):
            try:
                pipe.close()
            except OSError:
                pass

    def _write(self, msg: dict) -> None:
        self.proc.stdin.write((json.dumps(msg) + "\n").encode())
        self.proc.stdin.flush()


def start_dm20(project: Path, tmp: Path, timeout: float = 600) -> MCPClient:
    env = clean_env(CLAUDE_PROJECT_DIR=str(project), CLAUDE_PLUGIN_DATA=str(tmp / "plugin_data"),
                    DND_DM_DEBUG_LOG=str(tmp / "wrapper.log"))
    client = MCPClient([str(PLUGIN / "bin" / "dm20")], cwd=project, env=env,
                       stderr_path=tmp / "dm20.stderr", timeout=timeout)
    client.initialize()
    return client
