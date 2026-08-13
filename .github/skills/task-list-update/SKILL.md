---
name: task-list-update
description: Record the outcome of one approved subtask in the repository task register. Use before handover when implementation, tests, review, or a blocking decision changes task state.
---

# Task-list update

Use this skill after one approved subtask reaches a stopping point.

## Procedure

1. Read `TASKS.md` and the task source named by its row.
2. Identify the exact task ID and subtask. Do not create a second task list.
3. Check the current status before changing it.
4. Review the files changed, commands run, test results, open questions, and
   next decision.
5. Update the task row only when the evidence supports the new status:
   `in progress`, `ready for review`, `blocked`, or `complete`.
6. Append a dated subtask receipt under the task row. Include the task ID,
   subtask, files changed, checks, evidence, open questions, and next decision.
7. Do not mark a task `complete` when required checks fail, publication review
   is pending, or an approved stopping point has not been reached.
8. Invoke `/handover` after this update when the session state also needs to be
   recorded.

## Copilot CLI procedure

In Copilot CLI, invoke this project skill with natural language:

> Use `task-list-update` for `TASK.md` task `<task-id>`. Record the approved
> subtask, files changed, commands and checks, evidence, open questions, and
> next decision in `TASKS.md`. Do not mark it complete unless the acceptance
> evidence supports that status.

The skill writes a dated receipt under the matching task in the local
`TASKS.md` and returns the status, evidence, scope, and next decision.
`TASK.md` remains the active contract; the ignored local `TASKS.md` remains
the only task register. Create that register during task setup if it is
absent. This procedure is Copilot CLI-native and does not depend on Pi slash
commands.

## Required receipt

```text
Task: <task ID>
Subtask: <approved subtask>
Status: <in progress|ready for review|blocked|complete>
Files changed: <paths or none>
Checks: <commands and results>
Evidence: <artifacts, metrics, or review record>
Open questions: <questions or none>
Next decision: <human decision required>
```

## Boundaries

- The local `TASKS.md` is the only task register for this public demo and is
  intentionally not tracked.
- Preserve the task source and acceptance criteria; do not rewrite them to make
  a result appear complete.
- Do not invent test results, review approval, or publication approval.
- Do not commit or push.
- A skill records the update but cannot enforce that a caller used it. A hook
  or review gate must enforce any mandatory receipt policy.
- Keep the receipt factual, concise, and written in plain language.
