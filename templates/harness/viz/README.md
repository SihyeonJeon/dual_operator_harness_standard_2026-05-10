# Visualization Backend Layer

This layer keeps visualization explicit and bounded.

Default path:

```sh
python3 scripts/harnessctl.py report
python3 scripts/harnessctl.py viz-export --backend local_file
```

`report` creates a human-readable static status page.

`viz-export` turns `harness/events/events.jsonl` into sanitized local payloads
under `harness/reports/viz/`:

- `events.ndjson`
- `events.json`
- `summary.json`

No network write is performed by the default backend.

## Backend Selection Rule

A task-local `VISUALIZATION_SPEC.md` must choose the visualization backend
before production begins when the task creates a dashboard, timeline, graph,
external report, manager view, live status UI, or external viz adapter.

The built-in `local_file` backend is allowed for local evidence and smoke
checks. Any remote, SaaS, cloud, live dashboard, WebSocket, database, or public
evidence backend starts `UNVERIFIED` and requires:

- human backend selection;
- bounded connector policy;
- credential lifecycle entry when credentials are needed;
- redaction rules;
- worker-owned adapter implementation;
- smoke evidence;
- operator review.

## Ownership

Claude owns visualization/diagram information architecture and task-local
`VISUALIZATION_SPEC.md` review. Codex or another deterministic worker may
implement event plumbing after the Claude visualization spec is approved.
