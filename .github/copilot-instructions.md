# Copilot CLI project instructions

This repository is a public playbook for governed agentic-AI development. The
working contract is task-first, supervised, evidence-driven, and independent
of any one provider or CLI feature.

## Required workflow

1. Read `AGENTS.md`, `README.md`, and the matching row in `TASKS.md`.
2. Read the relevant skill and runbook before acting.
3. State the goal, files in scope, files unchanged, checks, and stopping point.
4. Use the smallest suitable model, effort, tool set, and edit.
5. Run focused tests and the repository-authorized validation checks.
6. Inspect the complete diff and public claims.
7. Record evidence, limitations, open questions, and the next decision.
8. Stop before commit, push, merge, publication, or an unclear boundary.

## Model routing

The root `TASKS.md` contains role-tagged router fixtures. Resolve a task
without starting another session:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-id ROUTER-PLAN-001
```

In Pi, configure and activate live assignments with:

```text
/router
/router show
/router task ROUTER-PLAN-001
```

`#implementer`, `#planner`, and `#reviewer` select implementation, planning,
and review. Extra tags remain context. A live Copilot model-activation adapter
is not claimed until it is validated against the installed CLI.

## Skills and hooks

Read the relevant skill under `.github/skills/`:

- `task-list-update` — record one approved subtask and next decision;
- `handover` — preserve state at a stopping point;
- `model-routing` — select role, model, and effort;
- `security-review` — review sensitive and adversarial content;
- `pipeline-run-triage` — review observable artifacts and failures.

The `.github/hooks/` configurations provide narrow boundaries:

- `session-state.json` invokes `copilot_session_state.py` for read-only context;
- `public-safety.json` invokes `copilot_pretool_check.py` for deny decisions and
  content review.

Hooks are context and boundary controls. They do not approve work, choose new
tasks, or replace human review.

## Commands and boundaries

Use only the focused checks named by the task and relevant runbook. Do not
install packages during the supervised demonstration. Do not add credentials,
private endpoints, personal data, or unreviewed network access. Do not publish
repository history from the agent session.

The repository remains the authority for task scope, receipts, evidence, and
stopping points.
