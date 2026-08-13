# Frozen example: task register and receipt

> **Frozen snapshot:** Illustrative end state only. This is not the active
> task register for a checkout.

| ID | Task | Source | Status |
|---|---|---|---|
| `PREFLIGHT-001` | Inspect the bounded sample file | preflight fixture | `ready for review` |

## Frozen subtask receipt

- **Task:** `PREFLIGHT-001`
- **Subtask:** Run the bounded inspection, security baseline, and healthy/warning
  evidence triage.
- **Status:** `ready for review`
- **Files changed:** none during the inspection; the receipt and handover are
  the stopping-point records.
- **Route example:** implementation with `gpt-5.6-luna` at `medium` effort;
  `execution_model_verified=false`.
- **Checks:** preflight suite - 6 passed; focused hook suite - 15 passed;
  model-routing suite - 17 passed; `git diff --check` passed.
- **Evidence:** healthy `test_rows=100` against threshold `>=50` returned
  `HEALTHY`; warning `test_rows=20` against threshold `>=50` returned
  `WARNING`. Both scenarios are deterministic `fixture-v1` artifacts with
  empty failure logs. Security baseline returned `accept` for public-safe
  content.
- **Open questions:** The warning fixture does not explain its low row count;
  live skill and hook loading, current threat intelligence, and provider
  execution identity remain unverified.
- **Next decision:** human review of the complete diff and evidence; stop
  before commit, push, merge, or publication.
