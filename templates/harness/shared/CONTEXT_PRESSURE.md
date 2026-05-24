# Context Pressure Controls

Purpose: prevent context accumulation from becoming context overload while
preserving the kit's shared-memory and feedback-loop advantages.

## Context Budget

Every task should define a bounded context pack:

- always-load files;
- active task files;
- team memory files;
- source evidence needed for the step;
- explicit on-demand references;
- excluded stale or unrelated files.

Agents should not load long logs, old tasks, full archives, generated reports,
or external-channel drafts unless they are needed for the current decision.
Use `harness/shared/WORKSPACE_LAYOUT.md` for active/archive separation and
`harness/shared/MEMORY_BACKEND.json` for retrieval backends.

## Pressure Signals

Treat these as context-pressure warnings:

- repeated re-reading of unrelated files;
- worker confusion about active part ownership;
- operator relying on private chat memory over files;
- multiple unrelated part-owner sessions mixed into one conversation;
- external drafts treated as canonical memory;
- task closure that updates reports but not internal state;
- large logs loaded without a query;
- unresolved conflicts between `progress.md`, `ACTIVE_SNAPSHOT.md`, and
  `feature_list.json`.

## Compaction Triggers

Compact before continuing when:

- a task or phase closes;
- a worker hands off or is replaced;
- a part is reopened after a long pause;
- event logs or review packets become too long for the current step;
- operator context becomes dominated by stale history;
- the next step needs a lower-tier worker that should not receive full
  operator context.

## Compaction Output

A compaction must leave:

- current goal and current task id;
- active slice and acceptance criteria;
- operator decisions and unresolved dissent;
- worker part ownership and resume handle;
- changed files or artifacts;
- verification evidence and `NOT-RUN` gates;
- next action;
- source paths for deeper retrieval.

## Context Pack Rule

New or resumed workers receive a task-local context pack, not the entire
operator memory. The pack must include owned paths, no-touch paths, success
criteria, stop conditions, part-owner status, model/effort routing, plugin
routing, and relevant source paths.

## Plugin Rule

At most four active context-saving plugins may be used per task. `caveman` is
the preferred compression slot when available and verified. Plugin output is
advisory until written to canonical harness files.

## Part-Owner Isolation

Part-owner worker sessions should be resumed only for the same part. Do not use
a high-context part-owner session for unrelated work just because it is already
warm. If a prior owner is unavailable, load the recorded context pack and record
the replacement reason in `WORKER_SESSION_REGISTRY.json`.

## External Channel Rule

Broadcast drafts, social comments, reviewer responses, cloud-runner logs, and
mobile/chat approvals are external-channel records. They become internal context
only after an operator summarizes and disposes them in canonical files.
