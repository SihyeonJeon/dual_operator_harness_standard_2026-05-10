# Docs

Start with the product README, then use these files when implementing or
auditing a generated harness.

## Core Manuals

| File | Use |
| --- | --- |
| [Harness implementer manual](HARNESS_IMPLEMENTER_MANUAL.md) | create a project-local harness from a project goal |
| [Operator manual](OPERATOR_MANUAL.md) | operate a generated harness after scaffold |
| [Optional extensions](OPTIONAL_EXTENSIONS.md) | add private adapters without polluting public source |
| [Evaluation rubric](EVALUATION_RUBRIC.md) | evaluate generated-harness outputs |

## Public Evidence

| File | Use |
| --- | --- |
| [Benchmarks](BENCHMARKS.md) | stable benchmark overview and command map |
| [Phase 2 benchmark roadmap](PHASE2_BENCHMARK_ROADMAP.md) | live variance and Korean-domain benchmark plan |
| [Benchmark report 2026-05-26](BENCHMARK_REPORT_2026-05-26.md) | dated run report |
| [Requirement traceability 2026-05-26](REQUIREMENT_TRACEABILITY_2026-05-26.md) | requirements reflected, partial, or excluded |

## Reference Notes

| File | Use |
| --- | --- |
| [Implementer file map](IMPLEMENTER_FILE_MAP.md) | generated source map for implementer context |
| [Cloud and visualization operator guide](CLOUD_VIZ_OPERATOR_GUIDE.md) | private overlay checklist for hosted lanes |

Root files such as `IMPLEMENTER.md`, `BOOTSTRAP.md`, `SPEC.md`, and
`POLICY_LINTER.md` are agent operating context. They stay at the repository
root so fresh sessions can load them in a predictable order.
