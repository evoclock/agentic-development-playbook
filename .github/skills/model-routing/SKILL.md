---
name: model-routing
description: Route task-tagged implementation, planning, and review work through Pi or a deterministic Copilot-compatible resolver.
---

# Model routing demo

Use this skill for the real model-router demonstration. The authoritative task
metadata is in the repository-root `TASKS.md`. The router reads hash tags from
the matching task row; it does not create a task board, routing ledger, or
second evidence store.

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

## Pi session procedure

Start Pi from the repository root. Trust the project-local extension when Pi
asks, then use `/router`:

```text
/router
```

The command opens six selectors: a model and effort for each role. The model
options come from Pi's actual authenticated catalogue. They are not read from
the public dry-run roster.

Inspect assignments:

```text
/router show
```

Activate a configured role:

```text
/router use implementation
/router use planning
/router use review
```

Activate a task route from the existing register:

```text
/router task ROUTER-IMPLEMENT-001
/router task ROUTER-PLAN-001
/router task ROUTER-REVIEW-001
```

`/router task <task-id>` reads `TASKS.md`, extracts the row's hash tags, maps
the first role tag through `models.json`, activates that role's selected model
and effort, and stores the active task in the current Pi session. Optional
command-line tags remain only as a compatibility/testing fallback when a row
has no routing tag.

The next agent turn receives the active task, role, tags, model, and effort as
routing context. The command itself does not start a provider request.

## Copilot-compatible resolver

Resolve the same task metadata without starting a provider:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-id ROUTER-REVIEW-001
```

Inspect the public dry-run roster:

```bash
python3 .github/skills/model-routing/model_router.py --list
```

Select an explicit configured route when a harness needs a deterministic
choice:

```bash
python3 .github/skills/model-routing/model_router.py \
  --role implementation --model local-coding --effort medium
```

The resolver emits JSON containing the task ID, normalized tags, matched tag,
role, model label, provider label, effort, selection mode, and reason. It is
safe to call from a Copilot workflow because it reads local configuration only.
It does not claim to change the active Copilot model; that adapter must be
validated separately.

## Configuration boundaries

- `.github/skills/model-routing/models.json` maps tags to roles and contains a
  public, provider-free roster for deterministic checks;
- Pi's `/router` uses `ctx.modelRegistry.getAvailable()` for real choices;
- task metadata belongs in the existing root `TASKS.md`;
- role assignments belong in the current Pi session;
- model labels and cost tiers do not prove authentication or provider access.

Do not add credentials, private endpoints, or a second task/evidence store.

## Validation

Run the focused resolver and Pi logic tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/skills/model-routing/tests -v
node --test .pi/extensions/model-router/logic.test.ts
```

After changing `.pi/extensions/model-router.ts`, restart Pi or run `/reload`.
Plain project discovery must register `/router` without attempting to load the
nested helper, test, or declaration files as separate extensions.

## Procedure and stop rules

1. Read the task contract and the matching `TASKS.md` row.
2. Confirm the row contains exactly one role tag or resolve a recorded conflict.
3. Configure implementation, planning, and review independently in Pi.
4. Use `/router task <task-id>` to activate the task's role route.
5. Record the route and checks in the existing task receipt when it affects
   implementation or review.
6. Stop at the approved task boundary; routing must not select new work.
