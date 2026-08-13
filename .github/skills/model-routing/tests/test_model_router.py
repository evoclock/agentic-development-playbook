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
    save_assignment,
    select_for_task,
    select_route,
    task_id_from_contract,
    task_tags_from_register,
    task_tags_from_contract,
    validate_config,
)


class ModelRouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = SKILL_ROOT / "models.json"
        cls.no_runtime_path = SKILL_ROOT / "test-no-runtime-models.json"
        cls.no_assignments_path = SKILL_ROOT / "test-no-assignments.json"
        cls.config = load_config(
            cls.config_path,
            runtime_models=cls.no_runtime_path,
            assignments=cls.no_assignments_path,
        )

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
            [sys.executable, str(script), "--list",
             "--runtime-models", str(self.no_runtime_path),
             "--assignments", str(self.no_assignments_path)],
            capture_output=True, text=True, check=True,
        )
        self.assertIn("local-coding", listed.stdout)
        selected = subprocess.run(
            [sys.executable, str(script), "--role", "planning", "--effort", "medium",
             "--runtime-models", str(self.no_runtime_path),
             "--assignments", str(self.no_assignments_path)],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(selected.stdout)["effort"], "medium")

    def test_cli_task_tags_and_interactive_selection(self):
        script = SKILL_ROOT / "model_router.py"
        tagged = subprocess.run(
            [sys.executable, str(script), "--task-id", "DEMO-002", "--role", "planning",
             "--tags", "ambiguous,python", "--runtime-models", str(self.no_runtime_path),
             "--assignments", str(self.no_assignments_path)],
            capture_output=True, text=True, check=True,
        )
        tagged_result = json.loads(tagged.stdout)
        self.assertEqual(tagged_result["matched_tag"], "ambiguous")

        task_only = subprocess.run(
            [sys.executable, str(script), "--task-id", "ROUTER-REVIEW-001",
             "--runtime-models", str(self.no_runtime_path),
             "--assignments", str(self.no_assignments_path)],
            capture_output=True, text=True, check=True,
        )
        task_only_result = json.loads(task_only.stdout)
        self.assertEqual(task_only_result["role"], "review")
        self.assertEqual(task_only_result["matched_tag"], "reviewer")

        interactive = subprocess.run(
            [sys.executable, str(script), "--interactive", "--task-id", "DEMO-002",
             "--role", "review", "--tags", "independent-review",
             "--runtime-models", str(self.no_runtime_path),
             "--assignments", str(self.no_assignments_path)],
            input="general-planner\nmedium\n", capture_output=True, text=True, check=True,
        )
        self.assertIn('"selection": "override"', interactive.stdout)
        self.assertIn('"task_id": "DEMO-002"', interactive.stdout)

    def test_cli_role_only_interactive_selection_and_filtered_list(self):
        script = SKILL_ROOT / "model_router.py"
        filtered = subprocess.run(
            [sys.executable, str(script), "--list", "--role", "implementation",
             "--runtime-models", str(self.no_runtime_path),
             "--assignments", str(self.no_assignments_path)],
            capture_output=True, text=True, check=True,
        )
        payload = json.loads(filtered.stdout)
        model_ids = {model["id"] for model in payload["models"]}
        self.assertIn("local-coding", model_ids)
        self.assertNotIn("review-specialist", model_ids)

        interactive = subprocess.run(
            [sys.executable, str(script), "--interactive", "--role", "implementation",
             "--runtime-models", str(self.no_runtime_path),
             "--assignments", str(self.no_assignments_path)],
            input="general-planner\nhigh\n", capture_output=True, text=True, check=True,
        )
        self.assertIn('"model_id": "general-planner"', interactive.stdout)
        self.assertIn('"effort": "high"', interactive.stdout)

    def test_config_can_be_loaded_from_a_user_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "models.json"
            path.write_text(self.config_path.read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual(
                len(load_config(
                    path,
                    runtime_models=self.no_runtime_path,
                    assignments=self.no_assignments_path,
                )["models"]),
                3,
            )

    def test_task_contract_selects_role_from_task_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "TASK.md"
            path.write_text(
                "Task ID: ROUTER-REVIEW-001\nRole tag: #reviewer #evidence\n",
                encoding="utf-8",
            )
            self.assertEqual(task_id_from_contract(path), "ROUTER-REVIEW-001")
            self.assertEqual(task_tags_from_contract(path, "ROUTER-REVIEW-001"), ["reviewer", "evidence"])
            result = select_for_task(self.config, "ROUTER-REVIEW-001", task_file=path)
            self.assertEqual(result["role"], "review")
            self.assertEqual(result["task_source"], str(path))

    def test_saved_assignments_drive_task_routes(self):
        with tempfile.TemporaryDirectory() as directory:
            assignments_path = Path(directory) / "models.assignments.json"
            save_assignment("review", "general-planner", "medium", assignments_path)
            config = load_config(
                self.config_path,
                runtime_models=self.no_runtime_path,
                assignments=assignments_path,
            )
            result = select_for_task(config, "ROUTER-REVIEW-001")
            self.assertEqual(result["model_id"], "general-planner")
            self.assertEqual(result["effort"], "medium")
            self.assertEqual(result["selection"], "tag")

    def test_cli_task_file_infers_id_and_uses_saved_assignment(self):
        script = SKILL_ROOT / "model_router.py"
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            task_path = directory_path / "TASK.md"
            assignments_path = directory_path / "models.assignments.json"
            task_path.write_text(
                "Task ID: CUSTOM-ROUTE-001\nRole tag: #reviewer #evidence\n",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable, str(script), "--role", "review",
                    "--model", "general-planner", "--effort", "medium",
                    "--save-assignment", "--assignments", str(assignments_path),
                    "--runtime-models", str(self.no_runtime_path),
                ],
                capture_output=True, text=True, check=True,
            )
            routed = subprocess.run(
                [
                    sys.executable, str(script), "--task-file", str(task_path),
                    "--assignments", str(assignments_path),
                    "--runtime-models", str(self.no_runtime_path),
                ],
                capture_output=True, text=True, check=True,
            )
            result = json.loads(routed.stdout)
            self.assertEqual(result["task_id"], "CUSTOM-ROUTE-001")
            self.assertEqual(result["task_source"], str(task_path))
            self.assertEqual(result["model_id"], "general-planner")
            self.assertEqual(result["effort"], "medium")

    def test_runtime_models_can_override_roster_and_realign_routes(self):
        runtime = {
            "models": [
                {
                    "id": "copilot-fast",
                    "label": "Copilot Fast",
                    "provider": "copilot",
                    "available": True,
                    "cost_tier": "low",
                    "capabilities": ["implementation", "planning", "review"],
                    "efforts": ["low", "medium", "high"],
                },
                {
                    "id": "copilot-review",
                    "label": "Copilot Review",
                    "provider": "copilot",
                    "available": True,
                    "cost_tier": "high",
                    "capabilities": ["review"],
                    "efforts": ["medium", "high", "max"],
                },
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            runtime_path = Path(directory) / "models.runtime.json"
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            config = load_config(
                self.config_path,
                runtime_models=runtime_path,
                assignments=self.no_assignments_path,
            )
            self.assertEqual({model["id"] for model in config["models"]}, {"copilot-fast", "copilot-review"})
            implementation = select_route(config, "implementation")
            planning = select_route(config, "planning")
            review = select_route(config, "review")
            self.assertEqual(implementation["model_id"], "copilot-fast")
            self.assertEqual(planning["model_id"], "copilot-fast")
            self.assertIn(review["model_id"], {"copilot-fast", "copilot-review"})


if __name__ == "__main__":
    unittest.main()
