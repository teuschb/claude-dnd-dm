# campaigns/

dm20-protocol stores each campaign here (`DM20_STORAGE_DIR` points at `rpg/dnd`).
`create_campaign` makes the folder; then copy in the starter files from
`../templates/` (see "Campaign Creation Workflow" in `../CLAUDE.md`).

Each campaign's `party/` folder (player link secrets, QR codes, the live feed) is
gitignored. Everything else is plain JSON/Markdown you can commit as the campaign
record.
