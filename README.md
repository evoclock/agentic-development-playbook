# Agentic development playbook

Public, synthetic material for practical agentic development in data-science
operations.

The repository contains a runnable synthetic pipeline and a GitHub Copilot CLI
walkthrough. It demonstrates project instructions, skills, read-only MCP
context, safety hooks, deterministic tests, review, and context boundaries.

This material was prepared for a Department for Education demonstration. It is
independent. It is not official DfE guidance.

## Start here

1. Read [`CONTENT-MAP.md`](CONTENT-MAP.md).
2. Read [`synthetic-project/README.md`](synthetic-project/README.md).
3. Read [`runbooks/README.md`](runbooks/README.md).
4. Read [`docs/publication-policy.md`](docs/publication-policy.md).
5. Use the recorded sequence as the main route.

## Run the executable example

From `synthetic-project/`:

```bash
python3 scripts/run_pipeline.py --scenario healthy --output-dir runs/demo-healthy
python3 -m unittest discover -s tests -v
```

The process generates synthetic records, validates them, creates features,
fits a deterministic baseline, calculates AUC, and writes provenance,
validation, failure, manifest, and health-report artifacts.

Available scenarios:

| Scenario | Result | Exit |
|---|---|---:|
| `healthy` | All configured checks pass | `0` |
| `evaluation-warning` | AUC is below its threshold | `1` |
| `row-loss` | Feature-row retention is below its threshold | `1` |
| `schema-failure` | Validation stops the run | `2` |

## Copilot CLI controls

The repository-level `.github/` directory contains:

- `copilot-instructions.md` — project workflow and boundaries;
- `skills/pipeline-run-triage/` — reusable artifact-review procedure;
- `hooks/session-state.json` — read-only session context;
- `hooks/public-safety.json` — narrow pre-tool safety decisions.

The read-only MCP example is documented in
[`synthetic-project/mcp/README.md`](synthetic-project/mcp/README.md).
Hook boundaries and the inactive context-pressure diagnostic are documented in
[`docs/copilot-hooks.md`](docs/copilot-hooks.md).

## What this playbook teaches

- how to give an agent useful project context;
- how to turn a repeatable procedure into a skill;
- how to expose reviewed read-only context through MCP;
- how to use narrow hooks for safety and session context;
- how to plan, implement, test, review, and document a change;
- how to separate deterministic checks from model judgement;
- how to manage context limits without claiming unavailable telemetry.

The recorded walkthrough uses GitHub Copilot CLI. The method is broader than
one harness. Harness-specific details belong in the relevant documentation.

## Public repository rules

- Keep examples synthetic.
- Use public sources and link to them.
- Use placeholders for credentials, paths, and endpoints.
- Do not track generated run output under `synthetic-project/runs/`.
- Review the complete diff before every commit.
- Obtain human approval before publishing.

See [`docs/publication-policy.md`](docs/publication-policy.md).

## Material status

Implemented now:

- executable synthetic pipeline;
- pipeline triage runbook;
- Copilot instructions and skill;
- read-only session and MCP examples;
- narrow pre-tool safety example;
- context-pressure boundary documentation.

Planned later:

- deep-dive runbooks `01` through `08`;
- Marp slides;
- D2 diagrams rendered as PNG;
- public outreach drafts.

Implemented examples are educational. They are not evidence of production
readiness or official adoption.
