# Project Agent Entry

Purpose: route any capable coding agent into the project-local harness without
depending on hidden chat memory.

Project goal:

```text
{{PROJECT_GOAL}}
```

## Startup Workflow

Before doing project work:

1. Confirm the working directory is the project root.
2. Run `./init.sh` if it exists and the user has not forbidden local checks.
3. Read `feature_list.json`, `progress.md`, and `session-handoff.md`.
4. Read `harness/shared/ROLE_FILE_INDEX.md`.
5. Read `harness/shared/ACTIVE_SNAPSHOT.md`.
6. Read `harness/shared/PROJECT_PROFILE.json`.
7. Read `harness/shared/WORKSTREAM_PROFILE.json`.
8. Read `harness/shared/OPERATOR_SESSION_REGISTRY.json`.
9. Read `harness/shared/OBSERVABILITY.md` and
   `harness/shared/VISUALIZATION_SPEC_POLICY.md`.
10. Read `harness/shared/RECORDS_POLICY.md` and
   `harness/shared/CONTEXT_PRESSURE.md`.
11. Read `harness/shared/AGENT_COMMUNICATION.md`.
12. Read `harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md`.
13. Read `harness/shared/CROSS_FEEDBACK_LOOP.md`.
14. Read `harness/shared/CONCEPT_TRANSLATION_POLICY.md`.
15. Read the role file that matches the user's instruction or the current agent
   surface.

If the user says only "you are operator", "act as operator", or equivalent,
become the fixed operator for the current agent surface:

- Codex-compatible agents load `harness/operators/codex/AGENT.md`.
  This root `AGENTS.md` is the Codex-compatible entry surface.
- Claude Code-compatible agents load `harness/operators/claude-code/AGENT.md`.
  Claude Code adapters under `.claude/` are generated views and must preserve
  the same file-backed shared memory.
- If the surface is unclear, load both operator role summaries, pick the closest
  surface, record the choice in `progress.md`, and continue only through
  reversible harness/orchestration work.

## Operating Rules

- Treat `harness/shared/` and task artifacts as canonical memory.
- Treat team `TEAM_CONTEXT.md` files as shared worker-team memory.
- Treat private chat memory as advisory only.
- Treat Claude Code adapters, Codex session context, MCP transcripts, and
  plugin summaries as advisory until written into canonical harness files.
- Treat private overlay connector responses, mobile/chat approvals, and long raw
  logs as non-canonical until an operator summarizes the decision or risk into
  canonical internal files.
- Preserve dual-operator parity: do not force consensus, erase dissent, or let
  one operator's runtime adapter outrank the other operator.
- Preserve context accumulation and shared feedback loops: update
  `progress.md`, `session-handoff.md`, task artifacts, `harness/shared/MEMORY.md`,
  `harness/shared/FAILURE_LEDGER.md`, and `harness/shared/RULE_CHANGE_LOG.md`
  when evidence requires it.
- Work one feature or sharp/deep slice at a time.
- For dashboards, timelines, graphs, status HTML views, manager views, live
  status UI, or state visualizations, create or approve a task-local
  `VISUALIZATION_SPEC.md` before production work.
- Use `python3 scripts/harnessctl.py event` and
  `python3 scripts/harnessctl.py report` when available to expose progress as
  compiled local evidence. The generated HTML is not canonical memory.
- Use `python3 scripts/harnessctl.py eval-run` for local scaffold/governance
  regression checks when relevant. It does not run arbitrary shell commands or
  perform network writes.
- Use bounded context packs and `harness/shared/CONTEXT_PRESSURE.md` before
  delegating to worker sessions, especially lower-tier or part-owner sessions.
- Use `harness/shared/AGENT_COMMUNICATION.md` to pass concise task packets and
  evidence paths instead of forwarding long transcripts between agents.
- Use `harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md` before approving the
  overall plan when the goal depends on current market, tools, comparables,
  standards, regulations, or public facts. Prefer
  `python3 scripts/harnessctl.py current-research` to record the evidence.
- Use `harness/shared/CROSS_FEEDBACK_LOOP.md` before operator closure for
  material artifacts. Prefer `python3 scripts/harnessctl.py cross-feedback` to
  record independent feedback without forcing consensus.
- Use `harness/shared/CONCEPT_TRANSLATION_POLICY.md` for user-facing output.
  Treat the user's wording as concept, not artifact copy, unless literal text
  was explicitly requested. Ordinary domain terms remain allowed when they read
  naturally in the artifact.
- Prefer `python3 scripts/harnessctl.py context-pack`, `worker-brief`,
  `model-route`, `task-packet`, `current-research`, and `cross-feedback` for
  repeatable routing, planning evidence, feedback, and handoff mechanics when
  the generated command surface is available.
- For software, web, app, API, game, automation, or UI work, require the
  evaluation packet to follow `harness/shared/SOFTWARE_FEEDBACK_POLICY.md`.
  Prefer `python3 scripts/harnessctl.py software-feedback` when project
  commands are known.
- Do not mark any feature or task complete without executable evidence or an
  explicit `NOT-RUN` entry with risk.
- Do not start production work until H0 and H1 bootstrap smoke are resolved or
  explicitly blocked with operator/human decision.

## Feature State

`feature_list.json` is the machine-readable scope source of truth. Each feature
must have behavior, verification, state, and evidence. A feature may move to
`passing` only after its verification path succeeds and evidence is recorded.
Verification commands in this file must be portable. Put local user paths,
package-cache paths, `NODE_PATH` workarounds, credentials, and temp-only
reproduction commands in task evidence files instead.

## Session End

Before ending a session:

1. Update `progress.md`.
2. Update `session-handoff.md`.
3. Update `feature_list.json` only when a state transition has evidence.
4. Update the current task packet and worker registry when phase ownership or
   closure changed.
5. Record blockers, `WARN`, and `NOT-RUN` gates.
6. Append a material event with `python3 scripts/harnessctl.py event` when the
   command is available.
7. Regenerate `harness/reports/status.html` with
   `python3 scripts/harnessctl.py report` when human visibility or local
   evidence history matters.
8. Run or record the relevant `harness/evals/` suite when scaffold or
   governance regression matters.
9. Leave a clean restart path through `./init.sh`.
