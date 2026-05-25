# Session Progress Log

Last updated: {{DATE}}
Project goal: {{PROJECT_GOAL}}
Adoption mode: {{MODE}}
Risk tier: {{RISK_TIER}}

## Current State

- Harness scaffold created.
- Production work has not started.
- H0 local smoke is active.
- H1 bootstrap restart smoke is pending.

## Active Feature

H0 - Harness scaffold doctor

## Done

- Project-local `harness/` directory created.
- Root agent entry files created.
- Shared context and operator role files created.
- Records policy and context-pressure controls created.
- MCP export and spec automation scaffolds created.

## In Progress

- H0 local smoke verification.

## Blockers And Risks

- Project-specific runtime commands are UNKNOWN.
- Planning runway and slice approval criteria are UNKNOWN.
- Material human decisions remain in `harness/shared/ACTIVE_SNAPSHOT.md`.
- Local report views remain separate from canonical project records.

## Decisions

- Project goal from input: {{PROJECT_GOAL}}
- Prior information and constraints: {{PRIOR_INFO_AND_CONSTRAINTS}}

## Evidence

- `harness/SCAFFOLDING_REPORT.md`
- `harness/IMPLEMENTER_HANDOFF.md`
- `harness/shared/ACTIVE_SNAPSHOT.md`

## Next Session

1. Run `./init.sh`.
2. Say "you are operator" to the selected fixed operator agent.
3. Resolve H0/H1 or record the exact blocker.
4. Ask the human only for material decisions that change scope, risk, cost,
   private data, irreversible action, or production authority.
