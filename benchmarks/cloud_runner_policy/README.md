# Cloud Runner Policy Smoke

Deterministic local smoke for generated cloud runner policy surfaces.

It checks that the public harness contains disabled-by-default cloud runner
descriptors, remote operation policy text, credential lifecycle boundaries,
offline operation boundaries, audit path requirements, smoke evidence
requirements, and no active cloud credentials.

This does not execute cloud jobs, open remote terminals, use credentials, call
providers, or test hosted reliability. The non-harness rows are authored
controls.

## Run

```sh
python3 benchmarks/cloud_runner_policy/score.py --check-summary
```

## Expected Summary

| surface | passed | failed | total | score |
| --- | ---: | ---: | ---: | ---: |
| unsafe active descriptor | 2 | 8 | 10 | 0.200 |
| partial placeholder | 8 | 2 | 10 | 0.800 |
| generated cloud example | 10 | 0 | 10 | 1.000 |
| generated policy docs | 10 | 0 | 10 | 1.000 |

## Limit

This is a policy and dry-run surface guard. A real cloud lane still needs a
project-private adapter, scoped credentials, budget, kill path, audit path, and
smoke evidence before use. Generated projects include `.gitignore` protection
for private overlays and active cloud credential descriptors.
