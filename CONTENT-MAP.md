# Content map

This repository supports one recorded GitHub Copilot CLI walkthrough and a set
of deeper manuals.

## Main route

The recording follows one synthetic data-science operations task:

1. frame the adoption problem;
2. inspect the executable project;
3. define scope and acceptance checks;
4. plan the change with GitHub Copilot CLI;
5. apply project instructions and the triage skill;
6. use read-only MCP context;
7. implement a small health-report check;
8. run deterministic scenarios and tests;
9. inspect the full diff;
10. review the result;
11. explain model and token choices.

The recording is the overview. The executable project and hook documentation
provide the current detail.

## Available material

| Area | Status | Purpose |
|---|---|---|
| `synthetic-project/` | implemented | Executable synthetic data-science pipeline |
| `.github/` | implemented | Copilot instructions, skill, and hooks |
| `docs/copilot-hooks.md` | implemented | Hook boundaries and telemetry limits |
| `synthetic-project/mcp/` | implemented | Read-only MCP context example |
| `synthetic-project/runbooks/` | implemented | Pipeline execution and triage procedure |
| `docs/publication-policy.md` | implemented | Public-content boundary and review |

## Planned material

| Area | Purpose |
|---|---|
| `runbooks/01` through `runbooks/08` | Deep walkthrough manuals |
| `slides/` | Marp source and generated slide material |
| `diagrams/` | D2 source and rendered diagrams |
| `outreach/` | Public summaries for related writing |

## Audience

The primary audience is data scientists who use AI tools and want a practical
introduction to agentic development.

The material starts with a small executable task. It introduces one control at
a time. It does not assume that the reader will run an autonomous agent.

## Public boundary

The video and local recording files are not part of this repository. The
repository contains only public scripts, examples, and manuals needed to repeat
the walkthrough.

All examples use synthetic data. Do not add private work context.
