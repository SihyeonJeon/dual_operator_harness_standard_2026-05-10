# Harness Implementer Manual

This manual is for the actor that creates a project-local harness from the kit.
The harness implementer is not Claude Code operator, Codex operator, a worker,
or an evaluator.

## Mission

Given only:

- the kit; and
- the user's project goal;

create a complete harness scaffold that can later be operated by fixed dual
operators and task-shaped worker teams.

The implementer designs the harness, not the project execution strategy. The
implementer must not choose a domain track, product/topic direction, platform,
budget, identity, user/audience target, deployment model, publication channel,
or external-action path simply because it seems useful for the stated goal.
Those are operational decisions for fixed operators and the human after handoff.

## Non-Authority Boundary

The implementer may:

- create harness files;
- classify the initial project type;
- infer an initial workstream profile and team topology from the goal;
- set unknown values to `UNKNOWN`;
- choose a conservative initial adoption mode;
- create H0 local smoke blueprint;
- create H1 bootstrap restart smoke blueprint;
- run implementer scaffold lifecycle hooks;
- create root operator-entry and restart files;
- create Claude Code adapter files under `.claude/`;
- create dual-operator parity, part ownership, plugin routing, and quality-gate
  files;
- create agent communication and software feedback policy files;
- create visualization spec policy and template files;
- create records policy and context-pressure control files;
- create read-only MCP export and spec automation scaffold files;
- create visualization backend policy, local event export adapter scaffold, and
  cloud/viz human decision guide;
- create dependency-free eval suite scaffold and schema;
- run doctor/linter checks;
- write a scaffolding report;
- write `harness/IMPLEMENTER_HANDOFF.md`;
- write `harness/IMPLEMENTER_HOOKS.md` and
  `harness/IMPLEMENTER_HOOKS_RUN.json`;
- write project-root `guide_for_human.md`;
- write project-root bilingual `README.md`;
- write `harness/runtime/OFFLINE_OPERATION.md`;
- write `harness/runtime/REMOTE_OPERATION_POLICY.md`;
- copy or generate local validation scripts into the target project.

The implementer must not:

- start production work;
- design the project-specific strategy needed to achieve the eventual goal;
- claim runtime capabilities are verified;
- approve MCP, cloud, deploy, merge, or secret access;
- decide material domain facts when the project goal does not contain them;
- become one of the fixed operators;
- hide assumptions in prose.

## Two-Input Procedure

1. Treat the project goal as the only binding project fact.
2. If prior information/constraints are absent, record them as `UNKNOWN`.
3. Create `PROJECT_PROFILE.json` using the project goal and `UNKNOWN` for
   missing fields.
4. Create `WORKSTREAM_PROFILE.json` with conservative initial workstream and
   team-topology inference while preserving planning, production, evaluation,
   operator review, and context update loops.
5. Create `ACTIVE_SNAPSHOT.md` with open questions.
6. Copy the canonical template tree into `harness/`.
7. Copy or render root `AGENTS.md`, `CLAUDE.md`, `init.sh`,
   `README.md`, `feature_list.json`, `progress.md`, `session-handoff.md`,
   and `.claude/` adapters.
8. Ensure fixed operator files point to shared canonical context.
9. Ensure worker session, role-file, sharp/deep, model-routing, council, and
   regulation-evolution policies exist.
10. Ensure dual-operator protocol, part ownership, plugin routing, and quality
    gates exist.
11. Ensure routine model aliases, agent communication policy, and software
    feedback policy exist.
12. Ensure visualization spec policy and template exist, and visualization
    production is blocked until a task-local spec is approved or explicitly not
    required.
13. Ensure records policy, context-pressure controls, read-only MCP export, and
    spec automation policy exist. These start as scaffolded/`UNVERIFIED`
    surfaces and do not approve external posting, private adapters, or remote
    operation.
14. Ensure visualization backend descriptors exist under `harness/viz/`, with
    `local_file` as the only verified local backend and external backends denied
    until human selection, bounded policy, credential lifecycle, and smoke
    evidence exist.
15. Ensure H0, H1, and F0 planning runway tasks exist but production work
    is not started.
16. Write `harness/IMPLEMENTER_HANDOFF.md`.
17. Write and update `harness/IMPLEMENTER_HOOKS.md` and
    `harness/IMPLEMENTER_HOOKS_RUN.json`.
18. Write project-root `guide_for_human.md`.
19. Write project-root bilingual `README.md`.
20. Write `harness/runtime/OFFLINE_OPERATION.md`.
21. Write `harness/runtime/REMOTE_OPERATION_POLICY.md`.
22. Write `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md`.
23. Write `harness/evals/README.md`, `harness/evals/golden_suite.json`, and
    `schemas/eval-suite.schema.json`.
24. Ensure the target project has its own validator, `scripts/harnessctl.py`,
    `scripts/implementer_hooks.py`, and schemas or equivalent local validation
    command.
25. Run `scripts/validate_harness.py <target-project>`.
26. Write `harness/SCAFFOLDING_REPORT.md`.

## When To Ask The User

Ask only when scaffolding would otherwise encode a material irreversible or
unsafe choice. Examples:

- production credentials or secrets;
- paid API/cloud spending;
- compliance-heavy domain activation;
- merge/deploy/publish authority;
- irreversible destructive tool access;
- a project goal too vague to identify even a starter H0 smoke.

Otherwise scaffold with `UNKNOWN` and let fixed operators ask later.

## Required Handoff To Operators

The implementer must leave:

- generated harness files;
- validation result;
- project goal;
- unknown constraints;
- open questions;
- H0 local smoke blueprint;
- H1 bootstrap restart smoke blueprint;
- F0 planning runway and slice gate blueprint;
- implementer hook policy and run evidence;
- root operator-entry and restart files;
- Claude Code adapter files that preserve `harness/shared/` and team
  `TEAM_CONTEXT.md` as canonical memory;
- dual-operator protocol that keeps Codex and Claude Code equal, preserves
  dissent, and forbids forced consensus;
- operator session registry for fixed Claude Code and Codex session handles;
- part-owner session reuse rules;
- context-saving plugin routing with a four-plugin cap and caveman compression
  slot;
- model routing for routine tasks through `sonnet`, `haiku`, and
  `gpt-5.3-codex-spark` aliases when verified locally;
- token-efficient agent communication through bounded task packets and evidence
  paths;
- quality gates for artifact, context-chain, runtime, UI/UX/layout/design, and
  feedback routing;
- software feedback policy for lint/static checks, runtime smoke, Playwright or
  equivalent browser/device evidence, and UI/UX/layout review;
- visualization spec policy, visualization spec template, and local
  `scripts/harnessctl.py` command surface for event logging, static HTML status
  reports, local viz export, visualization spec checks, dependency-free eval
  suites, task archive, bounded context packs, worker briefs, model routes,
  task packets, and software feedback evidence;
- `harness/evals/` golden scaffold suite and `schemas/eval-suite.schema.json`
  so operators can run local invariant checks before adding specialized
  domain evals;
- visualization backend policy under `harness/viz/`, with `local_file` as the
  only verified local backend and non-local adapters starting `UNVERIFIED`;
- records policy for canonical project records, compiled local report views, and
  public-kit out-of-scope private overlay channels;
- context-pressure controls for bounded context packs, compaction, plugin caps,
  and part-owner isolation;
- read-only MCP context export scaffold under `harness/mcp_server/`;
- spec automation policy and PRD/anti-PRD templates for planning before
  sharp/deep production;
- rendered `harness/spec/INPUT_PACKET.md` preserving the two-input intake
  packet for fixed operators;
- workspace layout, memory backend descriptor, and runner descriptors, all
  starting conservative and unverified where applicable;
- project-root human guide;
- project-root Korean/English README;
- offline/local-continuity note;
- remote/mobile/cloud operation policy;
- no production changes.
