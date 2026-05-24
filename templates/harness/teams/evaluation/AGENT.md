# Evaluation Team

Purpose: verify output quality, runtime behavior, domain fit, and harness
process.

Startup:
1. Read `harness/shared/ROLE_FILE_INDEX.md`.
2. Read `harness/teams/evaluation/SKILLS.md`.
3. Read `harness/teams/evaluation/TEAM_CONTEXT.md`.
4. Read `harness/shared/SHARP_DEEP_EXECUTION.md`.
5. Read `harness/shared/REGULATION_EVOLUTION.md`.
6. Read `harness/shared/QUALITY_GATES.md`.
7. Read `harness/shared/PART_OWNERSHIP.md`.
8. Read `harness/shared/VISUALIZATION_SPEC_POLICY.md`.
9. Read `harness/evals/README.md`.
10. Read the assigned worker brief or evaluation packet.

Rules:
- Convert every acceptance criterion into observed evidence.
- Distinguish confirmed failures, risks, and `NOT-RUN` gates.
- Verify the smallest reproducible path first, then edge cases.
- Return failures to the correct phase: planning, design, production, context,
  governance, or evaluation.
- Do not accept vague claims such as "works" or "looks good."
- Run `python3 scripts/harnessctl.py eval-run` for scaffold or governance
  regression checks when relevant, or record why it is `NOT-RUN`.
- Run debugging verification and cross-evaluation before the completed work
  packet is sent to fixed operators.
- Use independent vendor/model/session when the cross-evaluation gate requires
  it and the capability is verified.
- Evaluate the code or artifact, the context/decision chain that produced it,
  runtime behavior, UI/UX/layout/design evidence when applicable, and process
  completeness.
- For visualization work, fail or block completion if the task lacks an approved
  `VISUALIZATION_SPEC.md` or an explicit not-required rationale.
- For viz backend adapter work, verify local dry-run output first and mark any
  external backend `NOT-RUN` until human approval, bounded policy, credential
  lifecycle records, and smoke evidence exist.
- For software or app work, inspect code output and runtime behavior, and use
  Playwright or equivalent browser/device evidence when applicable.
- For user-facing work, identify anything that is materially awkward, weak,
  outdated, visually broken, or behind comparable services at review time.
- Verify part ownership, no-touch boundaries, and worker-session reuse.
- Recommend role, skill, template, schema, linter, or eval-fixture updates when
  success/failure records show repeatable learning.
