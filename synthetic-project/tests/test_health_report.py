from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pipeline_ops.health_report import evaluate_manifest, load_manifest, render_text  # noqa: E402


class HealthReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / "fixtures" / "run_manifest.json"

    def test_fixture_is_warning_for_auc(self):
        report = evaluate_manifest(load_manifest(self.path))
        self.assertEqual(report["status"], "warning")
        self.assertEqual(report["stages"], {"total": 5, "passed": 5, "warning": 0, "failed": 0})
        self.assertIn("WARN evaluate.auc: 0.790 < 0.800", render_text(report))

    def test_schema_error_fails(self):
        manifest = json.loads(self.path.read_text(encoding="utf-8"))
        manifest["stages"][1]["metrics"]["schema_errors"] = 2
        self.assertEqual(evaluate_manifest(manifest)["status"], "failed")

    def test_auc_above_threshold_is_healthy(self):
        manifest = json.loads(self.path.read_text(encoding="utf-8"))
        manifest["stages"][-1]["metrics"]["auc"] = 0.83
        self.assertEqual(evaluate_manifest(manifest)["status"], "healthy")

    def test_missing_manifest_field_is_rejected(self):
        manifest = json.loads(self.path.read_text(encoding="utf-8"))
        del manifest["dataset"]
        with self.assertRaisesRegex(ValueError, "dataset"):
            evaluate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
