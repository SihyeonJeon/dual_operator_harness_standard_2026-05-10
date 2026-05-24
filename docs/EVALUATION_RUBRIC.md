# Evaluation Rubric

Date: 2026-05-24

This rubric evaluates a generated harness, not the raw intelligence of any one
model. It is intended to work across software, research, writing, design,
operations, media, business, data, education, and other project domains.

## Scoring

- `2`: present by default in the generated harness and backed by executable or
  file evidence.
- `1`: possible or partially scaffolded, but needs project-specific operator or
  worker implementation.
- `0`: absent, contradicted, or not evidenced.
- `N/A`: outside the role of this kit. Do not convert `N/A` into a competitive
  win.

## Universal Criteria

| Criterion | PASS Standard | Current Status |
|---|---|---|
| Domain/task agnosticism | Project goal is classified into workstreams without assuming code/web as the default. | `2` |
| Team topology generation | Planning, design when needed, production, evaluation, and cross-evaluation lanes are selected from goal/risk/task shape. | `2` |
| Operator/worker separation | Fixed operators orchestrate/review; workers own production; roles are file-backed. | `2` |
| Dual-operator parity | Codex and Claude remain equal fixed operators; dissent is preserved. | `2` |
| Planning before sharp/deep production | PRD/anti-PRD/candidate slices precede production. | `2` |
| Cross-verification loop | Evaluation and review packets exist; reviewer output is evidence, not authority. | `2` |
| Context and memory continuity | Shared context, team context, session registries, part ownership, and context pressure rules exist. | `2` |
| Restartability | Fresh agent can load root state, shared context, active task, and resume from files. | `2` |
| Observability | Events, status HTML/JSON, local viz export payloads, and source hashes exist. | `2` |
| Visualization governance | `VISUALIZATION_SPEC.md` selects purpose/backend/redaction before dashboards or live views. | `2` |
| External publication safety | Broadcast drafts are approval gated publish requires approval redaction connector smoke and ledger | `2` |
| Credential and cloud safety | Default no secret access; remote/cloud/network writers are denied until bounded policy and smoke evidence exist. | `2` |
| Failure/success governance evolution | Failure ledger, rule change log, regulation evolution, and team context update loop exist. | `2` |
| Runtime durable execution | Checkpointed runtime that resumes exact graph execution after failure. | `N/A` |
| Model output quality | Quality of a generated website, paper, plan, or media artifact. | `N/A` |

## Evidence Requirements

A claim may be used publicly only if it has at least one of:

- command output recorded in a demo run;
- generated file path;
- screenshot;
- JSON/JSONL artifact;
- external source citation;
- explicit `NOT-RUN` with reason and risk.

## Claims Allowed Today

- The kit generates a domain-agnostic, file-backed dual-operator harness from a
  project goal.
- The generated harness includes restart files, shared/team memory, operator and
  worker role files, event logging, local report generation, visualization
  backend policy, external draft policy, and remote/cloud denial defaults.
- The website demo generated a richer static storefront with 5 generated bitmap
  assets, 27 task evidence files, 44 events, desktop/mobile screenshots, and
  operator closure records.
- The eval demo matched direct Codex accuracy and macro F1 on a 36-row Korean
  support-ticket smoke set while adding planning, design, coding, evaluation,
  operator review, event records, and restart handoff.

## Claims Not Yet Allowed

- "Generally better than LangGraph/CrewAI/OpenAI Agents SDK."
- "Better runtime durability than graph runtimes."
- "Fully autonomous."
- "Works perfectly for all domains."
- "External posting, hosted visualization, private RAG, or cloud execution is
  production-ready without project-specific adapter smoke."

## Next Evidence To Strengthen The Claim

Run at least three project types with the same rubric:

- software or website;
- LLM service/API or data workflow;
- non-development workstream such as research, planning, writing, business
  operations, or education.

For each run, capture:

- generated harness file count;
- validation result;
- number of events;
- approved or blocked visualization spec status;
- completed work packet;
- evaluation report;
- failure/success rule update or explicit no-change;
- screenshots or equivalent domain evidence.
