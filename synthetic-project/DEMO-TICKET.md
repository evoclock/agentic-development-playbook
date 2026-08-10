# Demo ticket: detect silent feature-row loss

## Problem

This ticket is the bounded correction applied after the foundation commit
`fe30ddf`. The executable pipeline can complete the feature stage while
retaining too few rows. In the `row-loss` scenario:

```text
records_in = 400
rows_out   = 196
retention  = 196 / 400 = 0.490
```

The current health report still returns `HEALTHY` because it checks stage status,
schema errors, and AUC, but not row retention.

## Change

Add a deterministic feature-row retention check to
`src/pipeline_ops/health_report.py`.

Requirements:

- compare `features.metrics.rows_out` with `ingest.metrics.records_in`;
- add `--min-row-retention`, default `0.99`;
- report `PASS` when the ratio meets the threshold;
- report `WARN` when the ratio is below the threshold;
- make a retention warning change the overall status to `WARNING`;
- keep the existing AUC and schema checks;
- keep the text and JSON output formats stable;
- add pass and warning tests;
- use no new dependency;
- do not change the runner, generated records, MCP server, or hook.

## Acceptance checks

Run from `synthetic-project/`:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_pipeline.py --scenario healthy --output-dir runs/accept-healthy
python3 scripts/run_pipeline.py --scenario row-loss --output-dir runs/accept-row-loss
python3 scripts/run_pipeline.py --scenario row-loss --output-dir runs/accept-row-loss --format json
```

The healthy command must return `0`. The row-loss command must return `1` and
include:

```text
WARN features.row_retention: 0.490 < 0.990
```

The AUC check must remain visible. The JSON report must contain a check named
`features.row_retention` with status `warning`.

The expected post-change output is in
`expected-output/after-row-retention-check.txt`.
