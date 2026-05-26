# Software Feedback Policy

Status: generated policy for development and coding workstreams

Use this file when the project goal or task slice includes software, web, app,
API, game, UI, automation, data pipeline, or other code-producing work.

When available, run the executable evidence collector instead of relying on a
freeform evaluator note:

```sh
python3 scripts/harnessctl.py software-feedback --task-id TASK --lint-command "..." --smoke-command "..."
```

## Required Feedback Axes

Development feedback is not limited to reading code output.

For each software slice, evaluation should cover:

- source or artifact inspection
- lint, type check, formatter check, or equivalent static command
- unit, integration, or domain regression test when available
- runtime smoke of the smallest reproducible path
- Playwright or equivalent browser/device verification when the artifact is
  user-facing or interactive
- UI/UX/layout review for overflow, responsiveness, visible hierarchy,
  interaction clarity, accessibility, and awkwardness versus the task context
- context-chain review: whether the implementation still matches the approved
  PRD, anti-PRD, worker brief, owned paths, and no-touch paths

## Playwright Rule

If a task produces or changes a web UI, browser workflow, local HTML report, or
interactive surface, the evaluator must either:

- run Playwright or an equivalent browser/device check and attach screenshots,
  traces, console errors, and viewport notes; or
- record `NOT-RUN` with the concrete reason, risk, and next command.

Visual review without a real browser/device check is not enough for final
closure when the task is interactive.

## Evidence Packet

A completed software work packet should include:

- commands run
- command results
- screenshots or trace path when UI is involved
- console/runtime errors
- relevant changed files
- failed or skipped checks
- evaluator verdict
- feedback routed back to planning, design, production, or evaluation

## Failure Routing

- lint or type failure returns to production
- failing runtime or browser workflow returns to production
- weak UI/UX/layout returns to design before production continues
- missing spec or unclear acceptance criteria returns to planning
- repeated failure becomes a regression fixture when it can be checked locally
