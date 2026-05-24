# H1 Bootstrap Restart Smoke Blueprint

Task id: H1-BOOTSTRAP-SMOKE
Status: NOT_STARTED

## Goal

Prove a fresh agent can start from repository files, run local harness checks,
see current state, and route into the correct fixed-operator role when the user
says "you are operator".

## Required Evidence

- root `AGENTS.md` exists and routes operator invocation;
- root `CLAUDE.md` exists and points Claude Code to the same harness entry;
- root `.claude/settings.json` loads hooks that point back to file-backed
  harness state;
- root `init.sh` runs `scripts/validate_harness.py .`;
- root `init.sh` can append an event and compile a local HTML report through
  `scripts/harnessctl.py`;
- `scripts/harnessctl.py eval-run` can write local eval results under
  `harness/evals/results/`;
- `feature_list.json` exists and has behavior, verification, state, and evidence
  fields for every feature;
- `progress.md` and `session-handoff.md` exist;
- `harness/shared/ROLE_FILE_INDEX.md` points to operator and team role files;
- `harness/shared/VISUALIZATION_SPEC_POLICY.md` is available for visualization
  pre-spec gating;
- fixed operator can identify H0/H1 status without chat history;
- both fixed operators can identify the peer-review and non-forced-consensus
  protocol from `DUAL_OPERATOR_PROTOCOL.md`;
- Claude Code project agents and skills point to `harness/shared/` and team
  `TEAM_CONTEXT.md` files rather than private memory;
- project-specific runtime commands are either recorded or explicitly `UNKNOWN`;
- H1 evaluation report is created after smoke execution.

## Stop Conditions

- Root entry files missing.
- Local validator fails.
- Feature state cannot be parsed.
- Operator invocation depends on hidden chat memory.
