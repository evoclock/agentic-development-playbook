# Adopting agentic AI with evidence

This public playbook is about adopting agentic AI responsibly in real
engineering and data-science work. It focuses on the work around the model:
clear tasks, useful project context, repeatable procedures, bounded tools,
deterministic checks, review, and recorded evidence.

The material was prepared for a Department for Education demonstration. It is
independent and is not official DfE or government guidance.

## Adoption is not the outcome

Installing an agentic tool, increasing usage, or selecting a larger model does
not prove that a process became faster, safer, or more reliable. A rollout
needs observable evidence about the task result and the controls around it.

This playbook therefore treats adoption as a governed workflow:

1. define the task, owner, acceptance checks, and stopping point;
2. provide the agent with the right repository context;
3. package repeatable procedures as skills and runbooks;
4. keep deterministic work in deterministic code;
5. give the agent only the tools and permissions it needs;
6. choose capability and effort deliberately rather than maximising them;
7. inspect tests, artifacts, the complete diff, limitations, and open questions;
8. use human review before irreversible actions or publication.

The useful measures are task-level measures: acceptance checks passed, defects
found, evidence produced, risks resolved, review time, and limitations made
visible. Prompt count, login count, and model size are not outcome measures.

See [`docs/adoption-and-outcomes.md`](docs/adoption-and-outcomes.md) for the
short rationale and source note.

## The workflow and control plane

![Agentic development workflow](diagrams/agentic-workflow.png)

The workflow diagram is the operating model behind the demonstration:

1. **Scope and context** — a human owner defines the objective, approval, and
   stop point; the task contract records the goal, paths, checks, and boundary.
2. **Controlled delivery** — project context, a repeatable skill, scoped tools,
   and deterministic checks turn an open-ended prompt into a reviewable process.
3. **Evidence and review** — tests, reports, artifacts, and the complete diff
   make the result inspectable before a human approves, revises, or stops it.

The maintained skills support different parts of that loop:

| Skill | Contribution |
|---|---|
| `task-list-update` | records one approved subtask, evidence, status, and next decision |
| `handover` | preserves repository and session state at a stopping point |
| `model-routing` | selects separate implementation, planning, and review routes |
| `security-review` | reviews PII, secrets, hidden Unicode, injection, and limited MCP markers |
| `pipeline-run-triage` | reviews observable artifacts, thresholds, warnings, and failures |

The hook control plane adds deterministic boundaries around the agent:

| Hook | Contribution |
|---|---|
| `session-state` / `copilot_session_state.py` | supplies read-only branch, task, receipt, and working-tree context |
| `public-safety` / `copilot_pretool_check.py` | denies selected history, destructive, elevated, and install actions and applies the security contract |

Skills explain procedure; hooks enforce narrow decisions; deterministic code
produces repeatable checks; human review remains the final control.

## The actual working demo: role-based model routing

The repository includes a real project-local Pi extension that makes one part
of this operating model executable. It assigns separate available models and
effort levels to three kinds of work:

- **implementation** — bounded coding and focused changes;
- **planning** — ambiguity, decomposition, and trade-offs;
- **review** — independent evidence, scope, and risk review.

The router is deliberately session-local. It does not create a task board,
routing ledger, or provider session.

### Start the Pi demo

From a trusted checkout:

```bash
cd /path/to/agentic-development-playbook
pi
```

If Pi asks whether to trust the project, approve the project-local extension.
Then configure the three assignments:

```text
/router
/router show
```

`/router` opens six selectors: a model and an effort for each role. The model
selector uses Pi's actual authenticated `ctx.modelRegistry.getAvailable()`
catalogue. It does not pretend that public configuration labels are live
providers.

Activate a configured role directly:

```text
/router use implementation
/router use planning
/router use review
```

### Route a task by its own tags

The root [`TASKS.md`](TASKS.md) is the authoritative task register. It also
contains nine public demo fixtures, three for each role. Their role tags are:

| Task tag | Route |
|---|---|
| `#implementer` | implementation |
| `#planner` | planning |
| `#reviewer` | review |

Other tags remain context. Point at the task; do not repeat the role tag:

```text
/router task ROUTER-IMPLEMENT-001
/router task ROUTER-PLAN-001
/router task ROUTER-REVIEW-001
```

The command reads the matching task row, maps its first role tag, activates
that role's selected model and effort, persists the active route in the
current Pi session, and injects the route into the next agent turn. A
conflicting explicit tag is rejected. The command itself does not start a
provider request.

### Copilot-compatible resolution

The same task-tag contract can be resolved without starting a provider:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-id ROUTER-REVIEW-001
```

The resolver emits the task ID, normalized tags, matched tag, role, configured
model label, effort, selection mode, and reason. It is suitable for a
Copilot-oriented workflow that needs a deterministic routing decision. A live
Copilot model-activation adapter is a separate harness concern and must be
validated before being claimed as active.

## Rollout path

Use the demo as a small, inspectable pilot rather than as a claim that an
organisation is ready to scale agentic AI.

### Prepare

- identify a bounded task with a human owner;
- write acceptance checks and a stopping point;
- classify work as implementation, planning, or review;
- decide what data, tools, credentials, and network access are actually needed;
- record the approved task and route in the existing project records.

### Pilot

- start in a supervised session;
- use the smallest capable model and effort;
- keep deterministic calculations and validations outside the model;
- review every proposed write and command;
- collect tests, artifacts, timings, decisions, and failure evidence;
- stop when the approved subtask is complete or a boundary is unclear.

### Review and learn

- compare the result with the acceptance checks;
- review the complete diff and the route that produced it;
- record defects, warnings, uncertainty, and open questions;
- distinguish a successful task from a successful rollout;
- change the process only when the evidence supports the change.

### Scale cautiously

Before expanding use, confirm ownership, access controls, data boundaries,
incident handling, model/provider availability, independent review, and an
approved evidence system. A local demo does not provide those production
assurances.

## Controls and boundaries

The repository demonstrates several complementary controls:

- `AGENTS.md` and `.github/copilot-instructions.md` define supervised working
  conventions;
- `.github/skills/` contains repeatable task, security, routing, and handover
  procedures;
- `.github/hooks/` contains narrow safety and session-context examples;
- `TASKS.md` records task scope, role tags, receipts, decisions, and stopping
  points;
- Pi stores router assignments in the current session rather than a parallel
  store;
- focused tests and complete-diff review provide evidence for changes.

The hook and security examples are deliberately narrow. They are not a full
DLP, WAF, threat-intelligence, permissions, or government-assurance system.
See [`docs/copilot-hooks.md`](docs/copilot-hooks.md) and
[`docs/security-threat-intelligence-boundary.md`](docs/security-threat-intelligence-boundary.md)
for limits and production questions.

## Navigation

- [`AGENTS.md`](AGENTS.md) — repository working contract;
- [`TASKS.md`](TASKS.md) — authoritative task register and router fixtures;
- [`.github/skills/model-routing/SKILL.md`](.github/skills/model-routing/SKILL.md)
  — routing procedure and tag contract;
- [`runbooks/07-model-efficiency.md`](runbooks/07-model-efficiency.md) —
  capability, effort, and routing guidance;
- [`runbooks/09-pi-fallback.md`](runbooks/09-pi-fallback.md) — Pi session and
  extension validation;
- [`docs/adoption-and-outcomes.md`](docs/adoption-and-outcomes.md) — why
  adoption and outcomes must be measured separately;
- [`docs/copilot-hooks.md`](docs/copilot-hooks.md) — hook boundaries and
  verification limits.

## Focused checks

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/skills/model-routing/tests -v
node --test .pi/extensions/model-router/logic.test.ts
```

After changing the Pi extension, restart Pi or run `/reload`. Plain project
startup must register `/router` without treating the nested helper, test, or
type-declaration files as separate extensions.

## Public-use rules

- keep task examples and evidence public-safe;
- do not add credentials, private endpoints, or personal data;
- do not install packages during the supervised demo;
- do not commit, push, or publish from the agent session;
- do not treat a configured model label as proof of provider availability;
- do not let routing select new work or replace human approval and review.

The examples are educational. They are not evidence of production readiness,
official policy, or successful organisational adoption.
