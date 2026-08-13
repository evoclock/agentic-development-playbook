# Adoption and outcomes

Rolling out an AI tool does not establish that a process became faster, safer,
or more reliable. Adoption is an input to change, not evidence of a successful
outcome.

A responsible rollout measures the work around the tool:

- define the task, owner, acceptance checks, and stop point;
- provide useful project context without copying an entire repository;
- package repeatable procedures as skills;
- choose model capability and effort deliberately;
- keep deterministic work in deterministic code;
- use scoped tools and narrow, reviewed boundaries;
- inspect tests, reports, artifacts, and the complete diff;
- record limitations, uncertainty, and open questions;
- keep a human responsible for irreversible actions and publication.

The workflow diagram at
[`diagrams/agentic-workflow.png`](../diagrams/agentic-workflow.png) shows this
progression from human scope and task contract, through controlled delivery, to
evidence and review.

The model router is one concrete implementation of the method. It separates
implementation, planning, and review assignments, reads task role tags from the
local `TASKS.md`, and keeps session-local assignments in an ignored runtime
file. The task register is intentionally local-only. The surrounding skills
and hooks make the larger process repeatable and bounded; the router alone is
not a governance system.

## What to measure

Useful rollout evidence is task-level evidence:

- acceptance checks passed or failed;
- defects found and resolved;
- evidence produced and reviewed;
- time spent planning, implementing, and reviewing;
- route and effort chosen for the work;
- warnings, limitations, and unresolved decisions;
- human decisions at approval and stopping points.

Prompt count, login count, and model size are not outcome measures. A local
demo can show that a control works; it cannot establish organisational
readiness, production safety, or productivity gains.

## Source note

This motivation was prompted by the public X article [*AI Adoption is a
Myth*](https://x.com/i/article/2085540776512192512). The article is an external
viewpoint, not a benchmark, endorsement, or evidence about this repository.
