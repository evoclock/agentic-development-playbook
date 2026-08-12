# Task register

This is the single task register for the public agent-routing demonstration.
The repository is the authority. Do not create a parallel board or handover
store. Historical pipeline receipts remain below as repository evidence, but
are not required by the router demo.

| ID | Task | Source | Status |
|---|---|---|---|
| `DEMO-001` | Guard small evaluation samples | legacy pipeline ticket | `ready for review` |
| `DEMO-002` | Secure agent context and route model work | Current approved session instruction | `in progress` |

## Status meanings

- `in progress`: approved work is underway;
- `ready for review`: the approved subtask has evidence, but a person must
  review it;
- `blocked`: the next action needs a decision or external dependency;
- `complete`: acceptance and publication decisions are complete.

## Router demo fixtures

These nine public-safe fixture tasks are the task metadata source for the Pi
router and the standalone Copilot-compatible resolver. The role tag is the
first mapped tag in the row; other tags remain context. They are examples in
this existing register, not a second task board or approval source.

| ID | Task example | Tags | Expected role |
|---|---|---|---|
| `ROUTER-IMPLEMENT-001` | Add a bounded validation check | `#implementer #python` | `implementation` |
| `ROUTER-IMPLEMENT-002` | Refactor a deterministic helper | `#implementer #typescript` | `implementation` |
| `ROUTER-IMPLEMENT-003` | Update a focused test | `#implementer #tests` | `implementation` |
| `ROUTER-PLAN-001` | Decompose an ambiguous task | `#planner #ambiguous` | `planning` |
| `ROUTER-PLAN-002` | Compare two implementation approaches | `#planner #tradeoff` | `planning` |
| `ROUTER-PLAN-003` | Define acceptance checks | `#planner #acceptance` | `planning` |
| `ROUTER-REVIEW-001` | Review a focused diff | `#reviewer #independent-review` | `review` |
| `ROUTER-REVIEW-002` | Check evidence and scope | `#reviewer #evidence` | `review` |
| `ROUTER-REVIEW-003` | Review security-boundary wording | `#reviewer #security` | `review` |

## Receipts

### `DEMO-001` / minimum test-row check

- Status: `ready for review`
- Files changed: legacy pipeline health-report source and tests.
- Checks: the legacy pipeline test suite passed with 46 tests; all four
  scenarios returned their expected exit codes; healthy output matched the
  expected post-change fixture.
- Evidence: `evaluate.test_rows` passes at `100 >= 50` and warns at `20 < 50`.
- Open questions: publication review remains open.
- Next decision: review the uncommitted diff before publication.

## Current session scope — DfE demo continuation

No Kanban ticket was supplied for this follow-on scope, so this explicit scope
is the task list for the session. It must be updated after each subtask.

**Scope:** Review and compact the D2 diagrams, update the public outreach and
supporting documentation already in progress, validate the maintained codebase
inventory, run the remaining bounded pipeline/link/safety/rendering checks,
and preserve the no-MCP/no-plugin/no-publication boundary. Copilot markdown,
skills, hooks, and live Pi/Copilot validation remain separate follow-on work.

**Current subtask:** Compact and enlarge the D2 diagram layouts, rerender the
SVGs, validate both sources, inspect the resulting dimensions, and stop.

**Definition of done:** The D2 sources are compact and readable, SVG output
validates and is reviewed, the inventory and final checks have factual receipts,
all unresolved decisions remain recorded, and no commit or publication claim is
made without human review.

### Session receipts — `dfe-agentic-development-demo`

- **Subtask:** Inventory update
  - **Status:** `ready for validation`
  - **Files changed:** `pipeline_output/codebase_inventory.jsonl`
  - **Checks:** inventory refreshed to 20 Python records; one new launcher-test
    record and seven refreshed records; no broader validation was run.
  - **Next decision:** validate the inventory separately.
- **Subtask:** Reliability investigation
  - **Status:** `complete for this session`
  - **Evidence:** no silently dropped tool call was found; three failures were
    ordinary wrong-directory/path attempts; the existing driver reliability
    patch was recorded separately and no target-repository files changed.
  - **Next decision:** continue bounded playbook validation.
- **Subtask:** Full standard-library suite
  - **Status:** `passed`
  - **Checks:** legacy pipeline test suite — 48 passed.
  - **Next decision:** continue bounded pipeline and diagram checks.
- **Subtask:** Healthy pipeline acceptance check
  - **Status:** `blocked by invocation mismatch`
  - **Evidence:** exit code `0`; only the generated artifact path differed
    from the expected acceptance output directory.
  - **Next decision:** rerun with the repository-root acceptance invocation;
    do not normalize the fixture without review.
- **Subtask:** D2 layout inspection
  - **Status:** `complete for this session`
  - **Evidence:** The prior SVG dimensions were `3295 × 431` and `2948 × 674`;
    the user rejected both layouts as too small and drawn out.
  - **Next decision:** see the dated D2 layout-correction receipt below.
- **Subtask:** D2 layout correction — 2026-08-11
  - **Task:** `DEMO-001`
  - **Status:** `complete for this session`
  - **Evidence:** The user rejected the two-row output because labels and arrows
    overlapped the boxes and the layout did not match the repository's stronger
    diagram precedent. The old SVGs remain unmodified as historical generated
    files only through the current working-tree replacement.
  - **Next decision:** use the redesigned receipt below.
- **Subtask:** D2 layout redesign and PNG export — 2026-08-11
  - **Task:** `DEMO-001`
  - **Status:** `complete for this session`
  - **Evidence:** The user subsequently identified arrow/header-label collisions;
    the clearance correction is recorded in the receipt below.
  - **Next decision:** use the corrected receipt below.
- **Subtask:** D2 arrow-label clearance correction — 2026-08-11
  - **Task:** `DEMO-001`
  - **Status:** `complete for this session`
  - **Files changed:** `diagrams/agentic-workflow.d2`,
    `diagrams/agentic-workflow.svg`, `diagrams/agentic-workflow.png`
  - **Checks:** the remaining workflow source validated; its SVG rendered with
    `d2 -l elk --pad 60`; its PNG rendered with the existing `rsvg-convert`;
    `git diff --check` passed. No package or browser was installed.
  - **Evidence:** Removed container/header labels from the workflow arrow lane
    and folded each stage title into its first node. The workflow PNG was
    visually inspected with no text, box, or arrow overlap found. The remaining
    outputs are `1079 × 2184`; its SVG viewBox matches that size. No commit,
    push, or publication was made.
  - **Next decision:** see the deletion receipt below.
- **Subtask:** Remove rejected control-boundaries diagram — 2026-08-11
  - **Task:** `DEMO-001`
  - **Status:** `ready for review`
  - **Files changed:** deleted `diagrams/control-boundaries.d2`,
    `diagrams/control-boundaries.svg`, and `diagrams/control-boundaries.png`;
    updated `README.md` and this receipt; removed the redundant map file.
  - **Checks:** the three artifacts no longer exist; active README and content
    map descriptions now name only the workflow diagram; `git diff --check`
    passed. No package or browser was installed.
  - **Evidence:** Applied the user's decision that a separate explanatory
    permitted/prohibited diagram is unnecessary. The workflow diagram remains
    the sole public diagram output.
  - **Open questions:** Human review of the remaining workflow SVG/PNG pair;
    inventory, pipeline, link, safety, and final-diff checks remain unperformed.
  - **Next decision:** human review of the remaining workflow pair, then approve
    the next separately bounded validation subtask.

## Admitted scope — secure agent context and model routing

The latest direct instruction supersedes the earlier recommendation to use
`copilot_session_state.py` as the lightweight replacement. The current scope is
focused on AGENTS.md, task organization, skills, hooks, and effective work with
agentic AI.

### Definition of done

- Add security-oriented demo skills/hooks based on Hillstar/Testudo prior art:
  PII and secret redaction, hidden Unicode/BIDI defense, payload and prompt-
  injection defense, OWASP/MCP threat checks, explicit accept/redact/reject
  decisions, and security acceptance checks.
- Add a deterministic model-routing skill/router that chooses the cheapest
  capable model for routine implementation and stronger models for ambiguous
  planning and review.
- Keep examples synthetic and public-safe; do not install packages, execute or
  register MCP/plugins, start live model sessions, commit, or push without
  approval.
- Add focused tests and run the full standard-library suite before treating the
  implementation as ready for review.

### Session receipt — scope admission and recovery checkpoint

- **Task:** `DEMO-002`
- **Status:** `in progress`
- **Files changed:** `TASKS.md`; `HANDOVER.md` pending append in this checkpoint.
- **Checks:** read-only inventory found no existing security or model-routing
  implementation in this playbook; Hillstar/Testudo prior art was inspected.
- **Evidence:** Existing `copilot_session_state.py` and read-only MCP examples
  remain prior playbook examples; no new implementation has started.
- **Open questions:** Which bounded file paths should contain the security
  skill, hook, router, fixtures, and tests? Which Testudo patterns are safe to
  reuse verbatim versus reimplement behind a small public demo interface?
- **Next decision:** approve the first implementation subtask: define the
  security result contract and add synthetic acceptance fixtures, then stop.

### Session receipt — remove rejected context-pressure diagnostic

- **Status:** `ready for review`
- **Files changed:** deleted the legacy context-pressure diagnostic and its
  test; removed both inventory records and active documentation references.
- **Checks:** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s
  legacy pipeline test suite — 40 passed; active-reference search passed;
  `git diff --check` passed.
- **Evidence:** No diagnostic file remains and no active documentation,
  inventory, or command reference remains. Historical handover text is
  retained under the append-only handover rule.
- **Open questions:** None for this cleanup.
- **Next decision:** begin the separately bounded security skill/hook
  implementation subtask.

### Session receipt — security result contract and synthetic fixtures

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** extended `.github/hooks/copilot_pretool_check.py`;
  extended `.github/hooks/tests/test_copilot_pretool_check.py`; added
  `.github/hooks/fixtures/security-review.json`.
- **Checks:** focused pre-tool tests — 10 passed; full suite — 42 passed;
  `python3 -m py_compile .github/hooks/copilot_pretool_check.py`;
  `git diff --check` passed.
- **Evidence:** The existing pre-tool hook now returns deterministic
  accept/redact/reject content-review results. Redaction findings remove
  synthetic PII/secrets from returned content without exposing raw evidence;
  prompt-injection, OWASP, and MCP-threat findings reject. Redact/reject
  results deny the tool because the hook cannot mutate tool arguments.
- **Open questions:** The detector is intentionally a small demo boundary,
  not complete DLP/WAF or government assurance. Inventory metadata needs a
  later refresh after implementation settles.
- **Next decision:** add the tracked security-review skill and update the
  active hook documentation/acceptance checks, then stop.

### Session receipt — relocate hook infrastructure out of the legacy pipeline subtree

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** moved `copilot_pretool_check.py`, `copilot_session_state.py`,
  their tests, and `security-review.json` under `.github/hooks/`; updated both
  hook configurations, runbook/slides references, and inventory paths.
- **Checks:** hook test suite — 15 passed; legacy pipeline suite — 27 passed;
  no hook/security implementation remains in the legacy pipeline subtree;
  `git diff --check` passed.
- **Evidence:** `.github/hooks/public-safety.json` and
  `.github/hooks/session-state.json` now invoke the relocated implementations.
  The relocated hook files are staged; no commit or push was made.
- **Open questions:** None for relocation.
- **Next decision:** add the tracked `.github/skills/security-review/SKILL.md`
  and update active hook documentation/acceptance checks.

### Session receipt — security skill and threat-freshness boundary

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** added and staged `.github/skills/security-review/SKILL.md`;
  updated `docs/copilot-hooks.md`, `runbooks/03-skills.md`, `runbooks/04-hooks.md`,
  `.github/copilot-instructions.md`, and the existing pipeline-triage skill.
- **Checks:** skill frontmatter/freshness contract passed; no active
  context-pressure or removed-CLI references; hook suite — 15 passed; pipeline
  suite — 27 passed; `git diff --check` passed.
- **Evidence:** The skill documents accept/redact/reject semantics and states
  explicitly that current OWASP checks are static, there is no automatic OWASP
  or CVE feed/update, and missing or stale threat intelligence is
  `REVIEW_REQUIRED` rather than `accept`.
- **Open questions:** A production deployment still needs an approved,
  authenticated threat-intelligence update path, pinned rule revisions, and
  independent security controls; this demo does not provide those.
- **Next decision:** implement the separate tracked model-routing skill/router.

### Session receipt — remove live OWASP rules and document production boundary

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** removed OWASP web-rule patterns from
  `.github/hooks/copilot_pretool_check.py`; changed the fixture to the limited
  MCP-marker case; added `docs/security-threat-intelligence-boundary.md`;
  updated the security skill and active hook/runbook documentation.
- **Checks:** hook suite — 15 passed; pipeline suite — 27 passed; no OWASP web
  rules remain in the live hook; required files/link targets exist;
  `git diff --check` passed.
- **Evidence:** The document states that OWASP/CVE scanning, threat-feed
  ingestion, signed rule bundles, SBOM matching, and automatic updates are
  outside this demo. It specifies the proper production lifecycle and the
  `REVIEW_REQUIRED` behavior for missing or stale intelligence.
- **Open questions:** The production process still needs an approved source,
  SBOM/CVE tooling, signing/provenance mechanism, owner, cadence, and existing
  evidence-system integration.
- **Next decision:** implement the separate tracked model-routing skill/router.

### Session receipt — tagged interactive model-routing demo

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** added the configurable roster, router, skill, and tests
  under `.github/skills/model-routing/`; updated `README.md`,
  `runbooks/07-model-efficiency.md`, and router inventory metadata.
- **Checks:** router tests — 10 passed; interactive session demo selected
  `general-planner` with `medium` effort for `DEMO-002` review; tagged planning
  selection matched `ambiguous` to `general-planner` with `high` effort;
  `git diff --check` passed.
- **Evidence:** `--list` displays the configured roster. `--task-id`, `--role`,
  and `--tags` emit a tagged route as JSON. `--interactive` displays compatible
  models, accepts a model and effort, and emits the selected route without
  starting a provider or persisting session state.
- **Open questions:** The roster contains public placeholder aliases and must
  be edited for the target harness's actual available models and effort names.
- **Next decision:** review and edit the router/README wording before staging;
  then run the final repository validation subtask.

### Session receipt — real Pi `/router` extension

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** added `.pi/extensions/model-router.ts`,
  `.pi/extensions/model-router-logic.ts`, and its Node test; updated the model
  routing skill, README, runbook, and task receipt.
- **Prior art reused:** Pi's `preset.ts` and `tools.ts` extension patterns,
  `ctx.ui.select()`, `pi.setModel()`, `pi.setThinkingLevel()`,
  `ctx.modelRegistry.getAvailable()`, and session custom entries.
- **Checks:** TypeScript extension type-check passed against the installed Pi
  declarations; router-logic Node tests — 3 passed; `git diff --check` passed.
- **Evidence:** `/router` configures implementation, planning, and review in
  interactive selectors; `/router use <role>` activates a configured route;
  `/router task <id> <tags>` maps tags to a role and activates its route;
  assignments are stored in the existing Pi session, not a parallel board.
- **Open questions:** This current Pi process must run `/reload` before the
  newly added project-local extension can register `/router`; the live TUI
  interaction has not been executed by the agent harness.
- **Next decision:** user runs `/reload` and tests `/router`; then review the
  extension behavior and wording before staging or final validation.

### Session receipt — project-local extension discovery fix

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** kept `.pi/extensions/model-router.ts` as the sole direct
  extension entrypoint; moved the helper and test to
  `.pi/extensions/model-router/logic.ts` and
  `.pi/extensions/model-router/logic.test.ts`; updated the two relative imports;
  appended this receipt to `TASKS.md`.
- **Prior art reused:** Pi's documented auto-discovery rule for direct
  `.pi/extensions/*.ts` files and nested `*/index.ts` entrypoints, plus the
  existing extension's `ctx.ui.select()` and session-router implementation.
- **Checks:** project-local auto-discovery registered `/router` with no invalid
  factory errors; plain Pi TUI interaction opened the `Implementation model`
  selector; helper tests — 3 passed; TypeScript check against installed Pi
  declarations — passed; `git diff --check` — passed; no scratch config remains.
- **Evidence:** the route picker still reports Pi's actual available catalogue;
  the extension source is reported as project-local auto-discovered; no package,
  session board, evidence store, commit, push, or staged file was created.
- **Open questions:** the draft wording, role/tag semantics, and activation
  behavior still need human review; the available-model catalogue is harness
  dependent.
- **Next decision:** review the three extension files and then decide whether
  any behavior or documentation changes are needed before staging.

### Session receipt — Pi router test type declarations

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** added the narrow local Node test-module declarations at
  `.pi/extensions/model-router/node-shims.d.ts`; referenced them from
  `logic.test.ts`; appended this receipt to `TASKS.md`.
- **Prior art reused:** the existing Node test file and the installed Pi
  declaration tree; no package or dependency installation was used.
- **Checks:** the original test-file type-check reproduced the two missing
  `node:*` errors; the isolated test type-check passed; combined router and
  test TypeScript check passed; Node tests — 3 passed; project-local Pi
  discovery returned `/router` with no extension errors; no scratch config
  remains.
- **Evidence:** the shim declares the two Node APIs used by the test plus the
  small Pi API surface needed for editor-style checking; runtime imports and
  behavior are unchanged, and the Copilot Python router is unaffected.
- **Open questions:** Copilot compatibility and shared task-tag routing remain
  untested until tomorrow; no live Copilot session was started.
- **Next decision:** validate the harness-neutral task-tag behavior in Copilot,
  then continue the task-aware `/router task <task-id>` implementation review.

### Session receipt — editor-style Pi extension type fallback

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** extended `.pi/extensions/model-router/node-shims.d.ts`
  with the exact Node and Pi type surface used by `model-router.ts`; added a
  type-reference directive to the extension; appended this receipt to
  `TASKS.md`.
- **Checks:** the original editor-style check reproduced 15 diagnostics;
  the same check now passes with 0 diagnostics; installed-Pi declaration
  type-check passes; Node tests — 3 passed; project-local Pi discovery still
  registers `/router` with no extension errors; no package was installed and
  no scratch file remains.
- **Evidence:** the fallback is type-only; the extension still loads the real
  Pi modules at runtime. The installed-Pi check validates the actual Pi API
  declarations separately.
- **Open questions:** Copilot validation and shared task-tag routing remain
  deferred until tomorrow; no live Copilot session was started.
- **Next decision:** test the shared task-tag contract in Copilot, then resume
  the task-aware task lookup implementation.

### Session receipt — adoption/control-plane documentation and validation

- **Task:** `DEMO-002`
- **Status:** `ready for review`
- **Files changed:** rewrote `README.md`, `AGENTS.md`,
  `.github/copilot-instructions.md`, the five maintained skill documents,
  `docs/adoption-and-outcomes.md`, `docs/copilot-hooks.md`, runbooks `INDEX`
  and `01`–`09`, `TASKS.md`, and `HANDOVER.md`.
- **Prior art reused:** `diagrams/agentic-workflow.png`, the adoption rationale,
  all five maintained skills, both hook configurations, and the existing Pi and
  standalone router implementation.
- **Diff summary:** restored the rollout/adoption/evidence narrative; documented
  the workflow diagram, complete skill set, complete hook set, role-based
  routing, task tags, Copilot/Pi boundaries, and publication controls; removed
  retired pipeline references from active documentation and root task/handover
  records.
- **Checks:** model-routing tests — 12 passed; hook tests — 15 passed; Pi logic
  tests — 4 passed; editor-style TypeScript check — passed; Pi RPC discovery
  registered `/router` with no extension errors; no-session task route smoke
  test activated the review route for `ROUTER-REVIEW-001`; relative Markdown
  links checked across 21 files; whitespace checks passed.
- **Evidence:** active README, skills, docs, runbooks, instructions, task
  register, and handover contain no retired pipeline references. The root
  `TASKS.md` remains the sole task register and contains the nine router
  fixtures. No package was installed, and no session file was created by the
  smoke test.
- **Open questions:** live Copilot hook loading and model activation remain
  unvalidated in this authoring environment; files inside the retired,
  self-contained subtree remain untouched.
- **Next decision:** human review of the documentation and focused diff; do
  not stage, commit, push, or publish without approval.
