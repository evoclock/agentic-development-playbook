from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from copilot_pretool_check import decision_for_payload  # noqa: E402


class CopilotPreToolTests(unittest.TestCase):
    def test_safe_command_returns_to_normal_permission_flow(self):
        self.assertEqual(decision_for_payload({"toolName": "bash", "toolArgs": {"command": "python3 -m unittest"}}), {})

    def test_push_is_denied(self):
        result = decision_for_payload({"toolName": "bash", "toolArgs": {"command": "git push origin main"}})
        self.assertEqual(result["permissionDecision"], "deny")
        self.assertIn("publication", result["permissionDecisionReason"])

    def test_fixture_write_is_denied(self):
        result = decision_for_payload({"toolName": "powershell", "toolArgs": {"command": "echo x > fixtures/run.json"}})
        self.assertEqual(result["permissionDecision"], "deny")

    def test_pascal_case_payload_is_supported(self):
        result = decision_for_payload({"tool_name": "bash", "tool_input": {"command": "npm install"}})
        self.assertEqual(result["permissionDecision"], "deny")

    def test_non_shell_tool_is_unchanged(self):
        self.assertEqual(decision_for_payload({"toolName": "view", "toolArgs": {}}), {})

    def test_invalid_payload_is_denied(self):
        self.assertEqual(decision_for_payload([])["permissionDecision"], "deny")

    def test_script_emits_json(self):
        script = ROOT / "scripts" / "copilot_pretool_check.py"
        result = subprocess.run([sys.executable, str(script)], input=json.dumps({"toolName": "bash", "toolArgs": {"command": "git push"}}),
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
