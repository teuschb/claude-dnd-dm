#!/usr/bin/env python3
"""Print this Claude Code session's current context size, in tokens.

Every turn (including each loop wake-up) re-reads the whole conversation, so a
long-lived DM loop session gets more expensive with every pass. The party-mode
loop runs this on an idle pass and suggests a fresh session past ~120k.

Finds the transcript as ~/.claude/projects/*/<CLAUDE_CODE_SESSION_ID>.jsonl.
Prints one line and only counts, never transcript content. Exits 0 even when
the transcript can't be found, so it never breaks a loop pass.
"""
import glob
import json
import os


def main():
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    paths = glob.glob(os.path.expanduser(f"~/.claude/projects/*/{sid}.jsonl")) if sid else []
    if not paths:
        print("context size unknown (no CLAUDE_CODE_SESSION_ID transcript found)")
        return
    last, turns, seen = 0, 0, set()
    with open(paths[0]) as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message")
            if d.get("type") != "assistant" or not isinstance(m, dict):
                continue
            u = m.get("usage") or {}
            if not u or m.get("id") in seen:
                continue
            seen.add(m.get("id"))
            turns += 1
            last = sum(u.get(k, 0) or 0 for k in
                       ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    print(f"context now: {last // 1000}k tokens over {turns} turns")


if __name__ == "__main__":
    main()
