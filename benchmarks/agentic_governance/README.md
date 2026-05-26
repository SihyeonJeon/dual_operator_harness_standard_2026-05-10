# Agentic Governance Benchmark

Deterministic local benchmark for project-level agent governance.

This benchmark does not call LLM APIs and does not measure model intelligence.
It creates reference project surfaces for adjacent tools, creates a real
generated harness from this kit, and scores whether a new session can recover
operating context, verify assurance gates, and preserve operator disagreement
from files in the project.

## Tracks

| track | question |
| --- | --- |
| framework_recovery | does the project surface preserve restart and governance evidence |
| mcp_assurance | does the project surface fail closed around MCP-style tools |
| dissent_preservation | does the project surface preserve disagreement instead of forcing consensus |

## Compared Surfaces

The reference surfaces are intentionally small and deterministic. They are not
full framework applications.

The rubric and reference surfaces are authored in this repo. This is a
repo-state assay, not an independent product ranking. `overall` is passed
framework criteria divided by 24.

| surface | represented capability |
| --- | --- |
| custom_python_loop | hand-written task state and resume script |
| langgraph_checkpoint_app | checkpointed graph project surface |
| crewai_flow_app | persisted flow project surface |
| openai_agents_session_app | session handoff tracing project surface |
| claude_code_project | Claude Code project hooks and subagents surface |
| generated_harness | real scaffold created by this public kit and initialized with `./init.sh` |

## Run

```sh
python3 benchmarks/agentic_governance/score.py --check-summary
```

Useful variants:

```sh
python3 benchmarks/agentic_governance/score.py --details
python3 benchmarks/agentic_governance/score.py --keep
```

## Expected Summary

| surface | overall | restart | governance | runtime | files |
| --- | ---: | ---: | ---: | ---: | ---: |
| custom_python_loop | 0.208 | 0.500 | 0.000 | 0.500 | 5 |
| langgraph_checkpoint_app | 0.417 | 0.800 | 0.133 | 1.000 | 9 |
| crewai_flow_app | 0.542 | 0.800 | 0.333 | 1.000 | 11 |
| openai_agents_session_app | 0.500 | 0.800 | 0.267 | 1.000 | 9 |
| claude_code_project | 0.500 | 0.400 | 0.533 | 0.250 | 9 |
| generated_harness | 0.958 | 0.900 | 1.000 | 0.750 | 151 |

| MCP surface | assurance |
| --- | ---: |
| raw_mcp_usage | 0.100 |
| permissive_mcp_client | 0.300 |
| generated_harness | 1.000 |

| dissent surface | preservation |
| --- | ---: |
| single_operator | 0.200 |
| forced_consensus_multi_agent | 0.300 |
| dual_operator_harness | 1.000 |

## Limit

The score rewards files and policies that make project governance recoverable.
It does not replace runtime benchmarks for latency, token cost, hosted
observability, model quality, or real failure injection under each framework's
production runtime.
