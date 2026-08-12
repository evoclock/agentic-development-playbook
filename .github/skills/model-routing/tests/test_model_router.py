from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(SKILL_ROOT))

from model_router import (  # noqa: E402
    load_config,
    roster,
    select_for_task,
    select_route,
    task_tags_from_register,
    validate_config,
)


class ModelRouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = SKILL_ROOT / "models.json"
        cls.config = load_config(cls.config_path)

    def test_roster_exposes_configured_models(self):
        models = roster(self.config)
        self.assertEqual({model["id"] for model in models}, {
            "local-coding", "general-planner", "review-specialist"
        })

    def test_default_routes_are_role_specific(self):
        implementation = select_route(self.config, "implementation")
        planning = select_route(self.config, "planning")
        review = select_route(self.config, "review")
        self.assertEqual((implementation["model_id"], implementation["effort"]), ("local-coding", "medium"))
        self.assertEqual((planning["model_id"], planning["effort"]), ("general-planner", "high"))
        self.assertEqual((review["model_id"], review["effort"]), ("review-specialist", "high"))

    def test_task_tags_select_a_role_route(self):
        result = select_for_task(
            self.config, "DEMO-002", "planning", tags=["ambiguous", "python"],
        )
        self.assertEqual(result["matched_tag"], "ambiguous")
        self.assertEqual(result["model_id"], "general-planner")
        self.assertEqual(result["selection"], "tag")
        self.assertEqual(result["tags"], ["ambiguous", "python"])

    def test_task_register_tags_select_roles_without_manual_role(self):
        expected = {
            "ROUTER-IMPLEMENT-001": ("implementation", "implementer"),
            "ROUTER-PLAN-001": ("planning", "planner"),
            "ROUTER-REVIEW-001": ("review", "reviewer"),
        }
        for task_id, (role, tag) in expected.items():
            with self.subTest(task_id=task_id):
                result = select_for_task(self.config, task_id)
                self.assertEqual(result["role"], role)
                self.assertEqual(result["matched_tag"], tag)
                self.assertIn(tag, result["tags"])

    def test_task_tags_can_be_read_from_a_supplied_register(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TASKS.md"
            path.write_text(
                "| `CUSTOM-001` | Review a route | `#reviewer #security` |\n",
                encoding="utf-8",
            )
            self.assertEqual(task_tags_from_register(path, "CUSTOM-001"), ["reviewer", "security"])
            result = select_for_task(self.config, "CUSTOM-001", task_register=path)
            self.assertEqual(result["role"], "review")
            self.assertEqual(result["matched_tag"], "reviewer")

    def test_task_without_matching_tag_uses_role_default(self):
        result = select_for_task(self.config, "DEMO-002", "review", tags=["routine"])
        self.assertIsNone(result["matched_tag"])
        self.assertEqual(result["model_id"], "review-specialist")
        self.assertEqual(result["selection"], "configured")

    def test_user_can_override_model_and_effort(self):
        result = select_route(self.config, "review", model_id="general-planner", effort="medium")
        self.assertEqual(result["model_id"], "general-planner")
        self.assertEqual(result["effort"], "medium")
        self.assertEqual(result["selection"], "override")

    def test_invalid_role_model_and_effort_are_rejected(self):
        with self.assertRaises(ValueError):
            select_route(self.config, "unknown")
        with self.assertRaises(ValueError):
            select_route(self.config, "implementation", model_id="review-specialist")
        with self.assertRaises(ValueError):
            select_route(self.config, "implementation", effort="high")

    def test_invalid_config_is_rejected(self):
        invalid = json.loads(json.dumps(self.config))
        invalid["routes"]["review"]["model"] = "missing"
        with self.assertRaises(ValueError):
            validate_config(invalid)

    def test_cli_lists_and_selects(self):
        script = SKILL_ROOT / "model_router.py"
        listed = subprocess.run(
            [sys.executable, str(script), "--list"],
            capture_output=True, text=True, check=True,
        )
        self.assertIn("local-coding", listed.stdout)
        selected = subprocess.run(
            [sys.executable, str(script), "--role", "planning", "--effort", "medium"],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(selected.stdout)["effort"], "medium")

    def test_cli_task_tags_and_interactive_selection(self):
        script = SKILL_ROOT / "model_router.py"
        tagged = subprocess.run(
            [sys.executable, str(script), "--task-id", "DEMO-002", "--role", "planning", "--tags", "ambiguous,python"],
            capture_output=True, text=True, check=True,
        )
        tagged_result = json.loads(tagged.stdout)
        self.assertEqual(tagged_result["matched_tag"], "ambiguous")

        task_only = subprocess.run(
            [sys.executable, str(script), "--task-id", "ROUTER-REVIEW-001"],
            capture_output=True, text=True, check=True,
        )
        task_only_result = json.loads(task_only.stdout)
        self.assertEqual(task_only_result["role"], "review")
        self.assertEqual(task_only_result["matched_tag"], "reviewer")

        interactive = subprocess.run(
            [sys.executable, str(script), "--interactive", "--task-id", "DEMO-002", "--role", "review", "--tags", "independent-review"],
            input="general-planner\nmedium\n", capture_output=True, text=True, check=True,
        )
        self.assertIn('"selection": "override"', interactive.stdout)
        self.assertIn('"task_id": "DEMO-002"', interactive.stdout)

    def test_config_can_be_loaded_from_a_user_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "models.json"
            path.write_text(self.config_path.read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual(len(load_config(path)["models"]), 3)


if __name__ == "__main__":
    unittest.main()
