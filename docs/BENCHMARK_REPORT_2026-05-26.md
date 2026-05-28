# Benchmark Report 2026-05-26

This report records the public evidence added for the harness kit.

The benchmark suite is intentionally conservative. It separates three claims:

- runtime checkpointing
- project-local governance and restart evidence
- security and disagreement handling surfaces

It does not claim that this kit is faster than LangGraph, CrewAI, OpenAI Agents
SDK, or Claude Code. The safe claim is narrower: this kit generates a stronger
repo-local operating layer around those tools.

## Official Source Basis

Checked sources are stored in `benchmarks/agentic_governance/sources.json`.

Source findings used for scoring:

- LangGraph documents built-in persistence, checkpoints, thread IDs, state history,
  and durable execution with replay requirements
- CrewAI documents Flows, state management, `@persist`, SQLite persistence,
  flow IDs, and flow visualization
- OpenAI Agents SDK documents sessions, SQLite-backed memory, handoffs,
  guardrails, and tracing
- Claude Code documents project hooks, subagents, settings, scoped tools,
  subagent context, and subagent lifecycle hooks
- OWASP MCP Top 10 and MCP security guidance reinforce the need for tool
  allowlists, credential hygiene, audit logs, and default-deny behavior

## Executed Benchmarks

### Requirements Traceability

Command:

```sh
python3 benchmarks/requirements_traceability/score.py --check-summary
```

Scope:

- generated harness scaffold and `./init.sh`
- 13 public operating categories
- 224 file, text, and absence checks
- no model calls
- private account-specific surfaces must be absent

Result:

| categories | passed categories | checks | failed checks | score |
| ---: | ---: | ---: | ---: | ---: |
| 13 | 13 | 224 | 0 | 1.000 |

Interpretation:

- the harness requirements are reflected in the public-safe scaffold for
  implementer bootstrap, dual operators, worker teams, context controls, hooks,
  spec gates, eval loops, budget governance, local visibility, bounded remote
  descriptors, and read-only MCP export
- hosted dashboards, enabled cloud runners, live provider outage tests, live
  human approval latency, native-review bilingual quality scoring, and
  account-specific private workflows are not claimed by this public kit

### Spec Gate Regression Guard

Command:

```sh
python3 benchmarks/spec_gate/score.py --check-summary
```

Scope:

- generated harness scaffold and `./init.sh`
- 12 planning-gate criteria
- two authored controls for regression sanity checks
- no model calls

This is a self-check for the generated harness scaffold. It verifies that the
public kit still emits planning-gate surfaces before production work. It does
not measure model quality, final artifact quality, or neutral superiority over
other tools.

Result:

| generated scaffold checks | failed | conformance |
| ---: | ---: | ---: |
| 12 | 0 | 100% |

Interpretation:

- the generated harness creates the planning runway, PRD/anti-PRD templates,
  candidate slice gate, worker brief contract, part ownership, evaluator gate,
  event evidence, status report, and operator closure surfaces before
  production work
- the authored controls are intentionally not presented as product rankings;
  they exist to keep this self-check from becoming a pure path-existence smoke
  test with no contrast

### Static Visualization

Command:

```sh
python3 benchmarks/static_viz/score.py --check-summary
```

Scope:

- generated harness scaffold and `./init.sh`
- default `local_file` visualization backend
- status HTML and JSON
- sanitized event JSON and NDJSON
- no network writes
- no hosted dashboard

Result:

| generated scaffold checks | failed | conformance |
| ---: | ---: | ---: |
| 12 | 0 | 100% |

Interpretation:

- the generated harness can turn canonical `events.jsonl` records into local
  static evidence views
- exported event fields are constrained to the allowlist used by
  `harnessctl.py`
- common secret and absolute local path patterns are not present in exported
  local evidence
- exported payloads are checked for private public-source markers and status
  JSON declares the report as a compiled view rather than canonical memory
- this does not claim real-time dashboard quality, hosted reliability, or
  external visualization backend readiness

### Replay Recovery

Command:

```sh
python3 benchmarks/replay_recovery/score.py --check-summary
```

Scope:

- 10 task shapes
- 1 deterministic scaffold generation per mode
- direct transcript baseline
- ad-hoc loop baseline
- generated harness from this public kit
- all modes are deterministic local fixtures, not captured live agent sessions
- harness-specific policy coverage is reported separately from generic recovery
  score
- this is a restart-surface check, not a degraded-state recovery test or an
  independent competitive ranking

Result:

| mode | cases | recovery score | policy coverage |
| --- | ---: | ---: | ---: |
| direct transcript | 10 | 0.110 | 0.000 |
| ad-hoc loop | 10 | 0.500 | 0.000 |
| generated harness | 10 | 1.000 | 1.000 |

Interpretation:

- direct transcript is cheapest but weak for file-only restart
- ad-hoc loop captures some state but lacks audit and governance surfaces
- generated harness leaves enough repo-local evidence for another session to
  resume without reading the original chat

### Bilingual README Parity

Command:

```sh
python3 benchmarks/bilingual_readme_parity/score.py --check-summary
```

Scope:

- generated project README scaffolded from this public kit
- Korean and English section parity for operational surfaces
- authored controls for Korean-only and thin bilingual summary outputs
- no model calls
- no native speaker fluency claim

Result:

| surface | passed | failed | total | score |
| --- | ---: | ---: | ---: | ---: |
| korean only control | 2 | 12 | 14 | 0.143 |
| bilingual summary control | 5 | 9 | 14 | 0.357 |
| generated harness | 14 | 0 | 14 | 1.000 |

Interpretation:

- generated harness README carries the same operating commands, role terms,
  context policy, visualization boundary, MCP boundary, remote boundary, and
  public/private boundary in both Korean and English sections
- this guard tests structural parity, not wording quality, translation quality,
  or publication readiness

### Agentic Governance

Command:

```sh
python3 benchmarks/agentic_governance/score.py --check-summary
```

Scope:

- reference project surfaces for LangGraph, CrewAI, OpenAI Agents SDK, Claude
  Code, custom Python loop
- real generated harness scaffolded and initialized from this kit
- deterministic file and policy checks

The reference surfaces and rubric are authored in this repo. They are small
surfaces based on official documentation, not full framework applications and
not an independent product ranking. The overall score is passed framework
criteria divided by 24.

Result:

| surface | overall | restart | governance | runtime |
| --- | ---: | ---: | ---: | ---: |
| custom Python loop | 0.208 | 0.500 | 0.000 | 0.500 |
| LangGraph checkpoint app | 0.417 | 0.800 | 0.133 | 1.000 |
| CrewAI flow app | 0.542 | 0.800 | 0.333 | 1.000 |
| OpenAI Agents session app | 0.500 | 0.800 | 0.267 | 1.000 |
| Claude Code project | 0.500 | 0.400 | 0.533 | 0.250 |
| generated harness | 0.958 | 0.900 | 1.000 | 0.750 |

Interpretation:

- LangGraph, CrewAI, and OpenAI Agents SDK are stronger on runtime persistence
  primitives
- Claude Code is strong on project hooks and subagents
- generated harness is strongest on repo-local governance, evidence, operator
  boundaries, worker scope, policy, and report surfaces
- generated harness has much higher file count, which is an operating overhead

### MCP Assurance

Result:

| surface | score |
| --- | ---: |
| raw MCP usage | 0.100 |
| permissive MCP client | 0.300 |
| generated harness | 1.000 |

Interpretation:

- the public kit has MCP trust policy, tool allowlist, credential lifecycle,
  local tool listing, audit event files, and report evidence
- this is not a full red-team test against live MCP servers

### Dissent Preservation

Result:

| surface | score |
| --- | ---: |
| single operator | 0.200 |
| forced consensus multi-agent fixture | 0.300 |
| dual operator harness | 1.000 |

Interpretation:

- the generated harness preserves non-coercion, separate positions, peer
  critique, disagreement records, human escalation, and rule-change paths
- this tests protocol surface availability, not model judgment quality

### Budget Governance Surface

Command:

```sh
python3 scripts/validate_kit.py
```

Scope:

- generated harness scaffold and `./init.sh`
- task-level `BUDGET.json` files
- runner budget fields and kill procedures
- `scripts/harnessctl.py budget-check`
- budget event fields in the observability schema
- no provider token-meter capture
- no live cost benchmark

Smoke command for a generated harness:

```sh
python3 scripts/harnessctl.py budget-check \
  --task-id F0-PLANNING-RUNWAY \
  --time-elapsed-minutes 181
```

Expected behavior:

- writes `budget.kill_required`
- writes `budget.escalation_required`
- exits non-zero so the runner can stop dispatch

Interpretation:

- the generated harness now has a local kill surface for task budget overruns
- runner adapters still need to pass observed token, time, and cost counters
- this is governance enforcement surface evidence, not live token-cost variance
  evidence

### Operational Resilience Policy Assay

Command:

```sh
python3 benchmarks/operational_resilience/score.py --check-summary
```

Scope:

- deterministic provider failover policy scenarios
- deterministic human approval gate scenarios
- generated harness scaffold and `./init.sh`
- no model provider calls
- no external approval channel or mobile latency measurement
- synthetic control baselines authored in this repo

This is a policy-surface unit test, not an independent product ranking and not
a live outage benchmark.

Provider failover policy surface:

| surface | score | completion policy | independent check policy |
| --- | ---: | ---: | ---: |
| single_vendor | 0.300 | 0.500 | 0.000 |
| retry_same_vendor | 0.350 | 0.625 | 0.000 |
| generated_harness_policy | 1.000 | 1.000 | 1.000 |

Approval gate policy surface:

| surface | score | false allow | false block | approval precision |
| --- | ---: | ---: | ---: | ---: |
| allow_all | 0.450 | 0.700 | 0.000 | 0.000 |
| block_all | 0.850 | 0.000 | 0.300 | 0.700 |
| generated_harness_policy | 1.000 | 0.000 | 0.000 | 1.000 |

Interpretation:

- generated harness policy files include model routing and permission gates for
  these fixed scenarios
- this is a policy-surface simulation, not a live outage or latency benchmark

### Cloud Runner Policy Smoke

Command:

```sh
python3 benchmarks/cloud_runner_policy/score.py --check-summary
```

Scope:

- generated cloud runner example descriptor
- remote operation policy text
- offline operation policy text
- credential lifecycle boundary
- no cloud execution
- no credentials
- no remote terminal control
- authored descriptor controls

Result:

| surface | passed | failed | total | score |
| --- | ---: | ---: | ---: | ---: |
| unsafe active descriptor | 2 | 8 | 10 | 0.200 |
| partial placeholder | 8 | 2 | 10 | 0.800 |
| generated cloud example | 10 | 0 | 10 | 1.000 |
| generated policy docs | 10 | 0 | 10 | 1.000 |

Interpretation:

- the public harness keeps cloud lanes disabled by default
- activation requires a project-private adapter, scoped credentials, budget,
  kill path, audit path, and smoke evidence
- generated project `.gitignore` excludes private overlays and active cloud
  credential descriptors
- this is not hosted reliability evidence and not a remote execution test

### Runtime Persistence Smoke

Command:

```sh
uv run --python 3.12 \
  --with langgraph \
  --with crewai \
  --with openai-agents \
  python benchmarks/runtime_persistence/score.py --check-summary
```

Scope:

- actual package imports for LangGraph, CrewAI, and OpenAI Agents SDK
- no LLM API calls
- deterministic state preservation and reload checks
- generated harness scaffold and `./init.sh`

Result:

Runtime package results:

| surface | score |
| --- | ---: |
| LangGraph memory checkpointer | 1.000 |
| CrewAI persisted flow | 0.900 |
| OpenAI Agents SQLite session | 1.000 |

Generated harness operating-layer smoke:

| surface | score |
| --- | ---: |
| generated harness restart evidence | 0.900 |

Interpretation:

- runtime frameworks are strong at runtime persistence
- the generated harness score is project restart evidence, not a runtime reload
  primitive
- this supports the kit's positioning as a complementary project operating
  layer, not a replacement runtime
- this smoke does not measure throughput, hosted durability, model quality, or
  production failure recovery under load

### Date Normalization

Command:

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

Result:

| run | accuracy |
| --- | ---: |
| direct session | 83.3% |
| harness first pass | 72.2% |
| harness after feedback | 100.0% |

Interpretation:

- first harness pass was worse than the direct session
- the useful behavior was feedback-loop capture into the same public regression
  fixture
- this proves regression capture, not hidden generalization

## Requested Topics Status

| topic | public status |
| --- | --- |
| replayability and recovery | implemented and validated |
| governance overhead | implemented as file count and governance score |
| MCP assurance | implemented as deterministic policy assay |
| dissent preservation | implemented as deterministic protocol assay |
| runtime persistence smoke | implemented with live dependencies and no LLM calls |
| date normalization feedback loop | implemented and validated |
| website visual comparison | implemented with screenshots |
| requirements traceability | implemented and validated |
| spec gate before sharp/deep work | scaffold regression guard implemented, not a neutral comparator |
| static visualization evidence | local export regression guard implemented, not a hosted dashboard benchmark |
| multi-vendor resilience | deterministic policy assay implemented, live outage not claimed |
| HITL latency | approval policy assay implemented, live latency not claimed |
| bilingual quality | deterministic README parity guard implemented, native review not claimed |
| cloud runner policy | descriptor and dry-run policy smoke implemented, real cloud execution not claimed |
| live framework throughput | not claimed |

## Public Claim Boundary

Safe claim:

> This kit generates a file-backed operating layer for restartable multi-agent
> projects. It is stronger than minimal project surfaces at repo-local
> governance, audit, handoff, and restart evidence. It complements runtime
> frameworks rather than replacing them.

Unsafe claim:

> This kit is universally better than LangGraph, CrewAI, OpenAI Agents SDK, or
> Claude Code.
