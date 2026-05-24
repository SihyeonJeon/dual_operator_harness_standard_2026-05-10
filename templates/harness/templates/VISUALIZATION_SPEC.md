# Visualization Spec

Task id:
Feature id:
Slice id:
Status: DRAFT | APPROVED | BLOCKED
Owner:
Date:

## Purpose

UNKNOWN

Decision or bottleneck this visualization helps expose:

- UNKNOWN

## Audience

Primary viewer:

- human | operator | evaluator | worker | public evidence | UNKNOWN

Control surface:

- read_only | approval_queue | incident_triage | external evidence | UNKNOWN

Visualization backend:

- local_file | static_html_report | external_dashboard | live_status | evidence_export | UNKNOWN

Backend owner:

- Claude visualization/design review owner: UNKNOWN
- Event plumbing / adapter worker: UNKNOWN

## Source Artifacts

Canonical files or event streams:

- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `harness/shared/ACTIVE_SNAPSHOT.md`
- `harness/events/events.jsonl`
- UNKNOWN

## Data Contract

Required fields:

- task id
- feature id
- trace id
- actor and actor type
- worker id or operator id when applicable
- part id when applicable
- event type
- status or verdict
- timestamp
- evidence path
- backend id
- adapter path when applicable
- redaction status
- smoke evidence path when applicable

Unknown or missing data behavior:

- UNKNOWN

Backend data flow:

- `harness/events/events.jsonl` -> UNKNOWN
- Network write: denied | dry-run | approved | UNKNOWN

## Views

Required views:

- task/tree view
- worker/part ownership view
- timeline view
- gate and blocker view
- decision/disagreement view
- evidence/report view

Out of scope:

- UNKNOWN

## Interaction

Filters, drilldowns, search, refresh, or live behavior:

- UNKNOWN

Empty, loading, error, and stale-data states:

- UNKNOWN

Refresh mode:

- static | refresh_on_command | live | UNKNOWN

## Redaction And Sharing

Sensitive fields:

- UNKNOWN

Public/evidence-safe fields:

- UNKNOWN

External sharing approval required:

- yes | no | UNKNOWN

Credential requirements:

- none | credential_id_only | secret_access_required | UNKNOWN

## Acceptance Criteria

- The visualization names its canonical source files.
- The visualization does not replace file-backed memory.
- The visualization exposes active blockers, current task state, open human
  decisions, and failed or not-run gates.
- The visualization shows stale or missing data explicitly.
- Redaction and sharing rules are applied.
- The selected backend is explicit.
- `events.jsonl` adapter behavior is dry-run or local-only unless human approval,
  bounded policy, credential lifecycle record, and smoke evidence exist.
- Claude visualization/design review has approved the information architecture
  for any dashboard, timeline, graph, external evidence view, manager view, or live
  status UI.

## Approval

Planning:

- NOT-RUN

Claude Visualization / Design:

- NOT-RUN

Evaluation:

- NOT-RUN

Operator:

- NOT-RUN

Evidence path:

- UNKNOWN
