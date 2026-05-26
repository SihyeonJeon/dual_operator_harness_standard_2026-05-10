# Cross Feedback Loop

Status: generated policy for complementary agent feedback

The harness keeps topology adaptive, but feedback discipline is mandatory.
Any material artifact must pass through an independent feedback path before
operator closure unless the task records why cross-feedback is not applicable.

## Loop

1. Producer creates an artifact from the approved brief.
2. Reviewer checks the artifact against acceptance criteria, current research,
   context boundaries, no-touch paths, and domain quality gates.
3. Reviewer records `PASS`, `WARN`, `FAIL`, or `NOT-RUN`.
4. `FAIL` routes to exactly one upstream owner: planning, design, production,
   evaluation, context update, governance update, or human decision.
5. `WARN` requires risk acceptance by the operator or human before closure.
6. Material dissent is preserved, not rewritten as consensus.

## Independence Rules

- The reviewer must not be the same worker session that produced the artifact
  unless the operator records why no independent reviewer exists.
- Cross-vendor or cross-model review is preferred when the claim is subjective,
  externally visible, high-risk, benchmark-like, or strategically important.
- Do not forward full transcripts. Use task packets, evidence paths, and bounded
  context packs.

## Gate

Operator closure needs one of:

- recorded cross-feedback with `PASS`;
- recorded cross-feedback with accepted `WARN`;
- explicit `NOT-RUN` rationale with risk and owner;
- trivial/internal task rationale.

Use:

```sh
python3 scripts/harnessctl.py cross-feedback --task-id TASK --producer A --reviewer B --verdict PASS --feedback "..."
```

This helper records feedback evidence. It does not force consensus.
