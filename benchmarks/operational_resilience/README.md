# Operational Resilience Policy Assay

Deterministic policy simulation for provider failover and human approval gates.

This benchmark does not call model providers, cloud runners, or external
approval channels. It scores small policy surfaces against fixed scenarios and
also checks the generated harness files from this public kit.

The baseline rows are synthetic controls authored in this repo, not competing
framework implementations. Treat this as a policy-surface unit test, not an
independent product ranking.

## Tracks

| track | question |
| --- | --- |
| provider_failover | can work continue when a preferred model/provider is unavailable |
| approval_gates | are risky actions blocked without stopping low-risk work |

## Run

```sh
python3 benchmarks/operational_resilience/score.py --check-summary
```

## Expected Summary

Provider failover policy surface:

| surface | score | completion policy | independent check policy | notes |
| --- | ---: | ---: | ---: | --- |
| single_vendor | 0.300 | 0.500 | 0.000 | one provider only |
| retry_same_vendor | 0.350 | 0.625 | 0.000 | retries but no independent path |
| generated_harness_policy | 1.000 | 1.000 | 1.000 | model routing policy plus generated harness evidence |

Approval gate policy surface:

| surface | score | false allow | false block | approval precision |
| --- | ---: | ---: | ---: | ---: |
| allow_all | 0.450 | 0.700 | 0.000 | 0.000 |
| block_all | 0.850 | 0.000 | 0.300 | 0.700 |
| generated_harness_policy | 1.000 | 0.000 | 0.000 | 1.000 |

## Limit

This is not a live vendor outage test and not a real mobile approval latency
test. The 1.000 scores apply only to the fixed synthetic scenarios in
`score.py`. It verifies whether a generated project has enough policy surface to
route around provider failure and gate risky actions before live adapters are
added.
