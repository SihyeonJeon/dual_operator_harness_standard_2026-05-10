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

### Replay Recovery

Command:

```sh
python3 benchmarks/replay_recovery/score.py --check-summary
```

Scope:

- 5 task shapes
- 3 deterministic runs per mode
- direct transcript baseline
- ad-hoc loop baseline
- generated harness from this public kit

Result:

| mode | score |
| --- | ---: |
| direct transcript | 0.110 |
| ad-hoc loop | 0.500 |
| generated harness | 0.950 |

Interpretation:

- direct transcript is cheapest but weak for file-only restart
- ad-hoc loop captures some state but lacks audit and governance surfaces
- generated harness leaves enough repo-local evidence for another session to
  resume without reading the original chat

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
| date normalization feedback loop | implemented and validated |
| website visual comparison | implemented with screenshots |
| multi-vendor resilience | specified but not live-run in public kit |
| HITL latency | specified but not live-run in public kit |
| bilingual quality | specified but not live-run in public kit |
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
