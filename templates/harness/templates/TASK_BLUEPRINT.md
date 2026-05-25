# Task Blueprint

Task id:
Feature id:
Slice id:
Risk tier: 0 | 1 | 2 | 3 | 4
Status: IN_PROGRESS
Quality mode: stability | creative-reframe | mixed

## Goal

UNKNOWN

## Prior Information And Constraints

UNKNOWN

## Definition Of Done

- UNKNOWN

## Sharp/Deep Slice

Active slice:
Why this slice now:
Explicit non-goals:
Deferred next-slice candidates:
Advancement rule: do not start the next production slice until this slice is
`DONE`, `BLOCKED`, or material `WARN` is accepted.

## Feature State Link

Feature state source: root `feature_list.json`
Required transition evidence:
- behavior verified;
- verification command or gate result recorded;
- evidence path or command output recorded;
- operator or evaluator accepted any `NOT-RUN` risk before `passing`;
- part ownership and no-touch boundaries are respected;
- feedback failures route back to the correct prior team.

## Owned Scope

- UNKNOWN

## No-Touch Scope

- UNKNOWN

## Part Ownership

Part id:

- UNKNOWN

Part owner / worker session:

- UNKNOWN

Merge or double-edit protocol:

- UNKNOWN

## Required Evidence

- UNKNOWN
- context and decision chain evidence;
- PRD/anti-PRD/evaluator evidence when the task starts from a vague or material
  goal;
- runtime evidence where applicable;
- visualization pre-spec evidence where dashboards, timelines, graphs, HTML
  status views, manager views, or live status UI are requested;
- UI/UX/layout/design evidence where applicable;
- debugging closure evidence;
- cross-evaluation evidence or `NOT-RUN` rationale;
- held-out, challenge, independent evaluator, or explicit `WARN` evidence when
  deterministic metrics, parser/classifier/extractor behavior, eval framework
  claims, or benchmark-style quality claims are in scope;
- regulation review result.

## Held-Out / Challenge Eval Gate

Use when the task can overfit to visible examples, including deterministic
parsers, classifiers, extractors, ranking or scoring systems, data transforms,
eval frameworks, and benchmark claims.

Status: NOT_REQUIRED | REQUIRED_PENDING | PASS | WARN_ACCEPTED | BLOCKED | NOT-RUN

Required:

- local golden/self eval result;
- held-out or challenge eval result, independent evaluator result, or accepted
  `WARN` explaining why no independent/challenge evidence exists;
- routing decision for every held-out or independent evaluator failure;
- accepted reusable failures promoted into local regression fixtures;
- portable root verification command separated from local hidden/private
  evaluator paths.

## Visualization Pre-Spec Gate

Use when the task creates or changes a dashboard, timeline, graph, HTML status
view, manager view, live status UI, or any other visualization of the harness or
project state.

Policy: `harness/shared/VISUALIZATION_SPEC_POLICY.md`
Spec template: `harness/templates/VISUALIZATION_SPEC.md`
Task spec path: `harness/tasks/{task_id}/VISUALIZATION_SPEC.md`

Status: NOT_REQUIRED | DRAFT | APPROVED | BLOCKED | NOT-RUN

Visualization production is blocked until planning, design, evaluation, and
operator review approve the task-local visualization spec or explicitly record
why the gate is not required.

## Records Policy Gate

Use when the task creates local reports, evidence summaries, private overlay
adapter outputs, mobile/chat approvals, or connector response summaries.

Policy:

- `harness/shared/RECORDS_POLICY.md`

Status: NOT_REQUIRED | LOCAL_ONLY | PRIVATE_OVERLAY_ONLY | BLOCKED | NOT-RUN

Canonical project records stay local to the harness. Publication drafts, social
channel logs, outreach records, connector logs, and private review ledgers are
outside the public kit and belong in private overlays.

## Context Pressure Gate

Use when the task is long-running, reopened, multi-team, external-facing, or
delegated to a lower-tier or resumed part-owner worker.

Policy: `harness/shared/CONTEXT_PRESSURE.md`

Required:

- bounded context pack;
- compaction or no-compaction rationale;
- part-owner session isolation check;
- source paths for on-demand retrieval.

## Team And Worker Topology

Team and worker count are task-shaped. Record chosen workers in
`WORKER_SESSION_REGISTRY.json`. Returning tasks should resume prior worker
sessions when safe, but a part-owner session must not be reused for unrelated
parts.

## Model And Effort Routing

Operators: highest verified model and effort.
Workers: lowest verified level that satisfies the gate.
Routine worker examples may use Sonnet, GPT Codex Spark, or equivalent verified
lower-tier models when task gates allow.
Simple, well-specified implementation chores should prefer a verified
configured routine worker session when available and safe.
Planning/spec/evaluation/cross-check: prefer stronger models when ambiguity or
downstream cost is material.

## Open Questions

- UNKNOWN

## Ambiguity Decision

If any open question changes scope, risk, tool permissions, cost, private data,
or irreversible action, stop and ask the user.
