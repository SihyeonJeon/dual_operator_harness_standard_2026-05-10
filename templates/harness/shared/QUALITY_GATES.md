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
- Canonical project records and compiled local report views stay separated per
  `harness/shared/RECORDS_POLICY.md`.
- Context pressure is checked for long, reopened, cross-team, or externally
  visible tasks per `harness/shared/CONTEXT_PRESSURE.md`.
- Current-state market/comparable research ran before overall planning when the
  task depends on current external reality, or `NOT-RUN` risk is explicit per
  `harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md`.
- Failures route back to the correct upstream team.
- Cross-evaluation is complete or explicitly justified.
- Cross-feedback is recorded for material artifacts, or `NOT-RUN` risk is
  explicit per `harness/shared/CROSS_FEEDBACK_LOOP.md`.

## Current Research Gate

- Load `harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md` before approving the
  overall plan.
- The research is as-of the command date, not model training date.
- Required outputs: source list or `NOT-RUN` rationale, current alternatives or
  comparable references when relevant, findings that change the plan, and
  planning decision impact.
- Prefer `python3 scripts/harnessctl.py current-research` to record the
  evidence packet.

## Cross Feedback Gate

- Load `harness/shared/CROSS_FEEDBACK_LOOP.md` before operator closure.
- Producer and reviewer should be independent for material artifacts.
- `FAIL` routes to exactly one upstream owner. `WARN` requires accepted risk.
- Prefer `python3 scripts/harnessctl.py cross-feedback` to record feedback
  evidence.

## Concept Translation Gate

- Load `harness/shared/CONCEPT_TRANSLATION_POLICY.md` when the task creates
  user-facing copy, UI, media, reports, demos, names, labels, or public output.
- The artifact should satisfy the user's concept without announcing the prompt
  or task label as copy.
- Exact request phrases, self-descriptive meta-copy, and awkward
  assignment-style wording in public/user-facing surfaces require explicit user
  approval. Ordinary domain terms are not banned just because the user used
  them.
- Prefer `python3 scripts/harnessctl.py concept-check` for literal phrase
  leakage when artifact paths and forbidden phrases are known.

## Software And App Gates

- Load `harness/shared/SOFTWARE_FEEDBACK_POLICY.md`.
- Prefer `python3 scripts/harnessctl.py software-feedback` when project
  commands are known.
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
  - independent evaluator evidence;
  - explicit `WARN` accepted by the operator or human explaining why only
    visible golden/self-eval evidence exists.
- Hidden, held-out, independent evaluator, or challenge eval failures reopen the
  task as a feedback slice before the previous closure can be reasserted.
- Accepted failures route back to the correct planning, production, or
  evaluation artifact and become future regression fixtures when they can be
  checked deterministically.
- Root `feature_list.json` verification commands stay portable. Local hidden
  evaluator paths, private overlay records, and temp-only challenge commands
  belong in task evidence.

## Benchmark Claim Gate

Before any public benchmark-style claim:

- Write a preregistration packet with `harnessctl.py preregister-benchmark`.
- Public proof runs require a clean git working tree and recorded commit SHA.
- First-pass arms must use the same task order, timeout, evidence access, and
  verifier-feedback prohibition.
- Recovery arms must receive the same `RECOVERY_EVIDENCE_PACKET.json` bytes.
- Non-verifier judging must use `harnessctl.py blind-redact` or equivalent
  identity stripping before review.
- Council decisions must use `harnessctl.py council-decision` and preserve
  dissent instead of rewriting disagreement as consensus.
- Report score, runtime, token/cost use, exceptions, timeout rate, and claim
  boundaries. Do not convert a local pilot into a public superiority claim.

## Visualization Gates

Use before producing dashboards, timelines, graphs, status HTML views,
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
they can be checked deterministically without secrets, network writes, or
arbitrary command execution.
