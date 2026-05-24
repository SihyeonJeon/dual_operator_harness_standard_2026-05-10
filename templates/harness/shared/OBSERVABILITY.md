# Observability

Every material action should be recoverable from files, not from chat memory.

## Event Log

Default local event log:

- `harness/events/events.jsonl`

Each line should match `schemas/observability-event.schema.json` when that
schema is available in the target project.

Default local command surface:

```sh
python3 scripts/harnessctl.py event --task-id TASK --actor OPERATOR --actor-type operator --event-type task.note
python3 scripts/harnessctl.py report
python3 scripts/harnessctl.py viz-export --backend local_file
python3 scripts/harnessctl.py viz-spec-check
python3 scripts/harnessctl.py eval-run
python3 scripts/harnessctl.py broadcast-draft --task-id TASK --title "Draft title"
python3 scripts/harnessctl.py review-packet --task-id TASK --question "Review question"
```

`harnessctl.py` is a thin file-backed helper, not an agent runtime.

## Visualization Export

`scripts/harnessctl.py viz-export --backend local_file` creates sanitized local
payloads from `harness/events/events.jsonl` under `harness/reports/viz/`. This
is the default smoke path for event visualization adapters and does not perform
network writes.

Workers may implement additional adapters under `harness/viz/`, but only after
the task-local `VISUALIZATION_SPEC.md` selects the backend and the human has
approved bounded policy, credential lifecycle, and smoke evidence requirements.

## Eval Runs

`scripts/harnessctl.py eval-run` runs the default
`harness/evals/golden_suite.json` scaffold invariant suite and writes local JSON
and Markdown results under `harness/evals/results/`. It appends an
`eval.suite_run` event to `harness/events/events.jsonl`.

This runner is intentionally small: it checks local files and JSON structures,
does not execute arbitrary shell commands, and performs no network writes.
Specialized eval tools may produce evidence for task reports, but their results
become canonical only when summarized into harness files.

## Required Event Classes

- session start and session end;
- task or feature claimed, blocked, completed, or reopened;
- tool use and permission denial;
- artifact write;
- verification gate pass, warn, fail, or not-run;
- eval suite pass, warn, fail, or not-run;
- context compaction;
- capability verification or invalidation;
- operator disagreement or human decision;
- regulation change.
- visualization spec drafted, approved, blocked, or marked not required.
- broadcast draft created, approved, rejected, published, corrected, or rolled
  back.
- external review packet created, review received, reviewer finding accepted,
  reviewer finding rejected, or follow-up created.
- internal/external channel summary promoted into canonical memory.

## Trace Rule

Use one trace id for a coherent task/slice. Evidence paths in task reports,
feature state, evaluation reports, and event log entries should agree.

## Human Visibility

`scripts/harnessctl.py report` compiles a local static HTML status page under
`harness/reports/`. The report is useful for human review and external evidence
history, but it is a compiled view over canonical files and must not replace
them.

Report UI/UX and diagrams are Claude-owned design surfaces. Claude should draft
or review the information architecture before workers change dashboard,
timeline, graph, manager-view, external evidence, or live-status rendering.

`harness/broadcast/` and `harness/reviewers/` are external-channel records.
They improve visibility and feedback, but they are not canonical memory until
operators summarize the relevant result into internal files.

## Minimal Manual Event

```json
{
  "event_id": "evt_UNKNOWN",
  "trace_id": "trace_UNKNOWN",
  "task_id": "H0-LOCAL-SMOKE",
  "actor": "UNKNOWN",
  "actor_type": "operator",
  "event_type": "gate.not_run",
  "timestamp": "UNKNOWN",
  "evidence_path": "UNKNOWN"
}
```
