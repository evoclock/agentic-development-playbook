# Pipeline triage evidence fixture

This small static fixture exercises `pipeline-run-triage` without the retired
synthetic pipeline project.

Read each scenario's `run_manifest.json`, `evaluation.json`,
`provenance.json`, `health_report.json`, and `failure_log.jsonl`. Compare the
observed `test_rows` with the configured minimum of `50`.

| Scenario | Test rows | Expected status |
|---|---:|---|
| `healthy` | 100 | `HEALTHY` |
| `warning` | 20 | `WARNING` |

The artifacts are evidence for the rehearsal only. Do not edit them to change
the result.
