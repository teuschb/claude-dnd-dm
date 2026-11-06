#!/usr/bin/env python3
"""PreToolUse hook for mcp__dm20-protocol__party_resolve_action and party_push.

Enforces the DM_LOOP.md pre-send checklist items that kept slipping when they
were prose-only rules:

  1. Plain words: no jargon from the campaign's banned-word list
     (party/../narration_rules.json -> "banned_words"), in public narrative
     or private messages. No internal ids (act_/res_) anywhere a player sees.
     No "beat" used as a pacing term, and no DCs in public narrative.
  2. Positions (combat only, party_resolve_action): a public narrative must
     include a "where everyone is" list.
  3. Reactions (combat only, party_resolve_action): when a public narrative
     resolves an attack or save, dm_notes must say how PC reactions were
     handled ("reactions: none possible" / "reactions: offered to <PC>" / ...).

Exemptions, per check, go in dm_notes: [positions-exempt: why],
[words-exempt: why]. Blocks with exit 2 and a reason on stderr; any internal
error allows the call (a hook bug must never stall the game).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CAMPAIGNS = Path(__file__).resolve().parents[2] / "campaigns"

ID_RE = re.compile(r"\b(act|res)_\d+\b")
BEAT_RE = re.compile(r"\b(a|the|this|that|next|last|one|each|every|same|single)\s+beat\b", re.I)
DC_RE = re.compile(r"\bDC\s*\d+\b")
POSITIONS_RE = re.compile(r"where everyone is", re.I)
ROLL_RE = re.compile(r"\bhit for\b|\b(attack|save|check)\b[^():\n]{0,25}:\s*\d+\s*[+-]", re.I)
REACTIONS_RE = re.compile(r"\breactions?\s*:", re.I)


def campaign_for(tool_input: dict) -> Path | None:
    """The campaign that owns this action, else the most recently active one."""
    logs = sorted(CAMPAIGNS.glob("*/party/actions.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    action_id = tool_input.get("action_id") or ""
    if action_id:
        for log in logs:
            if f'"{action_id}"' in log.read_text(encoding="utf-8"):
                return log.parent.parent
    return logs[0].parent.parent if logs else None


def private_texts(tool_input: dict) -> list[str]:
    pm = tool_input.get("private_messages") or {}
    if isinstance(pm, str):
        try:
            pm = json.loads(pm)
        except json.JSONDecodeError:
            return [pm]
    return [str(v) for v in pm.values()] if isinstance(pm, dict) else []


def word_problems(public: str, private: list[str], banned: dict[str, str]) -> list[str]:
    problems = []
    seen = public + "\n" + "\n".join(private)
    for word, plain in banned.items():
        if re.search(rf"\b{re.escape(word)}\w*\b", seen, re.I):
            problems.append(f'"{word}" is on the banned-jargon list; say "{plain}" instead')
    if ID_RE.search(seen):
        problems.append("an internal id (act_/res_) is in player-facing text")
    if BEAT_RE.search(seen):
        problems.append('"beat" is used as a pacing term ("a beat of silence"); say "a moment" or cut it')
    if DC_RE.search(public):
        problems.append("a DC is shown in public narrative (never show the DC)")
    return problems


def check(tool_name: str, tool_input: dict) -> str | None:
    campaign_dir = campaign_for(tool_input)
    if not campaign_dir:
        return None
    rules_file = campaign_dir / "narration_rules.json"
    rules = json.loads(rules_file.read_text(encoding="utf-8")) if rules_file.exists() else {}
    notes = tool_input.get("dm_notes") or ""
    public = (tool_input.get("narrative") or "").strip()
    problems = []

    if "[words-exempt:" not in notes.lower():
        problems += word_problems(public, private_texts(tool_input), rules.get("banned_words", {}))

    state_file = campaign_dir / "game_state.json"
    in_combat = state_file.exists() and json.loads(state_file.read_text(encoding="utf-8")).get("in_combat")
    if in_combat and public and tool_name.endswith("party_resolve_action"):
        if not POSITIONS_RE.search(public) and "[positions-exempt:" not in notes.lower():
            problems.append(
                'combat is live but the narrative has no "Where everyone is" list '
                "(each PC and enemy, with rough distances)"
            )
        if ROLL_RE.search(public) and not REACTIONS_RE.search(notes):
            problems.append(
                "this resolves an attack or save in combat, but dm_notes doesn't say how PC "
                'reactions were handled. Add e.g. "reactions: none possible", "reactions: offered '
                'to <PC>, held", or "reactions: <PC> declined". If a PC could react and hasn\'t been '
                "asked, pause and ask them privately first"
            )

    if problems:
        return (
            "Blocked by the DM_LOOP.md pre-send checklist: "
            + "; ".join(problems)
            + ". Fix and resend. Deliberate exceptions: [words-exempt: why] or "
            "[positions-exempt: why] in dm_notes."
        )
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        reason = check(payload.get("tool_name") or "", payload.get("tool_input") or {})
    except Exception as exc:  # never block the game on a hook bug
        print(f"check_narration_rules: skipped ({exc})", file=sys.stderr)
        return 0
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
