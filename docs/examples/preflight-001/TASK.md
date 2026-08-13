# Frozen example: active task contract

> **Frozen snapshot:** Illustrative end state only. This is not the active
> contract for the source checkout.

Task ID: PREFLIGHT-001
Role tag: #implementer

## Goal

Inspect the bounded sample and preflight evidence, exercise the maintained
skills and hooks, and return reviewable public-safe evidence without changing
the source checkout.

## Files in scope

- `src/sample.txt`
- `preflight/evidence/`
- `runbooks/10-skill-preflight.md`
- approved checks and the local task records created by the rehearsal

## Files unchanged

- the seeded fixture and evidence artifacts;
- the source checkout;
- generated evidence and provider state.

## Acceptance checks

- Read the toy conventions and confirm the task boundary.
- Refresh and save model-routing assignments for implementation, planning, and
  review, then route this contract before task work.
- Run the bounded inspection and authorized focused checks.
- Run the deterministic security baseline and report only public-safe
  categories.
- Compare healthy and warning evidence with their thresholds.
- Record a receipt and handover without publishing history.

## Allowed commands

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s preflight/tests -v`
- focused hook and model-routing test suites;
- `git diff --check`;
- read-only Git inspection;
- supervised model-bound `copilot -p` execution using the selected route.

## Stopping point

Stop with the receipt and handover ready for human review. Do not commit,
push, merge, publish, install packages, register MCP, or select new work.
