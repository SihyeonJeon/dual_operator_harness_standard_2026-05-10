# Session Continuity

Session separation is intentional. It reduces premature context compression,
hidden stale memory, and hallucination carried across unrelated work.

## Rules

- Fixed operators use persistent sessions.
- Worker sessions may change by task, role, location, runtime, or cost tier.
- Returning work should resume the previous worker session when safe.
- If resume is unavailable or unsafe, the replacement worker loads the recorded
  context pack and role files before acting.
- Every session handoff must prefer shared files and task artifacts over chat
  memory.
- Root `feature_list.json`, `progress.md`, and `session-handoff.md` are part of
  the canonical restart path and must stay consistent with task artifacts.
- A phase gate is not cleanly handed off until root feature state, current
  progress, session handoff, worker registry, event log, and compiled
  report/viz views either agree or record a blocker.
- Root feature verification commands must stay portable. Do not put local user
  paths, package-cache paths, `NODE_PATH`, or other machine-specific smoke
  commands in `feature_list.json`; keep those reproduction details in task
  evidence files.
- External-channel records such as broadcast drafts, reviewer packets, chat or
  mobile approvals, and connector responses must not be carried forward as
  canonical context until summarized into internal files.
- Context pressure should trigger compaction before unrelated worker sessions,
  lower-tier workers, or reopened parts receive stale full-session context.

## Required Handoff Data

Each worker registry entry should record:

- worker id;
- role and team;
- task id and slice id;
- runtime surface;
- model class and effort;
- session handle or resume command when available;
- context pack path;
- owned/no-touch paths;
- last checkpoint;
- unresolved questions;
- resume status.

## New Session Startup

Before acting, a new or resumed session must load:

1. relevant role file from `ROLE_FILE_INDEX.md`;
2. relevant `SKILLS.md`;
3. team `TEAM_CONTEXT.md` if it is a team worker;
4. current task blueprint;
5. assigned worker brief;
6. prior handoff/checkpoint if returning to an existing task.
7. bounded context pack defined by `CONTEXT_PRESSURE.md`.

## Root Handoff Files

`progress.md` records current status for the next session. `session-handoff.md`
records the restart path. `feature_list.json` records machine-readable scope and
state. These files are not substitutes for `harness/shared/`; they are the
lightweight entry layer that points a fresh agent back to shared canonical
memory.

## Compression Guard

If a summary drops uncertainty, failed gates, unresolved questions, or task
state, keep the task `PENDING_CROSS_CHECK` until an evaluator checks the
compressed summary against artifacts.

## Transcript Guard

Large command transcripts, patch diffs, browser logs, and connector responses
are internal evidence only. Public or human-facing summaries should cite paths,
counts, verdicts, and screenshots instead of pasting raw diffs or long logs.
