# Spec Automation Policy

Purpose: make planning and specification generation explicit before sharp/deep
production work starts.

## Default Flow

Project goal or operator intent moves through this sequence:

1. goal intake;
2. PRD draft;
3. anti-PRD or failure-mode draft;
4. evaluator critique;
5. candidate slices;
6. approved active slice;
7. worker brief;
8. production;
9. evaluation and cross-check;
10. operator closure;
11. context update and regulation review.

Production must not start from a vague goal alone unless the human explicitly
approves emergency one-incident fallback.

## Spec Agent Boundary

A spec agent or planning worker may generate PRD drafts and anti-PRD drafts.
Those drafts are proposals. Operators approve, revise, or reject them through
normal planning gates.

Spec automation must not decide:

- budget;
- irreversible external action;
- production deployment;
- regulated-domain advice;
- publication;
- connector activation;
- material product scope when ambiguous.

## PRD Requirements

Every PRD draft should state:

- user or audience;
- desired outcome;
- non-goals;
- constraints and risks;
- acceptance criteria;
- required evidence;
- open questions;
- proposed first sharp/deep slice.

## Anti-PRD Requirements

Every anti-PRD should state:

- likely failure modes;
- missing assumptions;
- overbroad slice risks;
- context overload risks;
- unsafe shortcuts;
- verification gaps;
- reasons to send work back to planning or human review.

## Evaluator Gate

The evaluator checks whether the PRD and anti-PRD make a worker brief
executable. If not, the task stays in planning.

## Visualization Dependency

If the planned work creates dashboards, timelines, graphs, external evidence HTML
views, manager views, live status UI, or state visualizations, the
pre-visualization specification gate must pass before production.
