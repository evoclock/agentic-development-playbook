# Runbooks

These runbooks describe the supervised agentic-AI rollout method and the live
model-routing demonstration. They are supporting procedures, not a second task
board or approval store.

## Start here

The workflow diagram at [`diagrams/agentic-workflow.png`](../diagrams/agentic-workflow.png)
shows the progression from human scope and task contract through controlled
delivery to evidence and review.

1. [`README.md`](../README.md) — adoption, outcomes, controls, and the demo;
2. [`AGENTS.md`](../AGENTS.md) — repository working contract;
3. local `TASKS.md` — ignored task register and router fixtures for the
   current checkout;
4. [`.github/skills/model-routing/SKILL.md`](../.github/skills/model-routing/SKILL.md)
   — task tags and route activation;
5. [`docs/adoption-and-outcomes.md`](../docs/adoption-and-outcomes.md) —
   why adoption and outcomes must be measured separately.

The complete skill set is under `.github/skills/`: `task-list-update` records
subtask evidence, `handover` preserves stopping-point state, `model-routing`
selects role routes, `security-review` checks risky content, and
`pipeline-run-triage` reviews observable artifacts and failures. The hook set
under `.github/hooks/` consists of `session-state` for read-only context and
`public-safety` for narrow pre-tool decisions.

## Deep-dive runbooks

- [`01-copilot-cli.md`](01-copilot-cli.md) — start a supervised Copilot session;
- [`02-project-context.md`](02-project-context.md) — define task context and
  acceptance checks;
- [`03-skills.md`](03-skills.md) — package repeatable procedures;
- [`04-hooks.md`](04-hooks.md) — inspect deterministic hook boundaries;
- [`05-mcp.md`](05-mcp.md) — review optional read-only context integrations;
- [`06-agentic-workflow.md`](06-agentic-workflow.md) — inspect, plan,
  implement, test, review, and stop;
- [`07-model-efficiency.md`](07-model-efficiency.md) — choose capability and
  effort deliberately;
- [`08-publication-checks.md`](08-publication-checks.md) — review public
  claims, links, and complete diffs;
- [`10-skill-preflight.md`](10-skill-preflight.md) — rehearse every skill and
  hook safely before a supervised demonstration;
- [`../docs/examples/preflight-001/`](../docs/examples/preflight-001/) —
  frozen snapshots illustrating the preflight end state for readers;
- The repository has no Pi extension or Pi fallback; the supported live
  demonstration is the Copilot CLI path in `01-copilot-cli.md`.

## Safe default

Use a clean checkout and a supervised session. Review every proposed command
and every diff. Do not provide production data or credentials to an agent. Do
not grant write access broader than the approved task requires. Keep a human in
control of irreversible actions and publication.

## Method

Use deterministic code for deterministic work. Use models for interpretation,
planning, and review. Select the smallest capable route, record evidence, state
limitations, and stop at the approved boundary.

## Terms

**Agent** means a model-driven tool that can inspect a project and use approved
capabilities.

**Skill** means a reusable procedure and output contract.

**Hook** means a command that runs at a defined point in an agent session.

**Route** means a selected model and effort assignment for a named role.

**MCP** means Model Context Protocol, an optional integration that requires a
separate review of source, permissions, and network access.
