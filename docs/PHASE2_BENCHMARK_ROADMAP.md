# Phase 2 Benchmark Roadmap

The public kit currently ships deterministic repo-state assays. That is the
right default for this repository because it is reproducible, credential-free,
and does not blur benchmark evidence with private accounts.

Phase 2 should live as a separate benchmark asset so live model variance does
not pollute the kit's deterministic validation suite.

## Live Framework Benchmark

Target shape:

- 5 tasks
- 100 runs per task
- 4 framework or harness modes
- same model set per mode where possible
- fixed budget and retry policy
- public result tables plus raw run records

Recommended modes:

- Easy Orchestration Harness generated project
- LangGraph app with checkpointing
- CrewAI flow with persistence
- custom Python loop baseline

Recommended metrics:

- cost per completed run
- latency per completed run
- task success rate
- interruption recovery time
- replay divergence rate
- human approval block rate
- token variance
- failure-to-regression conversion rate

The expected honest result is mixed. Runtime frameworks should stay strong on
runtime checkpointing and latency. The harness should be evaluated on restart
evidence, governance, failure recovery, and conversion of mistakes into
regression fixtures.

## Task Set

| Task | Purpose | Success signal |
| --- | --- | --- |
| tool chain | five ordered tool calls with state handoff | all required calls in order |
| multi-role synthesis | research, critique, revise, final packet | final packet cites critic changes |
| long chain reasoning | 10-step deterministic planning task | expected state transitions present |
| injected failure | stop after midpoint and resume | resumes from checkpoint, not start |
| domain fixture | Korean date, legal, or policy normalization fixture | accuracy and error capture |

## Korean Market Dogfooding

Separate public examples should use Korean-heavy tasks where the harness
structure matters:

- Korean date and policy normalization
- Korean legal or regulation RAG with source grounding
- Korean customer-support SOP generation with eval feedback
- Korean SFT or DPO dataset preparation with reviewer gates

These should be separate repos or example packages. The kit should link to
them only after the data, license, and benchmark boundary are clean.

## Release Rule

Do not add live benchmark headline claims to this kit README until the separate
benchmark repo includes:

- raw run records
- cost and latency capture
- model and version record
- deterministic replay scripts
- failure cases
- limitations section
- reproducibility instructions
