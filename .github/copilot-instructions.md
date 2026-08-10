# Copilot CLI project instructions

This is a public synthetic data-science operations playbook.
The runnable process is under `synthetic-project/`.

## Required workflow

1. Inspect the task, relevant source, and runbook.
2. State the files to change and the acceptance checks.
3. Use the smallest suitable change.
4. Add or update tests for code changes.
5. Run the real pipeline scenario and the full test suite.
6. Inspect the complete diff.
7. Report evidence, limits, and open questions.

The `sessionStart` hook provides a read-only branch, working-tree, task, and
test summary. It is context only. It does not approve work or replace review.

Hook boundaries and the context-pressure decision are documented in
`docs/copilot-hooks.md`.

The optional context diagnostic can classify launcher-supplied telemetry:

```text
python3 synthetic-project/scripts/copilot_context_pressure.py --percent 60
```

Copilot `sessionStart` does not reliably provide context usage percentages, so
this diagnostic is not installed as an active hook.

## Commands

Run these commands from the repository root:

```text
python3 synthetic-project/scripts/run_pipeline.py --scenario healthy
python3 synthetic-project/scripts/run_pipeline.py --scenario evaluation-warning
python3 synthetic-project/scripts/run_pipeline.py --scenario row-loss
python3 synthetic-project/scripts/run_pipeline.py --scenario schema-failure
python3 -m unittest discover -s synthetic-project/tests -v
```

Expected scenario meanings and artifacts are documented in
`synthetic-project/README.md` and
`synthetic-project/runbooks/pipeline-triage.md`.

## Boundaries

- Keep examples synthetic and public-safe.
- Use the standard library only.
- Do not install packages during the walkthrough.
- Do not add real data, secrets, private endpoints, or private paths.
- Keep generated run output under `synthetic-project/runs/`.
- Do not edit generated run output as a substitute for source changes.
- Do not publish repository history from the agent session.
- Treat warnings as evidence requiring review, not as personal judgements.

Use `/pipeline-run-triage` for run manifests, generated artifacts, thresholds,
health status, or promotion evidence.
