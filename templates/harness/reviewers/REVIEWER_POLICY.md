# External Reviewer Policy

Purpose: let operators request external AI or human review as evidence without
turning any reviewer into an authority over the project.

## Default State

- Reviewer adapters start `UNVERIFIED`.
- External review is evidence, not authority.
- A reviewer may disagree with operators; disagreement must be preserved.
- No forced consensus is allowed between Codex, Claude Code, external AI
  reviewers, or humans.
- Review packets must redact sensitive data before leaving the internal
  harness.

## When To Request Review

Request external review when:

- a phase closes;
- a public release, external evidence summary, or external claim is being
  prepared;
- architecture/API boundary risk is material;
- evaluation evidence is weak or disputed;
- regulated, security, privacy, or cost risk is material;
- a repeated failure suggests governance should change.

## Reviewer Axes

Typical axes:

- correctness;
- specification completeness;
- API and module boundaries;
- context and decision-chain integrity;
- security and privacy;
- documentation clarity;
- differentiation and external positioning;
- UI/UX/layout quality when applicable;
- regression and test adequacy.

## Review Packet

The operator creates a packet under `harness/reviewers/packets/` from
`harness/templates/EXTERNAL_REVIEW_PACKET.md`. The packet should include only
the minimum evidence needed for the review.

## Ledger

Append review outcomes to `harness/reviewers/REVIEW_LEDGER.jsonl`.

Each ledger entry should include:

- review id;
- reviewer adapter or human reviewer;
- task/phase;
- axes;
- evidence paths;
- verdict;
- material findings;
- operator disposition;
- follow-up task id when needed.

## Authority Boundary

External reviewer output must not directly change:

- feature state;
- production code;
- governance rules;
- publication status;
- cloud or connector permissions.

Operators decide how to route review evidence through the normal task,
evaluation, human-review, and regulation-evolution gates.
