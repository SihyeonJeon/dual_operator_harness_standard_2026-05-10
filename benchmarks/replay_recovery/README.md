# Replay Recovery Fixture

Small public fixture for measuring restart readiness after an interrupted agent
project.

This is not a model intelligence benchmark and not a full framework benchmark.
It measures whether a run leaves enough file-backed state for another session to
resume without reading the original chat.

## What It Measures

- recovery artifacts present
- recoverable project facts
- event count
- weighted recovery readiness score

The direct session fixture intentionally represents a normal chat transcript and
partial artifact. The generated harness fixture is created from this public kit,
then initialized with `./init.sh`.

## Run

```sh
python3 benchmarks/replay_recovery/score.py --check-summary
```

## Expected Summary

| run | recovery artifacts | recoverable facts | event count | score |
| --- | ---: | ---: | ---: | ---: |
| direct_session | 1/10 | 1/8 | 0 | 0.11 |
| generated_harness | 10/10 | 7/8 | 7 | 0.95 |

## Limit

The fixture compares restart state, not final output quality. Runtime frameworks
with durable execution should be compared separately on latency, cost, and
checkpoint semantics.
