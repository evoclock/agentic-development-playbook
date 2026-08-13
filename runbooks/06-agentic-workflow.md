# 06 — Plan, implement, test, review, stop

## Purpose

Use a short, evidence-driven loop for a bounded agentic-AI change. The loop is
the same progression shown in [`diagrams/agentic-workflow.png`](../diagrams/agentic-workflow.png):

```text
scope -> task contract -> project context -> skill -> scoped tools
      -> deterministic checks -> evidence -> human review -> stop
```

The agent does not receive broad authority because it can write code. The task,
paths, commands, route, and stopping point define the working boundary.

## Scope and context

Read:

- the current task row in `TASKS.md`;
- project instructions;
- relevant skills and runbooks;
- relevant source and tests;
- the acceptance and evidence contract.

Check the repository before planning:

```bash
git status --short --branch
git diff --stat
```

Record unrelated dirty paths and leave them unchanged.

## Plan

Ask for a bounded plan:

```text
Goal:
Files to change:
Files to leave unchanged:
Existing behaviour to preserve:
Acceptance checks:
Stopping point:
```

Use the Copilot `model-routing` skill after `TASK.md` has been created and
the role-tagged task has been read.
Choose implementation for bounded edits, planning for ambiguity, and review
for an independent evidence pass.

A plan that adds a dependency, expands permissions, publishes history, or
changes an unrelated task is outside the approved boundary.

## Controlled delivery

Use the smallest suitable edit and the relevant skill. Keep deterministic work
in code. Use scoped tools for read, test, edit, and review actions. Apply the
security-review skill before risky handoffs and respect the public-safety hook.

## Test and inspect evidence

Run focused checks first, then the authorized suite. Inspect the complete
changed-file list and diff:

```bash
git diff --check
git diff --stat
```

A passing test is one piece of evidence. Also inspect warnings, route choice,
public claims, limitations, and open questions.

## Review and report

Report:

- files read and prior art found;
- files changed and exact diff summary;
- commands and results;
- evidence supporting the status;
- limitations and open questions;
- next decision and stopping point.

Stop at the approved boundary. Do not commit, push, merge, or publish without
separate human approval.
