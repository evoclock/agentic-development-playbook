# Copilot skill preflight fixture

This directory is a public-safe, self-contained toy workspace for rehearsing
the repository skills before a supervised demonstration. It is not the real
task register and it is not a second project board.

It is source material, not the directory where the rehearsal runs. A clone
contains `demo-workspace/` as an empty tracked container. The preparation step
creates a named child such as `demo-workspace/preflight-001/`; all rehearsal
state belongs there.

The fixture deliberately includes:

- `README.md` — this workspace guide;
- `AGENTS.md` — toy project conventions;
- `.github/copilot-instructions.md` — toy Copilot instructions;
- `TASKS.md` — one bounded `PREFLIGHT-001` task;
- `src/sample.txt` — a harmless file for the bounded task;
- `evidence/` — small healthy and warning artifacts for pipeline triage.

The fixture deliberately does not include `TASK.md`, `HANDOVER.md`, or model
runtime state. The rehearsal creates those in a disposable workspace.

## Start the rehearsal from a clone

From the repository root, ask Copilot:

```text
Use the committed preflight fixture under preflight/. Invoke the existing
preparation script yourself to create the named disposable workspace
demo-workspace/preflight-001. Return the workspace path and do not modify the
source checkout.
```

Copilot should run the existing preparation script. It copies this toy
workspace, the maintained `.github/skills/` and `.github/hooks/`, and the
preflight runbook into the named child workspace. Its bootstrap commit is
local to that child and must never be published. Do not continue the
rehearsal in the source checkout.

Start or move to a Copilot session in the returned child workspace, then ask
it to:

```text
Read AGENTS.md, .github/copilot-instructions.md, README.md, TASKS.md, and
runbooks/10-skill-preflight.md. Create TASK.md for PREFLIGHT-001 with exactly
one role tag, bounded scope, acceptance checks, allowed commands, and a
stopping point. Do not edit any other file yet.
```

Continue with the prompts in
[`runbooks/10-skill-preflight.md`](../runbooks/10-skill-preflight.md). The
expected sequence is:

```text
TASK.md -> model route -> bounded task -> security review
          -> evidence triage -> TASKS.md receipt -> hook boundary -> HANDOVER.md
```

The model-routing stage is part of the rehearsal, not a preconfigured result.
Refresh the runtime roster, choose and save implementation, planning, and
review assignments, route `TASK.md`, and return the JSON route before the
bounded task begins. Model state, `TASK.md`, receipts, and `HANDOVER.md` stay
inside the child workspace.

For readers who are not running the rehearsal, the source checkout also
contains frozen snapshots under `docs/examples/preflight-001/`. They
illustrate the end results without becoming active task state; the preparation
script does not copy them into the runnable child.

## Automated check

From the returned child workspace, ask Copilot:

```text
Use the preflight runbook and run its automated checks. Report the result and
do not modify the real TASKS.md or HANDOVER.md.
```

Copilot runs the check through its own Bash tool. The participant does not
type a shell command; the first interaction is the natural-language prompt.
