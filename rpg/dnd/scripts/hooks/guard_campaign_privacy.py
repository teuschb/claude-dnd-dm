#!/usr/bin/env python3
"""PreToolUse hook for Bash: keep campaign data out of public repos.

This framework repo is public. Campaign files (characters, the secret arc,
session notes) belong in each campaign's own private repo, never here.
.gitignore already keeps campaigns/ and events/ out of the framework; this hook
backs it up for the git/gh commands Claude runs.

Blocks (exit 2, reason on stderr -> fed back to Claude) when a command:
  1. force-adds anything under campaigns/ or events/ (bypassing .gitignore),
  2. creates, forks or switches a repo to public from or about a campaign folder,
  3. commits or pushes while the framework repo tracks campaign files, or
  4. pushes while any campaign repo's remote is public or can't be confirmed
     private on GitHub.

Allows everything else, and any internal error in the checks for 1-3 (a hook
bug must never stall the game). Check 4 fails closed: an unverifiable remote
blocks the push and leaves the call to the human.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

DND = Path(__file__).resolve().parents[2]
ROOT = DND.parents[1]
CAMPAIGNS = DND / "campaigns"
SEG = r"[^;&|\n]*"  # stays within one shell command
FORCE_ADD_RE = re.compile(rf"\bgit\b{SEG}\badd\b{SEG}(\s-[a-zA-Z]*f\b|\s--force\b)")
PUBLIC_RE = re.compile(rf"\bgh\s+repo\s+(create|edit|fork)\b{SEG}(--public\b|--visibility[= ]public\b)")
COMMIT_OR_PUSH_RE = re.compile(rf"\bgit\b{SEG}\b(commit|push)\b")
PUSH_RE = re.compile(rf"\bgit\b{SEG}\bpush\b")
GITHUB_RE = re.compile(r"github\.com[:/]([^/]+)/([^/]+?)(\.git)?/?$")
HOW_TO = "See \"Saving a Campaign\" in rpg/dnd/CLAUDE.md."


def block(reason: str) -> None:
    print(f"Blocked to keep campaign data private: {reason} {HOW_TO}", file=sys.stderr)
    sys.exit(2)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, timeout=5).stdout.strip()


def touches_campaigns(command: str, cwd: str) -> bool:
    return "campaigns" in command or "events" in command or Path(cwd).resolve().is_relative_to(CAMPAIGNS)


def tracked_campaign_files() -> list[str]:
    files = git("-C", str(ROOT), "ls-files", "--", "rpg/dnd/campaigns", "rpg/dnd/events").splitlines()
    return [f for f in files if f != "rpg/dnd/campaigns/README.md"]


def remote_problem(repo: Path) -> str | None:
    url = git("-C", str(repo), "remote", "get-url", "origin")
    if not url:
        return None  # no remote, nothing to push to
    m = GITHUB_RE.search(url)
    if not m:
        return f"campaign repo '{repo.name}' pushes to {url}, which isn't GitHub, so it can't be checked as private."
    slug = f"{m.group(1)}/{m.group(2)}"
    try:
        out = subprocess.run(["gh", "repo", "view", slug, "--json", "visibility", "-q", ".visibility"],
                             capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return f"couldn't check whether {slug} (campaign '{repo.name}') is private: gh isn't available."
    visibility = out.stdout.strip().upper()
    if visibility in ("PRIVATE", "INTERNAL"):
        return None
    if visibility == "PUBLIC":
        return f"{slug} (campaign '{repo.name}') is PUBLIC. Make it private first: gh repo edit {slug} --visibility private."
    return f"couldn't confirm {slug} (campaign '{repo.name}') is private ({out.stderr.strip() or 'no answer from gh'})."


def main() -> None:
    data = json.load(sys.stdin)
    command = (data.get("tool_input") or {}).get("command") or ""
    cwd = data.get("cwd") or str(ROOT)

    try:
        if FORCE_ADD_RE.search(command) and touches_campaigns(command, cwd):
            block("force-adding campaign files would put them in the public framework repo.")
        if PUBLIC_RE.search(command) and touches_campaigns(command, cwd):
            block("campaign repos must be private. Use --private.")
        if COMMIT_OR_PUSH_RE.search(command):
            tracked = tracked_campaign_files()
            if tracked:
                block(f"the framework repo tracks campaign files ({', '.join(tracked[:3])}...). "
                      "Untrack them with git rm -r --cached rpg/dnd/campaigns rpg/dnd/events, "
                      "keeping campaigns/README.md.")
    except SystemExit:
        raise
    except Exception:
        pass

    if PUSH_RE.search(command) and CAMPAIGNS.is_dir():
        for repo in sorted(p for p in CAMPAIGNS.iterdir() if (p / ".git").exists()):
            problem = remote_problem(repo)
            if problem:
                block(f"{problem} If the human confirms it's private, they can run the push themselves.")


if __name__ == "__main__":
    main()
