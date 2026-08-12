# Demo ticket: guard small evaluation samples

## Problem

An AUC value is less useful when the evaluation sample is too small. The
pipeline currently checks AUC, schema errors, and feature-row retention, but it
does not check the number of test rows before using the AUC result.

The healthy scenario has `100` test rows. The new check will make that evidence
explicit and will also support a warning test with a smaller in-memory manifest.

## Change

Add a minimum evaluation sample-size check to
`src/pipeline_ops/health_report.py`.

Requirements:

- read `evaluate.metrics.test_rows`;
- add `--min-test-rows`, default `50`;
- report `PASS` when test rows meet the threshold;
- report `WARN` when test rows are below the threshold;
- make the warning change the overall status to `WARNING`;
- keep the schema, row-retention, and AUC checks;
- keep text and JSON output stable;
- add pass and warning tests;
- use no new dependency;
- do not change the runner, generated records, MCP server, or hooks.

## Acceptance checks

Run from `synthetic-project/`:

```bash
python3 -m unittest discover -s tests -v
```

The healthy command must return `0` and, after the change, include:

```text
PASS evaluate.test_rows: 100 >= 50
```

Add an in-memory test with `test_rows = 20`. It must include:

```text
WARN evaluate.test_rows: 20 < 50
```

The existing AUC, row-retention, and schema checks must remain visible.
The expected post-change healthy output is in
`expected-output/after-min-test-rows-check.txt`.
