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
Read AGENTS.md, TASKS.md, README.md, and
.github/skills/model-routing/SKILL.md. Return the approved task, its hash tags,
role, acceptance checks, files in scope, and stopping point. Do not edit files.
```

For a deterministic route preview, run:

```bash
python3 .github/skills/model-routing/model_router.py \
  --task-id ROUTER-PLAN-001
```

The resolver reads the existing task register and emits JSON. It does not start
another agent session or contact a provider.

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
