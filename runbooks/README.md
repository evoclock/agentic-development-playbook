# Runbooks

Runbooks provide the detailed path behind the recorded walkthrough.

## Available now

- [`synthetic-project/README.md`](../synthetic-project/README.md) — run the
  executable process and inspect its artifacts;
- [`synthetic-project/runbooks/pipeline-triage.md`](../synthetic-project/runbooks/pipeline-triage.md)
  — triage stages, metrics, provenance, and failures;
- [`docs/copilot-hooks.md`](../docs/copilot-hooks.md) — active hook boundaries
  and context-pressure limits;
- [`docs/publication-policy.md`](../docs/publication-policy.md) — public review
  rules.

## Planned deep-dive runbooks

- `01-copilot-cli.md` — install, sign in, start a session, and use safe defaults;
- `02-project-context.md` — add repository instructions and acceptance checks;
- `03-skills.md` — package a repeatable data-science operations procedure;
- `04-hooks.md` — run checks and reject unsafe tool calls;
- `05-mcp.md` — expose a read-only runbook or schema source;
- `06-agentic-workflow.md` — plan, implement, test, review, and stop;
- `07-model-efficiency.md` — route work and control context and token use;
- `08-publication-checks.md` — review public material before publishing.

These deep-dive files are not yet tracked. The available material is the
current source of truth.

## Safe default

Use a clean clone of the repository.

Start with a supervised session. Review every proposed command and every diff.
Do not use production data.
Do not give an agent write access to data that it does not need.
Do not add an MCP server without reviewing its code, permissions, and network
access.

## Terms

**Agent** means a model-driven tool that can inspect a project and use approved
tools.

**Skill** means a reusable set of instructions and supporting resources for a
specific task.

**Hook** means a command that runs at a defined point in an agent session.

**MCP** means Model Context Protocol. It provides a standard way to connect an
agent to tools or data sources.

## Method

Use the smallest suitable model and the smallest suitable tool set.

Use deterministic code for deterministic work.
Use a model for judgement, interpretation, or planning.
Keep a human in control of irreversible actions.
Record the checks that support the result.
