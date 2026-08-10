# Demo ticket: feature-row retention check

Add a deterministic feature-row retention check to the health report.

Requirements:

- compare `features.metrics.rows_out` with `ingest.metrics.records_in`;
- add `--min-row-retention`, default `0.99`;
- report `PASS` when the ratio meets the threshold;
- report `WARN` when it does not;
- keep the existing AUC and schema checks;
- add pass and warning tests;
- keep text and JSON output stable;
- use no new dependency;
- do not change the fixture or MCP server.

Acceptance checks from this directory:

```bash
python3 -m unittest discover -s tests -v
python3 src/pipeline_ops/health_report.py fixtures/run_manifest.json
python3 src/pipeline_ops/health_report.py fixtures/run_manifest.json --format json
```

The text report must include:

```text
PASS features.row_retention: 0.998 >= 0.990
```

The overall baseline status remains `WARNING` because the AUC warning remains.
