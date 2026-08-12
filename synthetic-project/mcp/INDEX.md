# Read-only MCP context server

`ops_context_server.py` is a small standard-library MCP server for the
recorded GitHub Copilot CLI walkthrough.

It exposes two read-only tools:

- `get_pipeline_context` — reads the project overview, runbook, demo ticket, or
  static manifest fixture;
- `list_evidence` — lists the tracked context files used by the walkthrough.

The server does not write files. It does not make network requests. It does not
accept arbitrary filesystem paths.

## DfE recording boundary

The default DfE recording does not register or run this server. It refers to MCP
as a reviewed, read-only context pattern only. Use the registration command
below only after a separate policy decision approves a live MCP test.

## Optional registration with Copilot CLI

Run this command from the repository root after reviewing the source:

```bash
copilot mcp add dsops-context -- python3 synthetic-project/mcp/ops_context_server.py
```

The command registers a local process. It does not install a package.
Use `/mcp` in Copilot CLI to inspect registered servers.

## Example request

The `get_pipeline_context` tool accepts one of:

```text
overview
runbook
ticket
fixture_manifest
```

For example, `{"item":"ticket"}` returns the tracked demo task that explains
the evaluation sample-size problem.

MCP provides reviewed context. It does not replace tests, artifact inspection,
or human review.
