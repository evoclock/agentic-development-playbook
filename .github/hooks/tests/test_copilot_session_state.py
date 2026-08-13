from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOK_ROOT = ROOT / ".github" / "hooks"
sys.path.insert(0, str(HOOK_ROOT))

from copilot_session_state import hook_output, render_context, review_repo  # noqa: E402


class CopilotSessionStateTests(unittest.TestCase):
    def fixture_repo(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "fixture"], cwd=repo, check=True)
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=repo, check=True)
        return repo

    def test_clean_repo_is_reported(self):
        repo = self.fixture_repo()
        state = review_repo(repo)
        self.assertEqual(state["branch"], "main")
        self.assertEqual(state["status"], [])
        self.assertEqual(state["diff_stat"], "(clean)")

    def test_dirty_repo_paths_are_reported(self):
        repo = self.fixture_repo()
        (repo / "README.md").write_text("changed\n", encoding="utf-8")
        (repo / "notes.txt").write_text("new\n", encoding="utf-8")
        state = review_repo(repo)
        self.assertEqual(len(state["status"]), 2)
        context = render_context(state, {"source": "resume"})
        self.assertIn("Working tree: review required", context)
        self.assertIn("Session source: resume", context)
        self.assertNotIn(str(repo), context)

    def test_task_and_handover_state_are_reported(self):
        repo = self.fixture_repo()
        (repo / "TASK.md").write_text("Task ID: DEMO\nRole tag: #reviewer\n", encoding="utf-8")
        (repo / "TASKS.md").write_text("| DEMO | task | `ready for review` |\n", encoding="utf-8")
        (repo / "HANDOVER.md").write_text("Status: current\n", encoding="utf-8")
        context = render_context(review_repo(repo))
        self.assertIn("Task contract: present (TASK.md)", context)
        self.assertIn("Task register: present (TASKS.md)", context)
        self.assertIn("Handover: present (HANDOVER.md)", context)
        self.assertIn("Receipt sequence: /task-list-update then /handover", context)

    def test_output_is_native_additional_context(self):
        repo = self.fixture_repo()
        output = hook_output({"source": "new"}, repo=repo)
        self.assertEqual(set(output), {"additionalContext"})
        self.assertIn("SESSION STATE (read-only)", output["additionalContext"])

    def test_script_emits_json(self):
        script = HOOK_ROOT / "copilot_session_state.py"
        result = subprocess.run([sys.executable, str(script)], input='{"source":"new"}',
                                cwd=ROOT.parent, capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)
        self.assertIn("Branch:", output["additionalContext"])


if __name__ == "__main__":
    unittest.main()
