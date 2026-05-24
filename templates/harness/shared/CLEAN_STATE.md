# Clean State

Session completion requires both task evidence and restartability.

## Exit Checklist

- Current feature/task state is updated in `feature_list.json` or the task
  artifact.
- `progress.md` and `session-handoff.md` describe the current state.
- Required verification commands ran, or each skipped gate has a `NOT-RUN`
  rationale and risk.
- `harness/events/events.jsonl` records material task, gate, blocker, or human
  decision events when `scripts/harnessctl.py` is available.
- Root feature state, progress log, session handoff, worker registry, current
  task packet, event log, status report, and viz export agree before a material
  phase is called complete.
- Root feature verification commands are portable and do not contain local user
  paths, package-cache paths, or `NODE_PATH`.
- `python3 scripts/harnessctl.py report` has been run when human visibility,
  remote review, or external evidence is part of the task.
- If external visibility matters, a draft may be created with
  `python3 scripts/harnessctl.py broadcast-draft`; it remains unapproved and
  non-canonical until disposed under `harness/broadcast/BROADCAST_POLICY.md`.
- If external review matters, a packet may be created with
  `python3 scripts/harnessctl.py review-packet`; reviewer output remains
  evidence, not authority, until routed through evaluation/operator disposition.
- Internal and external records are separated according to
  `harness/shared/CHANNEL_RECORDS.md`.
- Context pressure has been checked when the session is long, a worker was
  replaced, a part was reopened, or summaries could hide stale assumptions.
- Temporary debug artifacts are removed or listed as intentional evidence.
- `./init.sh` remains available as the standard restart path.
- If Claude Code hooks or subagents were used, material outcomes are summarized
  into `harness/shared/`, `harness/tasks/`, or team `TEAM_CONTEXT.md` files.
- Any repeated failure is considered for `FAILURE_LEDGER.md` and
  `RULE_CHANGE_LOG.md`.

## Failure Semantics

If clean state cannot be reached, mark the active item `blocked`, preserve
evidence, and make the next restart action explicit.
