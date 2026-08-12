# Executable synthetic pipeline

This directory contains a small, public-safe data-science operations process.
It runs locally with the Python standard library. It generates synthetic
records, validates them, creates features, fits a deterministic baseline model,
calculates an evaluation metric, and writes run evidence.

It does not use real data, a model service, a network, or a package install.
The name `synthetic-churn-training` is a scenario label only.

## Process flow

```text
seed + scenario
      |
      v
  ingest: generate records
      |
      v
  validate: check the record contract
      |
      v
  features: filter a time window and derive three features
      |
      v
  train: fit a mean-difference linear baseline
      |
      v
  evaluate: score the test split and calculate rank-based AUC
      |
      v
  evidence: manifest, metrics, provenance, failure log, health report
```

The model is intentionally simple. Its purpose is to create reproducible
operational evidence, not to claim useful predictive performance.

## Run the deterministic checks

Run from `synthetic-project/`:

```bash
python3 -m unittest discover -s tests -v
```

The command generates 400 records with seed `17`. It writes nine files under
the selected output directory. The `runs/` directory is ignored by Git because
it contains generated local evidence.

The command prints a health report and returns an exit code:

- `0` — all configured checks pass;
- `1` — a review warning is present;
- `2` — a required check failed or input is invalid.

## Scenarios

| Scenario | Process change | Current result |
|---|---|---|
| `healthy` | 30-day feature window and normal scores | `HEALTHY`, exit `0` |
| `evaluation-warning` | Test scores are inverted | `WARNING`, exit `1` |
| `row-loss` | 15-day feature window keeps only 196 of 400 rows | `WARNING`, exit `1` |
| `schema-failure` | One generated record loses `event_count` | `FAILED`, exit `2` |

The `row-loss` result is deliberate. The process records the loss and the
health report checks it. The retention check is foundation evidence for the
recorded workflow. The current demo task adds a minimum evaluation sample-size
check.

## Evidence artifacts

A successful run writes:

| File | Purpose |
|---|---|
| `raw_records.jsonl` | Generated input records |
| `validation.json` | Record-contract checks and errors |
| `features.jsonl` | Rows retained for modelling and derived features |
| `model.json` | Deterministic baseline weights and training counts |
| `evaluation.json` | Test counts, calculated AUC, threshold, score mode |
| `provenance.json` | Seed, scenario, source revision, and generator version |
| `run_manifest.json` | Stage order, statuses, metrics, and artifact references |
| `failure_log.jsonl` | One evidence record per pipeline failure; empty on success |
| `health_report.json` | Structured status and check results |

The schema-failure scenario stops after validation. It writes six files and a
failure record, but it does not write feature, model, or evaluation artifacts.

## Inspect the evidence

For example:

```bash
python3 -m json.tool runs/demo-healthy/run_manifest.json
python3 -m json.tool runs/demo-healthy/provenance.json
cat runs/demo-healthy/failure_log.jsonl
```

Use the runbook in [`runbooks/pipeline-triage.md`](runbooks/pipeline-triage.md)
when deciding what the evidence supports.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

The tests cover deterministic generation, validation failures, feature-window
retention, model calculation, AUC warnings, artifact creation, early stop on a
schema failure, and the current row-loss gap.

## Recorded task

[`DEMO-TICKET.md`](DEMO-TICKET.md) is intentionally small enough for a complete
agentic walkthrough. The agent must add a minimum evaluation sample-size check
without changing the runner, generated records, or control-plane boundaries.

Expected outputs are kept in [`expected-output/`](expected-output/):

- `baseline.txt` — healthy run;
- `evaluation-warning.txt` — computed evaluation warning;
- `after-row-retention-check.txt` — foundation retention warning;
- `after-min-test-rows-check.txt` — expected output for the current task;
- `schema-failure.txt` — validation stop and failure status.
