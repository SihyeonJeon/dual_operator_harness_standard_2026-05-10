# Requirement Traceability 2026-05-26

This document records which harness requirements are reflected in the public
kit, which surfaces are policy-only, and which surfaces belong in private
project overlays.

## Public Kit Result

Command:

```sh
python3 benchmarks/requirements_traceability/score.py --check-summary
```

Result:

| category | public status |
| --- | --- |
| implementer bootstrap | implemented |
| dual operator and council | implemented |
| worker team and part ownership | implemented |
| context memory and pressure | implemented |
| hook lifecycle | implemented |
| spec before execution | policy and templates implemented |
| evaluation feedback loop | implemented |
| visibility and static reports | local-only implemented |
| remote and credential boundary | policy and descriptors implemented |
| read-only MCP export | reference export implemented |
| benchmark evidence | public fixtures implemented |
| public/private boundary | private account surfaces excluded |

The traceability assay scaffolds a generated harness and checks 143 file,
content, and absence conditions. Current result: 143 passed, 0 failed.

## Benchmark Topics

| requested topic | current public implementation | claim boundary |
| --- | --- | --- |
| replayability across task shapes | `benchmarks/replay_recovery` 10 deterministic task-shape cases | deterministic repo-state assay, not live model variance |
| recovery after interruption | `benchmarks/replay_recovery` plus generated status and event files | restart evidence, not hosted runtime recovery |
| governance overhead | `benchmarks/agentic_governance` file count and governance score | overhead is explicit, not hidden |
| planning before sharp/deep work | `benchmarks/spec_gate` | scaffold regression guard, not a neutral comparator |
| static visualization | `benchmarks/static_viz` | local export guard, not hosted dashboard quality |
| MCP assurance | `benchmarks/agentic_governance` plus `MCP_TRUST.json` and read-only server | policy and local surface, not live red-team coverage |
| dissent preservation | `benchmarks/agentic_governance` council surface | protocol preservation, not model judgment accuracy |
| provider failover | `benchmarks/operational_resilience` | policy assay, not live outage handling |
| human approval gates | `benchmarks/operational_resilience` | policy assay, not real approval latency |
| runtime persistence | `benchmarks/runtime_persistence` optional package smoke | runtime frameworks are compared only on state reload smoke |
| bilingual quality | `benchmarks/bilingual_readme_parity` | deterministic README parity guard, not native fluency scoring |
| cloud runner policy | `benchmarks/cloud_runner_policy` | descriptor and dry-run policy smoke, not real cloud execution |

## Harness Requirements Coverage

| requirement | reflected in public kit | notes |
| --- | --- | --- |
| project goal only intake | yes | scaffold treats unknown constraints as `UNKNOWN` |
| harness implementer role | yes | `IMPLEMENTER.md`, implementer hooks, scaffold report |
| fixed Codex and Claude Code operators | yes | equal operator files, session registry, model routing |
| operator as orchestrator, not worker | yes | operator files and workstream profile state the boundary |
| worker teams by planning/design/production/evaluation | yes | team files and team context files generated |
| same part returns to same worker when safe | yes | part ownership and worker session registry |
| lower-tier worker routing for routine work | yes | `MODEL_ROUTING.json` |
| context accumulation and shared memory | yes | root state, shared memory, team memory, event log |
| context overload controls | yes | context pressure controls and context pack rule |
| feedback loop into rules and evals | yes | failure ledger, rule-change log, eval suites |
| internal records separate from public-facing summaries | yes | records policy keeps canonical memory local |
| hooks stronger than plain markdown | yes | Claude Code lifecycle hooks plus local validators |
| visualization before backend selection | yes | local report default, backend spec gate required |
| live worker tree or hosted dashboard | no | intentionally not enabled by default |
| remote or cloud runner | partial | descriptors and policy only, no enabled cloud lane |
| PRD and anti-PRD automation | partial | templates and policy exist, autonomous spec agent not included |
| private publishing or account-specific posting | excluded | belongs in a private project overlay |
| private AI review adapter | excluded | public kit keeps local review artifacts and deterministic checks |
| private memory database backend | excluded | public kit uses file-backed state and read-only MCP export |

## Public-Safe Backlog

These are the next items that can improve the public kit without exposing
private account workflows.

1. Static visualization example built from `events.jsonl`
2. Local spec-agent command that fills PRD and anti-PRD drafts without network
3. Real cloud runner adapter example with project-private credentials
4. Larger live-model replay/recovery benchmark with real variance data
5. Native bilingual review fixture with explicit public reference outputs

## Interpretation

The core harness architecture is reflected: implementer separation, dual
operators, worker teams, fixed part ownership, hooks, context controls, eval
loops, local visibility, and MCP export.

The public kit intentionally stops before private account automation, hosted
execution, private storage, or real remote-control activation. Those are
project overlays, not public source.
