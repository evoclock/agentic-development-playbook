# 01 — Supervised Copilot CLI session

## Purpose

Start a supervised Copilot CLI session for the agentic-AI rollout demonstration.
This runbook establishes context, task ownership, model-routing intent, and
review boundaries. It does not grant publication or production authority.

## Prerequisites

- a clean or understood checkout;
- Copilot CLI installed and authenticated through an approved local process;
- Python 3 available for the deterministic resolver;
- a human ready to review commands, writes, and diffs.

Check the environment without changing the repository:

```bash
git status --short --branch
python3 --version
copilot --version
```

## Start the session

Run Copilot CLI from the repository root so it can discover `.github/`:

```bash
copilot
```

Use `/help` to inspect commands supported by the installed version. Start with
this bounded prompt:

```text
Read AGENTS.md, README.md, and the local TASKS.md if it exists; if it does not,
create the local register during task setup. Then read
.github/skills/model-routing/SKILL.md. Create or read the active TASK.md
contract, return its task ID, role tag, acceptance checks, files in scope, and
stopping point, and do not edit files yet.
```

Then use the Copilot-native model-routing flow:

```text
Use the project model-routing skill. Run
python3 .github/skills/model-routing/sync_runtime_models.py, read the generated
models.runtime.json, present model and effort choices for implementation,
planning, and review, save the confirmed assignments, then route TASK.md
before any task work.
```

The skill calls `sync_runtime_models.py`, which writes
`.github/skills/model-routing/models.raw.jsonl` and
`.github/skills/model-routing/models.runtime.json`. It then calls
`model_router.py` to write `models.assignments.json` and to emit the selected
task route as JSON. These scripts do not start another agent session.
Use the emitted model and effort to launch the bounded task through a separate
process:

```bash
copilot --model <model_id> --effort <effort> -p '<task prompt>'
```

The selected model must perform the task and use its own Bash tool when needed.
Record the launch command, session ID, usage, and tool telemetry when exposed;
launch evidence is not provider execution attestation.

## Review every action

For each proposed command:

1. read the command;
2. check its path and scope;
3. check whether it writes files or changes history;
4. approve only the smallest suitable command;
5. inspect the result before the next prompt.

Stop and report if the task is unclear, a command requests an install, a
private path, publication, or an out-of-scope write.

## Session receipt

Record locally:

- CLI version and harness identity;
- task ID and role tag;
- commands reviewed;
- tests and checks run;
- final status, limitations, and open questions.

Do not track raw session output or credentials. The local authoring environment
may not include Copilot CLI; validate final hook loading and model-activation
behaviour on the target work machine before claiming it is active.
