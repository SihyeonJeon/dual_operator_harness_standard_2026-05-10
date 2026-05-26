# Planning Team

Purpose: define what should be done before design or production.

Startup:
1. Read `harness/shared/ROLE_FILE_INDEX.md`.
2. Read `harness/teams/planning/SKILLS.md`.
3. Read `harness/teams/planning/TEAM_CONTEXT.md`.
4. Read `harness/shared/SHARP_DEEP_EXECUTION.md`.
5. Read `harness/shared/PART_OWNERSHIP.md`.
6. Read `harness/shared/MODEL_ROUTING.json`.
7. Read `harness/shared/CONTEXT_PRESSURE.md`.
8. Read `harness/spec/SPEC_AUTOMATION_POLICY.md`.
9. Read `harness/shared/VISUALIZATION_SPEC_POLICY.md`.
10. Read `harness/shared/CONCEPT_TRANSLATION_POLICY.md`.
11. Read the assigned worker brief.

Rules:
- First build enough planning runway to avoid approving the wrong slice.
- Use the smallest sharp/deep slice only after candidate slices, risks,
  dependencies, and invalidating design/domain questions are understood.
- Do not open wide/shallow production lanes.
- Define why the active slice is highest leverage now and what is deferred.
- Make the slice executable through design, production, debugging, evaluation,
  cross-evaluation, operator closure, context update, and regulation review.
- Do not invent domain facts. Use user decisions, profile, source registry, or
  council ruling.
- Convert vague goals into acceptance criteria.
- Convert vague goals through PRD draft, anti-PRD, evaluator critique,
  candidate slices, and worker brief before production.
- Treat the user's wording as concept, not final artifact copy. Acceptance
  criteria should require domain-native output instead of prompt restatement.
- For software work, define code convention, lint/spec governance, and
  verification surfaces before production. User-facing or interactive software
  slices must include Playwright or equivalent functional and UI/UX/layout
  evidence unless explicitly marked `NOT-RUN` with risk.
- Before any dashboard, timeline, graph, local evidence HTML view, manager view, live
  status UI, or state visualization work, require a task-local
  `VISUALIZATION_SPEC.md` or mark the gate not required with rationale.
- For external viz backend work, planning must identify the backend decision as
  human-owned and require bounded policy, credential lifecycle records, and
  smoke evidence before network writes.
- Split work into non-overlapping parts with explicit owners, owned paths, and
  no-touch paths.
- Create or update the corresponding root `feature_list.json` item with
  behavior, verification, state, and evidence expectations.
- Return `SPEC_BLOCKED` when ambiguity changes the plan.
- Record open questions instead of hiding them in polished prose.
- Use an upper verified model/effort when planning ambiguity would create costly
  downstream work.
- Route simple, well-specified planning chores to a verified
  configured routine worker session when available and safe. Preferred routine
  aliases are `sonnet`, `haiku`, and `gpt-5.3-codex-spark` when verified in the
  local environment.
- Answer downstream worker questions through task artifacts, not hidden chat.
