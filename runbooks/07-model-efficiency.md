# 07 — Model, effort, and context efficiency

## Purpose

Route each part of the workflow to the smallest suitable capability. The goal
is useful evidence, not maximum prompt length, model size, or effort.

The workflow diagram places routing inside controlled delivery, between the
task contract and evidence/review. The surrounding skills and hooks remain
active regardless of the selected model.

## Separate deterministic and judgement work

Use deterministic code for validation, calculations, exit codes, artifact
writing, and repeatable safety decisions. Use an agent for interpreting a
task, selecting relevant files, proposing a bounded plan, explaining evidence,
reviewing a diff, and identifying uncertainty.

## Three role routes

| Role | Suitable work | Evidence |
|---|---|---|
| `implementation` | bounded coding and focused changes | diff and tests |
| `planning` | ambiguity, decomposition, and trade-offs | plan and decisions |
| `review` | independent evidence, scope, and risk review | findings and receipt |

### Copilot CLI configuration

In Copilot CLI, ask the project skill:

> Sync the Copilot model roster, show all compatible models and effort levels,
> ask me to choose implementation, planning, and review assignments, save the
> choices, and route the active `TASK.md` contract.

The Copilot path uses `sync_runtime_models.py`,
`model_router.py --save-assignment`, and `model_router.py --task-file TASK.md`.
Do not use the Python `--interactive` flag through a Copilot tool call; it
requires terminal stdin.

## Task routing

The local `TASKS.md` owns task metadata for the current checkout. Create the
ignored register during task setup if it is absent. Role tags map as follows:

| Tag | Role |
|---|---|
| `#implementer` | implementation |
| `#planner` | planning |
| `#reviewer` | review |

Additional tags remain context. Activate the tagged task from the active
contract:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-file TASK.md
```

The route is stored in ignored session state and emitted as JSON. It does not
create a task board or start a provider request. A conflicting explicit tag is
rejected.

For a provider-free Copilot-compatible preview:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-id ROUTER-PLAN-001
```

## Context budget

Before a long prompt:

1. read the session-state summary;
2. read the current task row and route;
3. read only relevant symbols, tests, and runbooks;
4. state what has already been established;
5. identify the next decision and stopping point.

Prefer a short task contract over a transcript, a file/symbol list over a
tree dump, and summarized evidence over raw logs. Never paste credentials,
private context, or unreviewed session output into a prompt.

## Measure useful work

Record facts that support rollout decisions:

- time to a bounded plan;
- files inspected and changed;
- tests and acceptance checks passed;
- evidence produced and reviewed;
- route and effort selected;
- warnings, limitations, and unresolved decisions;
- human decisions at approval and stopping points.

Do not use prompt count, login count, or model size as a proxy for value.

## Review efficiency

Use a separate review route for threshold changes, exit-code changes, hooks,
MCP permissions, public claims, and scope expansion. The reviewer should
inspect evidence and the complete diff, not merely repeat implementation.

## Stop rules

Stop when a check fails, the task boundary expands, a safety or approval
boundary is reached, or the approved subtask is complete. Record the receipt in
`TASKS.md`; use `HANDOVER.md` when wider session state must survive a stop.
Routing must not select new work.
