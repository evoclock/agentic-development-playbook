# 04 — Hooks and deterministic boundaries

## Purpose

Use narrow Copilot CLI hooks for read-only session context and selected
pre-tool safety decisions. In the workflow shown by
[`diagrams/agentic-workflow.png`](../diagrams/agentic-workflow.png), hooks sit
around controlled delivery: they provide context before work and make narrow
deterministic decisions before tools run.

Hooks are deterministic code; they do not replace project instructions, skills,
tests, human approval, or operating-system controls.

The active configuration is under:

```text
.github/hooks/session-state.json
.github/hooks/public-safety.json
```

The implementations are under:

```text
.github/hooks/copilot_session_state.py
.github/hooks/copilot_pretool_check.py
```

The two maintained hook surfaces are:

| Configuration | Implementation | Boundary |
|---|---|---|
| `session-state.json` | `copilot_session_state.py` | read-only session and task context |
| `public-safety.json` | `copilot_pretool_check.py` | narrow pre-tool deny and content review |

Their focused tests live under `.github/hooks/tests/`; the security fixture is
under `.github/hooks/fixtures/security-review.json`.

## Inspect before enabling

Read the configuration and scripts before using them:

```bash
python3 -m json.tool .github/hooks/session-state.json
python3 -m json.tool .github/hooks/public-safety.json
python3 .github/hooks/copilot_session_state.py --help
```

Run Copilot CLI from the repository root so it can discover `.github/`.

## `sessionStart`

The state hook emits read-only context such as:

- branch and commit;
- modified and untracked paths;
- the current `TASKS.md` task and receipt;
- whether `HANDOVER.md` is present;
- the required task-list and handover sequence;
- the relevant test command;
- a short diff summary.

It returns native Copilot `additionalContext`. It does not approve work, choose
a task, write a checkpoint, or publish a repository.

## `preToolUse`

For ordinary calls it returns `{}` so normal Copilot permission handling stays
active. It returns a deny decision for selected commands:

- publication or history changes without the required receipt;
- destructive Git operations;
- recursive or forced deletion;
- elevated commands;
- package installation or removal.

The rules are deliberately narrow. They are not a general shell-security
boundary.

The same hook applies the security-review contract to tool arguments:

- `accept` keeps normal permission flow;
- `redact` finds sensitive content and denies the original payload because the
  hook cannot mutate it;
- `reject` stops configured prompt-injection or limited MCP-marker content.

Missing or stale threat intelligence is `REVIEW_REQUIRED`, not acceptance. See
`docs/security-threat-intelligence-boundary.md` for the production process.

## Test the hook commands

Run the focused hook tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/hooks/tests -v
```

Probe a deny decision directly:

```bash
echo '{"toolName":"bash","toolArgs":{"command":"git push origin main"}}' \
  | python3 .github/hooks/copilot_pretool_check.py
```

The result must contain `"permissionDecision":"deny"`.

## Verification limit

The authoring environment may not include the target Copilot CLI. On the work
machine, verify the installed version, hook discovery, session context,
pre-tool decisions, normal permission handling for safe calls, and any approved
provider integration. Unit tests are not proof that a target CLI loaded the
configuration.
