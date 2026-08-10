# Pipeline run triage

Use this runbook for the synthetic health report.

## Procedure

1. Read `fixtures/run_manifest.json`.
2. Run the health report.
3. Record the run ID, pipeline, dataset, and status.
4. Compare each warning or failed check with its threshold.
5. Record the evidence used for the decision.
6. Keep the raw fixture unchanged.
7. Review before promotion.

## Status meanings

| Status | Meaning | Next step |
|---|---|---|
| `HEALTHY` | All configured checks passed. | Continue to the next approved step. |
| `WARNING` | A check needs review. | Review before promotion. |
| `FAILED` | A required check did not pass. | Resolve the check and rerun. |

The baseline evidence is:

- `validate.metrics.schema_errors = 0`;
- `ingest.metrics.records_in = 120000`;
- `features.metrics.rows_out = 119800`;
- `evaluate.metrics.auc = 0.79`;
- minimum AUC threshold `0.80`.

The baseline report therefore contains:

```text
WARN evaluate.auc: 0.790 < 0.800
```

Use only evidence in the manifest and report. Do not invent a cause for a
warning. This project is synthetic and does not represent a real service.
