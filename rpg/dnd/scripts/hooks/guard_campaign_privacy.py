#!/usr/bin/env python3
"""PreToolUse hook for Bash: ask before campaign data goes somewhere public.

Campaign data (characters, the DM's secret arc and other spoilers, session
notes) can live in this framework repo or in a separate campaign-data repo
symlinked in at rpg/dnd/campaigns (see "Saving Campaigns" in rpg/dnd/CLAUDE.md).
Either is fine. What this hook adds is friction before that data becomes
public by accident.

Asks the human to approve (permissionDecision "ask", with the reason) when a
command:
  1. runs `git push` while a repo holding campaign data has a remote that is
     public, or that can't be confirmed private on GitHub, or
  2. creates, forks or switches a repo to public while campaign data is in git.

A repo whose owner already chose to publish its campaigns
(`git config dnd.campaignsPublic true` in that repo) is skipped: the choice
was made once, at setup. Never blocks, and allows on any internal error (a hook
bug must never stall the game).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

DND = Path(__file__).resolve().parents[2]
ROOT = DND.parents[1]
SEG = r"[^;&|\n]*"  # stays within one shell command
ARG = r"""(?:"[^"]*"|'[^']*'|\S+)"""
# `git [global options] push`, at the start of a command (after ; && || | or
# VAR=val prefixes), so "push" inside a commit message or another subcommand's
# arguments doesn't match. Global options that take a value: -C, -c, --git-dir...
GIT_OPTS = rf"(?:\s+(?:-[Cc]\s+{ARG}|--(?:git-dir|work-tree|namespace|exec-path)\s+{ARG}|-{{1,2}}[\w-]+(?:=\S*)?))*"
PUSH_RE = re.compile(rf"(?:^|[;&|\n(]|\bthen\b|\bdo\b)\s*(?:\w+={ARG}\s+)*git{GIT_OPTS}\s+push\b")
URL_RE = re.compile(r"^(?:[\w+.-]+://|[\w.-]+@[\w.-]+:)")
PUBLIC_RE = re.compile(rf"\bgh\s+repo\s+(create|edit|fork)\b{SEG}(--public\b|--visibility[= ]public\b)")
GITHUB_RE = re.compile(r"github\.com[:/]([^/\s]+)/([^/\s]+?)(\.git)?/?$")
CONTENTS = "characters, the DM's secret arc and other spoilers, session notes"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, timeout=5).stdout.strip()


def campaign_repos() -> list[Path]:
    """Repos holding campaign data, minus those whose owner chose public."""
    repos = []
    if git("-C", str(ROOT), "ls-files", "--", "rpg/dnd/campaigns", "rpg/dnd/events"):
        repos.append(ROOT)
    link = DND / "campaigns"
    if link.is_symlink():
        top = git("-C", str(link.resolve()), "rev-parse", "--show-toplevel")
        if top and Path(top) != ROOT:
            repos.append(Path(top))
    return [r for r in repos if git("-C", str(r), "config", "--bool", "dnd.campaignsPublic") != "true"]


def push_targets(repo: Path, args: str) -> set[str]:
    """URLs the push could go to: raw URLs in the command, remotes named in it, else the default."""
    tokens = [t.strip("\"'") for t in re.findall(ARG, args)]
    urls = {t for t in tokens if URL_RE.match(t)}
    remotes = set(git("-C", str(repo), "remote").split())
    named = remotes & set(tokens)
    if not (urls or named):
        default = git("-C", str(repo), "rev-parse", "--abbrev-ref", "@{push}").split("/")[0]
        named = {default if default in remotes else "origin"} & remotes
    return urls | {git("-C", str(repo), "remote", "get-url", "--push", r) for r in named}


def visibility_problem(url: str) -> str | None:
    m = GITHUB_RE.search(url)
    if not m:
        return f"{url} isn't on GitHub, so it can't be checked as private"
    slug = f"{m.group(1)}/{m.group(2)}"
    try:
        out = subprocess.run(["gh", "repo", "view", slug, "--json", "visibility", "-q", ".visibility"],
                             capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return f"couldn't check whether {slug} is private (gh isn't available)"
    visibility = out.stdout.strip().upper()
    if visibility in ("PRIVATE", "INTERNAL"):
        return None
    if visibility == "PUBLIC":
        return f"{slug} is PUBLIC: anyone can read it"
    return f"couldn't confirm {slug} is private"


def ask(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


def main() -> None:
    command = (json.load(sys.stdin).get("tool_input") or {}).get("command") or ""
    pushing, publishing = PUSH_RE.search(command), PUBLIC_RE.search(command)
    if not (pushing or publishing):
        return
    repos = campaign_repos()
    if not repos:
        return

    if publishing:
        ask(f"This makes a repo public while campaign data is in git ({CONTENTS}). "
            "If this repo holds it, anyone will be able to read it, including your players. Approve only if that's intended.")

    problems = []
    for repo in repos:
        urls = push_targets(repo, command[pushing.end():].split("\n")[0].split("&&")[0].split(";")[0].split("|")[0])
        problems += [f"{repo.name}: {p}" for p in map(visibility_problem, sorted(urls - {""})) if p]
    if problems:
        ask(f"This push may publish campaign data ({CONTENTS}). " + "; ".join(problems) +
            ". Approve only if that's intended. To stop being asked, record the choice: "
            "git config dnd.campaignsPublic true (in that repo).")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        pass
