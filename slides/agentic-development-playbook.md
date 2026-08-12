---
marp: true
theme: default
paginate: true
size: 16:9
title: Adopting Agentic AI successfully
description: Data science operations playbook.
---

<style>
:root {
  --paper: #f6f2e9;
  --ink: #172124;
  --muted: #657174;
  --card: #fffdf8;
  --line: #d8d2c5;
  --teal: #087f8c;
  --orange: #d05b36;
  --red: #b83232;
  --green: #16705a;
  --violet: #6657a8;
}
section {
  background: var(--paper);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  padding: 6vh 7vw 7vh;
}
section::after { color: var(--muted); font-size: 0.55em; }
h1 { font-size: 2.5em; line-height: 1.02; letter-spacing: -0.04em; max-width: 14ch; margin: .2em 0 .35em; }
h2 { font-size: 1.65em; line-height: 1.08; letter-spacing: -0.03em; margin: 0 0 .45em; }
h3 { font-size: 1em; margin: .1em 0 .35em; }
p, li { font-size: .82em; line-height: 1.4; }
ul { padding-left: 1.1em; }
.eyebrow { color: var(--muted); font-size: .55em; font-weight: 750; letter-spacing: .15em; text-transform: uppercase; }
.lede { color: var(--muted); font-size: 1.05em; line-height: 1.35; max-width: 42ch; }
.small { color: var(--muted); font-size: .58em; }
.muted { color: var(--muted); }
.source { color: var(--muted); font-size: .48em; margin-top: 2.5em; }
.grid2 { display: grid; grid-template-columns: 1fr 1.15fr; gap: 3.5vw; align-items: center; }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1em; align-items: stretch; }
.grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75em; align-items: stretch; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 15px; box-shadow: 0 8px 28px #4a3d2510; padding: .8em 1em; }
.card p { margin: .35em 0 0; }
.kpi { font-size: 1.8em; font-weight: 750; letter-spacing: -.04em; line-height: 1; }
.teal { color: var(--teal); }
.orange { color: var(--orange); }
.red { color: var(--red); }
.green { color: var(--green); }
.violet { color: var(--violet); }
.callout { border-left: 5px solid var(--teal); padding: .25em 0 .25em 1em; max-width: 52ch; }
.warning { border-left-color: var(--red); }
.flow { display: flex; align-items: stretch; gap: .35em; margin: 1.4em 0; }
.flow .node { flex: 1; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: .65em .5em; text-align: center; font-size: .68em; }
.flow .arrow { align-self: center; color: var(--teal); font-size: 1.2em; }
.stage { border-top: 5px solid var(--teal); }
.stage:nth-child(2n) { border-top-color: var(--orange); }
.stage:nth-child(3n) { border-top-color: var(--violet); }
.code { background: #172124; color: #f6f2e9; border-radius: 12px; padding: 1em 1.2em; font: .72em/1.55 ui-monospace, SFMono-Regular, Menlo, monospace; }
.code .good { color: #75c7aa; }
.code .warn { color: #f2a28a; }
pre.snippet { margin: 0; font-size: .58em; line-height: 1.25; white-space: pre-wrap; overflow-wrap: anywhere; }
table { width: 100%; border-collapse: collapse; background: var(--card); font-size: .68em; }
th, td { border-bottom: 1px solid var(--line); padding: .55em .7em; text-align: left; }
th { color: var(--muted); font-size: .8em; letter-spacing: .08em; text-transform: uppercase; }
.lead { display: flex; flex-direction: column; justify-content: center; }
.lead h1 { max-width: 12ch; }
.center { text-align: center; }
.center h1, .center h2 { margin-left: auto; margin-right: auto; }
</style>


<div class="lead">

# Adopting Agentic AI successfully

<div class="lede">Data science operations playbook</div>

</div>

---

# Adoption =/= successful outcomes.

Roll out of agentic AI tooling does not automatically guarantee that a process will become faster, safer, or more reliable.

How can we measure successful outcomes?

**Measure the task results:** Checks, metrics, artifacts, tests, scope, review evidence.

<p class="source">Framing source: <em>AI Adoption is a Myth</em>, @vasuman</p>

---

## A task needs a contract before it needs a tool

<div class="grid3">
<div class="card"><div class="kpi teal">01</div><h3>Define</h3><p>State the task, paths in scope, acceptance checks, and stopping point.</p></div>
<div class="card"><div class="kpi orange">02</div><h3>Execute</h3><p>Use context, a repeatable skill, and narrowly permitted actions.</p></div>
<div class="card"><div class="kpi violet">03</div><h3>Evidence</h3><p>Leave behind outputs that another person can inspect and challenge.</p></div>
</div>

---

<div class="eyebrow">The repository shape</div>

## Context becomes a controlled path to evidence

<div class="flow">
<div class="node">Project<br>context</div><div class="arrow">→</div>
<div class="node">Repeatable<br>skill</div><div class="arrow">→</div>
<div class="node">Scoped<br>tools</div><div class="arrow">→</div>
<div class="node">Deterministic<br>pipeline</div><div class="arrow">→</div>
<div class="node">Artifacts &<br>review</div>
</div>

<div class="grid3">
<div class="card"><h3>Human judgement</h3><p>Choose the task, boundaries, and stopping point.</p></div>
<div class="card"><h3>Deterministic code</h3><p>Generate, validate, calculate, and report repeatably.</p></div>
<div class="card"><h3>Reviewable handoff</h3><p>Inspect the complete diff and the generated evidence.</p></div>
</div>

---

## So, context and skills make tasks repeatable.

<div class="grid4">
<div class="card"><h3>Instructions</h3><p>Project boundaries and commands.</p></div>
<div class="card"><h3>Skill</h3><p>Reusable procedures.</p></div>
<div class="card"><h3>Runbooks</h3><p>Explicit steps and evidence contracts.</p></div>
<div class="card"><h3>Checks</h3><p>Tests, artifacts, and complete diff review.</p></div>
</div>

<div class="callout"><p>Making agents useful is only possible through explicit process building.</p></div>

---

<div class="eyebrow">Repository and project initialisation</div>

## Set the conventions before the agent starts changing files

<div class="grid3">
<div class="card"><h3>Code</h3><p>State the language, file layout, naming conventions, formatter, linter, and test runner; for example, Ruff and pytest.</p></div>
<div class="card"><h3>Communication</h3><p>Use ASD-STE100-style plain language: short sentences, defined terms, explicit actions, and low cognitive overhead.</p></div>
<div class="card"><h3>Task direction</h3><p>Give the goal, paths, acceptance checks, commands, and stop condition. Keep unrelated history out of the task context.</p></div>
</div>

<div class="callout warning"><p>A goal-only instruction may produce an answer, but it does not establish the conventions, scope, checks, or stopping point needed for reproducibility and auditability.</p></div>

<p class="small">This is why a minimal-instruction approach is unsuitable for the controlled implementation path shown here, even when it is useful for exploratory work.</p>

---

<div class="eyebrow">Hooks</div>

## Use a hook when the boundary must be deterministic

<div class="grid2">
<div class="code">
<span class="good">sessionStart</span> → report git status, diff summary,
task list, and HANDOVER.md

<span class="warn">preToolUse</span> → deny push, history changes, or fixture
writes without the required task scope

<span class="good">subtask complete</span> → require the task receipt
and handover state to be updated
</div>
<div>
<h3>How to build one</h3>
<ol>
<li>Choose one event and one narrow decision.</li>
<li>Define a machine-readable input and output.</li>
<li>Return allow, deny, or additional context.</li>
<li>Test safe, unsafe, malformed, and edge-case payloads.</li>
<li>Keep the script short, local, and auditable.</li>
</ol>
<p class="small">A hook is more appropriate than a skill when skipping the rule must be impossible or must produce a visible denial.</p>
</div>
</div>

---

<div class="eyebrow">Implemented hook</div>

## The repository hook returns a decision, not a suggestion

<div class="grid2">
<pre class="code snippet">"preToolUse": [{
  "type": "command",
  "bash": "python3 .github/hooks/copilot_pretool_check.py",
  "cwd": "."
}]</pre>
<pre class="code snippet">if pattern.search(command):
    if pattern is HISTORY_PATTERN and not task_receipt_ready(repo):
        reason += " Update TASKS.md first."
    return {"permissionDecision": "deny",
            "permissionDecisionReason": reason}</pre>
</div>

<p class="small">Source: <code>.github/hooks/public-safety.json</code> and <code>.github/hooks/copilot_pretool_check.py</code>. The hook has tests for safe, unsafe, malformed, and missing-receipt inputs.</p>

---

<div class="eyebrow">Skills</div>

## Use a skill for a repeatable procedure

<div class="grid2">
<div class="card">
<h3>Build your own</h3>
<ul>
<li>write the inputs, steps, outputs, and stopping point;</li>
<li>keep the procedure narrow enough to review;</li>
<li>add examples and failure cases;</li>
<li>test any scripts it calls.</li>
</ul>
</div>
<div class="card">
<h3>Use an audited skill</h3>
<ul>
<li>pin its source and revision;</li>
<li>inspect scripts, dependencies, and permissions;</li>
<li>run static checks before enabling it;</li>
<li>record what was reviewed.</li>
</ul>
</div>
</div>

<div class="callout"><p>The handover skill records the repository state, task list, diff, tests, open questions, and next decision. A completion hook or review gate is needed if the task list must be updated rather than merely requested.</p></div>

---

<div class="eyebrow">Implemented skill</div>

## The skill records the subtask before handover

<div class="grid2">
<pre class="code">---
name: task-list-update
description: Record the outcome of one
approved subtask in TASKS.md.
---

1. Read TASKS.md and the task source.
2. Check the current status.
3. Record files, checks, evidence,
   questions, and the next decision.
4. Invoke /handover at the stop point.</pre>
<pre class="code">/task-list-update /handover

TASK: DEMO-001
STATUS: ready for review
EVIDENCE: 48 tests passed
NEXT: human diff review</pre>
</div>

<p class="small">Source: <code>.github/skills/task-list-update/SKILL.md</code>. The handover skill writes the wider session record after the task-list receipt.</p>

---

<div class="eyebrow">MCP servers and plugins</div>

## MCP servers and plugins are not permitted at DfE

<table>
<thead><tr><th>Component</th><th>What it would add</th><th>DfE boundary</th></tr></thead>
<tbody>
<tr><td>Skill</td><td>A documented procedure and, sometimes, local scripts</td><td>Use only when the source and scripts are permitted and audited.</td></tr>
<tr><td>Plugin</td><td>Additional agent capabilities or commands</td><td>No installation, execution, or self-authoring.</td></tr>
<tr><td>MCP server</td><td>Context or tools through a protocol boundary</td><td>No installation, registration, execution, or self-authoring.</td></tr>
</tbody>
</table>

<div class="callout warning"><p>This presentation can describe MCP servers and plugins as concepts. It must not demonstrate or enable them at DfE.</p></div>

---

<div class="eyebrow">Supply-chain and static analysis</div>

## Review the code before installing or enabling it

<div class="grid2">
<pre class="code"><span class="good">sfw</span> uv add &lt;package&gt;
<span class="good">sfw</span> npm install &lt;package&gt;
<span class="good">sfw</span> pipx install &lt;package&gt;
<span class="good">sfw</span> &lt;other-package-manager&gt; ...</pre>
<div>
<ul>
<li>Use Snyk or an equivalent dependency and vulnerability scan.</li>
<li>Run static analysis over permitted scripts and skills.</li>
<li>Inspect install, update, network, and filesystem behaviour for permitted dependencies.</li>
<li>Do not hide installation commands inside scripts.</li>
<li>Record the package source, version, and scan result.</li>
</ul>
</div>
</div>

<p class="small"><code>sfw</code> is the installation wrapper for permitted dependencies. The public instructions show how to wrap actions; they do not install packages during the demo.</p>

---

<div class="eyebrow">Research and control strength</div>

## AGENTS.md and CLAUDE.md are the softest instruction layer

<div class="flow">
<div class="node"><code>AGENTS.md</code><br><code>CLAUDE.md</code><br><span class="small">passive prose, advisory</span></div><div class="arrow">→</div>
<div class="node">Skills and<br>runbooks<br><span class="small">procedural guidance</span></div><div class="arrow">→</div>
<div class="node">Hooks and<br>runtime checks<br><span class="small">deterministic enforcement</span></div>
</div>

<div class="grid2">
<div class="card"><h3>Trade-off</h3><p>Stronger controls reduce reliance on model judgement, but a rigid rule can block a legitimate action or misclassify a safe one. The design needs an escalation path.</p></div>
<div class="card"><h3>Selected ArXiv sources</h3><p class="small"><em>Evaluating AGENTS.md</em> · arXiv:2602.11988<br><em>On the Impact of AGENTS.md Files</em> · arXiv:2601.20404<br><em>Configuration Smells in AGENTS.md Files</em> · arXiv:2606.15828<br><em>ContextCov</em> · arXiv:2603.00822</p></div>
</div>

<p class="small">The studies do not justify a universal recipe. They support measuring guidance, keeping it focused, and compiling important constraints into checks. Model fine-tuning is outside this presentation.</p>
