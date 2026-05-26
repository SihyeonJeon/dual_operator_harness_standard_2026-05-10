# Requirements Traceability Assay

This benchmark checks whether the public kit still generates the required
operating surfaces after refactors.

It scaffolds a temporary harness, runs `./init.sh`, and checks for:

- implementer bootstrap and scaffold validation
- dual operator files and council protocol
- worker team memory and part ownership
- context pressure controls and restart files
- Claude Code hook lifecycle
- PRD and anti-PRD gates before production
- evaluator loop and local regression files
- local-only visualization export and status HTML
- remote runner and credential boundaries
- read-only MCP context export
- public benchmark evidence
- absence of account-specific private surfaces in the public harness

It is not a live model benchmark. It does not test hosted dashboards, cloud
execution, live provider outage recovery, live human approval latency, or
bilingual output quality.

```sh
python3 benchmarks/requirements_traceability/score.py --check-summary
```
