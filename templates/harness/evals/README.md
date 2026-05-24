# Harness Evals

This directory holds project-local evaluation suites and results. It is not a
replacement for specialized LLM eval frameworks. Its job is to ensure every
generated harness starts with portable, dependency-free regression checks over
canonical files, events, and governance boundaries.

## Default Suite

Run the scaffold invariant suite:

```sh
python3 scripts/harnessctl.py eval-run
```

The default suite is `harness/evals/golden_suite.json`. Results are written to:

- `harness/evals/results/latest.json`
- `harness/evals/results/latest.md`
- `harness/events/events.jsonl` as an `eval.suite_run` event

## Public Release Suite

Run the 22-check public-safe scorecard:

```sh
python3 scripts/harnessctl.py eval-run \
  --suite harness/evals/public_release_suite.json \
  --output harness/evals/results/public_release.json
```

This suite is derived from the generated-harness evaluation checklist. It checks
portable governance evidence without requiring private connectors, credentials,
hosted dashboards, or a project-specific RAG service.

## Case Types

Supported dependency-free case types:

- `file_exists`
- `text_contains`
- `json_has_key`
- `json_equals`
- `json_array_min_length`
- `event_count_min`
- `events_schema_valid`
- `verified_evidence_integrity`

These checks do not run arbitrary shell commands and do not perform network
writes. Project-specific test, build, browser, research, writing, safety, or
domain evals should be represented as separate evidence in task artifacts and
may be summarized into this suite only when the check is deterministic and
safe.

`text_contains` is case-insensitive by default. Set `case_sensitive: true` on a
case only when exact capitalization matters.

## Governance Rule

Every substantial task should either:

- run a relevant eval suite; or
- record why the suite is `NOT-RUN` in the task evaluation report.

Add new cases when failure or success records show a reusable invariant. Follow
`harness/shared/REGULATION_EVOLUTION.md` before changing required gates.
