# Channel Records

Purpose: keep internal context and external-channel records separate so the
harness can accumulate useful memory without turning drafts, chats, social
posts, or reviewer comments into hidden authority.

## Internal Canonical Records

The following are canonical internal project records:

- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `harness/shared/`
- `harness/tasks/`
- `harness/teams/*/TEAM_CONTEXT.md`
- `harness/events/events.jsonl`
- approved evaluation and human-review packets

Operators and workers must update these records when evidence changes the
project state, rules, risk, or next action.

## External Channel Records

The following are external-channel or outward-facing records:

- `harness/broadcast/`
- `harness/reviewers/`
- connector dry-runs, previews, drafts, API responses, social metrics, comments,
  public posts, release pages, blog entries, chat approvals, and mobile
  approvals

External records are not canonical memory until an operator summarizes the
relevant decision, evidence, or outcome back into the internal records.

## Separation Rules

- Internal context may generate external drafts.
- External feedback may inform internal decisions only after explicit summary
  and disposition.
- Hidden external conversations do not override file-backed harness memory.
- Public-facing artifacts must cite internal evidence paths when practical.
- External publication must not expose private internal memory.
- Public-facing artifacts must not paste raw internal transcripts, full diffs,
  credential traces, connector responses, or private local paths. Use concise
  evidence references, screenshots, metrics, and redacted summaries.
- Reviewer findings remain evidence, not authority.

## Hook Expectations

SessionEnd, Stop, TaskCompleted, broadcast, reviewer, and remote/mobile hooks
should record two separate things when applicable:

- internal event or decision record;
- external draft, approval, review, or publication record.

If only one of the two records exists, the missing side is a `NOT-RUN` or
`BLOCKED` gate, not an implicit pass.
