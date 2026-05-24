# Dual Operator Harness Standard

Status: normative scaffold spec, 2026-05-10.

This standard creates a file-backed governance and orchestration harness around
any project. It is not a standalone agent runtime.

## Required Inputs

The scaffold MUST be creatable from two minimum inputs:

- this kit;
- project goal.

Unknown facts MUST be represented as `UNKNOWN`, not invented.
Prior information and constraints MAY be supplied. If absent, they are recorded
as `UNKNOWN`.

## Domain-Free Rule

This kit is topic-neutral. It must be usable for software, research, writing,
design, operations, education, media, business, internal tooling, and other
project types. A generated harness may load a domain pack only when the inputs
or later human-approved operator work justify it.

## Implementer Rules

- The harness implementer is a scaffolding actor, not a fixed operator.
- The implementer may create harness structure and run validation.
- The implementer MUST NOT start target-project production work.
- The implementer MUST NOT design, optimize, or execute the domain strategy
  required to accomplish the target project's eventual objective.
  Objective execution belongs to fixed operators and approved workers after
  handoff.
- The implementer MUST keep domain-specific choices, topic tracks, platform or
  tool choices, vendors, budgets, public claims, publication/distribution
  channels, and runtime activation as `UNKNOWN` unless the two inputs
  explicitly provide them.
- The implementer MUST leave `SCAFFOLDING_REPORT.md` and
  `SCAFFOLDING_CHECKLIST.md`.
- The implementer MUST leave `harness/IMPLEMENTER_HANDOFF.md`.
- The implementer MUST run and record scaffold lifecycle hooks in
  `harness/IMPLEMENTER_HOOKS_RUN.json`.
- The implementer MUST leave a project-root `guide_for_human.md` describing
  what the human must decide next.
- The implementer MUST hand off to the fixed operators after scaffold
  validation and H0 preparation.

## Required Architecture

A generated harness MUST include:

- project-root `AGENTS.md`
- project-root `README.md`
- project-root `CLAUDE.md`
- project-root `init.sh`
- project-root `feature_list.json`
- project-root `progress.md`
- project-root `session-handoff.md`
- project-root `guide_for_human.md`
- project-root `scripts/implementer_hooks.py`
- project-root `scripts/harnessctl.py`
- project-root `.claude/settings.json`
- project-root `.claude/README.md`
- project-root `.claude/hooks/session_start_context.py`
- project-root `.claude/hooks/pre_tool_use_guard.py`
- project-root `.claude/hooks/stop_clean_state.py`
- project-root `.claude/hooks/task_completed_gate.py`
- project-root `.claude/agents/harness-planner.md`
- project-root `.claude/agents/harness-production-worker.md`
- project-root `.claude/agents/harness-evaluator.md`
- project-root `.claude/agents/harness-operator-reviewer.md`
- project-root `.claude/skills/harness-operator/SKILL.md`
- project-root `.claude/skills/harness-task-close/SKILL.md`
- `harness/SCAFFOLDING_REPORT.md`
- `harness/SCAFFOLDING_CHECKLIST.md`
- `harness/IMPLEMENTER_HANDOFF.md`
- `harness/IMPLEMENTER_HOOKS.md`
- `harness/IMPLEMENTER_HOOKS_RUN.json`
- `harness/shared/PROJECT_PROFILE.json`
- `harness/shared/HARNESS_CONFIG.json`
- `harness/shared/ACTIVE_SNAPSHOT.md`
- `harness/shared/CAPABILITY_REGISTRY.json`
- `harness/shared/TOOL_REGISTRY.json`
- `harness/shared/PERMISSION_POLICY.json`
- `harness/shared/MCP_TRUST.json`
- `harness/shared/COUNCIL_MCP.md`
- `harness/shared/CONTEXT.md`
- `harness/shared/MEMORY.md`
- `harness/shared/FAILURE_LEDGER.md`
- `harness/shared/RULE_CHANGE_LOG.md`
- `harness/shared/IDENTITY.md`
- `harness/shared/CREDENTIAL_LIFECYCLE.md`
- `harness/shared/INCIDENT_RESPONSE.md`
- `harness/shared/OPERATOR_SESSION_REGISTRY.json`
- `harness/shared/WORKER_SESSION_REGISTRY.json`
- `harness/shared/ROLE_FILE_INDEX.md`
- `harness/shared/REGULATION_EVOLUTION.md`
- `harness/shared/SESSION_CONTINUITY.md`
- `harness/shared/SHARP_DEEP_EXECUTION.md`
- `harness/shared/WORKSPACE_LAYOUT.md`
- `harness/shared/MEMORY_BACKEND.json`
- `harness/shared/WORKSTREAM_PROFILE.json`
- `harness/shared/DUAL_OPERATOR_PROTOCOL.md`
- `harness/shared/PART_OWNERSHIP.md`
- `harness/shared/PLUGIN_ROUTING.json`
- `harness/shared/QUALITY_GATES.md`
- `harness/shared/VISUALIZATION_SPEC_POLICY.md`
- `harness/shared/CHANNEL_RECORDS.md`
- `harness/shared/CONTEXT_PRESSURE.md`
- `harness/shared/OBSERVABILITY.md`
- `harness/shared/CLEAN_STATE.md`
- `harness/operators/claude-code/AGENT.md`
- `harness/operators/claude-code/SKILLS.md`
- `harness/operators/codex/AGENT.md`
- `harness/operators/codex/SKILLS.md`
- `harness/teams/planning/AGENT.md`
- `harness/teams/planning/TEAM_CONTEXT.md`
- `harness/teams/planning/SKILLS.md`
- `harness/teams/design/AGENT.md`
- `harness/teams/design/TEAM_CONTEXT.md`
- `harness/teams/design/SKILLS.md`
- `harness/teams/coding/AGENT.md`
- `harness/teams/coding/TEAM_CONTEXT.md`
- `harness/teams/coding/SKILLS.md`
- `harness/teams/evaluation/AGENT.md`
- `harness/teams/evaluation/TEAM_CONTEXT.md`
- `harness/teams/evaluation/SKILLS.md`
- `harness/templates/TASK_BLUEPRINT.md`
- `harness/templates/WORKER_BRIEF.json`
- `harness/templates/EVALUATION_REPORT.md`
- `harness/templates/VISUALIZATION_SPEC.md`
- `harness/templates/BROADCAST_DRAFT.md`
- `harness/templates/EXTERNAL_REVIEW_PACKET.md`
- `harness/spec/INPUT_PACKET.md`
- `harness/spec/SPEC_AUTOMATION_POLICY.md`
- `harness/spec/PRD_DRAFT.md`
- `harness/spec/ANTI_PRD.md`
- `harness/broadcast/BROADCAST_POLICY.md`
- `harness/broadcast/DRAFT_QUEUE.md`
- `harness/broadcast/PUBLISHED_LEDGER.jsonl`
- `harness/broadcast/connectors/generic_publication.example.json`
- `harness/broadcast/connectors/manual_export.example.json`
- `harness/reviewers/REVIEWER_POLICY.md`
- `harness/reviewers/REVIEW_LEDGER.jsonl`
- `harness/reviewers/adapters/ai_reviewer.example.json`
- `harness/reviewers/adapters/human_reviewer.json`
- `harness/mcp_server/README.md`
- `harness/mcp_server/MANIFEST.json`
- `harness/mcp_server/server.py`
- `harness/tasks/H0-LOCAL-SMOKE/BLUEPRINT.md`
- `harness/tasks/H1-BOOTSTRAP-SMOKE/BLUEPRINT.md`
- `harness/tasks/F0-PLANNING-RUNWAY/BLUEPRINT.md`
- `harness/tasks/active/.gitkeep`
- `harness/tasks/archive/.gitkeep`
- `harness/events/events.jsonl`
- `harness/reports/README.md`
- `harness/evals/README.md`
- `harness/evals/golden_suite.json`
- `harness/evals/results/.gitkeep`
- `harness/runtime/OFFLINE_OPERATION.md`
- `harness/runtime/REMOTE_OPERATION_POLICY.md`
- `harness/runtime/RUNNERS/local_runner.json`
- `harness/runtime/RUNNERS/claude_code_runner.json`
- `harness/runtime/RUNNERS/codex_runner.json`
- `harness/runtime/RUNNERS/remote_runner.json`
- `harness/runtime/RUNNERS/cloud_runner.example.json`
- `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md`
- `harness/viz/README.md`
- `harness/viz/VIZ_BACKENDS.json`
- `harness/viz/adapters/local_file.json`
- `harness/viz/adapters/WORKER_ADAPTER_BRIEF.md`

## Operator Rules

- The human is final authority.
- Fixed operators are equal peers.
- The two fixed operators MUST always use persistent fixed sessions.
- Dual-operator meetings MUST NOT force consensus or erase dissent.
- Material disagreement MUST be recorded and presented to the human when
  evidence does not settle it.
- Fixed operators SHOULD use the highest verified model class and highest
  verified reasoning effort available under the user's approved plan/budget.
- Fixed operators do not perform production implementation work unless the
  human explicitly activates a one-incident fallback.
- Operators may write governance, task, context, and evidence artifacts.
- Operators MUST ask the user when a material decision is ambiguous.
- Operators MUST NOT treat hidden chat memory as authority over file-backed
  context.
- Operators MUST share the same `harness/shared/` files and current task
  artifacts as canonical memory, regardless of which operator is currently
  talking with the user.
- Claude Code adapters, Codex private session context, plugin summaries, and MCP
  transcripts are advisory until summarized into canonical harness files.
- Raw command transcripts and full patch diffs are internal evidence, not public
  records. Public or human-facing summaries SHOULD use evidence paths,
  screenshots, counts, verdicts, and redacted summaries.
- Broadcast drafts, publication ledgers, social responses, reviewer packets,
  reviewer outputs, chat/mobile approvals, and external connector responses are
  external-channel records. They are not canonical memory until an operator
  summarizes and disposes the relevant evidence in internal records.
- Operators receive completed work packets after planning, execution,
  debugging, evaluation, and cross-check. They do not micromanage coding or
  production work in the middle of the loop.
- Operators SHOULD use `scripts/harnessctl.py` for local validation, event
  logging, dependency-free eval suites, local viz export, visualization spec
  checks, broadcast draft creation, external review packet creation, and static
  HTML status reports when available. The generated reports and external drafts
  are compiled views or channel records, not canonical memory.
- Visualization and diagram information architecture is Claude-owned. Codex or
  another deterministic worker MAY implement static report rendering and
  `events.jsonl` adapter plumbing after task-local Claude visualization review.
- Generated bitmap image requests are Codex-owned by default. Product photos,
  mock photographs, hero images, raster illustrations, and image-generation
  variants SHOULD route through Codex image generation, then be reviewed for
  fit, publication rights, and evidence paths before production use.
- Non-local visualization backends MUST remain `UNVERIFIED` until human backend
  selection, bounded policy, credential lifecycle records, smoke evidence, and
  operator review exist.
- Operators MAY create external-facing drafts after task closure, but automatic
  external publication is denied. Publication requires human approval, redaction,
  connector smoke evidence, and a publication ledger entry.
- Operators MAY request external AI or human review at phase boundaries.
  Reviewer output is evidence, not authority, and must not force consensus or
  bypass normal evaluation/human-review gates.
- Operators may modify operator/team `AGENT.md`, `SKILLS.md`, shared policies,
  templates, schemas, and linter rules as governance work based on documented
  success/failure records, according to `REGULATION_EVOLUTION.md`.

## Human Guide Rule

Every generated harness MUST include project-root `guide_for_human.md`. It must
state:

- fixed operator session names or placeholders;
- what the human must decide before operation;
- safe local commands;
- local HTML report command and visualization spec check command;
- local viz export command and external viz backend approval requirements;
- denied actions until approval and smoke evidence exist;
- handoff status from implementer to operators;
- whether cloud, mobile, or offline operation is designed, deployed, or
  unverified.

The guide is a human control surface. It must not approve external actions by
itself.

Every generated project MUST include a project-root `README.md` with both Korean
and English sections. It must explain the project goal, startup commands,
operator entry phrase, canonical-memory rule, visualization spec gate, and
remote/mobile/cloud denial until approved policy and smoke evidence exist.

## Root Entry Rule

Every generated project MUST include root `AGENTS.md` and `init.sh` so a fresh
agent session can start without hidden chat context. If the user says only
"you are operator", the root entrypoint MUST route the current agent into the
matching fixed-operator role and require it to load shared context, feature
state, progress, and the current task artifact before acting.

`feature_list.json` is the root scope state primitive. Each feature entry MUST
include behavior, verification, state, and evidence. A feature MUST NOT move to
`passing` without successful verification evidence or an explicit human/operator
decision recorded as risk.

Feature verification commands MUST be portable. Machine-specific absolute paths,
package-cache paths, `NODE_PATH` workarounds, credential paths, and temporary
local reproduction commands belong in task evidence files, not in root
`feature_list.json`.

After a material gate, root feature state, progress log, session handoff, worker
registry, current task packet, event log, status report, and viz export MUST
either agree or record a blocker before the session is considered clean.

## Claude Code Adapter Rule

Generated Claude Code adapters under `.claude/` are executable views over the
file-backed harness. They MUST NOT create a competing memory authority.

- `.claude/settings.json` SHOULD install SessionStart, PreToolUse,
  TaskCompleted, and Stop hooks that point back to root state and
  `harness/shared/`.
- `.claude/agents/` project subagents SHOULD map to planning, production,
  evaluation, and advisory operator-review lanes.
- `.claude/skills/` SHOULD provide operator-entry and task-closure skills.
- Claude Code agent teams, hooks, subagents, and skills remain `UNVERIFIED`
  capabilities until smoked in the target runtime.
- Team agents MUST use team `TEAM_CONTEXT.md` files as shared team memory.

## Offline And Continuity Rules

The generated harness MUST be locally usable without the original standard kit.
At minimum, validation scripts required for the generated project must be copied
or generated into the target project.

The generated harness MUST include an offline/local-continuity note explaining:

- which functions work with no network;
- which functions require network, cloud, credentials, or external platforms;
- what cannot run if the local machine is powered off;
- what additional approved cloud runner would be required for always-on work;
- how remote terminal, mobile approval, chat connector, and always-on lanes are
  denied until bounded-runner policy, approval channel, audit log, budget, kill
  procedure, and smoke evidence exist;
- how file-backed memory and approval packets are used when no remote service
  is available.

Offline-capable does not mean unsupervised external action. Network writes,
external communications, payments, contracts, postings, submissions,
browser/computer-use, secrets, and cloud execution remain denied until
separately approved and smoke-tested.

H1 bootstrap restart smoke MUST prove that root entry files, local validation,
feature state, progress, and operator routing work for a fresh session.

## Worker And Team Rules

- Worker and team type/count are task-shaped and project-goal-shaped.
- The generated harness MUST record an initial workstream profile and team
  topology inference from the project goal, but this inference does not approve
  production strategy, external action, budget, domain claims, or regulated use.
- Worker sessions MAY vary by work location, surface, task phase, model family,
  or cost tier.
- A returning task SHOULD resume the prior worker instance/session when the
  session remains available and safe.
- Worker session identity, surface, role, task, context pack, owned paths,
  checkpoint, and resume handle MUST be recorded in
  `WORKER_SESSION_REGISTRY.json`.
- Worker briefs MUST define part id, part scope, owned paths/artifacts, no-touch
  paths/artifacts, and whether the worker is the part owner.
- A part-owner worker session SHOULD be resumed for the same part when safe and
  MUST NOT be reused for unrelated parts without an explicit recorded reason.
- Worker model and effort MUST be selected by task difficulty. Operators remain
  highest verified model/effort; routine workers may use lower verified tiers
  such as Sonnet, Codex Spark, or an equivalent configured routine worker tier
  when gates allow. Simple, well-specified worker chores SHOULD prefer the
  configured routine worker session when available and safe.
- At most four active context-saving plugins may be used per task. `caveman` is
  the preferred context-compression slot when available and verified. Plugin
  output is advisory until written to file-backed harness artifacts.
- If a worker cannot resume its prior session, the replacement worker MUST load
  the recorded context pack and the registry must record the reason.
- Workers may ask an upstream team, such as planning or design, when production
  work reveals missing or contradictory spec details.
- Upstream questions go through team artifacts. They do not turn operators into
  development managers.
- New or resumed worker sessions MUST reload the relevant role files listed in
  `ROLE_FILE_INDEX.md`.
- Dashboard, timeline, graph, external evidence HTML, manager-view, live status UI, and
  state-visualization work MUST NOT start until the task has an approved
  task-local `VISUALIZATION_SPEC.md` or an explicit not-required rationale.
  The spec must define purpose, audience, source artifacts, data contract,
  views, interaction, redaction, update cadence, acceptance criteria, and
  approval evidence.

## Capability Rules

- Every runtime/tool/vendor capability starts as `UNVERIFIED`.
- A capability becomes `VERIFIED` only with evidence path, date, and reviewer.
- A capability affecting security, merge, deploy, secrets, cloud, MCP, or
  production writes SHOULD move toward repeatable smoke or CI evidence.

## Tool Rules

Every tool exposed to agents MUST have a `TOOL_REGISTRY` entry with:

- input schema;
- output schema;
- side-effect class;
- approval policy;
- timeout;
- retry policy;
- idempotency class;
- auth scopes;
- output trust level;
- audit event class.

Side-effecting tools MUST NOT run without an approval policy.

## Evaluation Rules

- Non-trivial work remains `PENDING_CROSS_CHECK` until independently evaluated.
- H0 local smoke MUST exist before real production work.
- High-risk tasks require independent evaluation and human review.
- Evaluation evidence MUST name commands, artifacts, environment, verdict, and
  not-run gates.
- Generated harnesses MUST include a dependency-free golden eval suite under
  `harness/evals/` and `scripts/harnessctl.py eval-run` so scaffold invariants
  can be regression-tested without the original kit, network access, or
  arbitrary command execution.
- A local golden set proves regression coverage, not generalization. For
  deterministic parsers, classifiers, extractors, ranking/scoring systems, data
  transforms, eval frameworks, and benchmark-style quality claims, clean
  `PASS` or `passing` requires held-out/challenge eval evidence, independent
  evaluator evidence, or an explicit accepted `WARN`.
- Hidden, held-out, external reviewer, or challenge eval failures arriving after
  closure MUST reopen the work as a feedback slice. The external record must be
  summarized into internal artifacts, accepted failures must route to the
  responsible artifact, and reusable failures SHOULD become local regression
  fixtures before closure is reasserted.
- Project-specific eval suites MAY be added after planning/evaluation defines
  deterministic checks. Specialized LLM/RAG/agent eval tools may be integrated
  as evidence producers, but their outputs are not canonical memory until
  summarized into harness files.
- Cross-evaluation and debugging must be completed before a work packet is
  presented to fixed operators for closure.
- Evaluation MUST inspect the code or produced artifact, the context and
  decision chain that led to it, runtime evidence, UI/UX/layout/design evidence
  when applicable, and process completeness.
- Evaluation SHOULD include Playwright/browser/device evidence for applicable
  interactive work and should check whether user-facing output is materially
  awkward, weak, outdated, or behind comparable services at review time.
- Failures and material WARNs MUST route feedback to planning, design,
  production, evaluation, context, governance, or human decision.

## Context Loading Rules

- Always-loaded files MUST stay lightweight.
- Heavy standards, examples, old task artifacts, long logs, and domain packs
  MUST be referenced on demand.
- Each team MUST have its own context loading guide stating files to always
  read, files to read for the active phase, and files to read only on demand.
- Each team SHOULD have a `TEAM_CONTEXT.md` shared by workers in that team.
- Context pressure MUST be managed with bounded context packs, compaction
  triggers, source-path summaries, part-owner isolation, and explicit separation
  between internal canonical records and external-channel records.
- Worker model and effort SHOULD be the lowest verified level that can satisfy
  the task gates.
- Planning, spec-writing, evaluation, cross-check, and worker-brief generation
  SHOULD use a stronger model class than trivial implementation workers when
  task ambiguity or downstream cost is material.

## Sharp Deep Execution Rules

- Production work MUST proceed narrow/deep by default.
- Planning MUST run a pre-slice runway, validate candidate slices, then approve
  one active slice and make it executable through design, production, debugging,
  evaluation, cross-evaluation, operator closure, context update, and regulation
  review.
- The next production slice MUST NOT start until the current slice is `DONE`,
  `BLOCKED`, or material `WARN` has been accepted.
- Broad market/frontier scan, inventory, and roadmap discovery are allowed only
  as discovery inputs; production returns to one sharp/deep slice.
- Goal-to-work conversion SHOULD pass through PRD draft, anti-PRD, evaluator
  critique, candidate slices, and worker brief before production unless a
  human-approved emergency fallback is recorded.

## Change Rules

- Governance changes require human approval.
- In standard/full mode, governance changes also require dual-operator review.
- Repeated failures MUST update `FAILURE_LEDGER.md` and, when practical, a
  schema, linter, template, or eval fixture.
- Substantial task closure MUST include a regulation review: update role files,
  skills, templates, schemas, linter, or eval fixtures when evidence shows a
  repeatable improvement, or record that no change was needed.

## Distribution Rule

Agents SHOULD use `AGENTS.md`, `BOOTSTRAP.md`, `SPEC.md`, `templates/`,
`schemas/`, and `scripts/` for normal operation.
