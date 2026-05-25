# Implementer Hooks

These hooks run around the harness implementer scaffold lifecycle. They are
scaffold controls, not operator authority.

## Hook Lifecycle

1. `PreScaffoldGoalIntake`
   - requires a non-empty project goal;
   - refuses to scaffold into the standard kit root;
   - records that production work has not started;
   - preserves missing material facts as `UNKNOWN`.

2. `IntakeValidate`
   - records the two-input intake boundary;
   - confirms absent prior constraints are treated as `UNKNOWN`;
   - refuses to turn intake into project execution strategy.

3. `ProfileDeriveAudit`
   - audits `PROJECT_PROFILE.json`;
   - rejects blank values where `UNKNOWN` is required;
   - checks that `primary_goal` came from input rather than invention.

4. `AdoptionModeSelect`
   - records `lite`, `standard`, or `full`;
   - keeps the selection heuristic visible for fixed operators.

5. `DomainPackSelect`
   - records selected domain packs;
   - defaults to no domain pack unless inputs justify one;
   - prevents hidden project strategy selection by the implementer.

6. `PostScaffoldValidation`
   - checks generated root and harness artifacts;
   - records validator result;
   - appends an implementer event to `harness/events/events.jsonl`;
   - keeps handoff to fixed operators explicit.

7. `HandoffComplete`
   - verifies human guide, implementer handoff, H0/H1/F0 tasks, fixed operator
     session registry, records policy boundary, and context-pressure controls;
   - records that the implementer role is complete;
   - confirms production work has not started.

## Evidence

Run evidence is recorded in:

- `harness/IMPLEMENTER_HOOKS_RUN.json`
- `harness/events/events.jsonl`
- `harness/SCAFFOLDING_REPORT.md`

## Boundary

Hooks may validate scaffold safety and completeness. They must not choose
project strategy, start production work, approve external actions, or replace
fixed operator review.
