# Security threat-intelligence boundary

## Status

**Proper production process documented; implementation intentionally out of
scope for this synthetic demonstration.**

This document explains the control gap between the lightweight demo hook and a
security process suitable for sensitive government workloads. It is a design
boundary, not evidence that the production process exists.

## What the current demo does

The tracked hook at `.github/hooks/copilot_pretool_check.py` provides a narrow,
standard-library baseline for tool arguments:

- synthetic email and NHS-number redaction;
- common API-key, bearer-token, and private-key-marker redaction;
- hidden Unicode/BIDI and HTML-comment removal;
- a small prompt-injection detector;
- a small set of MCP tool-poisoning and credential-relay markers;
- `accept`, `redact`, and `reject` outcomes;
- public-safe finding metadata without matched secret or PII values.

The hook cannot rewrite the original Copilot tool payload. `redact` and
`reject` therefore deny the original action and require a reviewing caller to
use cleaned content or stop.

## What the current demo does not do

It does not provide:

- a complete OWASP web or application-security scanner;
- a complete OWASP MCP assessment;
- a CVE database or dependency-vulnerability matcher;
- an SBOM, CPE/PURL resolution, reachability analysis, or exploitability
  assessment;
- automatic ingestion of NVD, CISA KEV, vendor, OWASP, or model-threat feeds;
- signed rule bundles, feed provenance, expiry enforcement, or downgrade
  protection;
- continuous monitoring, incident response, penetration testing, or formal
  government accreditation.

A clean result means only that no configured baseline rule matched. It does not
mean that content, dependencies, tools, models, or infrastructure are safe
against current threats.

## Proper production process

### 1. Establish the threat model

Document the system boundary before choosing scanners or feeds:

- data classes and legal/policy handling requirements;
- users, agents, models, tools, MCP servers, files, queues, and external
  services;
- trust boundaries and allowed data movement;
- authorization and approval points for read, write, publish, and execute
  actions;
- logging, retention, encryption, key management, network-egress, and
  isolation requirements;
- failure behaviour when a control, feed, or reviewer is unavailable.

The threat model is the acceptance authority. A regex result cannot override
an authorization or data-boundary decision.

### 2. Separate the control families

Do not combine unrelated checks into one pattern list:

1. **Content safety and DLP** — PII, secrets, hidden Unicode/BIDI, prompt
   injection, malicious documents, and tool-description poisoning.
2. **Application security** — reviewed OWASP/ASVS controls, code analysis,
   dependency analysis, API tests, authentication, authorization, input
   validation, output encoding, SSRF controls, and isolation.
3. **MCP/tool security** — server identity, capability allowlists, schemas,
   least privilege, provenance, tool-description integrity, egress controls,
   confused-deputy protections, and human approval for consequential actions.
4. **Dependency and infrastructure vulnerability management** — SBOM-backed
   CVE/advisory matching, asset ownership, exploitability, patch windows, and
   compensating controls.

Each family needs its own owner, evidence, severity model, and acceptance
criteria. A content hook is not a CVE scanner.

### 3. Build an approved threat-intelligence pipeline

Use approved authoritative sources appropriate to the environment, for example:

- OWASP Top 10, ASVS, and OWASP MCP guidance for control design;
- NVD CVE data, CISA Known Exploited Vulnerabilities, and vendor advisories
  for dependency and product vulnerabilities;
- model-provider advisories, incident reports, and a reviewed prompt-injection
  regression corpus for agent-specific threats.

A governed update job should:

1. fetch only from allowlisted sources through the approved network path;
2. validate source signatures, TLS, schema, timestamps, and provenance;
3. normalize advisories into a versioned internal representation;
4. match CVEs to an SBOM and asset inventory rather than searching arbitrary
   text for CVE strings;
5. prioritize exploitation evidence, affected versions, exposure, and
   compensating controls;
6. run regression, false-positive, and safety tests;
7. produce a signed, hash-addressed rule/advisory bundle;
8. open the existing review/change path with source references, diff, tests,
   owner, and expiry; and
9. deploy only an approved bundle, with rollback and downgrade protection.

The runtime hook should consume a pinned, verified bundle. It should not make
an uncontrolled network request during every agent action.

### 4. Define freshness and failure behaviour

The deployed bundle should expose at least:

- bundle and schema revision;
- source identifiers and retrieval timestamps;
- reviewer and approval reference;
- content hash and signature reference;
- effective and expiry timestamps;
- affected control families;
- rollback predecessor.

If verification fails, the bundle is expired, provenance is missing, or the
approved current-threat review is unavailable, the effective status is
`REVIEW_REQUIRED`. Sensitive, external-transmission, publication, and
irreversible actions should fail closed or require an explicit human decision.

An emergency advisory path should permit an expedited reviewed update without
bypassing provenance, signature, testing, or rollback records.

### 5. Handle CVEs as dependency risk

CVE handling should be driven by an SBOM and asset inventory:

- identify packages, versions, operating-system components, images, and
  services with stable package identifiers;
- match against NVD/vendor advisories and CISA KEV where relevant;
- determine whether the affected component is present, reachable, exposed, and
  actually used;
- assign an owner and remediation or compensating-control deadline;
- retest after upgrade or mitigation; and
- retain the advisory, affected asset, decision, evidence, and approver.

Do not claim that the prompt/content hook performs any of these functions.

### 6. Preserve the decision boundary

The production decision model should distinguish:

- `ACCEPT` — all required controls are current and passed;
- `REDACT` — content can be safely transformed and the transformed value is
  used without retaining the original;
- `REJECT` — a threat or policy violation blocks the action;
- `REVIEW_REQUIRED` — evidence, freshness, provenance, authorization, or
  context is insufficient for an automated decision.

`REVIEW_REQUIRED` must not silently collapse into `ACCEPT` because a static
pattern list found nothing.

### 7. Keep evidence in the owning system

Use the existing approved task, change, release, and audit systems. Do not
create a second ledger or evidence store for this demo. Every rule-bundle
change should link:

- source/advisory identifiers;
- bundle digest and signature verification;
- affected controls and assets;
- test and scan results;
- reviewer/approver;
- deployment and rollback evidence;
- open risks and expiry/review date.

Sensitive evidence must be minimized and redacted before it enters logs,
receipts, prompts, or tickets.

## Minimum production acceptance gates

Before claiming that current-threat coverage exists, require evidence of:

1. an approved threat model and data-flow review;
2. separate content, application, MCP, dependency, and infrastructure control
   owners;
3. a signed and provenance-tracked threat/advisory bundle;
4. SBOM-backed dependency matching and asset ownership;
5. current OWASP/MCP control review and regression fixtures;
6. prompt-injection and hidden-payload red-team coverage;
7. expiry, stale-feed, invalid-signature, rollback, and downgrade tests;
8. fail-closed or human-review behaviour at each sensitive action boundary;
9. monitoring, incident response, remediation SLAs, and periodic independent
   review; and
10. a clear statement of residual risk and what the controls do not cover.

## Current handoff

The demo deliberately stops at the lightweight baseline and this boundary
 document. The next production-design task is to select the organisation's
 approved sources, SBOM/dependency tooling, signing/provenance mechanism,
 update owner, review cadence, and existing evidence system. That task must be
 separately approved and must not be implemented by adding a live network
 updater to the Copilot hook.
