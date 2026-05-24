# Quality Gates

Evaluation must test both the artifact and the reasoning chain that produced it.

## Universal Gates

- Acceptance criteria map to observed evidence.
- Context and decision chain match the approved blueprint.
- Part ownership and worker session handoff are recorded.
- No-touch boundaries were respected.
- Required verification ran or `NOT-RUN` risk is explicit.
- Relevant local eval suite ran through `scripts/harnessctl.py eval-run`, or
  the task explains why no deterministic suite applies.
- Visualization work has an approved pre-visualization spec or an explicit
  `NOT-RUN`/not-required rationale.
- External-facing drafts follow `harness/broadcast/BROADCAST_POLICY.md` and are
  not published without human approval, redaction, connector smoke evidence, and
  a publication ledger entry.
- External reviewer findings follow `harness/reviewers/REVIEWER_POLICY.md` and
  are treated as evidence, not authority.
- Internal canonical records and external-channel records stay separated per
  `harness/shared/CHANNEL_RECORDS.md`.
- Context pressure is checked for long, reopened, cross-team, or externally
  visible tasks per `harness/shared/CONTEXT_PRESSURE.md`.
- Failures route back to the correct upstream team.
- Cross-evaluation is complete or explicitly justified.

## Software And App Gates

- Code or artifact inspection.
- Static checks, lint, type checks, tests, or equivalent project commands.
- Runtime smoke for the smallest reproducible path.
- Browser or device verification when the result is interactive.
- Playwright or equivalent evidence for UI workflows when available.
- UI/UX/layout/design review for overflow, interaction, responsiveness,
  accessibility, and visible awkwardness.
- Product-context review: whether the result is materially weaker, more awkward,
  or less complete than comparable services at the time of review.

## Held-Out And Challenge Eval Gate

Use this gate for deterministic parsers, classifiers, extractors, ranking or
scoring systems, data transforms, eval frameworks, benchmark claims, and any
task where a metric can be tuned to the visible fixture set.

- A local golden set proves regression coverage, not generalization.
- A clean `PASS` or `passing` quality claim needs one of:
  - held-out or challenge eval evidence not used while tuning the artifact;
  - independent evaluator or reviewer packet evidence;
  - explicit `WARN` accepted by the operator or human explaining why only
    visible golden/self-eval evidence exists.
- Hidden, held-out, external reviewer, or challenge eval failures reopen the
  task as a feedback slice before the previous closure can be reasserted.
- Accepted failures route back to the correct planning, production, or
  evaluation artifact and become future regression fixtures when they can be
  checked deterministically.
- Root `feature_list.json` verification commands stay portable. Local hidden
  evaluator paths, private reviewer records, and temp-only challenge commands
  belong in task evidence.

## Visualization Gates

Use before producing dashboards, timelines, graphs, external evidence HTML views,
manager views, live status UI, or other state visualizations.

- `harness/shared/VISUALIZATION_SPEC_POLICY.md` has been loaded.
- A task-local `VISUALIZATION_SPEC.md` names source artifacts, event streams,
  data contract, views, interaction, stale-data behavior, redaction, sharing
  risk, and acceptance criteria.
- Static HTML reports are marked as compiled views over canonical files, not as
  canonical memory.
- Missing or ambiguous visualization spec returns `SPEC_BLOCKED`.

## Non-Software Gates

- Source provenance and claim hygiene for research.
- Narrative, structure, voice, and taste criteria for writing.
- Operational fit, handoff clarity, and repeatability for SOP/process work.
- Visual/media continuity and artifact inspection for design/media work.

## Feedback Loop

Every `FAIL`, material `WARN`, or unresolved `NOT-RUN` must be routed to exactly
one next action:

- planning;
- design;
- production;
- evaluation;
- context update;
- governance update;
- human decision.

Reusable failures should become future eval cases under `harness/evals/` when
they can be checked deterministically without secrets, external publication, or
arbitrary command execution.
