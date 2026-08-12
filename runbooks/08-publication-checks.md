# 08 — Public publication checks

## Purpose

Review every changed file as public material before a commit, push, or
publication decision. A passing test does not prove that documentation, claims,
configuration, or examples are safe to publish.

## Public boundary

Include only:

- public-safe task examples;
- generic procedures and public links;
- explicit limitations and verification boundaries;
- repeatable commands that do not expose credentials or private infrastructure.

Do not include:

- personal data, credentials, tokens, or keys;
- private paths, hosts, endpoints, or procedures;
- unedited session output;
- claims of official endorsement, production approval, or successful adoption;
- a configured model label presented as proof of provider availability.

Use placeholders when an example needs a path, endpoint, or credential.

## Deterministic checks

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/hooks/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .github/skills/model-routing/tests -v
node --test .pi/extensions/model-router/logic.test.ts
git diff --check
```

Run additional task-specific checks named by the relevant runbook. Validate the
workflow PNG/SVG pair if diagrams changed.

## Claims and sources

For every external claim, identify a public source, state version limits, and
remove claims that cannot be verified. Do not imply Department for Education
approval, adoption, or testing. State clearly whether validation used Pi,
Copilot CLI, or a deterministic local check.

## Complete diff and approval

Before commit or push:

1. read every changed file;
2. inspect the complete diff and changed-file list;
3. run focused tests, type checks, link checks, and rendering checks as needed;
4. search for secrets, private paths, stale claims, and obsolete references;
5. record open questions and the next decision;
6. obtain explicit human approval.

An automated agent cannot approve its own publication.
