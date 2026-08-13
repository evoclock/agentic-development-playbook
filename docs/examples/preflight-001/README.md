# Frozen `PREFLIGHT-001` snapshots

> **Frozen snapshot:** This directory is reader-facing example material. It
> illustrates the end results of the rehearsal; it is not an active task
> register or evidence store.

These public-safe snapshots show the shapes produced after:

```text
TASK.md -> model route -> bounded task -> security review
          -> evidence triage -> TASKS.md receipt -> HANDOVER.md
```

The route, metrics, and wording are synthetic and explanatory. They do not
attest that a provider executed the task, and they must not be copied into an
active workspace as current state.

- `TASK.md` shows the bounded task contract;
- `TASKS.md` shows a representative route and subtask receipt;
- `HANDOVER.md` shows the stopping-point record.

To run the rehearsal yourself, start with the empty
`demo-workspace/<session-name>/` container and follow
`runbooks/10-skill-preflight.md`. The preparation script does not copy these
snapshots into the runnable child.
