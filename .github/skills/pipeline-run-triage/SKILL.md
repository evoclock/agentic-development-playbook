---
name: pipeline-run-triage
description: Review a synthetic data-science pipeline run using generated artifacts, thresholds, provenance, and failure evidence. Use when a task concerns run manifests, pipeline health, validation, AUC, row retention, warnings, failures, or promotion evidence.
---

# Pipeline run triage

Use this skill for the executable project under `synthetic-project/`.

## Procedure

1. Read `synthetic-project/runbooks/pipeline-triage.md`.
2. Read the task and inspect the relevant run directory.
3. Run the requested scenario with `synthetic-project/scripts/run_pipeline.py`.
4. Read `run_manifest.json`, `validation.json`, `evaluation.json`, `provenance.json`, and `failure_log.jsonl` as relevant.
5. Compare each check with its configured threshold.
6. State the status, evidence, next controlled action, and unchanged files.
7. Run focused tests, then the full suite when code changes are complete.

## Output format

```text
Status: <HEALTHY|WARNING|FAILED>
Evidence:
- <artifact>: <metric, observed value, and threshold>
Action: <next controlled step>
Scope: <files changed and files unchanged>
```

## Boundaries

- Use only evidence in generated artifacts and the runbook.
- Do not invent a cause for a warning.
- Treat a warning as review evidence, not as a judgement about a person.
- Do not edit generated run output to make a check pass.
- Keep promotion decisions subject to human review.
- Keep examples synthetic and standard-library only.
