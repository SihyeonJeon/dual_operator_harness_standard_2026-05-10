# Session Handoff

Date: {{DATE}}
Status: IMPLEMENTER_HANDOFF_COMPLETE

## Restart Path

1. Open the project root.
2. Run `./init.sh`.
3. Read `AGENTS.md`.
4. Read `feature_list.json` and `progress.md`.
5. If acting as an operator, load the matching role from `harness/operators/`.

## Canonical Memory

- Root scope state: `feature_list.json`
- Current progress: `progress.md`
- Shared harness memory: `harness/shared/`
- Current task artifacts: `harness/tasks/`
- Internal/external boundary: `harness/shared/CHANNEL_RECORDS.md`
- Context pressure controls: `harness/shared/CONTEXT_PRESSURE.md`

## Open Work

- H0 local smoke must be verified or blocked with evidence.
- H1 bootstrap restart smoke must be verified or blocked with evidence.
- Planning runway is pending; first production slice remains a candidate until
  planning/design/evaluation gates approve it.

## Do Not Carry Forward As Authority

- Hidden chat context from the implementer.
- Unrecorded assumptions about domain strategy, budget, tools, deployment,
  audience, or compliance.
- Broadcast drafts, reviewer output, MCP export output, social comments, or
  connector responses that were not summarized into internal harness files.
