#!/usr/bin/env python3
"""PreToolUse hook for mcp__dm20-protocol__party_resolve_action.

Enforces the Party Mode rule "lead with what the acting player did/said":
players never see each other's raw posts, so every PUBLIC narrative must show
the acting character's action before the world's response.

Blocks (exit 2, reason on stderr -> fed back to the DM) when a non-blank
narrative:
  1. never names the acting character within its opening (first ~300 chars), or
  2. the player's post contains a quoted line of dialogue and none of the
     quoted lines is carried into the narrative (verbatim or closely).

Allows everything else: blank narratives (OOC/private replies), actions the
hook can't find, and any internal error (a hook bug must never stall the game).
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

CAMPAIGNS = Path(__file__).resolve().parents[2] / "campaigns"
OPENING_CHARS = 300
PARTY_WORDS = {"party", "group", "everyone", "three", "trio", "you", "all"}
DIRECTOR_RE = re.compile(
    r"\b(dm|advance the story|move on|move onto|go ahead and|start session|end (the )?session|"
    r"let'?s kick|archiv\w*|recap)\b", re.I)  # OOC instructions to the DM, not in-scene actions
EXEMPT_RE = re.compile(r"\[lead-exempt:[^\]]+\]", re.I)
STOP = {"the", "and", "you", "your", "for", "with", "that", "this", "are", "was", "but", "not", "can", "our", "all"}


def words(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"['\u2019]s\b", "", text.lower())  # possessives: Mira's -> mira
    return re.findall(r"[a-z0-9]+", text)


def quoted_lines(text: str) -> list[str]:
    """Dialogue the player wrote, pairing quote marks in order (straight or curly)."""
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    parts = text.split('"')
    return [parts[i] for i in range(1, len(parts) - 1, 2) if len(words(parts[i])) >= 3]


def find_action(action_id: str):
    """Return (action, campaign_dir) from the most recently written actions.jsonl."""
    logs = sorted(CAMPAIGNS.glob("*/party/actions.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    for log in logs:
        for line in log.read_text(encoding="utf-8").splitlines():
            if f'"{action_id}"' not in line:
                continue
            rec = json.loads(line)
            if rec.get("id") == action_id:
                return rec, log.parent.parent
    return None, None


def character_aliases(campaign_dir: Path, player_id: str) -> list[str]:
    chars = json.loads((campaign_dir / "characters.json").read_text(encoding="utf-8"))
    extra_file = campaign_dir / "lead_aliases.json"
    extra = json.loads(extra_file.read_text(encoding="utf-8")) if extra_file.exists() else {}
    for ch in chars.values():
        if ch.get("id") == player_id:
            names = [ch.get("name", ""), ch.get("player_name") or ""]
            aliases = {a.lower() for a in extra.get(player_id, [])}
            for n in names:
                for w in words(n):
                    if len(w) >= 3 and w not in {"von", "van", "the", "n/a"}:
                        aliases.add(w)
            return sorted(aliases)
    return []


def all_pc_aliases(campaign_dir: Path) -> list[str]:
    chars = json.loads((campaign_dir / "characters.json").read_text(encoding="utf-8"))
    out: list[str] = []
    for ch in chars.values():
        out += character_aliases(campaign_dir, ch.get("id", ""))
    return out


def quote_carried(quote: str, narrative_words: list[str]) -> bool:
    """True if the line appears verbatim or closely paraphrased (>=50% of its content words)."""
    content = [w for w in words(quote) if len(w) >= 3 and w not in STOP]
    if not content:
        return True
    have = set(narrative_words)
    return sum(w in have for w in content) / len(content) >= 0.5


def check(tool_input: dict) -> str | None:
    narrative = (tool_input.get("narrative") or "").strip()
    if not narrative:
        return None  # OOC / private-only resolve: nothing broadcast
    if re.fullmatch(r"[*_\s]*\(.*\)[*_\s]*", narrative, flags=re.S):
        return None  # a purely parenthetical meta line, e.g. "*(The DM sends a private message.)*"
    if EXEMPT_RE.search(tool_input.get("dm_notes") or ""):
        return None  # deliberate, logged exception (e.g. a full scene reset after an OOC complaint)
    action, campaign_dir = find_action(tool_input.get("action_id", ""))
    if not action:
        return None
    if DIRECTOR_RE.search(action.get("text", "")) and not quoted_lines(action.get("text", "")):
        return None  # "advance the story", "start session 2", ...: a director command, nothing to restate
    problems = []

    aliases = character_aliases(campaign_dir, action.get("player_id", ""))
    opening = words(narrative[:OPENING_CHARS])
    action_words = words(action.get("text", ""))[:4]
    if any(w in ("we", "let", "lets", "our", "us") for w in action_words):
        # a whole-party declaration ("let's continue", "we set camp"): any PC or the group may lead
        aliases = sorted(set(aliases) | PARTY_WORDS | set(all_pc_aliases(campaign_dir)))
    if aliases and not any(a in opening for a in aliases):
        problems.append(
            f"the narrative doesn't name the acting character ({' / '.join(aliases)}) "
            f"in its opening — lead with what they did/said, THEN the response"
        )

    quotes = quoted_lines(action.get("text", ""))
    if quotes and not any(quote_carried(q, words(narrative)) for q in quotes):
        sample = quotes[0][:80]
        problems.append(
            f'the player wrote dialogue (e.g. "{sample}…") but none of it appears in the '
            f"narrative — quote or closely paraphrase their line before the reaction"
        )

    if problems:
        return (
            "Blocked by the 'lead with the player's action' rule (DM_LOOP.md): "
            + "; and ".join(problems)
            + ". Rewrite the narrative and resend. (Other players never see this player's post.) "
            "If this is a deliberate exception, put '[lead-exempt: <reason>]' in dm_notes."
        )
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        reason = check(payload.get("tool_input") or {})
    except Exception as exc:  # never block the game on a hook bug
        print(f"check_resolve_leads: skipped ({exc})", file=sys.stderr)
        return 0
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
