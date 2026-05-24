# Bootstrap Contract

Purpose: create a complete project-local harness from the kit and the user's
project goal.

Minimum inputs:

1. this kit;
2. `PROJECT_GOAL`: what the project is trying to accomplish.

Optional input:

- `PRIOR_INFO_AND_CONSTRAINTS`: known facts, constraints, tools, budget, risks,
  preferences, forbidden shortcuts, and operating requirements.

The bootstrap agent may create harness files. It is not one of the fixed
operators and it must not start production work for the target project.
It must not design the project-specific strategy needed to achieve the target
goal unless the inputs explicitly specify that strategy.

## Required Behavior

1. Create an intake packet from the two inputs using
   `templates/input/INPUT_PACKET.md`.
2. Derive a first `PROJECT_PROFILE` from the project goal, with missing fields
   set to `UNKNOWN`.
3. Choose the smallest adoption mode that fits the stated risk:
   `lite`, `standard`, or `full`.
4. Select domain packs only when the two inputs justify them.
5. Scaffold `harness/` from `templates/harness/`.
6. Create root restart and operator-entry files from `templates/root/`:
   - `README.md`
   - `AGENTS.md`
   - `CLAUDE.md`
   - `init.sh`
   - `feature_list.json`
   - `progress.md`
   - `session-handoff.md`
   - `scripts/implementer_hooks.py`
   - `scripts/harnessctl.py`
   - `.claude/` Claude Code adapters
7. Create or copy the required JSON contracts:
   - `harness/shared/HARNESS_CONFIG.json`
   - `harness/shared/PROJECT_PROFILE.json`
   - `harness/shared/CAPABILITY_REGISTRY.json`
   - `harness/shared/TOOL_REGISTRY.json`
   - `harness/shared/PERMISSION_POLICY.json`
   - `harness/shared/MCP_TRUST.json`
8. Create the operator manuals under:
   - `harness/operators/claude-code/AGENT.md`
   - `harness/operators/codex/AGENT.md`
9. Create session and routing controls:
   - `harness/shared/OPERATOR_SESSION_REGISTRY.json`
   - `harness/shared/WORKER_SESSION_REGISTRY.json`
   - `harness/shared/CONTEXT_LOADING.md`
   - `harness/shared/WORKSPACE_LAYOUT.md`
   - `harness/shared/MEMORY_BACKEND.json`
   - `harness/shared/MODEL_ROUTING.json`
   - `harness/shared/TEAM_TOPOLOGY.md`
   - `harness/shared/WORKSTREAM_PROFILE.json`
   - `harness/shared/DUAL_OPERATOR_PROTOCOL.md`
   - `harness/shared/PART_OWNERSHIP.md`
   - `harness/shared/PLUGIN_ROUTING.json`
   - `harness/shared/QUALITY_GATES.md`
   - `harness/shared/VISUALIZATION_SPEC_POLICY.md`
   - `harness/shared/CHANNEL_RECORDS.md`
   - `harness/shared/CONTEXT_PRESSURE.md`
   - `harness/shared/COUNCIL_MCP.md`
   - `harness/shared/ROLE_FILE_INDEX.md`
   - `harness/shared/REGULATION_EVOLUTION.md`
   - `harness/shared/SESSION_CONTINUITY.md`
   - `harness/shared/SHARP_DEEP_EXECUTION.md`
10. Mark every runtime, model, MCP server, cloud lane, hook, browser/computer-use
   surface, and vendor-specific feature as `UNVERIFIED` until project-local
   smoke evidence exists.
11. Create `harness/tasks/H0-LOCAL-SMOKE/BLUEPRINT.md`.
12. Create `harness/tasks/H1-BOOTSTRAP-SMOKE/BLUEPRINT.md`.
13. Create `harness/tasks/F0-PLANNING-RUNWAY/BLUEPRINT.md`.
14. Create `harness/SCAFFOLDING_REPORT.md` and
    `harness/SCAFFOLDING_CHECKLIST.md`.
15. Create `harness/IMPLEMENTER_HANDOFF.md`.
16. Create `harness/IMPLEMENTER_HOOKS.md` and
    `harness/IMPLEMENTER_HOOKS_RUN.json`.
17. Create project-root `guide_for_human.md`.
18. Create project-root bilingual `README.md`.
19. Create `harness/runtime/OFFLINE_OPERATION.md`.
20. Create `harness/runtime/REMOTE_OPERATION_POLICY.md`.
21. Create `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md`.
22. Create `harness/runtime/RUNNERS/` runner descriptors for local, Claude
    Code, Codex, and remote/cloud runners. Every runner starts
    `UNVERIFIED` and network-denied by default.
23. Create active/archive workspace placeholders under `harness/tasks/active/`
    and `harness/tasks/archive/`.
24. Create external-interface, reviewer, MCP export, and spec automation
    scaffolds:
    - `harness/broadcast/BROADCAST_POLICY.md`
    - `harness/broadcast/DRAFT_QUEUE.md`
    - `harness/broadcast/PUBLISHED_LEDGER.jsonl`
    - `harness/broadcast/connectors/`
    - `harness/reviewers/REVIEWER_POLICY.md`
    - `harness/reviewers/REVIEW_LEDGER.jsonl`
    - `harness/reviewers/adapters/`
    - `harness/mcp_server/`
    - `harness/spec/INPUT_PACKET.md`
    - `harness/spec/SPEC_AUTOMATION_POLICY.md`
    - `harness/spec/PRD_DRAFT.md`
    - `harness/spec/ANTI_PRD.md`
25. Create visualization backend descriptors and adapter brief:
    - `harness/viz/README.md`
    - `harness/viz/VIZ_BACKENDS.json`
    - `harness/viz/adapters/local_file.json`
    - `harness/viz/adapters/WORKER_ADAPTER_BRIEF.md`
26. Create dependency-free eval scaffold:
    - `harness/evals/README.md`
    - `harness/evals/golden_suite.json`
    - `harness/evals/results/.gitkeep`
    - `schemas/eval-suite.schema.json`
27. Copy or generate local project validation scripts and schemas so the
    generated harness can be validated after this kit is moved or deleted.
28. Copy or generate `scripts/harnessctl.py` so the generated project can log
    events, compile local static HTML status reports, export local viz payloads,
    check visualization specs, run dependency-free eval suites, create broadcast
    drafts, and create external review packets without the standard kit
    directory.
29. Run and record implementer scaffold lifecycle hooks:
    `PreScaffoldGoalIntake`, `IntakeValidate`, `ProfileDeriveAudit`,
    `AdoptionModeSelect`, `DomainPackSelect`, `PostScaffoldValidation`, and
    `HandoffComplete`.
30. Run `scripts/validate_harness.py <target-project>` or perform the same
    checks manually.

## Ambiguity Handling

Do not resolve material ambiguity silently. Ask the user when the answer changes:

- project scope or non-goals;
- target user/audience;
- risk tier or adoption mode;
- budget or cloud/API usage;
- irreversible actions;
- legal, medical, financial, HR, public-sector, or safety implications;
- production write/merge/deploy authority;
- secret or private-data access;
- human taste decisions;
- domain canon or factual claims.

If the ambiguity is not material for scaffolding, write `UNKNOWN` and add it to
`harness/shared/ACTIVE_SNAPSHOT.md` under `Open Questions`.

## Completion Bar

Bootstrap is complete only when:

- the implementer has not become a fixed operator;
- scaffolding report and checklist exist;
- required files exist;
- schemas are present;
- root restart files exist and make "you are operator" sufficient to enter the
  fixed-operator flow;
- Claude Code adapters exist under `.claude/` and route back to file-backed
  shared memory rather than separate private memory;
- doctor/linter passes or records explicit `WARN`/`NOT-RUN` items;
- H0 local smoke is ready but not falsely marked complete;
- H1 bootstrap restart smoke is ready but not falsely marked complete;
- operators are instructed to ask the user about material ambiguity.
- both operators are configured as fixed persistent sessions;
- both operators share `harness/shared/` and task artifacts as canonical memory;
- dual-operator protocol forbids forced consensus and preserves dissent;
- Codex remains an equal fixed operator; Claude Code adapters are generated
  views, not operator hierarchy;
- worker teams preserve their shared memory in team `TEAM_CONTEXT.md` files and
  task artifacts;
- model routing keeps operators on highest verified model/effort while workers
  use the lowest verified tier that satisfies task gates;
- worker session registry preserves part-owner sessions for the same part and
  prevents unrelated reuse;
- plugin routing caps context-saving plugins at four and includes caveman as the
  preferred compression slot when verified;
- visualization spec policy exists and blocks dashboard, timeline, graph, HTML
  external evidence, manager-view, live status UI, and state-visualization production
  until a task-local spec is approved or explicitly marked not required;
- visualization backend policy exists, `local_file` is the only verified local
  backend, and external viz backends remain `UNVERIFIED` until human selection,
  bounded policy, credential lifecycle, and smoke evidence exist;
- local `scripts/harnessctl.py` exists for validation, event logging, static
  HTML report compilation, local viz export, visualization spec checks,
  dependency-free eval suite execution, broadcast draft creation, and external
  review packet creation;
- `harness/evals/golden_suite.json` exists and can be run with
  `python3 scripts/harnessctl.py eval-run` without network writes or arbitrary
  command execution;
- local `scripts/implementer_hooks.py` exists and
  `IMPLEMENTER_HOOKS_RUN.json` records the full scaffold lifecycle hook status;
- project-root `README.md` includes Korean and English sections for GitHub
  upload;
- council MCP is registered as advisory only and requires project-root smoke;
- workstream profile records initial goal-shaped team topology without making
  production strategy decisions;
- worker session registry exists so returning tasks can resume prior worker
  instances when safe;
- context loading is split into lightweight always-load and on-demand reference
  layers.
- role and skill files are present for both fixed operators and every team;
- planning is instructed to run a planning runway, validate candidate slices,
  and approve one sharp/deep slice before production work;
- task closure includes regulation review before advancing to the next slice.
- `SCAFFOLDING_REPORT.md` records inputs, unknowns, validation result, and
  handoff state.
- `IMPLEMENTER_HANDOFF.md` states that the implementer role is complete and
  that operators, not the implementer, own future project operation.
- `guide_for_human.md` exists and lists safe commands, required human
  decisions, fixed session placeholders, and denied actions.
- `runtime/OFFLINE_OPERATION.md` explains local/offline operation, no-network
  limits, and any cloud/always-on gap.
- `runtime/REMOTE_OPERATION_POLICY.md` denies unrestricted remote terminal,
  cloud, mobile, chat, and always-on operation until a bounded connector,
  approval channel, audit path, budget, kill procedure, and smoke evidence are
  recorded.
- `runtime/CLOUD_VIZ_OPERATOR_GUIDE.md` lists human decisions for cloud lane
  selection, viz backend selection, credentials, bounded policy, smoke evidence,
  and adapter activation.
- generated project validation does not require the standard kit directory to
  remain inside the target project.
- `CHANNEL_RECORDS.md` separates internal canonical records from external
  broadcast/reviewer/channel records.
- `CONTEXT_PRESSURE.md` defines context budget, compaction triggers, context
  pack rules, plugin caps, and part-owner isolation.
- `BROADCAST_POLICY.md`, `DRAFT_QUEUE.md`, broadcast connector descriptors, and
  `PUBLISHED_LEDGER.jsonl` exist. Broadcast is draft-only until human approval
  and connector smoke evidence exist.
- `REVIEWER_POLICY.md`, reviewer adapters, and `REVIEW_LEDGER.jsonl` exist.
  External reviewer output is evidence, not authority.
- `mcp_server/` exists as a read-only `UNVERIFIED` context export with
  `search_past_decisions`, `get_capability_status`, `get_current_task`, and
  `list_open_questions`.
- `SPEC_AUTOMATION_POLICY.md`, `PRD_DRAFT.md`, and `ANTI_PRD.md` exist so goal
  intake goes through planning/spec/evaluator gates before sharp/deep production.
