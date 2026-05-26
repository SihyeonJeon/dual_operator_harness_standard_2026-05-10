# Benchmarks

This page keeps benchmark evidence separate from the product README.

The suite is conservative by design:

- deterministic local fixtures unless a command explicitly says otherwise
- public-safe generated harnesses only
- no credential use
- no account-specific posting
- no hidden model calls in default validation
- scope boundaries stated beside each result

Run the full public validation suite:

```sh
python3 scripts/validate_kit.py
```

## Summary

| Benchmark | Command | Result | Boundary |
| --- | --- | --- | --- |
| requirements traceability | `python3 benchmarks/requirements_traceability/score.py --check-summary` | 166/166 checks | scaffold coverage, not live model quality |
| spec gate | `python3 benchmarks/spec_gate/score.py --check-summary` | 12/12 checks | planning surfaces, not artifact quality |
| static visualization | `python3 benchmarks/static_viz/score.py --check-summary` | 12/12 checks | local export, not hosted dashboard UX |
| replay recovery | `python3 benchmarks/replay_recovery/score.py --check-summary` | generated harness 1.000 | restart surface, not runtime graph reload |
| bilingual README parity | `python3 benchmarks/bilingual_readme_parity/score.py --check-summary` | 14/14 checks | structural parity, not native fluency |
| budget governance | `python3 scripts/validate_kit.py` | generated validator checks budget files and budget-check surface | structure and local kill signal, not provider meter capture |
| agentic governance | `python3 benchmarks/agentic_governance/score.py --check-summary` | generated harness 0.958 | repo-state assay, not product ranking |
| operational resilience | `python3 benchmarks/operational_resilience/score.py --check-summary` | generated policy 1.000 | policy simulation, not live outage handling |
| cloud runner policy | `python3 benchmarks/cloud_runner_policy/score.py --check-summary` | descriptor 1.000, docs 1.000 | disabled descriptors, not real cloud jobs |
| date normalization | `python3 benchmarks/date_normalization/score.py --all --check-summary` | feedback loop 100.0% | 36-row public fixture |

## Requirements Traceability

The traceability assay scaffolds a generated harness and checks whether public
requirements are reflected in public-safe files.

| categories | checks | failed | score |
| ---: | ---: | ---: | ---: |
| 13 | 166 | 0 | 1.000 |

Covered areas include implementer bootstrap, fixed operators, worker teams,
part ownership, context pressure controls, hook lifecycle, spec gates, local
reports, bounded remote descriptors, read-only MCP export, benchmark evidence,
and public/private separation.

See [Requirement traceability](REQUIREMENT_TRACEABILITY_2026-05-26.md) for the
reflected, partial, excluded, and not-claimed areas.

## Spec Gate

The spec gate guard checks that generated harnesses include planning surfaces
before production work starts.

| generated scaffold checks | failed | conformance |
| ---: | ---: | ---: |
| 12 | 0 | 100% |

Measured surfaces include goal intake, PRD, anti-PRD, slice approval, worker
brief, part ownership, evaluator gate, local visibility, and operator closure.

Not measured here: model intelligence, product quality, or human preference.

## Static Visualization

The public harness defaults to local static views. It emits `status.html`,
`status.json`, and sanitized event payloads under `harness/reports/viz/`.

| generated scaffold checks | failed | conformance |
| ---: | ---: | ---: |
| 12 | 0 | 100% |

Measured surfaces include event field allowlisting, redaction smoke, source
metadata, local file export, and no network writes.

Not measured here: hosted backend reliability, live collaboration, or real-time
dashboard latency.

## Replay Recovery

Deterministic repo-state assay with 10 task shapes and one scaffold generation
per mode. The generated harness row is the real public scaffold output plus
`./init.sh`. The control rows are authored fixtures.

Score formula: `0.6 * artifact coverage + 0.4 * generic recoverable fact
coverage`. Harness-specific policy coverage is reported separately.

| mode | cases | artifact coverage | fact coverage | policy coverage | status report | event count | score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| direct transcript | 10 | 0.100 | 0.125 | 0.000 | 0.000 | 0 | 0.110 |
| ad-hoc loop | 10 | 0.500 | 0.500 | 0.000 | 0.000 | 0 | 0.500 |
| generated harness | 10 | 1.000 | 1.000 | 1.000 | 1.000 | 7 | 1.000 |

Interpretation: the generated harness is heavier, but leaves durable project
state that another session can use without the original conversation.

## Bilingual README Parity

Generated project README files include Korean and English operating sections.
The guard checks structural parity.

| surface | passed | failed | total | score |
| --- | ---: | ---: | ---: | ---: |
| korean only control | 2 | 12 | 14 | 0.143 |
| bilingual summary control | 5 | 9 | 14 | 0.357 |
| generated harness | 14 | 0 | 14 | 1.000 |

This is not a native fluency benchmark or translation quality benchmark.

## Agentic Governance

This deterministic comparison checks reference project surfaces for common
agent stacks and one generated harness. The reference rows are small authored
surfaces, not full product implementations.

| surface | overall | restart | governance | runtime | files |
| --- | ---: | ---: | ---: | ---: | ---: |
| custom Python loop surface | 0.208 | 0.500 | 0.000 | 0.500 | 5 |
| LangGraph checkpoint surface | 0.417 | 0.800 | 0.133 | 1.000 | 9 |
| CrewAI flow surface | 0.542 | 0.800 | 0.333 | 1.000 | 11 |
| OpenAI Agents session surface | 0.500 | 0.800 | 0.267 | 1.000 | 9 |
| Claude Code project surface | 0.500 | 0.400 | 0.533 | 0.250 | 9 |
| generated harness | 0.958 | 0.900 | 1.000 | 0.750 | 156 |

The useful reading is narrow: runtime frameworks are strong at runtime state
and graph behavior. The generated harness adds repo-local governance, audit,
handoff, policy, and restart evidence around those tools.

## Budget Governance

Generated harnesses include task budgets, runner budget fields, and a local
budget threshold command:

```sh
python3 scripts/harnessctl.py budget-check \
  --task-id F0-PLANNING-RUNWAY \
  --time-elapsed-minutes 120
```

The command writes `budget.ok`, `budget.warning`, `budget.kill_required`, and
`budget.escalation_required` events as thresholds are crossed. The public kit
does not claim provider token-meter capture by itself. Runner adapters must
pass observed token, time, and cost counters into the command.

Additional policy tracks:

| track | baseline | generated harness |
| --- | ---: | ---: |
| MCP assurance | 0.300 permissive client | 1.000 |
| dissent preservation | 0.300 forced consensus fixture | 1.000 |

## Operational Resilience

Policy simulation for provider failover and human approval gates. It does not
call model providers, cloud runners, or approval services.

Provider failover policy:

| surface | score | completion policy | independent check policy |
| --- | ---: | ---: | ---: |
| single_vendor | 0.300 | 0.500 | 0.000 |
| retry_same_vendor | 0.350 | 0.625 | 0.000 |
| generated_harness_policy | 1.000 | 1.000 | 1.000 |

Approval gate policy:

| surface | score | false allow | false block | approval precision |
| --- | ---: | ---: | ---: | ---: |
| allow_all | 0.450 | 0.700 | 0.000 | 0.000 |
| block_all | 0.850 | 0.000 | 0.300 | 0.700 |
| generated_harness_policy | 1.000 | 0.000 | 0.000 | 1.000 |

The result verifies that generated projects contain model-routing and
permission policies before real adapters are added.

## Cloud Runner Policy

The public kit includes disabled-by-default remote and cloud runner
descriptors. The smoke checks descriptor shape and policy docs without running
cloud jobs or using credentials.

| surface | passed | failed | total | score |
| --- | ---: | ---: | ---: | ---: |
| unsafe active descriptor | 2 | 8 | 10 | 0.200 |
| partial placeholder | 8 | 2 | 10 | 0.800 |
| generated cloud example | 10 | 0 | 10 | 1.000 |
| generated policy docs | 10 | 0 | 10 | 1.000 |

Real cloud lanes belong in private overlays with scoped credentials, budget,
kill path, audit path, and smoke evidence.

## Runtime Persistence

Optional live dependency smoke. This imports real packages through `uv` and
does not call LLM APIs.

```sh
uv run --python 3.12 \
  --with langgraph \
  --with crewai \
  --with openai-agents \
  python benchmarks/runtime_persistence/score.py --check-summary
```

| surface | score |
| --- | ---: |
| LangGraph memory checkpointer | 1.000 |
| CrewAI persisted flow | 0.900 |
| OpenAI Agents SQLite session | 1.000 |
| generated harness restart evidence | 0.900 |

This confirms the boundary: runtime frameworks handle runtime persistence. The
harness adds project restart evidence, governance, handoff, policy, reports,
and evaluation structure around them.

## Date Normalization Loop

Challenge set: 36 public rows in `benchmarks/date_normalization/cases.jsonl`.
Each row includes an input phrase, reference date, locale assumptions, and the
expected normalized date.

| run | public fixture rows | accuracy | errors |
| --- | ---: | ---: | ---: |
| direct session | 36 | 83.3% | 6 |
| harness first pass | 36 | 72.2% | 10 |
| harness after feedback | 36 | 100.0% | 0 |

The first harness pass was worse. The useful behavior was the loop after
failure: failed cases were routed back into the same fixture, converted into
regression coverage, and reflected in kit rules.
