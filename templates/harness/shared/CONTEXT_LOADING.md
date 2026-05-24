# Context Loading

Always-loaded context must stay small. Agents load the smallest context pack
that can safely complete the current step.

## Global Always-Load

Budget target: small enough for every operator startup. If the combined pack
starts crowding out the current task, compact `progress.md`,
`session-handoff.md`, and `ACTIVE_SNAPSHOT.md` before loading old artifacts.

- root `AGENTS.md`
- root `feature_list.json`
- root `progress.md`
- root `session-handoff.md`
- `harness/shared/ACTIVE_SNAPSHOT.md`
- `harness/shared/PROJECT_PROFILE.json`
- `harness/shared/WORKSTREAM_PROFILE.json`
- `harness/shared/HARNESS_CONFIG.json`
- `harness/shared/ROLE_FILE_INDEX.md`
- `harness/shared/DUAL_OPERATOR_PROTOCOL.md`
- `harness/shared/OBSERVABILITY.md`
- `harness/shared/CHANNEL_RECORDS.md`
- `harness/shared/CONTEXT_PRESSURE.md`
- current task blueprint

## Operator On-Demand

- `.claude/settings.json` and `.claude/hooks/` when Claude Code behavior is
  being verified or debugged
- `PLUGIN_ROUTING.json`
- `PART_OWNERSHIP.md`
- `QUALITY_GATES.md`
- `CAPABILITY_REGISTRY.json`
- `TOOL_REGISTRY.json`
- `PERMISSION_POLICY.json`
- `MCP_TRUST.json`
- `OBSERVABILITY.md`
- `CHANNEL_RECORDS.md`
- `CONTEXT_PRESSURE.md`
- `broadcast/BROADCAST_POLICY.md` when external drafts, external evidence, or
  public release notes are in scope
- `reviewers/REVIEWER_POLICY.md` when external AI/human review is being used
- `mcp_server/README.md` when read-only context export is being verified
- `VISUALIZATION_SPEC_POLICY.md`
- `CLEAN_STATE.md`
- `REGULATION_EVOLUTION.md`
- `SESSION_CONTINUITY.md`
- `SHARP_DEEP_EXECUTION.md`
- relevant council transcript
- relevant failure ledger entries

## Planning Team

Always:
- project profile
- active snapshot
- current blueprint
- `harness/teams/planning/TEAM_CONTEXT.md`
- `harness/shared/PART_OWNERSHIP.md`

On demand:
- domain governance
- source registry
- prior planning reports
- market/frontier scan reports
- workstream profile when team topology is being changed
- `harness/spec/SPEC_AUTOMATION_POLICY.md`
- PRD/anti-PRD drafts when a goal is not yet executable
- visualization spec policy and template when visualization is in scope

## Design Team

Always:
- project profile
- active blueprint
- planning report
- `harness/teams/design/TEAM_CONTEXT.md`

On demand:
- style guide
- asset manifest
- visual references
- `VISUALIZATION_SPEC.md` when dashboards, timelines, graphs, reports, manager
  views, or live status UI are in scope
- prior screenshots/renders

## Coding Or Production Team

Always:
- worker brief
- owned/no-touch paths
- relevant conventions
- `harness/teams/coding/TEAM_CONTEXT.md`
- part ownership contract

On demand:
- architecture docs
- design spec
- visualization spec for dashboard/report/status UI work
- source registry
- failure ledger entries

## Evaluation Team

Always:
- blueprint
- acceptance criteria
- worker result
- evaluation template
- `harness/teams/evaluation/TEAM_CONTEXT.md`

On demand:
- domain gates
- prior regressions
- traces/screenshots/logs
- external review packets or ledgers only when the review is part of the active
  evidence chain
- visualization spec and generated HTML report when visualization is in scope
- cross-vendor verification policy
