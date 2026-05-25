# Records Policy

Purpose: keep project memory file-backed, local, and explicit.

This public kit does not create social posts, blog drafts, release posts,
outreach drafts, publication ledgers, private review ledgers, or connector
response logs. Those workflows belong in a private project overlay, not in the
generated public harness.

## Canonical Project Records

The following are canonical project records:

- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `harness/shared/`
- `harness/tasks/`
- `harness/teams/*/TEAM_CONTEXT.md`
- `harness/events/events.jsonl`
- approved evaluation and human-review packets

Operators and workers update these records when evidence changes the project
state, rules, risk, or next action.

## Local Report Views

Generated reports are views over canonical records:

- `harness/reports/status.html`
- `harness/reports/status.json`
- `harness/reports/viz/`

Reports are useful for human inspection. They are not separate memory authority.

## Out Of Scope In Public Kit

The public harness must not generate or maintain:

- social, blog, newsletter, or release-post drafts;
- publication ledgers;
- private channel metrics or comments;
- external connector responses;
- private review packet ledgers;
- mobile/chat approval logs.

If a project needs those workflows, add them in a private overlay with its own
credential lifecycle, approval policy, redaction rules, and smoke evidence.

## Separation Rules

- Hidden chat context does not override file-backed harness memory.
- Private connector responses and external conversations must not be copied into
  canonical files unless the operator summarizes the relevant decision and risk.
- Public-facing artifacts must cite internal evidence paths when practical.
- Public-facing artifacts must not paste raw internal transcripts, full diffs,
  credential traces, connector responses, or private local paths.
