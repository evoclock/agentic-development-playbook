# Portable reliability-watchdog reference

`reliability-watchdog.ts` is a Pi-compatible reference adapter for testing in
Pi or a compatible CLI environment. It demonstrates:

- a visible `/reliability` command;
- post-write detection for `edit`, `write`, write-like Bash, and IPython code;
- non-blocking reconciliation evidence;
- supervised timeout/abort guidance; and
- explicit refusal to retrigger work or mutate a board.

This is not evidence that GitHub Copilot CLI loads Pi extensions or hooks. Test
it in the target work-machine harness and record the actual loader/event
contract before adapting it to Copilot.

The adapter intentionally uses repository-relative paths and does not import
access credentials, start services, or modify a Kanban board. Its log format
is a portable demonstration record, not a project-specific reconciliation
schema.

## Local smoke check

From the repository root, inspect the extension and run the existing Pi
extension checks. Do not install packages as part of this reference copy.
After changing it, reload the harness before testing `/reliability`.
