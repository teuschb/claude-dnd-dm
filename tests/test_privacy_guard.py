"""guard_campaign_privacy.py: ask before campaign data is pushed somewhere public.

Real git repos in a temp dir; a fake `gh` on PATH answers the visibility
lookup, so nothing touches the network.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

from helpers import FixtureProject

SCRIPT = "guard_campaign_privacy.py"
REMOTE = "https://github.com/example/campaigns.git"
FAKE_GH = """#!/bin/sh
echo "$@" >> "$FAKE_GH_LOG"
case "$FAKE_GH_VISIBILITY" in
  fail) exit 1 ;;
  *) echo "$FAKE_GH_VISIBILITY" ;;
esac
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.com",
                           "-c", "commit.gpgsign=false", *args],
                          check=True, capture_output=True, text=True).stdout


def init_repo(repo: Path, remote: str | None = REMOTE) -> None:
    git(repo, "init", "-q", "-b", "main")
    if remote:
        git(repo, "remote", "add", "origin", remote)


class PrivacyGuard(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = FixtureProject()
        self.addCleanup(self.fx.__exit__)
        bin_dir = self.fx.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(FAKE_GH)
        (bin_dir / "gh").chmod(0o755)
        self.gh_log = self.fx.tmp / "gh.log"
        self.env = {"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "FAKE_GH_LOG": str(self.gh_log),
                    "FAKE_GH_VISIBILITY": "PUBLIC"}
        # the project repo tracks its campaign data
        init_repo(self.fx.root)
        git(self.fx.root, "add", "-A")
        git(self.fx.root, "commit", "-qm", "fixture")

    def run_guard(self, command: str, visibility: str = "PUBLIC", via: str = "env"):
        payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
        r = self.fx.run_hook(SCRIPT, payload, via=via, env={**self.env, "FAKE_GH_VISIBILITY": visibility})
        self.assertEqual(r.returncode, 0, r.stderr)  # the guard never blocks, it only asks
        return json.loads(r.stdout)["hookSpecificOutput"] if r.stdout.strip() else None

    def assertAsks(self, out, *fragments: str) -> None:
        self.assertIsNotNone(out, "expected the guard to ask")
        self.assertEqual(out["permissionDecision"], "ask")
        for f in fragments:
            self.assertIn(f, out["permissionDecisionReason"])

    # -- pushes ------------------------------------------------------------------------
    def test_push_to_public_repo_asks(self) -> None:
        for via in ("env", "cwd"):
            with self.subTest(via=via):
                self.assertAsks(self.run_guard("git push", via=via), "example/campaigns is PUBLIC")
        self.assertIn("repo view example/campaigns", self.gh_log.read_text())

    def test_push_to_private_repo_is_silent(self) -> None:
        self.assertIsNone(self.run_guard("git push origin main", visibility="PRIVATE"))
        self.assertIsNone(self.run_guard("git push", visibility="INTERNAL"))

    def test_unconfirmed_visibility_asks(self) -> None:
        self.assertAsks(self.run_guard("git push", visibility="fail"), "couldn't confirm")

    def test_non_github_remote_asks(self) -> None:
        git(self.fx.root, "remote", "set-url", "origin", "git@gitlab.com:example/campaigns.git")
        self.assertAsks(self.run_guard("git push", visibility="PRIVATE"), "isn't on GitHub")

    def test_push_spellings_are_detected(self) -> None:
        for cmd in ("git -C . push", "cd x && git push", "GIT_TRACE=1 git push", "git -c a.b=c push origin",
                    "git push https://github.com/other/thing.git main"):
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(self.run_guard(cmd), cmd)

    def test_push_named_in_other_text_is_ignored(self) -> None:
        for cmd in ('git commit -m "push the fix"', "git log --grep push", "echo git push", "git status"):
            with self.subTest(cmd=cmd):
                self.assertIsNone(self.run_guard(cmd), cmd)

    def test_recorded_public_choice_is_silent(self) -> None:
        git(self.fx.root, "config", "dnd.campaignsPublic", "true")
        self.assertIsNone(self.run_guard("git push"))

    def test_untracked_campaign_data_is_silent(self) -> None:
        git(self.fx.root, "rm", "-rq", "--cached", "rpg")
        git(self.fx.root, "commit", "-qm", "untrack")
        self.assertIsNone(self.run_guard("git push"))

    def test_symlinked_campaigns_repo_is_checked(self) -> None:
        # campaigns/ moved to its own repo and symlinked back; the project repo tracks no campaign data
        store = self.fx.tmp / "campaign-store"
        shutil.move(str(self.fx.data / "campaigns"), store)
        init_repo(store, "https://github.com/example/private-campaigns.git")
        git(store, "add", "-A")
        git(store, "commit", "-qm", "store")
        (self.fx.data / "campaigns").symlink_to(store, target_is_directory=True)
        out = self.run_guard("git push")
        self.assertAsks(out, "campaign-store", "example/private-campaigns is PUBLIC")
        self.assertIsNone(self.run_guard("git push", visibility="PRIVATE"))

    # -- making repos public -------------------------------------------------------------
    def test_making_a_repo_public_asks(self) -> None:
        for cmd in ("gh repo create mine --public", "gh repo edit --visibility public",
                    "gh repo edit --visibility=public", "gh repo fork x/y --public"):
            with self.subTest(cmd=cmd):
                self.assertAsks(self.run_guard(cmd), "makes a repo public")
        self.assertIsNone(self.run_guard("gh repo create mine --private"))
        self.assertAsks(self.run_guard("cd x && gh repo create mine --public"), "makes a repo public")

    def test_gh_repo_public_named_in_other_text_is_ignored(self) -> None:
        # regression: a commit message describing the guard triggered it
        for cmd in ('git commit -m "test gh repo create x --public"',
                    "git commit -F - <<'EOF'\nguard tests: symlinked repos, gh repo\n"
                    "  create/edit/fork --public, opt-out\nEOF",
                    "echo gh repo edit --visibility public"):
            with self.subTest(cmd=cmd):
                self.assertIsNone(self.run_guard(cmd), cmd)

    # -- not a D&D project ------------------------------------------------------------------
    def test_project_without_campaign_data_is_silent(self) -> None:
        shutil.rmtree(self.fx.root / ".claude")  # data dir becomes <project>/dnd, which doesn't exist
        self.assertIsNone(self.run_guard("git push"))
        self.assertIsNone(self.run_guard("gh repo create mine --public"))


if __name__ == "__main__":
    unittest.main()
