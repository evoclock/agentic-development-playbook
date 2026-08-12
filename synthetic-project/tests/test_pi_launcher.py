from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "start_pi_demo.sh"


class PiLauncherTests(unittest.TestCase):
    def run_fake(self, mode):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "pi"
            fake.write_text("#!/bin/sh\nprintf '%s\n' \"$@\"\n", encoding="utf-8")
            fake.chmod(0o755)
            env = {**os.environ, "PATH": f"{directory}:{os.environ['PATH']}"}
            return subprocess.run([str(SCRIPT), mode, "inspect the task"], cwd=ROOT,
                                  env=env, capture_output=True, text=True, check=False)

    def test_plan_mode_disables_tools(self):
        result = self.run_fake("plan")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--no-tools", result.stdout)
        self.assertNotIn("--approve", result.stdout)
        self.assertIn("pipeline-run-triage/SKILL.md", result.stdout)

    def test_work_mode_allowlists_tools(self):
        result = self.run_fake("work")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--tools", result.stdout)
        self.assertIn("read,bash,edit,write", result.stdout)

    def test_unknown_mode_is_rejected(self):
        result = subprocess.run([str(SCRIPT), "unknown"], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
