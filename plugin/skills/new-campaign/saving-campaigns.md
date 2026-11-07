(`<plugin root>` below is the plugin root path given in the `dnd-dm:new-campaign` SKILL.md; substitute it before running any command. `<data dir>` is the project's data dir.)

# Saving Campaigns

Campaigns are gitignored by default (the data dir's `.gitignore` is written from `<plugin root>/templates/data-dir.gitignore` when the plugin first creates the data dir), so a new campaign is **not backed up**. Backup matters for two things: losing the disk, and running the DM from more than one place (a phone or claude.ai/code web session works from a fresh clone and only sees campaigns that were pushed). Multiplayer doesn't need git: players connect to the DM's machine through their links.

If the data dir has no `.gitignore` (for example a data dir that existed before the plugin), write it from `<plugin root>/templates/data-dir.gitignore` before anything else. It always ignores `campaigns/*/party/`, `campaigns/*/voice_registry.yaml`, `campaigns/*/rulebooks/cache/` and `rulebook_cache/`.

Ask once per clone of the project (the answer is recorded in `git config dnd.campaignStorage`, which is local and never committed). Explain the consequences in plain words, and confirm with the human before creating any GitHub repo. Ask in this order:

**1. "Do you want a separate repo just for your campaign data?"** Recommended: the game data and the project stay apart.
- Create it **private**: `gh repo create dnd-campaigns --private`, then confirm `gh repo view dnd-campaigns --json visibility` says `PRIVATE`.
- Set it up outside this project (default `~/dnd-campaigns`) and symlink it in. dm20 creates `campaigns/` and `events/` on startup, so move anything already there. `<data dir>` is the project's D&D data dir:
  ```bash
  D=~/dnd-campaigns; mkdir -p "$D" && cd "$D" && git init -b main
  cp "<plugin root>/templates/campaign-data-repo.gitignore" .gitignore
  mkdir -p "<data dir>/campaigns" "<data dir>/events"
  mv "<data dir>/campaigns" "$D/campaigns" && mv "<data dir>/events" "$D/events"
  ln -s "$D/campaigns" "<data dir>/campaigns" && ln -s "$D/events" "<data dir>/events"
  git add -A && git commit -m "Campaign data" && git remote add origin <url from gh> && git push -u origin main
  ```
  Then restart Claude Code so dm20 picks up the moved folders. `git config dnd.campaignStorage separate` (in the project repo).
- Everything except `party/` is backed up, spoilers included: the arc and hidden notes are exactly what's worth keeping, and the repo is private. Commit and push from `~/dnd-campaigns` at session end.

**2. If not: "Keep it all in this project's repo, as a private repo?"** Check where the project's repo points. If it has a public remote, they can't make campaign data private by ignoring files alone: either make that repo private, or create a new private repo for the project (a GitHub *fork* of a public repo is always public):
```bash
git remote rename origin upstream          # keep pulling updates from the old remote
gh repo create <name> --private --source . --remote origin --push
```
Confirm it says `PRIVATE`, then ask: **back up the campaign data in it, or keep it on this machine only?**
- Back up: delete the "Campaign data" block (`campaigns` and `events`) from `<data dir>/.gitignore` and commit. `party/` stays ignored. `git config dnd.campaignStorage same-repo`.
- Local only: leave the ignore as is. `git config dnd.campaignStorage local`.

**3. If they don't want a private repo,** say plainly what public means: anyone can read the characters, the DM's secret arc and every spoiler in it, and the session notes, including the players themselves. Then ask once more: **keep campaigns gitignored (not backed up), or publish them?** Their answer is final; don't re-ask.
- Gitignored: `git config dnd.campaignStorage local`.
- Publish: delete the "Campaign data" block from `<data dir>/.gitignore`, then `git config dnd.campaignsPublic true` (the privacy hook skips repos marked this way) and `git config dnd.campaignStorage public`.

Sharing with a co-DM: keep the repo private and add them as a collaborator (`gh api -X PUT repos/<owner>/<repo>/collaborators/<user> -f permission=push`).

## The guard hook

`scripts/guard_campaign_privacy.py` runs before every Bash command. When a `git push` targets a public (or unverifiable) remote of a repo holding campaign data, or a `gh repo` command makes a repo public while campaign data is in git, it asks the human to approve and says what would become readable. It never blocks, and it skips a repo whose owner already chose public (`git config dnd.campaignsPublic true` in that repo). It checks the repo the data dir sits in and, if `campaigns` or `events` is a symlink, the repo the link resolves into.
