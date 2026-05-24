# Claude Code Harness Adapter

This directory is generated glue for Claude Code. It is not the canonical
harness memory.

Canonical state remains:

- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `harness/shared/`
- `harness/tasks/`
- team `TEAM_CONTEXT.md` files

The files here make Claude Code load that state through project settings,
hooks, skills, and project subagents. If a Claude Code runtime feature is
unavailable, record it as `UNVERIFIED` in `harness/shared/CAPABILITY_REGISTRY.json`
and continue through file-backed harness artifacts.

These files do not make Claude Code the lead operator. Codex remains an equal
fixed operator through root `AGENTS.md`, `harness/operators/codex/AGENT.md`, and
`harness/shared/DUAL_OPERATOR_PROTOCOL.md`.

Local visibility helpers live outside this adapter:

- `python3 scripts/harnessctl.py event`
- `python3 scripts/harnessctl.py report`
- `python3 scripts/harnessctl.py viz-export --backend local_file`
- `python3 scripts/harnessctl.py viz-spec-check`
- `python3 scripts/harnessctl.py eval-run`
- `python3 scripts/harnessctl.py broadcast-draft`
- `python3 scripts/harnessctl.py review-packet`

Generated HTML reports are compiled views over canonical state. Visualization
production still requires `harness/shared/VISUALIZATION_SPEC_POLICY.md` and a
task-local `VISUALIZATION_SPEC.md`.

Claude owns visualization/diagram information architecture. Codex or another
worker may implement event plumbing after the approved visualization spec.

Broadcast drafts and external review packets are external-channel records. They
are not canonical memory until summarized into internal harness files under the
rules in `harness/shared/CHANNEL_RECORDS.md`.
