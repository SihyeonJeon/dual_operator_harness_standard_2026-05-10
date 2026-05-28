# Policy Linter Contract

This file defines checks that a generated harness must satisfy before it is
treated as operational.

## Required P0 Checks

- `PROJECT_PROFILE.json` exists and contains no missing required keys.
- Root `README.md` exists and includes Korean and English sections.
- Root `AGENTS.md` exists and routes "you are operator" to a fixed operator.
- Root `init.sh`, `feature_list.json`, `progress.md`, and
  `session-handoff.md` exist.
- Root `scripts/implementer_hooks.py` exists for scaffold lifecycle hooks.
- Root `scripts/harnessctl.py` exists for local validation, event logging,
  static HTML status reports, local viz export, visualization spec checks,
  dependency-free eval suites, task archive, and compiled local reports.
- `feature_list.json` entries contain behavior, verification, state, and
  evidence.
- `feature_list.json` verification commands contain no local user path,
  package-cache path, `NODE_PATH`, credential path, or temp-only reproduction
  command.
- A feature marked `passing` has evidence.
- After any material gate, root state, progress, handoff, worker registry, event
  log, task packet, status report, and viz export agree or the gate is recorded
  as `BLOCKED` or `WARN`.
- `SCAFFOLDING_REPORT.md` exists and records project goal.
- `SCAFFOLDING_CHECKLIST.md` exists.
- `IMPLEMENTER_HOOKS.md` and `IMPLEMENTER_HOOKS_RUN.json` exist and define
  scaffold lifecycle hook evidence for intake, profile derivation, adoption
  mode selection, domain-pack selection, validation, and handoff completion.
- `.claude/settings.json`, `.claude/hooks/`, `.claude/agents/`, and
  `.claude/skills/` exist for Claude Code-compatible generated harnesses.
- Claude Code adapters point to `harness/shared/` and team `TEAM_CONTEXT.md`
  files, not a competing private memory authority.
- Unknown values are represented as `UNKNOWN`, not blank strings.
- `HARNESS_CONFIG.json` exists and `mode` is `lite`, `standard`, or `full`.
- `CAPABILITY_REGISTRY.json` exists.
- No capability has status `VERIFIED` without `evidence_path`, `verified_at`,
  and `reviewer`.
- `TOOL_REGISTRY.json` exists.
- Every tool has `input_schema`, `output_schema`, `side_effect_class`,
  `approval`, `timeout_seconds`, `retry_policy`, `idempotency`, `auth_scopes`,
  `output_trust_level`, and `audit_event`.
- Any side-effecting tool must require approval.
- `PERMISSION_POLICY.json` exists and fail-closed defaults are present.
- `MCP_TRUST.json` exists even when no MCP servers are configured.
- `OPERATOR_SESSION_REGISTRY.json` exists and records both fixed operator
  sessions as `UNVERIFIED` unless evidence, reviewer, and timestamp exist.
- `WORKSPACE_LAYOUT.md` exists and defines active/archive task layout and
  archive rules.
- `MEMORY_BACKEND.json` exists and requires retrieval source paths; optional
  RAG/graph backends start `UNVERIFIED`.
- `WORKSTREAM_PROFILE.json` exists and preserves planning, production, and
  evaluation as logical lanes.
- `DUAL_OPERATOR_PROTOCOL.md` exists, forbids forced consensus, and preserves
  operator dissent.
- `PART_OWNERSHIP.md` exists and part-owner worker sessions are isolated to the
  same part.
- `PLUGIN_ROUTING.json` exists, caps active context plugins at four, and
  includes `caveman` as preferred context-compression slot.
- `QUALITY_GATES.md` exists and covers artifact, context-chain, runtime,
  UI/UX/layout/design, and feedback routing checks.
- `QUALITY_GATES.md` includes a held-out/challenge eval gate. Deterministic
  parsers, classifiers, extractors, ranking or scoring systems, data
  transforms, eval frameworks, and benchmark-style quality claims cannot claim a
  clean `PASS` from visible golden/self eval alone unless held-out/challenge
  evidence, independent evaluator evidence, or explicit accepted `WARN` is
  recorded.
- `scripts/harnessctl.py integration-evidence` exists and generated Claude Code
  `PreToolUse` guards block unbounded broad searches and source edits that lack
  matching `INTEGRATION_EVIDENCE.json`.
- `VISUALIZATION_SPEC_POLICY.md` and `templates/VISUALIZATION_SPEC.md` exist.
  Visualization production is blocked until a task-local spec is approved or
  explicitly marked not required.
- `viz/VIZ_BACKENDS.json`, `viz/README.md`, `viz/adapters/local_file.json`, and
  `viz/adapters/WORKER_ADAPTER_BRIEF.md` exist. `local_file` is the only
  verified local backend; external viz backends start `UNVERIFIED`, deny
  network writes by default, and require human backend selection, bounded
  policy, credential lifecycle records, and smoke evidence.
- Visualization and diagram information architecture is Claude-owned. Codex or
  deterministic workers may implement event plumbing only after approved
  visualization spec review.
- `RECORDS_POLICY.md` exists and defines canonical project records, compiled
  local report views, and public-kit out-of-scope private overlay channels.
- `CONTEXT_PRESSURE.md` exists and defines context budget, compaction triggers,
  context pack rules, plugin caps, and part-owner isolation.
- `mcp_server/MANIFEST.json`, `mcp_server/README.md`, and `mcp_server/server.py`
  exist as a read-only `UNVERIFIED` harness context export.
- `spec/INPUT_PACKET.md` exists and preserves the rendered two-input intake
  packet for operator handoff.
- `SPEC_AUTOMATION_POLICY.md`, `PRD_DRAFT.md`, and `ANTI_PRD.md` exist so goal
  intake can be turned into reviewed specs before sharp/deep production.
- `MODEL_ROUTING.json` keeps operators highest verified while worker tiers are
  task-difficulty-shaped and simple work can route to a configured routine
  worker session.
- `AGENT_PROVIDER_OVERRIDES.json` exists. Extra user-owned LLM or agent
  surfaces are candidate-only, start `UNVERIFIED`, and do not replace Codex and
  Claude Code fixed operators by default.
- Operator manuals exist and include an ambiguity protocol.
- H0 local smoke blueprint exists.
- H1 bootstrap restart smoke blueprint exists.
- F0 planning runway blueprint exists.
- `OBSERVABILITY.md` and `CLEAN_STATE.md` exist.
- `evals/README.md`, `evals/golden_suite.json`, and
  `evals/results/.gitkeep` exist. The golden suite uses only safe local
  primitives and can run through `scripts/harnessctl.py eval-run` without
  network writes or arbitrary command execution.
- `runtime/OFFLINE_OPERATION.md` and `runtime/REMOTE_OPERATION_POLICY.md`
  exist. Remote terminal, cloud, mobile, chat, and always-on operation are
  denied until bounded connector policy and smoke evidence exist.
- `runtime/CLOUD_VIZ_OPERATOR_GUIDE.md` exists and lists the human decision
  guide for cloud lane selection, viz backend selection, credentials, smoke
  evidence, and adapter activation.
- `runtime/RUNNERS/*.json` descriptors exist for local, Claude Code, Codex,
  and remote/cloud lanes. Every runner starts `UNVERIFIED` and
  denies network by default.
- `harness/tasks/active/` and `harness/tasks/archive/` placeholders exist.
- Target-local schemas exist.
- Generated adapter files, if any, are marked as generated views.

## Required P1 Checks

- `IDENTITY.md`, `CREDENTIAL_LIFECYCLE.md`, and `INCIDENT_RESPONSE.md` exist.
- `ACTIVE_SNAPSHOT.md` contains an `Open Questions` section.
- `FAILURE_LEDGER.md` and `RULE_CHANGE_LOG.md` exist.
- Evaluation report template includes `PASS`, `WARN`, `FAIL`, and `NOT-RUN`.
- Human review packet template exists for standard/full mode.
- Reusable held-out, challenge, or independent evaluator failures are promoted into local
  regression fixtures when they can be checked deterministically.

## Failure Semantics

- P0 failure: scaffold is not operational.
- P1 failure: scaffold may run H0 but cannot enter full production mode.
- Not-run checks must be listed explicitly; absence is not a pass.
