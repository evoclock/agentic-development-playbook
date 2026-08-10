# Pipeline run triage

This runbook explains how to run and inspect the executable synthetic pipeline.
It is a local teaching example. It does not represent a production service.

## Run a scenario

From `synthetic-project/`:

```bash
python3 scripts/run_pipeline.py --scenario healthy --output-dir runs/triage-healthy
```

The command creates 400 records with seed `17` and writes evidence under the
selected output directory. Use a new directory for each scenario.

Available scenarios:

| Scenario | Expected exit | Purpose |
|---|---:|---|
| `healthy` | `0` | Complete process with passing checks |
| `evaluation-warning` | `1` | Complete process with AUC below target |
| `row-loss` | `1` after the correction | Complete process with a retention warning |
| `schema-failure` | `2` | Stop after input validation failure |

The row-loss run records `196` feature rows from `400` input rows. The
retention check reports this as a warning and returns exit code `1`.

## Stage evidence

### Ingest

Read `run_manifest.json` and confirm:

```text
stages[0].name = ingest
stages[0].metrics.records_in = 400
```

Read `raw_records.jsonl` to inspect the generated records. The records contain
only synthetic identifiers, counts, segments, labels, and a train/test split.

### Validate

Read `validation.json`:

```json
{
  "records_checked": 400,
  "schema_errors": 0,
  "missing_required_values": 0,
  "duplicate_rows": 0
}
```

For `schema-failure`, the validator records one missing `event_count`, writes
`failure_log.jsonl`, and stops before feature generation.

### Features

Read the feature stage in `run_manifest.json` and inspect `features.jsonl`.
The healthy scenario has:

```text
rows_in  = 400
rows_out = 400
```

The row-loss scenario has:

```text
rows_in  = 400
rows_out = 196
retention = 196 / 400 = 0.490
```

This is the problem selected for the Copilot task. A passed stage status does
not prove that the stage preserved enough rows.

### Train

Read `model.json`. The baseline uses a deterministic mean-difference linear
calculation. It records the training row counts and three weights. It is not a
claim about a useful production model.

### Evaluate

Read `evaluation.json`:

```text
test_rows   = 100
auc         = 0.827542 for healthy
auc target  = 0.800000
```

The evaluation-warning scenario inverts the test scores. Its calculated AUC is
`0.172458`, so the report returns `WARNING` and exit code `1`.

## Health decision

Read `health_report.json` or the command output.

| Status | Meaning | Action |
|---|---|---|
| `HEALTHY` | All current checks pass. | Continue to the next approved step. |
| `WARNING` | A metric needs review. | Review evidence before promotion. |
| `FAILED` | A required stage or check failed. | Resolve the issue and rerun. |

The report is evidence about configured checks. It is not a claim that a model
is suitable for a real decision.

## Provenance and failures

Read `provenance.json` to confirm:

- run ID;
- pipeline and dataset names;
- source revision;
- generator version;
- scenario;
- random seed;
- deterministic flag.

Read `failure_log.jsonl`. It is empty for successful runs. For a validation
failure it contains the failed stage, severity, code, message, and evidence
file.

## Recorded change

The correction adds the feature-row retention check. The row-loss run reports:

```text
WARN features.row_retention: 0.490 < 0.990
```

Use only evidence in the generated artifacts. Do not invent a cause for a
warning. Do not edit generated run output as part of the code change.
