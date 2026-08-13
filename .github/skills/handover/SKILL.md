---
name: handover
description: Record the current repository, task, evidence, open questions, and next decision in HANDOVER.md at an approved stopping point.
---

# Handover

Use this skill after `/task-list-update` when a subtask or session reaches a
stopping point.

## Procedure

1. Read the local `TASKS.md` and identify the current task and latest receipt.
2. Inspect `git status --short` and `git diff --stat`.
3. Record the files read, prior art found, files changed, exact diff summary,
   commands run, test results, open questions, and next decision.
4. Write or update the repository-root `HANDOVER.md`.
5. Keep the handover factual and public-safe. Do not include secrets, tokens,
   private endpoints, private home paths, or unverified claims.
6. Preserve the latest task-list receipt. Do not create a second task board,
   approval store, or evidence store.
7. Stop after the handover is written. Do not commit or push.

## Copilot CLI procedure

At a supervised stopping point in Copilot CLI, invoke this project skill with:

> Use `handover` now. Read `TASK.md`, `TASKS.md`, and the current Git state.
> Write or update the root `HANDOVER.md` with the current task, repository
> state, files read and changed, commands and tests, evidence, limitations,
> open questions, and next decision. Do not commit or push.

The output is the repository-root `HANDOVER.md`. It is durable resume state,
not a second task register or approval store. Run `task-list-update` first;
the handover records the resulting receipt and keeps the next session fresh.
This is the Copilot CLI procedure; Pi is not assumed to load the skill.

## Required handover headings

```markdown
# Handover

## Current task
## Repository state
## Files read
## Prior art
## Files changed
## Commands and tests
## Open questions
## Next decision
```

## Boundaries

- `HANDOVER.md` is the repository handover record for this public demo.
- The local `TASKS.md` is ignored by Git but must exist before handover so the
  latest receipt can be preserved.
- Run `/task-list-update` first so the task register has the subtask receipt.
- Do not claim a task is complete when review or acceptance is pending.
- Keep examples synthetic and standard-library only.
- A skill records the handover; a hook reports its presence and a review gate can
  require it before publication.
