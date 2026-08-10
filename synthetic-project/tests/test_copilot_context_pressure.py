from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from copilot_context_pressure import classify  # noqa: E402


class ContextPressureTests(unittest.TestCase):
    def test_normal_band(self):
        result = classify(59.9)
        self.assertEqual(result["band"], "NORMAL")
        self.assertTrue(result["substantive_work_allowed"])

    def test_checkpoint_band(self):
        result = classify(60)
        self.assertEqual(result["band"], "CHECKPOINT_REQUIRED")
        self.assertFalse(result["substantive_work_allowed"])

    def test_emergency_band(self):
        result = classify(90)
        self.assertEqual(result["band"], "EMERGENCY_CHECKPOINT")

    def test_unknown_is_conservative(self):
        result = classify(None)
        self.assertEqual(result["band"], "UNKNOWN")
        self.assertTrue(result["short_turn_only"])

    def test_cli_json(self):
        script = ROOT / "scripts" / "copilot_context_pressure.py"
        result = subprocess.run([sys.executable, str(script), "--percent", "90", "--json"],
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["band"], "EMERGENCY_CHECKPOINT")


if __name__ == "__main__":
    unittest.main()
