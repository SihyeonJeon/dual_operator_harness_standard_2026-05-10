# Part Ownership And Worker Session Reuse

Large projects are split into parts. A worker that owned one substantial part
should be recalled for that same part when safe, and should not be reused for
unrelated parts merely because its session is warm.

## Rules

- Every worker brief must name `part_id`, owned paths/artifacts, no-touch
  paths/artifacts, and upstream/downstream interfaces.
- A part-owner worker session is reused when the same part is reopened and the
  prior session is available, safe, and not stale.
- A part-owner worker is not assigned unrelated parts unless the human/operator
  records an explicit reason.
- If ownership overlaps, planning must split the work or create a merge protocol
  before production starts.
- Double-editing the same file/artifact is forbidden unless a task artifact
  records the order, owner, merge point, and evaluator.
- When a part is updated, the part-owner session must update its checkpoint and
  the relevant team `TEAM_CONTEXT.md`.

## Registry Fields

`WORKER_SESSION_REGISTRY.json` records:

- worker id;
- part id and part scope;
- owned paths/artifacts;
- no-touch paths/artifacts;
- session handle;
- context pack;
- last checkpoint;
- resume status;
- reason when a replacement worker is used.

## Context Discipline

Do not mix unrelated part context into a part-owner session. If a worker needs
read-only context from another part, provide a bounded artifact summary instead
of loading that worker into the other part's production loop.

