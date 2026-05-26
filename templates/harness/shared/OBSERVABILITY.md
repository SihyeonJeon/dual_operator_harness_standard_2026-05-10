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
python3 scripts/harnessctl.py context-pack --task-id TASK
python3 scripts/harnessctl.py worker-brief --task-id TASK --owned-path PATH
python3 scripts/harnessctl.py model-route --role worker --task-difficulty routine --simple
python3 scripts/harnessctl.py task-packet --task-id TASK --sender A --receiver B --intent handoff --summary "..."
python3 scripts/harnessctl.py current-research --task-id TASK --query "..." --source "..." --finding "..."
python3 scripts/harnessctl.py cross-feedback --task-id TASK --producer A --reviewer B --verdict PASS --feedback "..."
python3 scripts/harnessctl.py concept-check --task-id TASK --artifact-path PATH --forbidden-phrase "..."
python3 scripts/harnessctl.py software-feedback --task-id TASK --lint-command "..." --smoke-command "..."
```

`harnessctl.py` is a thin file-backed helper, not an agent runtime.

## Executable Governance Helpers

The generated control surface code handles repeatable, domain-neutral work:

- `context-pack` compiles bounded source excerpts and recent event references;
- `worker-brief` renders a task-local worker brief from the canonical template;
- `model-route` applies `MODEL_ROUTING.json` without relying on prose memory;
- `task-packet` writes bounded agent-to-agent handoff JSON;
- `current-research` records command-date market/comparable evidence before
  overall planning when current external reality matters;
- `cross-feedback` records independent feedback without forcing consensus;
- `concept-check` catches literal prompt phrase and self-descriptive meta-copy
  leakage in user-facing artifacts;
- `software-feedback` executes lint/static, runtime smoke, optional test, and
  optional Playwright commands and writes evidence packets.

Agents may still make project-specific judgments, but these repeatable steps
should be run by code when available.

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
- local report or visualization export created.
- private overlay output summarized into canonical memory.

## Trace Rule

Use one trace id for a coherent task/slice. Evidence paths in task reports,
feature state, evaluation reports, and event log entries should agree.

## Human Visibility

`scripts/harnessctl.py report` compiles a local static HTML status page under
`harness/reports/`. The report is useful for human review and local evidence
history, but it is a compiled view over canonical files and must not replace
them.

Report UI/UX and diagrams are Claude-owned design surfaces. Claude should draft
or review the information architecture before workers change dashboard,
timeline, graph, manager-view, status, or live-status rendering.

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
