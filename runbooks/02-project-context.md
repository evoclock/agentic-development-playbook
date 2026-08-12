# 02 — Project context and acceptance checks

## Purpose

Give an agent the smallest context needed to work safely. Useful context is a
task contract, not a transcript of the whole repository.

## Read context in this order

1. `AGENTS.md`;
2. `README.md`;
3. the matching row in `TASKS.md`;
4. `.github/skills/model-routing/SKILL.md`;
5. the relevant source and tests;
6. the relevant runbook;
7. the expected evidence or output contract.

Do not paste credentials, private context, raw session logs, or an entire
repository into a prompt.

## Task contract

A bounded task should state:

```text
Task ID:
Role tag: #implementer | #planner | #reviewer
Goal:
Files to change:
Files to leave unchanged:
Existing behaviour to preserve:
Acceptance checks:
Commands allowed:
Stopping point:
```

The root `TASKS.md` is the authoritative task register. The router reads the
hash tags from the matching row. Extra tags provide context; the first mapped
role tag selects the route.

## Inspect before editing

Run read-only checks from the repository root:

```bash
git status --short --branch
python3 .github/skills/model-routing/model_router.py \
  --task-id ROUTER-IMPLEMENT-001
```

In Pi, inspect the current route with:

```text
/router show
```

## Plan contract

Before editing, ask the agent to state:

```text
Goal:
Files to change:
Files to leave unchanged:
Existing behaviour to preserve:
Acceptance checks:
Stopping point:
```

A plan that adds a dependency, changes permissions, publishes history, or
expands beyond the task row is outside the approved boundary.

## Acceptance and evidence

Run focused checks first, then the repository-authorized suite. Inspect the
complete changed-file list and diff. Report evidence, limitations, and open
questions before selecting another task.
