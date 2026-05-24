# Claude Code Entry

This project uses the file-backed harness in `harness/`.
Claude Code project adapters live under `.claude/`, but they are generated
views over the same file-backed harness. They do not make Claude Code the lead
operator over Codex.

If the user says "you are operator" or asks you to operate the project, load
`AGENTS.md`, run the startup workflow there, then load
`harness/operators/claude-code/AGENT.md`.

Do not rely on this file alone. Canonical shared memory is in `harness/shared/`,
with current scope in `feature_list.json`, `progress.md`, and task artifacts.
Team-shared memory is in `harness/teams/*/TEAM_CONTEXT.md`.
Dual-operator parity and non-forced consensus are defined in
`harness/shared/DUAL_OPERATOR_PROTOCOL.md`.
Internal/external record separation and context-pressure control are defined in
`harness/shared/CHANNEL_RECORDS.md` and `harness/shared/CONTEXT_PRESSURE.md`.

Before building dashboards, timelines, graphs, external evidence HTML views, manager
views, live status UI, or state visualizations, load
`harness/shared/VISUALIZATION_SPEC_POLICY.md` and require a task-local
`VISUALIZATION_SPEC.md`.

Use `python3 scripts/harnessctl.py eval-run` for local scaffold/governance
regression checks when relevant. It is a safe local evaluator, not a replacement
for task-specific evidence.

Use `python3 scripts/harnessctl.py broadcast-draft` only for local draft
creation. Use `python3 scripts/harnessctl.py review-packet` only for redacted
review packets. Neither command approves publication or makes reviewer output
authority.
