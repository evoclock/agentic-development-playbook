# 10 — Skill preflight rehearsal

## Purpose

Use this runbook before a supervised demonstration to exercise every
maintained skill and both hooks. Start from a clone of the playbook and run
the rehearsal in a named child of the tracked, empty `demo-workspace/`
container. Do not run it in the source checkout or use its real task
register. The self-contained `preflight/` fixture seeds a toy `README.md`,
`AGENTS.md`, `.github/copilot-instructions.md`, `TASKS.md`, and sample file.
It intentionally does not seed `TASK.md` or `HANDOVER.md`; the rehearsal
creates those in the named child workspace.

Do not create a competing `CONVENTIONS.md`. The fixture's `AGENTS.md` and
`.github/copilot-instructions.md` are the convention files for the rehearsal.

For readers who are not running the rehearsal, the source checkout contains
frozen snapshots under `docs/examples/preflight-001/`. They illustrate the
end results of the contract, route, receipt, and handover stages. They are
synthetic, non-authoritative, and not copied into the runnable child.

## Start in a Copilot session

From the source checkout, ask Copilot:

```text
Use the committed preflight fixture under preflight/. Invoke the existing
preparation script yourself to create the named disposable workspace
demo-workspace/preflight-001. Return the workspace path and do not modify the
source checkout.
```

The preparation script creates the named child, copies the toy project plus
canonical skills and hooks, and creates a local bootstrap commit so the
read-only session-state hook has a Git head. The parent checkout ignores the
child contents. Never publish the bootstrap commit. Start or move to a
Copilot session in the returned child before continuing.

This preparation demonstrates workspace isolation: the source checkout
provides the reusable fixture, while the child receives the state that the
rehearsal is expected to create.

Every prompt below is run from `demo-workspace/preflight-001/`. If a different
session name is used, substitute that child path consistently. The source
checkout should gain no rehearsal task, receipt, handover, model state, or
generated evidence.

## Automated preflight

In the named child workspace, ask Copilot:

```text
Use the preflight runbook and run the automated checks from preflight/tests.
Report the result and do not modify TASKS.md or HANDOVER.md.
```

The test covers:

- Copilot CLI sections, output contracts, and boundaries in all five skills;
- role selection from a synthetic `TASK.md` and saved model assignment;
- read-only session-state reporting before and after `HANDOVER.md`;
- pre-tool history gating before and after a synthetic task receipt;
- security fixture decisions and the small `preflight/evidence/` triage
  fixture.

The hook does not write `TASKS.md`. It only returns a permission decision.
`task-list-update` is the procedure that records a receipt; `handover` then
preserves the stopping-point state.

This automated stage demonstrates that the five skill contracts, route
selection, session-state reporting, pre-tool boundary, security baseline, and
static evidence fixture work before a person starts the manual rehearsal.
Copilot runs the test command through its own Bash tool; the participant does
not type it.

## Manual Copilot rehearsal

The disposable workspace already contains the toy conventions and task
register. Do not commit, push, publish, install packages, register MCP, or use
real data.

### 1. Read conventions and create the task contract

Ask Copilot:

```text
Read AGENTS.md, .github/copilot-instructions.md, README.md, TASKS.md, and
runbooks/10-skill-preflight.md in this disposable workspace. Create a root
TASK.md for PREFLIGHT-001 with exactly one role tag, goal, files in scope,
files unchanged, acceptance checks, allowed commands, and stopping point. Do
not edit the source checkout or any other file yet.
```

Expected evidence: Copilot reports the task ID, one role tag, bounded paths,
checks, and stop point. `TASKS.md` remains the only task register.

This step demonstrates context loading and task scoping. The role tag and
acceptance boundary turn an open-ended request into a reviewable contract
before any task work begins.

### 2. Select and route a role

Ask Copilot:

```text
Use the project model-routing skill. Refresh the runtime roster, show model
and effort choices for implementation, planning, and review, let me choose
each assignment, save the choices, and route TASK.md. Return the JSON route
before doing task work.
```

Expected artifacts: ignored `models.raw.jsonl`, `models.runtime.json`, and
`models.assignments.json`, followed by a route containing `PREFLIGHT-001`,
the mapped role, selected model, and effort. This model-routing step is
required user-run rehearsal work; do not use a pre-seeded route or skip it.
All three assignments and the route must be created in the child workspace.

This step demonstrates deliberate capability and effort selection. It keeps
the assignment state session-local, makes the selected route inspectable, and
separates choosing a role route from claiming that a provider actually ran.

### 3. Run one bounded task

Ask Copilot:

```text
Read TASK.md and use the selected route in this disposable workspace. Perform
only the bounded inspection in the contract, run its allowed checks, and
report changed files, unchanged files, evidence, limitations, and open
questions. Do not publish history or modify the source checkout.
```

The selected route must be executed through a model-bound process:

ask Copilot to launch a new model-bound Copilot process using the emitted model,
effort, and bounded task prompt.

The launched model performs the inspection and may call Bash itself. Preserve
its session identifier and usage telemetry when the CLI exposes them.

Expected evidence: the task stays within its contract and produces a
reviewable result rather than selecting new work.

This step demonstrates model-bound execution under a bounded contract. The
result should include checks and limitations, while launch telemetry is kept
distinct from provider execution attestation.

### 4. Exercise security review

Ask Copilot:

```text
Use security-review on the proposed task output and any content that would be
sent to a tool or file. Run the deterministic baseline, return accept, redact,
or reject with public-safe categories, and stop for redact or reject.
```

Use the existing security fixtures. Expected decisions include `accept` for
clean content, `redact` for synthetic PII or secrets, and `reject` for
injection or limited MCP-threat markers. Never paste raw sensitive values into
the receipt.

This step demonstrates the content-safety boundary before model output is
sent to a tool or file. `accept` means only that no configured baseline rule
matched; `redact` and `reject` stop the original payload.

### 5. Exercise evidence triage

Ask Copilot:

```text
Use pipeline-run-triage for PREFLIGHT-001. Read
preflight/evidence/README.md and the healthy and warning artifacts, compare
observed values with thresholds, and return status, evidence, action, scope,
and open questions. Do not edit the evidence fixture.
```

Expected statuses are artifact-backed `HEALTHY`, `WARNING`, `FAILED`, or
`REVIEW_REQUIRED`; a warning is evidence for review, not a personal judgement.

This step demonstrates deterministic evidence review. The skill compares
observed values with thresholds and reports an artifact-backed action without
inventing a cause for a warning or promoting a result.

### 6. Record the subtask receipt

Ask Copilot:

```text
Use task-list-update for TASK.md task PREFLIGHT-001. Record the approved
subtask, files, commands and checks, evidence, open questions, and next
decision in TASKS.md. Do not mark it complete without acceptance evidence.
```

Expected evidence: a dated receipt is appended to `TASKS.md` with the required
fields. The hook is not expected to edit this file.

This step demonstrates the human-controlled task record: the approved
subtask, files, checks, evidence, uncertainty, and next decision are captured
without silently marking the task complete.

### 7. Verify hook boundaries

In the disposable checkout, request a history-changing command but do not
approve it:

```text
Propose the command `git commit -m preflight` for review, but do not execute it.
```

Expected hook result: `deny`. Before the receipt exists, the reason also
requires a `TASKS.md` update. After the receipt exists, publication remains
denied because human approval is still required.

This step demonstrates enforcement rather than documentation alone. The hook
recognizes a history-changing boundary, requires the relevant receipt, and
still leaves commit or publication approval with a person.

### 8. Preserve handover state

Ask Copilot:

```text
Use handover now. Read TASK.md, TASKS.md, and the current Git state. Write or
update root HANDOVER.md with the current task, repository state, files read,
prior art, files changed, commands and tests, open questions, and next
decision. Do not commit or push.
```

Expected artifact: `HANDOVER.md` with the required headings and a next
decision that stops before publication.

This step demonstrates durable stopping-point state. A later session can see
the task, repository state, evidence, limitations, and next decision without
turning handover into a second task board or approval store.

## Cleanup and evidence

Review the complete diff inside the named child, record the rehearsal
outcome, and remove only that named child workspace when finished. Keep
`demo-workspace/.gitkeep` and the source checkout's `TASKS.md`,
`HANDOVER.md`, generated model state, and working tree unchanged unless a
separate task explicitly approves those writes.

Cleanup demonstrates that rehearsal state is disposable while the playbook
and its empty entry point remain reusable for the next person.
