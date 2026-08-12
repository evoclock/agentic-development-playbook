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

- `TASKS.md` is the only task register for this public demo.
- Preserve the task source and acceptance criteria; do not rewrite them to make
  a result appear complete.
- Do not invent test results, review approval, or publication approval.
- Do not commit or push.
- A skill records the update but cannot enforce that a caller used it. A hook
  or review gate must enforce any mandatory receipt policy.
- Keep the receipt factual, concise, and written in plain language.
