# Cloud And Visualization Operator Guide

This guide is copied into generated projects as
`harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md`.

## Core Rule

`VISUALIZATION_SPEC.md` decides the visualization shape before production.

- Local status HTML from `python3 scripts/harnessctl.py report` is built in and
  safe as a compiled local view.
- External dashboards, live status UIs, external evidence views, and remote viz
  backends require task-local backend selection first.
- `events.jsonl` can be exported locally with
  `python3 scripts/harnessctl.py viz-export --backend local_file`.
- Any non-local backend remains `UNVERIFIED` until human backend selection,
  bounded policy, credential lifecycle entry, smoke evidence, and operator
  review exist.

## Human Decision Surface

- Choose the viz backend.
- Choose the cloud lane from `harness/runtime/RUNNERS/*.json`.
- Approve bounded policy: allowed commands, network rule, timeout, budget,
  audit path, and kill procedure.
- Manage credentials without committing local credential files or exposing raw secret values to
  worker memory.
- Review smoke evidence before enabling a network-writing adapter.

## Worker Delegation Surface

- Implement `events.jsonl` -> selected backend adapter.
- Generate dry-run payloads.
- Generate smoke evidence.
- Maintain redaction tests.
- Improve local report UI after Claude visualization/design review.

Claude owns visualization and diagram information architecture. Codex or a
deterministic worker may implement event plumbing after the approved spec.
