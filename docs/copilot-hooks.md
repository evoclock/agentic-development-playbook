# Copilot hook boundaries

This repository demonstrates narrow GitHub Copilot CLI hooks for a supervised
agentic workflow. The hooks provide context and deterministic boundary
decisions; they are not a complete governance or security system.

## Active hooks

### `sessionStart`

The session-start command emits read-only context:

- branch and commit;
- modified and untracked paths;
- the current `TASKS.md` task and receipt;
- whether `HANDOVER.md` is present;
- the task-list and handover sequence;
- the relevant focused checks;
- a short diff summary.

It returns native Copilot `additionalContext`. It does not approve work, select
a task, write a handover, or replace human review.

### `preToolUse`

The pre-tool command returns `{}` for ordinary calls so normal permission
handling remains active. It returns a deny decision for selected commands:

- repository publication or history changes without the required receipt;
- destructive Git operations;
- recursive or forced deletion;
- elevated commands;
- package installation or removal.

The rules are deliberately narrow. They are not a general shell-security
boundary.

### Security content review

The pre-tool hook applies the `accept`, `redact`, or `reject` contract from
`.github/skills/security-review/SKILL.md` to tool arguments:

- `accept` keeps normal permission flow;
- `redact` identifies sensitive content and denies the original payload because
  the hook cannot mutate it;
- `reject` stops configured prompt-injection or limited MCP-marker content.

It covers the public demo boundary for PII, secrets, hidden Unicode/BIDI
controls, and selected injection markers. It does not implement an OWASP web
scanner, CVE database, or automatic threat-intelligence update. Missing or
stale threat intelligence is `REVIEW_REQUIRED`, not acceptance. See
[`security-threat-intelligence-boundary.md`](security-threat-intelligence-boundary.md)
for the production process.

## Task receipt boundary

Hook payloads do not provide a reliable semantic `subtask complete` event. The
`task-list-update` skill records the approved subtask in `TASKS.md`, and the
`handover` skill records wider session state in `HANDOVER.md`.

The pre-tool hook checks for the required receipt before a commit, push, merge,
or rebase can enter human review. It does not mark work complete and does not
replace review.

## Verification limit

The local authoring environment may not include the target Copilot CLI. The
scripts have unit and subprocess tests, but final validation must check the
installed CLI version, hook discovery, session context, pre-tool decisions,
and normal permission handling on the target machine.
