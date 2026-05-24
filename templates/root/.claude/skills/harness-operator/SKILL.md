---
name: harness-operator
description: Load and operate this project-local dual-operator harness. Use when the user says "you are operator" or asks Claude Code to operate the generated harness.
---

# Harness Operator Skill

Use this skill to enter the generated harness without relying on hidden chat
memory.

1. Read root `AGENTS.md`.
2. Run or review `./init.sh` unless the user forbids local checks.
3. Read `feature_list.json`, `progress.md`, and `session-handoff.md`.
4. Read `harness/shared/ROLE_FILE_INDEX.md`.
5. Load `harness/operators/claude-code/AGENT.md`.
6. Load `harness/shared/ACTIVE_SNAPSHOT.md`,
   `harness/shared/PROJECT_PROFILE.json`, and
   `harness/shared/WORKSTREAM_PROFILE.json`.
7. Load `harness/shared/OBSERVABILITY.md` and
   `harness/shared/VISUALIZATION_SPEC_POLICY.md`.
8. Continue only through file-backed state and task artifacts.

Preserve shared memory:

- Operator memory: `harness/shared/`, `feature_list.json`, `progress.md`,
  `session-handoff.md`, `harness/tasks/`
- Team memory: `harness/teams/*/TEAM_CONTEXT.md`
- Do not treat Claude Code skill memory or private chat as authority.
- Use `python3 scripts/harnessctl.py report` for a local compiled HTML status
  view when needed. The report is not canonical memory.
- Use `python3 scripts/harnessctl.py viz-export --backend local_file` for local
  event payloads when a viz backend worker needs smoke evidence.
- Treat visualization and diagram information architecture as Claude-owned;
  event plumbing may be delegated only after approved `VISUALIZATION_SPEC.md`.
