# Team Topology

Team and worker count are selected by project goal, risk, and task shape.
The initial inference is recorded in `harness/shared/WORKSTREAM_PROFILE.json`.
Operators may refine it through regulation rules and task evidence.

## Rules

- Do not preserve a fixed team count just because an example used it.
- Use the smallest topology that satisfies the gates.
- Treat planning, production, and evaluation as always-present logical lanes.
- Before the overall plan, run current-state market/comparable research when
  the goal depends on current external reality. If it is not needed or cannot
  run, record the `NOT-RUN` rationale and risk.
- Activate design, cross-evaluation, council, or specialized workers only when
  the workstream profile, risk, or task evidence justifies them.
- Add workers only when ownership is disjoint or independent evaluation is
  required.
- Material artifacts need an independent cross-feedback loop or an explicit
  not-applicable rationale before operator closure.
- Record each worker in `WORKER_SESSION_REGISTRY.json`.
- Returning tasks should resume the prior worker session when safe.
- If a worker discovers missing planning/design/spec information, it asks the
  relevant upstream team through a task artifact.
- Visualization work adds a pre-production spec gate: planning/design must
  approve a task-local `VISUALIZATION_SPEC.md` before dashboard, timeline,
  graph, local evidence HTML, manager-view, live status UI, or state-visualization
  production starts.
- Visualization/diagram information architecture is Claude-owned. Codex or a
  deterministic worker may implement `events.jsonl` plumbing and adapters after
  Claude design review approves the spec.
- Operators do not debug or code inside the development loop.
- Team sessions may change, but role files, skills, and team context must be
  reloaded from `ROLE_FILE_INDEX.md`.
- Each completed substantial task must include regulation review before the next
  production slice starts.

## Closure Flow

Current research -> planning -> design -> production/coding -> debugging ->
evaluation -> cross-feedback -> cross-evaluation -> completed work packet ->
fixed operators -> human when material -> context update -> regulation review
-> next slice.
