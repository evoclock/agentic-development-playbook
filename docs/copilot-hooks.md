# Copilot hook boundaries

This repository demonstrates GitHub Copilot CLI hooks for the synthetic pipeline.
The hooks are public examples. They are not a complete governance system.

## Active hooks

### `sessionStart`

The session-start command emits read-only context:

- branch and commit;
- modified and untracked paths;
- the synthetic demo task;
- the test command;
- a short diff summary.

It returns native Copilot `additionalContext`. It does not approve work, select
a task, write a handover, or replace human review.

### `preToolUse`

The pre-tool command returns `{}` for ordinary calls so normal permission
handling remains active. It returns a deny decision for selected commands:

- repository publication or history changes;
- destructive Git operations;
- recursive or forced deletion;
- elevated commands;
- package installation or removal;
- writes to the synthetic fixture directory.

The rules are deliberately narrow. They are not a general shell security
boundary.

## Context-pressure boundary

This repository does **not** install an active context-pressure hook.

A separate private control-plane implementation contains a useful reference
classifier. It is not copied here because the Copilot `sessionStart` payload
does not provide reliable context-usage percentages.

Installing a hook that claims to measure context pressure without receiving a
measurement would create false confidence. This repository therefore provides
only a standalone diagnostic:

```bash
python3 synthetic-project/scripts/copilot_context_pressure.py --percent 60
```

A supervised launcher may also set:

```text
AGENT_CONTEXT_PERCENT=60
```

The diagnostic reports four bands:

| Band | Meaning |
|---|---|
| `NORMAL` | Normal work is allowed. |
| `CHECKPOINT_REQUIRED` | Write a checkpoint and compact before substantive work. |
| `EMERGENCY_CHECKPOINT` | Checkpoint active state, compact, and stop substantive work. |
| `UNKNOWN` | Telemetry is unavailable; use short turns and obtain a measurement. |

The diagnostic is advisory. It is not installed in `.github/hooks/` and does
not claim to control Copilot context management.

## Verification limit

The local authoring environment does not include GitHub Copilot CLI. The scripts
have unit and subprocess tests. Final hook loading and decision behaviour must
be checked on a machine with the target Copilot CLI version.
