---
name: pipeline-run-triage
description: Review a deterministic evidence run using artifacts, thresholds, provenance, and failure evidence. Use when a task concerns validation, metrics, warnings, failures, or promotion evidence.
---

# Evidence-run triage

Use this skill when an agent must review an executable deterministic process and
explain its evidence. The process may be a validation job, test run, evaluation,
security check, or other approved evidence-producing command.

## Procedure

1. Read the matching task row and acceptance contract in `TASKS.md`.
2. Read the relevant runbook and inspect the approved evidence directory.
3. Run the focused tests when scenario evidence is missing.
4. Read the relevant manifest, validation, metrics, provenance, and failure
   artifacts.
5. Compare every check with its configured threshold or acceptance condition.
6. State the status, evidence, next controlled action, and unchanged files.
7. Run focused tests, then the authorized wider suite when code changes are
   complete.

## Copilot CLI procedure

When validation, metrics, warnings, failures, or promotion evidence is part of
the active `TASK.md`, ask Copilot:

> Use `pipeline-run-triage` for `<task-id>`. Read the relevant runbook and
> approved artifacts, run only the focused authorized checks, compare observed
> values with every threshold, and return the required status, evidence,
> action, scope, and open questions. Do not edit generated evidence.

The skill returns `HEALTHY`, `WARNING`, `FAILED`, or `REVIEW_REQUIRED` with
artifact-backed evidence. It does not publish, promote, or replace human
approval. This is the Copilot CLI procedure; no Pi command is implied.

## Output format

```text
Status: <HEALTHY|WARNING|FAILED|REVIEW_REQUIRED>
Task: <task id and role tag>
Evidence:
- <artifact>: <metric, observed value, and threshold>
Action: <next controlled step>
Scope: <files changed and files unchanged>
Open questions: <explicit uncertainty>
```

## Boundaries

- Use only evidence in approved artifacts and the relevant runbook.
- Do not invent a cause for a warning.
- Treat a warning as review evidence, not a judgement about a person.
- Do not edit generated evidence to make a check pass.
- Keep promotion and publication decisions subject to human review.
- Use public-safe, standard-library examples and do not expose private data.
