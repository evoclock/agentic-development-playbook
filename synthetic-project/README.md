# Synthetic pipeline health demo

This project reports the health of one synthetic batch-training run.
It uses only the Python standard library. It contains no real data.

## Run it

From this directory:

```bash
python3 src/pipeline_ops/health_report.py fixtures/run_manifest.json
```

The baseline fixture has five passed stages and one evaluation warning.
The AUC is `0.790`; the default threshold is `0.800`.
A warning returns exit code `1`.

Expected output is stored in [`expected-output/baseline.txt`](expected-output/baseline.txt).
The JSON form is available with `--format json`.

## Test it

```bash
python3 -m unittest discover -s tests -v
```

The tests cover manifest validation, status calculation, text output, and
failure/warning behaviour.

## Recorded task

[`DEMO-TICKET.md`](DEMO-TICKET.md) asks for a feature-row retention check.
The expected post-change report is in
[`expected-output/after-row-retention-check.txt`](expected-output/after-row-retention-check.txt).

The triage procedure is in [`runbooks/pipeline-triage.md`](runbooks/pipeline-triage.md).
