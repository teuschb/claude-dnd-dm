#!/usr/bin/env python3
"""SessionStart hook: put the always-on D&D ground rules into context.

Plain stdout from a SessionStart command hook is added to Claude's context.
Prints nothing unless the project is a D&D project (it has a data dir, or
.claude/dnd-dm.json), so the plugin is silent in every other project.
Never fails the session: any internal error prints nothing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dnd_paths  # noqa: E402

RULES = """\
D&D project detected (dnd-dm plugin). For any D&D work (running a session, creating a campaign, rules, levelling, Party Mode), load the `dnd-dm:dm` skill first; it points to the other dnd-dm skills.
Data dir (campaigns live here): {data}
Plugin root: {plugin}
Ground rules, always in force (full text in the `dnd-dm:dm` skill):
- Dice are never invented. Roll only with the d20-mcp `roll` tools (mcp__plugin_dnd-dm_d20-mcp__roll), never dm20's `roll_dice`. If d20-mcp is unavailable, say so before improvising or estimating a result.
- Never label content as improvised or prepared. Log every improvised NPC, place and motive in the campaign records. Never invent an outcome the dice or world state didn't produce; roll on IMPROV_TOOLKIT.md instead.
- Let it fail. Failed rolls fail for real and stand. Routine actions by competent characters just succeed. Never curate encounters toward safe or winnable outcomes.
- Announce advantage or disadvantage before rolling, and say why.
- Never reveal DCs, stakes tables or complication-die results. State what a failure would cost, in plain words, before a risky roll.
- Never auto-decline a held reaction. Keep it open however long it takes; a logged "owner OK" isn't proof it was resolved. Ask the player.
- The player drives; dice and world logic decide. Don't propose plot beats or steer toward a "good" story.
- Pause often: narrate in small chunks and check in on what the player wants next.
- At the end of each session, offer a debrief (which rolls were load-bearing, what they want more or less of).
- Rules content comes only from the SRD 5.2 sources (dm20 lookup, then the data dir's reference/ overrides, then the plugin's reference/). Never invent rules content.
"""


def main() -> None:
    payload = {}
    try:
        payload = json.load(sys.stdin)
    except Exception:
        pass
    root = dnd_paths.project_root(payload.get("cwd"))
    if not dnd_paths.is_dnd_project(root):
        return
    sys.stdout.write(RULES.format(data=dnd_paths.data_dir(root), plugin=dnd_paths.PLUGIN_ROOT))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
