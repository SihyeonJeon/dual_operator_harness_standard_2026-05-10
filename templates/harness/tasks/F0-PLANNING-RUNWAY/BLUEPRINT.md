# F0 Planning Runway And Slice Gate Blueprint

Task id: F0-PLANNING-RUNWAY
Status: NOT_STARTED

## Goal

Run the pre-production planning runway before any sharp/deep production slice is
approved. The output is not production work. The output is a justified,
worker-ready slice candidate or an explicit blocker.

## Required Inputs

- root `feature_list.json`
- root `progress.md`
- root `session-handoff.md`
- `harness/shared/PROJECT_PROFILE.json`
- `harness/shared/WORKSTREAM_PROFILE.json`
- `harness/shared/TEAM_TOPOLOGY.md`
- `harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md`
- `harness/shared/CROSS_FEEDBACK_LOOP.md`
- `harness/shared/SHARP_DEEP_EXECUTION.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/templates/TASK_BLUEPRINT.md`
- `harness/templates/WORKER_BRIEF.json`
- `harness/templates/VISUALIZATION_SPEC.md`

## Planning Runway

Before approving a slice, planning must record:

- confirmed and rejected interpretations of the project goal;
- current-state market/comparable research as-of the command date, or a
  `NOT-RUN` rationale with risk when current external reality does not matter
  or cannot be checked;
- detected workstreams and risk assumptions;
- material unknowns and human-decision blockers;
- candidate deliverable map;
- candidate team topology;
- candidate verification surfaces;
- whether visualization is necessary, and if so the purpose, audience, source
  artifacts, data contract, redaction constraints, and acceptance criteria that
  must be specified before visualization production starts;
- two or more slice candidates when the first choice is not obvious;
- why rejected slice candidates are deferred;
- whether design, research, domain review, or council input can invalidate the
  candidate slice.

## Slice Approval Gate

A sharp/deep slice becomes active only after:

- planning states why this slice is highest leverage now;
- design or domain discovery has run when it could change the slice boundary;
- current-state research has informed the plan when market, tools,
  alternatives, standards, regulations, or public facts could change it;
- evaluation defines the evidence needed for closure;
- visualization work, if present, has a task-local `VISUALIZATION_SPEC.md`
  approved or is explicitly marked not required;
- cross-evaluation or council is scheduled when risk or ambiguity warrants it;
- the operator confirms no material strategy, budget, credential, compliance,
  deployment, public communication, customer contact, or irreversible external
  action has been silently decided;
- root `feature_list.json` and the task blueprint reflect the approved slice.

## Completion Evidence

- `WORKSTREAM_PROFILE.json` is confirmed or updated with rationale.
- `CURRENT_RESEARCH.json` exists when current-state research is material, or
  the task records a `NOT-RUN` rationale and risk.
- Cross-feedback is scheduled for material artifacts, or not-applicable
  rationale is recorded.
- `TEAM_TOPOLOGY.md` remains compatible with planning, production, and
  evaluation lanes.
- A project-specific task blueprint exists under `harness/tasks/`, or exact
  blockers are recorded.
- Any dashboard, timeline, graph, local evidence HTML view, manager view, live status
  UI, or state visualization has passed the pre-visualization spec gate or is
  blocked before production.
- A worker brief exists only if a slice passed the approval gate.
- `progress.md`, `session-handoff.md`, and `ACTIVE_SNAPSHOT.md` record the
  approved slice, candidate set, or blocker.
- No operator has performed production work directly.

## Stop Conditions

- The project goal is too ambiguous to choose one slice.
- Choosing the slice would decide budget, credentials, deployment, compliance,
  public communication, customer contact, or irreversible external action.
- Planning, design, evaluation, or council finds the candidate slice wrong.
- The inferred risk tier or workstream profile appears materially wrong.
