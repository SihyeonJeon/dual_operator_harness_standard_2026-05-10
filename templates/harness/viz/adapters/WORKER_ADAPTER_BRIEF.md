# Worker Adapter Brief: Events To Viz Backend

Status: template

Use this brief when a worker is asked to connect `harness/events/events.jsonl`
to a project-selected visualization backend.

## Required Inputs

- Approved task-local `VISUALIZATION_SPEC.md`
- Human-selected backend id
- Bounded connector policy
- Credential lifecycle entry if credentials are needed
- Redaction rules
- Smoke evidence target path

## Non-Negotiable Rules

- Do not read `.env` or secret stores unless the operator has recorded explicit
  credential approval.
- Do not perform network writes in dry-run or smoke mode.
- Do not send internal deliberation, private logs, absolute local paths, tokens,
  customer data, or unapproved claims.
- Do not make the viz backend canonical memory. Canonical memory remains local
  harness files.
- Append an event to `harness/events/events.jsonl` for every dry run, smoke run,
  failed push, and successful push.

## Adapter Contract

The adapter must accept sanitized events from:

```text
harness/events/events.jsonl
```

It must produce:

- a dry-run payload file;
- a smoke evidence file;
- an audit event;
- rollback or disable instructions.

## Suggested Worker Steps

1. Read `harness/viz/VIZ_BACKENDS.json`.
2. Read the approved task-local `VISUALIZATION_SPEC.md`.
3. Implement adapter code under a project-specific path.
4. Add a dry-run command that writes payload locally.
5. Add a smoke command that proves authentication and schema mapping without
   publishing private data.
6. Record smoke evidence path in `VIZ_BACKENDS.json`.
7. Leave backend status `UNVERIFIED` until operator review changes it with
   evidence.
