# Workspace Layout

Purpose: keep active work small while preserving long-term memory and evidence.

## Active Workspace

Active task work lives in:

- `harness/tasks/`
- `harness/tasks/active/`

Only current or immediately relevant tasks should remain active. Operators and
workers should load active tasks first and read older tasks on demand.

## Archive Workspace

Archived task work lives in:

- `harness/tasks/archive/`

Archive is durable storage, not always-load context. Archived items are searched
or summarized when needed.

## Seven-Day Rule

A task artifact should be considered for archive when all are true:

- it has been closed, blocked, or superseded;
- it is older than 7 days or no longer part of the current slice;
- its durable decisions have been summarized into internal canonical records;
- no active worker session depends on it as the current context pack.

## Move Rules

- Do not archive the active task.
- Do not archive unresolved human decisions.
- Do not archive a task without preserving source paths in `progress.md`,
  `session-handoff.md`, or `harness/shared/MEMORY.md`.
- Do not treat archive as deletion.

## Context Rule

Use archive as retrieval memory, not prompt stuffing. A resumed or replacement
worker receives a bounded context pack with source paths, not the whole archive.
