# 03 — Skills for repeatable agentic work

## Purpose

Package a repeatable procedure as a project skill. A skill should guide an
agent through evidence review without duplicating the whole project manual.

The maintained skill set covers the full workflow shown in
[`diagrams/agentic-workflow.png`](../diagrams/agentic-workflow.png):

```text
.github/skills/task-list-update/SKILL.md       # scope, receipt, next decision
.github/skills/handover/SKILL.md                # durable stopping-point state
.github/skills/model-routing/SKILL.md           # role/model/effort selection
.github/skills/security-review/SKILL.md        # content and handoff boundary
.github/skills/pipeline-run-triage/SKILL.md    # artifact and failure review
```

Together they move the agent from a human-owned task contract, through
controlled delivery, to reviewable evidence. They do not grant permissions or
replace human approval.

## Skill anatomy

A project skill contains:

- YAML frontmatter;
- a lowercase hyphenated name matching its directory;
- a description saying when to use it;
- a short, ordered procedure;
- an output contract;
- explicit boundaries and stop rules.

The description is the routing signal available before the full skill is
loaded. Keep the body short enough for progressive disclosure.

## How the skills enhance agentic development

- `task-list-update` makes scope and completion explicit instead of relying on
  an implicit conversation state;
- `handover` preserves evidence and open questions when a session stops;
- `model-routing` matches implementation, planning, and review work to
  separate capability and effort choices;
- `security-review` creates a deterministic accept, redact, or reject boundary
  before risky content is handed to a tool or model;
- `pipeline-run-triage` turns observable artifacts and thresholds into a
  repeatable evidence review.

The workflow diagram places these skills between the task contract and human
review: skills make the procedure repeatable, scoped tools limit actions, and
deterministic checks make outcomes inspectable.

## Model-routing skill (Copilot CLI path)

Use the routing skill when a task needs an explicit implementation, planning,
or review route. Create/read `TASK.md` first, then ask Copilot:

```text
Use the project model-routing skill. Sync the Copilot roster, show compatible
models and all effort levels, ask me to select implementation/planning/review
assignments, save them, and route TASK.md before doing task work.
```

The skill calls:

```bash
python3 .github/skills/model-routing/sync_runtime_models.py
python3 .github/skills/model-routing/model_router.py \
  --task-file TASK.md
```

The first command writes raw and normalized roster outputs. The second emits
the task route and reads the saved role assignments.

## Output contract

A skill response should use this shape:

```text
Status: <READY|REVIEW_REQUIRED|BLOCKED|FAILED>
Task: <task id and role tag>
Evidence:
- <check>: <observed result>
Action: <next controlled step>
Scope: <files changed and files unchanged>
Open questions: <explicit uncertainty>
```

The skill must use evidence from tracked files and commands. It must not invent
causes, convert warnings into personal judgements, or grant permissions.

## Validation

Check the frontmatter and confirm:

- the name matches the directory;
- the description is present and trigger-specific;
- the body names the evidence paths;
- the output contract is unambiguous;
- the procedure has a stopping point.

Run the focused model-routing checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/skills/model-routing/tests -v
```

## Boundaries

A skill provides procedure and context. It does not grant permissions, replace
hooks, make a source authoritative, or replace human review. Keep credentials,
private endpoints, and personal data out of skills and examples.
