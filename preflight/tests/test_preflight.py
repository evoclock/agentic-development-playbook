from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT_ROOT = ROOT / "preflight"
EXAMPLE_ROOT = ROOT / "docs" / "examples" / "preflight-001"
HOOK_ROOT = ROOT / ".github" / "hooks"
SKILLS_ROOT = ROOT / ".github" / "skills"
ROUTER_SCRIPT = SKILLS_ROOT / "model-routing" / "model_router.py"
SECURITY_FIXTURES = HOOK_ROOT / "fixtures" / "security-review.json"

sys.path.insert(0, str(HOOK_ROOT))
sys.path.insert(0, str(PREFLIGHT_ROOT))

from copilot_pretool_check import decision_for_payload, security_review  # noqa: E402
from copilot_session_state import hook_output  # noqa: E402
from prepare_workspace import copy_fixture, initialize_git  # noqa: E402


SKILL_CONTRACTS = {
    "handover": ("## Required handover headings", "HANDOVER.md"),
    "model-routing": ("models.runtime.json", "TASK.md"),
    "pipeline-run-triage": ("HEALTHY", "REVIEW_REQUIRED"),
    "security-review": ("accept", "redact", "reject"),
    "task-list-update": ("## Required receipt", "TASKS.md"),
}


class SkillPreflightTests(unittest.TestCase):
    def fixture_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
        subprocess.run(
            ["git", "config", "user.email", "fixture@example.invalid"],
            cwd=repo,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "fixture"],
            cwd=repo,
            check=True,
        )
        (repo / "README.md").write_text("preflight fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
        subprocess.run(
            ["git", "commit", "-q", "-m", "fixture"],
            cwd=repo,
            check=True,
        )
        return repo

    def test_skill_documents_define_copilot_contracts(self):
        for skill, markers in SKILL_CONTRACTS.items():
            with self.subTest(skill=skill):
                path = SKILLS_ROOT / skill / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                frontmatter = text.split("---", 2)[1]
                self.assertIn(f"name: {skill}", frontmatter)
                self.assertRegex(frontmatter, r"(?m)^description:\s+\S")
                self.assertIn("## Copilot CLI procedure", text)
                self.assertTrue(
                    "## Boundaries" in text
                    or "## Configuration boundaries" in text
                )
                self.assertIn("TASKS.md", text)
                for marker in markers:
                    self.assertIn(marker, text)

        agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        instructions_text = (
            ROOT / ".github" / "copilot-instructions.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Do not commit or push", agents_text)
        self.assertIn("Stop before commit, push, merge, publication", instructions_text)
        for path in (ROOT / "AGENTS.md", ROOT / ".github" / "copilot-instructions.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("TASKS.md", text)

    def test_seeded_fixture_has_the_starting_files_only(self):
        for relative_path in (
            "README.md",
            "AGENTS.md",
            "TASKS.md",
            ".github/copilot-instructions.md",
            "src/sample.txt",
            "prepare_workspace.py",
        ):
            self.assertTrue((PREFLIGHT_ROOT / relative_path).is_file(), relative_path)
        self.assertFalse((PREFLIGHT_ROOT / "TASK.md").exists())
        self.assertFalse((PREFLIGHT_ROOT / "HANDOVER.md").exists())

    def test_frozen_snapshots_are_reader_only_examples(self):
        for relative_path in ("README.md", "TASK.md", "TASKS.md", "HANDOVER.md"):
            path = EXAMPLE_ROOT / relative_path
            self.assertTrue(path.is_file(), relative_path)
            text = path.read_text(encoding="utf-8")
            self.assertIn("Frozen snapshot", text, relative_path)
            self.assertIn("PREFLIGHT-001", text, relative_path)

    def test_preparation_builds_a_self_contained_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "workspace"
            copy_fixture(target)
            initialize_git(target)
            for relative_path in (
                "README.md",
                "AGENTS.md",
                "TASKS.md",
                ".github/copilot-instructions.md",
                ".github/skills/model-routing/SKILL.md",
                ".github/hooks/copilot_pretool_check.py",
                "preflight/tests/test_preflight.py",
                "preflight/evidence/healthy/health_report.json",
                "runbooks/10-skill-preflight.md",
            ):
                self.assertTrue((target / relative_path).is_file(), relative_path)
            self.assertFalse((target / "TASK.md").exists())
            self.assertFalse((target / "HANDOVER.md").exists())
            self.assertFalse((target / "docs" / "examples" / "preflight-001").exists())
            for relative_path in (
                ".github/skills/model-routing/models.raw.jsonl",
                ".github/skills/model-routing/models.runtime.json",
                ".github/skills/model-routing/models.assignments.json",
            ):
                self.assertFalse((target / relative_path).exists(), relative_path)
            head = subprocess.run(
                ["git", "-C", str(target), "rev-parse", "--verify", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertTrue(head.stdout.strip())

    def test_task_contract_routes_and_session_state_are_visible(self):
        repo = self.fixture_repo()
        task_path = repo / "TASK.md"
        task_path.write_text(
            "\n".join(
                [
                    "Task ID: PREFLIGHT-001",
                    "Role tag: #implementer",
                    "Goal: inspect a bounded fixture",
                    "Stopping point: return evidence without publication",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (repo / "TASKS.md").write_text(
            "| `PREFLIGHT-001` | Inspect fixture | `#implementer` |\n",
            encoding="utf-8",
        )
        runtime_path = repo / "models.runtime.json"
        runtime_path.write_text(
            json.dumps(
                {
                    "models": [
                        {
                            "id": "copilot-fast",
                            "label": "Copilot Fast",
                            "provider": "copilot",
                            "available": True,
                            "capabilities": ["implementation", "planning", "review"],
                            "efforts": ["medium", "high"],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        assignments_path = repo / "models.assignments.json"
        assignments_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "assignments": {
                        "implementation": {
                            "model": "copilot-fast",
                            "effort": "medium",
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

        routed = subprocess.run(
            [
                sys.executable,
                str(ROUTER_SCRIPT),
                "--task-file",
                str(task_path),
                "--runtime-models",
                str(runtime_path),
                "--assignments",
                str(assignments_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        result = json.loads(routed.stdout)
        self.assertEqual(result["task_id"], "PREFLIGHT-001")
        self.assertEqual(result["role"], "implementation")
        self.assertEqual(result["model_id"], "copilot-fast")
        self.assertEqual(result["effort"], "medium")
        self.assertEqual(result["task_source"], str(task_path))

        state_before_handover = hook_output({"source": "preflight"}, repo=repo)
        context = state_before_handover["additionalContext"]
        self.assertIn("Task contract: present (TASK.md)", context)
        self.assertIn("Task register: present (TASKS.md)", context)
        self.assertIn("Handover: missing (HANDOVER.md)", context)

        (repo / "HANDOVER.md").write_text(
            "# Handover\n\n## Current task\nPREFLIGHT-001\n",
            encoding="utf-8",
        )
        state_after_handover = hook_output({"source": "preflight"}, repo=repo)
        self.assertIn("Handover: present (HANDOVER.md)",
                      state_after_handover["additionalContext"])

    def test_pretool_hook_gates_history_without_writing_receipts(self):
        repo = self.fixture_repo()
        tasks_path = repo / "TASKS.md"
        tasks_path.write_text("# Task register\n", encoding="utf-8")
        before = tasks_path.read_text(encoding="utf-8")
        denied_without_receipt = decision_for_payload(
            {"toolName": "bash", "toolArgs": {"command": "git commit -m preflight"}},
            repo=repo,
        )
        self.assertEqual(denied_without_receipt["permissionDecision"], "deny")
        self.assertIn("Update TASKS.md", denied_without_receipt["permissionDecisionReason"])
        self.assertEqual(tasks_path.read_text(encoding="utf-8"), before)

        tasks_path.write_text(
            "\n".join(
                [
                    "# Task register",
                    "## Receipts",
                    "Files changed: none",
                    "Checks: preflight",
                    "Evidence: synthetic fixture",
                    "Next decision: human review",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        denied_with_receipt = decision_for_payload(
            {"toolName": "bash", "toolArgs": {"command": "git commit -m preflight"}},
            repo=repo,
        )
        self.assertEqual(denied_with_receipt["permissionDecision"], "deny")
        self.assertNotIn("Update TASKS.md", denied_with_receipt["permissionDecisionReason"])

    def test_security_and_pipeline_evidence_contracts(self):
        for case in json.loads(SECURITY_FIXTURES.read_text(encoding="utf-8")):
            with self.subTest(case=case["name"]):
                result = security_review(case["content"])
                self.assertEqual(result["decision"], case["decision"])
                for forbidden in case["absent"]:
                    self.assertNotIn(forbidden, result["content"])
                    self.assertNotIn(forbidden, json.dumps(result["findings"]))

        evidence_root = PREFLIGHT_ROOT / "evidence"
        healthy_report = json.loads(
            (evidence_root / "healthy" / "health_report.json").read_text()
        )
        warning_report = json.loads(
            (evidence_root / "warning" / "health_report.json").read_text()
        )
        self.assertEqual(healthy_report["status"], "HEALTHY")
        self.assertEqual(warning_report["status"], "WARNING")
        self.assertEqual(healthy_report["checks"][0]["observed"], 100)
        self.assertEqual(warning_report["checks"][0]["observed"], 20)
        self.assertEqual(healthy_report["checks"][0]["threshold"], 50)
        self.assertEqual(warning_report["checks"][0]["threshold"], 50)


if __name__ == "__main__":
    unittest.main()
