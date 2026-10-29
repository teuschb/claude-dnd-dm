# campaigns/

dm20-protocol stores each campaign here (`DM20_STORAGE_DIR` points at `rpg/dnd`).
`create_campaign` makes the folder; then copy in the starter files from
`../templates/` (see "Campaign Creation Workflow" in `../CLAUDE.md`).

**Nothing in this folder is committed to the framework repo** (it's gitignored,
except this README). The framework repo is public, so campaign files kept in it
would be one push away from being published.

To keep a campaign's history in git, make the campaign folder its own
**private** repo (see "Saving a Campaign" in `../CLAUDE.md`). Each campaign's
`party/` folder (player link secrets, QR codes, the live feed) stays out of
that repo too.
