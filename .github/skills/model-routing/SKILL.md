---
name: model-routing
description: Route task-tagged implementation, planning, and review work through GitHub Copilot CLI.
---

# Model routing demo

Use this skill for the real model-router demonstration. The authoritative task
metadata is in the local `TASKS.md` for the current checkout. It is ignored by
Git and must be created during task setup when absent. The router reads hash
tags from the matching task row; it does not create a task board, routing
ledger, or second evidence store.

## Role tags

The first mapped role tag in a task row selects the route:

| Tag | Role | Purpose |
|---|---|---|
| `#implementer` | `implementation` | bounded coding and focused changes |
| `#planner` | `planning` | ambiguity, decomposition, and trade-offs |
| `#reviewer` | `review` | independent evidence, scope, and risk review |

Other tags, such as `#python`, `#security`, or `#evidence`, remain context and
do not change the selected role. Conflicting explicit tags are rejected.

The demo fixtures are:

```text
ROUTER-IMPLEMENT-001  #implementer
ROUTER-IMPLEMENT-002  #implementer
ROUTER-IMPLEMENT-003  #implementer
ROUTER-PLAN-001       #planner
ROUTER-PLAN-002       #planner
ROUTER-PLAN-003       #planner
ROUTER-REVIEW-001     #reviewer
ROUTER-REVIEW-002     #reviewer
ROUTER-REVIEW-003     #reviewer
```

## Copilot CLI procedure

In Copilot CLI, do not use the Python script's `input()` prompts: tool
execution does not provide interactive stdin. Instead, when this skill is
invoked, refresh the runtime roster, present compatible models and efforts
with Copilot's user-choice interaction, then call the resolver with the
selected values:

1. Run `sync_runtime_models.py`.
2. Read `models.runtime.json`.
3. Ask the user to choose a model and effort for implementation, planning, and
   review independently.
4. Resolve and save each choice with `--role`, `--model`, `--effort`, and
   `--save-assignment`.
5. Read the active `TASK.md` contract and resolve it with `--task-file TASK.md`.
6. Execute the task through a new model-bound Copilot process using the
   emitted model and effort:

   ```bash
   copilot --model <model_id> --effort <effort> -p '<task prompt>'
   ```

   The task prompt must tell that selected model to perform the bounded work,
   use its own Bash tool when needed, and record public-safe execution
   evidence. The caller must capture the CLI session identifier and usage
   output when exposed. This is launch evidence; provider execution remains
   unattested unless the CLI explicitly attests it.

The Python interactive mode remains for a real terminal with connected stdin;
it is not the Copilot-session interaction path.

The Copilot onboarding prompt is:

> Use the project `model-routing` skill. Run
> `python3 .github/skills/model-routing/sync_runtime_models.py`, read
> `models.runtime.json`, present compatible model and effort choices for each
> role, save the confirmed assignments, then read `TASK.md` and route it before
> any task work.

Resolve the same task metadata without starting a provider:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-file TASK.md
```

Inspect the fallback roster:

```bash
python3 .github/skills/model-routing/model_router.py --list
```

Select an explicit configured route when a harness needs a deterministic
choice:

```bash
python3 .github/skills/model-routing/model_router.py \
  --role implementation --model local-coding --effort medium
```

Persist a selected role assignment for subsequent task routing:

```bash
python3 .github/skills/model-routing/model_router.py \
  --role implementation --model local-coding --effort medium \
  --save-assignment
```

The resolver emits JSON containing the task ID, task source, normalized tags,
matched tag, role, model label, provider label, effort, selection mode, reason,
and a model-bound execution template. It validates and records routing state;
the caller must use that template to launch the selected Copilot process.

## Configuration boundaries

- `.github/skills/model-routing/models.json` is the public fallback roster;
- `.github/skills/model-routing/models.runtime.json` is the Copilot session
  roster snapshot;
- `.github/skills/model-routing/models.assignments.json` is session routing
  state and must not contain credentials;
- local `TASKS.md` is the authoritative register and `TASK.md` is the active
  task contract;
- model labels and cost tiers do not prove authentication or provider access.

Do not add credentials, private endpoints, or a second task/evidence store.

## Validation

Run the focused resolver tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/skills/model-routing/tests -v
```

## Procedure and stop rules

1. Read the task contract and the matching `TASKS.md` row.
2. Confirm the row contains exactly one role tag or resolve a recorded conflict.
3. Configure implementation, planning, and review independently through
   Copilot user interaction.
4. Read `TASK.md` and route it with the saved assignment.
5. Launch the bounded task with the selected model and effort through
   `copilot --model ... --effort ... -p ...`.
6. Record the route, launch evidence, checks, and any exposed session
   telemetry in the existing task receipt when it affects implementation or
   review.
7. Stop at the approved task boundary; routing must not select new work.
