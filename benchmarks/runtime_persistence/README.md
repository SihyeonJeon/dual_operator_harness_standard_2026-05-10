# Runtime Persistence Smoke

Optional live dependency smoke for runtime persistence APIs.

This benchmark installs and imports real framework packages when run through
`uv`. It does not call LLM APIs. It checks whether each runtime can preserve and
reload minimal deterministic state.

## Run

```sh
uv run --python 3.12 \
  --with langgraph \
  --with crewai \
  --with openai-agents \
  python benchmarks/runtime_persistence/score.py --check-summary
```

## Compared Surfaces

| surface | real dependency used |
| --- | --- |
| langgraph_memory_checkpointer | `langgraph` StateGraph with `InMemorySaver` |
| crewai_persist_flow | `crewai` Flow with `@persist()` |
| openai_agents_sqlite_session | `openai-agents` `SQLiteSession` |
| generated_harness | public kit scaffold plus `./init.sh` |

## Expected Summary

Runtime package results:

| surface | score | passed | total |
| --- | ---: | ---: | ---: |
| langgraph_memory_checkpointer | 1.000 | 10 | 10 |
| crewai_persist_flow | 0.900 | 9 | 10 |
| openai_agents_sqlite_session | 1.000 | 10 | 10 |

Generated harness operating-layer smoke:

| surface | score | passed | total |
| --- | ---: | ---: | ---: |
| generated_harness_restart_evidence | 0.900 | 9 | 10 |

The generated harness row is project restart evidence, not a runtime reload
primitive.

## Limit

This smoke is intentionally small. It verifies runtime persistence primitives,
not throughput, hosted durability, graph complexity, model quality, or production
failure recovery under load.
