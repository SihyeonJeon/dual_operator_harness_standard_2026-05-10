# Claude Code Entry

This project uses the file-backed harness in `harness/`.
Claude Code project adapters live under `.claude/`, but they are generated
views over the same file-backed harness. They do not make Claude Code the lead
operator over Codex.

Root `CLAUDE.md` is intentional. Claude Code reads project-level guidance from
the repository root, while `.claude/` contains settings, hooks, agents, and
skills.

If the user says "you are operator" or asks you to operate the project, load
`AGENTS.md`, run the startup workflow there, then load
`harness/operators/claude-code/AGENT.md`.

Do not rely on this file alone. Canonical shared memory is in `harness/shared/`,
with current scope in `feature_list.json`, `progress.md`, and task artifacts.
Team-shared memory is in `harness/teams/*/TEAM_CONTEXT.md`.
Dual-operator parity and non-forced consensus are defined in
`harness/shared/DUAL_OPERATOR_PROTOCOL.md`.
Local record policy and context-pressure control are defined in
`harness/shared/RECORDS_POLICY.md` and `harness/shared/CONTEXT_PRESSURE.md`.
Agent-to-agent communication and token-saving context packets are defined in
`harness/shared/AGENT_COMMUNICATION.md`.
Concept-to-artifact copy rules are defined in
`harness/shared/CONCEPT_TRANSLATION_POLICY.md`. Ordinary domain terms are
allowed when they read naturally in the artifact.

Before building dashboards, timelines, graphs, status HTML views, manager
views, live status UI, or state visualizations, load
`harness/shared/VISUALIZATION_SPEC_POLICY.md` and require a task-local
`VISUALIZATION_SPEC.md`.

Use `python3 scripts/harnessctl.py eval-run` for local scaffold/governance
regression checks when relevant. It is a safe local evaluator, not a replacement
for task-specific evidence.

For software, web, app, API, or UI work, load
`harness/shared/SOFTWARE_FEEDBACK_POLICY.md`. Final feedback should cover
lint/static checks, runtime smoke, and Playwright or equivalent browser/device
evidence for interactive surfaces when available.

For repeatable mechanics, prefer the executable helpers over manual prose:
`python3 scripts/harnessctl.py context-pack`, `worker-brief`, `model-route`,
`task-packet`, `concept-check`, and `software-feedback`.

The public kit keeps account-specific posting, outreach, connector logs, and
private review workflows outside the scaffold. Private overlays own those
adapters when a project needs them.
