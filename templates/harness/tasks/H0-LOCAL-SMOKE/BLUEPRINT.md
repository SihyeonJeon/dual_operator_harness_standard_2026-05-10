# H0 Local Smoke Blueprint

Task id: H0-LOCAL-SMOKE
Status: IN_PROGRESS

## Goal

Prove the generated harness can run one smallest meaningful vertical slice for
the supplied project profile without relying on unverified capabilities.

## Constraints

- Production work must not begin before this smoke is ready.
- All runtime capabilities start as `UNVERIFIED`.
- If the project goal is too ambiguous to choose a smoke slice, ask the user.
- Root agent entry files must exist before an operator session begins.

## Required Evidence

- project profile exists;
- root `AGENTS.md`, `init.sh`, `feature_list.json`, `progress.md`, and
  `session-handoff.md` exist;
- root `scripts/harnessctl.py` exists and exposes validation, event logging,
  static HTML report generation, visualization spec checks, and eval-run;
- `harness/evals/golden_suite.json` exists and can check scaffold invariants
  without network writes or arbitrary command execution;
- root `.claude/settings.json`, `.claude/agents/`, `.claude/hooks/`, and
  `.claude/skills/` exist as Claude Code adapters;
- active snapshot exists;
- operator files exist and include ambiguity protocol;
- operator config states fixed persistent sessions and highest verified model/effort;
- worker session registry exists;
- context loading policy keeps always-loaded files small;
- council MCP policy exists and is advisory only until H1 smoke passes;
- both fixed operators share the same `harness/shared/` files;
- dual operator protocol forbids forced consensus and preserves dissent;
- model routing keeps operators highest verified while workers use task-shaped
  lower verified tiers when gates allow;
- part ownership policy prevents reusing a part-owner worker session for
  unrelated parts;
- plugin routing caps active context plugins at four and includes caveman as
  preferred compression slot when verified;
- visualization spec policy and template exist;
- each team has a `TEAM_CONTEXT.md` file;
- model routing policy separates operator, planning, implementation, debugging,
  evaluation, and cross-evaluation model levels;
- role file index exists;
- operator and team skill files exist;
- session continuity policy exists;
- regulation evolution policy exists;
- sharp/deep execution policy exists;
- planning can run a runway that validates candidate slices before production;
- tool registry exists;
- permission policy exists;
- H0 evaluation report is created after smoke execution.
- H1 bootstrap restart smoke blueprint exists.
