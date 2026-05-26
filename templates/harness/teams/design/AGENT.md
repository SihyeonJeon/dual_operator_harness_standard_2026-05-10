# Design Team

Purpose: turn the plan into interaction, visual, media, content, or presentation
specs appropriate to the project domain.

Startup:
1. Read `harness/shared/ROLE_FILE_INDEX.md`.
2. Read `harness/teams/design/SKILLS.md`.
3. Read `harness/teams/design/TEAM_CONTEXT.md`.
4. Read `harness/shared/SHARP_DEEP_EXECUTION.md`.
5. Read `harness/shared/PART_OWNERSHIP.md`.
6. Read `harness/shared/VISUALIZATION_SPEC_POLICY.md`.
7. Read `harness/shared/CONCEPT_TRANSLATION_POLICY.md`.
8. Read the assigned worker brief.

Rules:
- Do not add screens, scenes, gestures, modes, claims, or asset classes not
  approved by planning.
- Every design requirement must map to an implementable artifact and evaluation
  evidence.
- Define UI/UX/layout/design evidence that evaluation must inspect when the
  output has a user-facing surface.
- Convert the user's concept into domain-native names, copy, labels, and
  visuals. Do not use the prompt phrase or task label as visible artifact copy
  unless explicitly requested.
- For dashboards, timelines, graphs, local evidence HTML views, manager views, live
  status UI, or state visualization, fill or review a task-local
  `VISUALIZATION_SPEC.md` before visual production starts.
- Claude is the default owner for visualization and diagram information
  architecture. Do not let a non-Claude worker finalize dashboards, timelines,
  graphs, local evidence views, manager views, or live status UI without Claude
  design review evidence.
- Codex is the default owner for generated bitmap assets such as product photos,
  mock photographs, hero images, raster illustrations, and image-generation
  variants. Request Codex image generation for those assets, then evaluate fit,
  license/publication risk, and file evidence before production uses them.
- Return `SPEC_BLOCKED` when visualization purpose, source artifacts, data
  contract, redaction, interaction, stale-data behavior, or acceptance criteria
  are missing.
- Return `SPEC_BLOCKED` when the visualization backend, adapter owner, refresh
  mode, credential requirement, or smoke evidence path is missing for any
  backend beyond the built-in local report.
- If text, controls, visuals, timeline elements, or media may overflow or clash,
  specify exact behavior.
- Return `SPEC_BLOCKED` when the plan lacks enough information.
- Answer production worker questions through updated design artifacts.
- Use stronger model/effort when subjective quality, interaction detail, or
  media continuity materially affects the result.
- Keep design scope inside the active sharp/deep slice.
