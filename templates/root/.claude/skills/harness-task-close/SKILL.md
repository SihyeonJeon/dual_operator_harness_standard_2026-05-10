---
name: harness-task-close
description: Close or block a harness task with evidence, clean state, shared context updates, and regulation review.
---

# Harness Task Closure Skill

Closure must preserve canonical project records and the records policy boundary.

Before any operator closure:

1. Confirm the task blueprint and worker brief exist or record why they do not.
2. Confirm evaluation report verdict is `PASS`, `WARN`, `FAIL`, or `NOT-RUN`.
3. If visualization exists, confirm `VISUALIZATION_SPEC.md` is approved or the
   not-required rationale is recorded.
4. Confirm root `feature_list.json` transition has evidence before `passing`.
5. Update `progress.md` and `session-handoff.md`.
6. Summarize durable findings into `harness/shared/MEMORY.md` only when they are
   not derivable from repository files.
7. Update the relevant `harness/teams/*/TEAM_CONTEXT.md` when team-level
   practice changed.
8. Run or record `python3 scripts/validate_harness.py .`.
9. Run or record `python3 scripts/harnessctl.py report` when human visibility or
   local evidence review is part of the task.
10. Run or record `python3 scripts/harnessctl.py eval-run` when scaffold,
    governance, or project-local golden checks are relevant.
11. Run or record `python3 scripts/harnessctl.py viz-export --backend
    local_file` when a visualization backend adapter or event payload is part of
    the task.
12. Check `harness/shared/RECORDS_POLICY.md` and
    `harness/shared/CONTEXT_PRESSURE.md` before closing long, reopened,
    multi-team, or private-overlay-adjacent work.
13. Apply `harness/shared/REGULATION_EVOLUTION.md` and record no-change when no
   rule update is warranted.

Do not close work from private chat claims alone.
