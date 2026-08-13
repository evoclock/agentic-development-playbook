# Active task contract

Task ID: PREFLIGHT-001
Role tag: #implementer

## Goal

Provide one complete, clone-friendly skill-preflight demonstration: a blank
runnable child workspace for participants and frozen end-state snapshots for
readers, with model-routing kept as an explicit rehearsal stage.

## Files in scope

- `demo-workspace/.gitkeep`
- `.gitignore`
- `docs/examples/preflight-001/README.md`
- `docs/examples/preflight-001/TASK.md`
- `docs/examples/preflight-001/TASKS.md`
- `docs/examples/preflight-001/HANDOVER.md`
- `README.md`
- `preflight/README.md`
- `preflight/prepare_workspace.py`
- `preflight/tests/test_preflight.py`
- `runbooks/10-skill-preflight.md`
- `runbooks/INDEX.md`
- `TASK.md`
- `TASKS.md`
- `HANDOVER.md`

All preparation, routing, checks, and model-bound execution are performed by
Copilot from within the supervised session; the participant does not type
shell commands.

## Files unchanged

- the seeded `preflight/` fixture and evidence artifacts;
- existing hook and model-routing behavior;
- generated model state, telemetry receipts, and external evidence.

## Acceptance checks

- A clone has only `demo-workspace/.gitkeep`; the user creates a named child
  workspace for the live rehearsal.
- Frozen `PREFLIGHT-001` snapshots show the task contract, route/evidence
  receipt, handover, limitations, and next decision for readers.
- Documentation directs runners to the blank child and directs readers to the
  frozen snapshots; model-routing remains an explicit user-run stage.
- The preparation script excludes generated model state and does not copy the
  frozen snapshots into active child state.
- The preflight, hook, and model-routing suites pass, and `git diff --check`
  passes.
- No commit, push, merge, publication, package installation, MCP registration,
  or real data is used.

## Allowed commands

- run the preflight test runner through Copilot's Bash tool;
- run the focused hook and model-routing checks through Copilot's Bash tool;
- inspect diff whitespace and Git state through Copilot's tools;

## Stopping point

Stop after the complete demo package, task receipt, and handover are updated.
Do not run the end-to-end demo or modify generated evidence.
