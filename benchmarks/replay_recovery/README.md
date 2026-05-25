# Replay Recovery Benchmark

Deterministic local benchmark for restart readiness after an interrupted agent
project.

It measures whether another session can resume from files in the repo without
reading the original chat. It does not measure model intelligence, hosted
runtime latency, or final artifact quality.

The non-harness modes are reproducible baseline fixtures, not captured vendor
sessions. Score formula: `0.6 * artifact coverage + 0.4 * fact coverage`.

## Compared Modes

| mode | fixture |
| --- | --- |
| direct_transcript | transcript plus one partial artifact |
| ad_hoc_loop | task json, state json, log, resume script |
| generated_harness | public kit scaffold plus `./init.sh` |

## Task Set

`tasks.json` contains five project shapes:

- website storefront
- date normalization CLI
- RAG evidence gate
- incident response SOP
- market research packet

Default run size: 5 tasks x 3 runs = 15 runs per mode.

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

| mode | runs | artifact coverage | fact coverage | status report | event count | score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| direct_transcript | 15 | 0.100 | 0.125 | 0.000 | 0 | 0.110 |
| ad_hoc_loop | 15 | 0.500 | 0.500 | 0.000 | 0 | 0.500 |
| generated_harness | 15 | 1.000 | 0.875 | 1.000 | 7 | 0.950 |

## Limit

The generated harness is intentionally heavier than the first two modes. The
score rewards recoverable state, audit files, and resume evidence, not speed.
Runtime frameworks with durable execution should be compared separately on
checkpoint semantics, cost, latency, and hosted deployment behavior.
