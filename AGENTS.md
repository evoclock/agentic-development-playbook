# Project instructions

This repository is a public playbook for governed agentic-AI development. It
explains adoption, rollout, evidence, controls, and a live role-based
Copilot CLI model router.

## Start here

1. Read `README.md`.
2. Read the local `TASKS.md` and matching task row; if it is absent, create
   the local register as part of the approved task setup before routing.
3. Read the relevant skill under `.github/skills/`.
4. Read the relevant runbook and workflow diagram.
5. Inspect Git status before editing.

## Working method

- State the goal, files in scope, files unchanged, checks, and stopping point.
- Use the smallest suitable change.
- Keep deterministic work in code and use the smallest suitable route.
- Add or update tests for code changes.
- Run the focused checks and authorized repository suite.
- Inspect the complete diff before publication.
- Report evidence, limits, and open questions.

## Commands

From the repository root:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .github/hooks/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .github/skills/model-routing/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s preflight/tests -v
```

Use the task-specific runbook for any additional deterministic checks. Do not
edit generated or external evidence to make a check pass.

## Boundaries

- Use public-safe examples and no personal or confidential data.
- Do not install packages during the demo.
- Do not add secrets, private paths, private endpoints, or real records.
- Do not edit generated output to make a check pass.
- Do not register or run MCP in the default demonstration.
- Do not commit or push without explicit human approval.
- Keep the agent session supervised.

Project-specific Copilot instructions, skills, and hooks are under `.github/`.
The repository does not include a Pi implementation; provider availability and
Copilot model activation remain target-CLI concerns.
