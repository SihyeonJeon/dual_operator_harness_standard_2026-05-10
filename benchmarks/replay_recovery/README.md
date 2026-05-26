# Replay Recovery Benchmark

Deterministic local benchmark for restart readiness after an interrupted agent
project.

It measures whether another session can resume from files in the repo without
reading the original chat. It does not measure model intelligence, hosted
runtime latency, final artifact quality, or statistical variance across model
runs. It is a restart-surface check, not a degraded-state recovery test.

All modes are deterministic local fixtures. The generated harness mode is the
real public scaffold output plus `./init.sh`, not a captured live agent
session. Score formula: `0.6 * artifact coverage + 0.4 * generic recoverable
fact coverage`. Harness-specific policy coverage is reported separately and is
not included in the recovery score.

## Compared Modes

| mode | fixture |
| --- | --- |
| direct_transcript | transcript plus one partial artifact |
| ad_hoc_loop | task json, state json, log, resume script |
| generated_harness | public kit scaffold plus `./init.sh` |

## Task Set

`tasks.json` contains ten project shapes:

- website storefront
- date normalization CLI
- RAG evidence gate
- incident response SOP
- market research packet
- MCP security assay
- bilingual policy brief
- data pipeline audit
- hardware procurement matrix
- regulated release gate

Default run size: 10 tasks x 1 deterministic scaffold generation = 10 cases per
mode. `--runs` is available for mechanical repeat checks, but repeated runs are
not presented as statistical samples.

Generic recoverable facts include goal echo, active task, next action,
verification state, event count, report path, and canonical memory path.
Harness-specific policy coverage includes unknown-decision boundary, operator
entrypoint, part ownership policy, and context pressure policy.

## Run

```sh
python3 benchmarks/replay_recovery/score.py --check-summary
```

Useful variants:

```sh
python3 benchmarks/replay_recovery/score.py --runs 10
python3 benchmarks/replay_recovery/score.py --details --keep
```

## Expected Summary

| mode | cases | artifact coverage | fact coverage | policy coverage | status report | event count | score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| direct_transcript | 10 | 0.100 | 0.125 | 0.000 | 0.000 | 0 | 0.110 |
| ad_hoc_loop | 10 | 0.500 | 0.500 | 0.000 | 0.000 | 0 | 0.500 |
| generated_harness | 10 | 1.000 | 1.000 | 1.000 | 1.000 | 7 | 1.000 |

## Limit

The generated harness is intentionally heavier than the first two modes. The
score rewards recoverable state, audit files, and resume evidence, not speed.
Runtime frameworks with durable execution should be compared separately on
checkpoint semantics, cost, latency, and hosted deployment behavior.
The direct transcript and ad-hoc loop rows are authored controls, so this
assay is illustrative evidence for the generated scaffold rather than an
independent competitive ranking.
