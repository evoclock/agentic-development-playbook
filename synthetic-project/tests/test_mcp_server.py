from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))

import ops_context_server  # noqa: E402


class McpContextTests(unittest.TestCase):
    def test_initialize_exposes_tools(self):
        response = ops_context_server.handle_request({"jsonrpc": "2.0", "id": 1,
                                                       "method": "initialize", "params": {}})
        self.assertEqual(response["result"]["serverInfo"]["name"], "dsops-context")
        self.assertIn("tools", response["result"]["capabilities"])

    def test_tools_are_read_only_context_tools(self):
        response = ops_context_server.handle_request({"jsonrpc": "2.0", "id": 2,
                                                       "method": "tools/list", "params": {}})
        self.assertEqual({tool["name"] for tool in response["result"]["tools"]},
                         {"get_pipeline_context", "list_evidence"})

    def test_ticket_context_is_available(self):
        response = ops_context_server.handle_request({
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "get_pipeline_context", "arguments": {"item": "ticket"}},
        })
        text = response["result"]["content"][0]["text"]
        self.assertIn("row retention", text)
        self.assertFalse(response["result"]["isError"])

    def test_unknown_item_is_an_error_result(self):
        response = ops_context_server.handle_request({
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "get_pipeline_context", "arguments": {"item": "private"}},
        })
        self.assertTrue(response["result"]["isError"])

    def test_stdio_protocol_returns_json_lines(self):
        script = ROOT / "mcp" / "ops_context_server.py"
        requests = "\n".join([
            json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
            json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}),
        ]) + "\n"
        result = subprocess.run([sys.executable, str(script)], input=requests,
                                capture_output=True, text=True, check=True)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([response["id"] for response in responses], [1, 2])


if __name__ == "__main__":
    unittest.main()
