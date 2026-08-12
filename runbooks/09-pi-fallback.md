# 09 — Pi model-router demonstration

## Purpose

Use Pi as the live interactive harness for the role-based model router. This
is a harness-specific demonstration of the broader adoption workflow; it is
not evidence that Copilot CLI ran, and it is not a provider or production
readiness test.

## Scope

This track demonstrates:

- project trust and local extension discovery;
- a human-owned task contract in `TASKS.md`;
- separate implementation, planning, and review assignments;
- task-tag lookup and route activation;
- session-local persistence;
- focused tests, type checks, and discovery evidence.

The Copilot instructions and hooks are not assumed to load in Pi. Verify each
harness feature separately before describing it as active.

## Start Pi

From the repository root:

```bash
pi
```

Trust the project-local resources when Pi asks. After changing the extension,
use `/reload` or restart Pi. Plain startup should load only
`.pi/extensions/model-router.ts`; helper, test, and declaration files are
nested and must not appear as separate extension failures.

## Configure routes

Open the TUI configuration flow:

```text
/router
```

Select a model and effort for implementation, planning, and review. Inspect:

```text
/router show
```

Activate a role:

```text
/router use planning
```

The extension calls `pi.setModel()` and `pi.setThinkingLevel()` for the
selected assignment. A route activation does not start a model request until a
subsequent prompt.

## Activate tagged tasks

The root `TASKS.md` contains the public router fixtures. Use task IDs without
repeating their role tags:

```text
/router task ROUTER-IMPLEMENT-001
/router task ROUTER-PLAN-001
/router task ROUTER-REVIEW-001
```

Expected mapping:

```text
#implementer -> implementation
#planner     -> planning
#reviewer    -> review
```

Extra row tags remain context. The command persists the assignment and active
task in the current Pi session and injects routing context into the next agent
turn. It does not create another task board or evidence store.

## Provider-free resolver

The Copilot-compatible deterministic resolver reads the same task register:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-id ROUTER-REVIEW-001
```

It emits JSON and does not contact a provider or start a session. Do not claim
that it changes Copilot's active model until a target CLI adapter is validated.

## Focused validation

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/skills/model-routing/tests -v
node --test .pi/extensions/model-router/logic.test.ts
```

Run a strict type check against the installed Pi declarations when available.
Also verify project-local discovery with:

```bash
printf '%s\n' '{"id":"commands","type":"get_commands"}' \
  | pi --mode rpc --no-session --no-tools --offline --approve
```

The response should include an extension command named `router` and no invalid
factory errors.

## Recording disclosure

Use this wording when Pi is the recorded harness:

> This segment uses Pi as the interactive model-routing harness. It verifies
> the project-local extension, task-tag resolution, and session-local route
> state. It does not claim that GitHub Copilot CLI executed the workflow or
> that a configured model label proves provider availability.

Do not describe Pi output as Copilot hook decisions. Do not claim that the
Copilot hooks or an MCP server ran in Pi unless separately validated.

Stop if the task, path scope, trust decision, model catalogue, or harness
identity is unclear.
