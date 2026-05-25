# Role File Index

This is the lightweight startup index for agents. Do not put long guidance here.
Point to role files instead.

## Fixed Operators

Root always-load for any operator invocation:

- `AGENTS.md`
- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `harness/shared/ROLE_FILE_INDEX.md`
- `harness/shared/ACTIVE_SNAPSHOT.md`
- `harness/shared/PROJECT_PROFILE.json`
- `harness/shared/WORKSTREAM_PROFILE.json`
- `harness/shared/DUAL_OPERATOR_PROTOCOL.md`
- `harness/shared/OPERATOR_SESSION_REGISTRY.json`
- `harness/shared/MODEL_ROUTING.json`
- `harness/shared/PLUGIN_ROUTING.json`
- `harness/shared/OBSERVABILITY.md`
- `harness/shared/RECORDS_POLICY.md`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md` when cloud/viz/backend choices are in scope
- `harness/viz/VIZ_BACKENDS.json` when visualization backend work is in scope
- current task blueprint

Claude Code operator always-load:

- `harness/operators/claude-code/AGENT.md`
- `harness/operators/claude-code/SKILLS.md`
- `.claude/settings.json` when using Claude Code runtime features
- `.claude/README.md` when debugging generated Claude adapters
- `harness/shared/HARNESS_CONFIG.json`
- `harness/shared/DUAL_OPERATOR_PROTOCOL.md`
- `harness/shared/OPERATOR_SESSION_REGISTRY.json`
- `harness/shared/RECORDS_POLICY.md`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md` when cloud/viz/backend choices are in scope
- `harness/viz/VIZ_BACKENDS.json` when visualization backend work is in scope
- current task blueprint

Codex operator always-load:

- `harness/operators/codex/AGENT.md`
- `harness/operators/codex/SKILLS.md`
- `harness/shared/HARNESS_CONFIG.json`
- `harness/shared/DUAL_OPERATOR_PROTOCOL.md`
- `harness/shared/OPERATOR_SESSION_REGISTRY.json`
- `harness/shared/RECORDS_POLICY.md`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md` when cloud/viz/backend choices are in scope
- `harness/viz/VIZ_BACKENDS.json` when visualization backend work is in scope
- current task blueprint

## Teams

Planning worker always-load:

- `harness/teams/planning/AGENT.md`
- `harness/teams/planning/SKILLS.md`
- `harness/teams/planning/TEAM_CONTEXT.md`
- `harness/shared/PART_OWNERSHIP.md`
- `harness/shared/MODEL_ROUTING.json`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/spec/SPEC_AUTOMATION_POLICY.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md` when cloud/viz/backend choices are in scope
- assigned worker brief

Design worker always-load:

- `harness/teams/design/AGENT.md`
- `harness/teams/design/SKILLS.md`
- `harness/teams/design/TEAM_CONTEXT.md`
- `harness/shared/PART_OWNERSHIP.md`
- `harness/shared/MODEL_ROUTING.json`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/viz/VIZ_BACKENDS.json` when visualization backend work is in scope
- assigned worker brief

Coding or production worker always-load:

- `harness/teams/coding/AGENT.md`
- `harness/teams/coding/SKILLS.md`
- `harness/teams/coding/TEAM_CONTEXT.md`
- `harness/shared/PART_OWNERSHIP.md`
- `harness/shared/MODEL_ROUTING.json`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/viz/VIZ_BACKENDS.json` when visualization backend work is in scope
- `harness/viz/adapters/WORKER_ADAPTER_BRIEF.md` when implementing a viz adapter
- assigned worker brief

Evaluation worker always-load:

- `harness/teams/evaluation/AGENT.md`
- `harness/teams/evaluation/SKILLS.md`
- `harness/teams/evaluation/TEAM_CONTEXT.md`
- `harness/shared/QUALITY_GATES.md`
- `harness/shared/RECORDS_POLICY.md`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/evals/README.md`
- `harness/evals/golden_suite.json` when scaffold or governance regression is in scope
- `harness/viz/VIZ_BACKENDS.json` when visualization backend work is in scope
- `harness/shared/MODEL_ROUTING.json`
- assigned worker brief

## Session Change Rule

When any operator, team, or worker session changes, the new session must reload
the relevant files in this index before acting. Old chat memory is not enough.
Claude Code subagents and skills must write durable findings back to these
file-backed artifacts; their private context is not shared memory.
