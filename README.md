# Easy Orchestration Harness

[![CI](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml)

A file-backed harness generator for restartable agent projects

It turns one project goal into a local harness with role files, shared state,
event logs, eval fixtures, status reports, and restart instructions. The goal is
not to replace LangGraph, CrewAI, OpenAI Agents SDK, Claude Code, or other agent
runtimes. It gives those tools a project-level operating layer that survives
after the chat window is gone.

## Why

Direct agent sessions can produce strong output, but project state often stays
inside conversation memory.

This kit writes the operating state into the repo:

- what the project is trying to do
- which files are canonical state
- which worker owns which part
- what was tested
- what failed
- what changed because of the failure
- how the next session should resume

## Quick Start

```sh
git clone https://github.com/SihyeonJeon/easy-orchestration-harness.git
cd easy-orchestration-harness
python3 scripts/validate_kit.py

python3 scripts/scaffold_harness.py \
  --target ../my-project \
  --goal "your project goal"

cd ../my-project
./init.sh
python3 scripts/harnessctl.py report
```

Then open Claude Code, Codex, Cursor, or another agent session inside the
generated project, let it read `AGENTS.md`, and send:

```text
you are operator
```

## What It Generates

```text
project/
  AGENTS.md
  CLAUDE.md
  feature_list.json
  progress.md
  session-handoff.md
  guide_for_human.md
  scripts/
    harnessctl.py
    validate_harness.py
  harness/
    operators/
    teams/
    shared/
    tasks/
    events/events.jsonl
    evals/
    reports/status.html
    viz/
    runtime/
    mcp_server/
```

## Operating Model

| Layer | Purpose |
| --- | --- |
| root state | fresh sessions can start from files, not hidden chat memory |
| operators | fixed review and orchestration roles |
| teams | planning, design, production, evaluation lanes |
| task packets | owned paths, no-touch paths, evidence requirements |
| events | append-only task and gate history |
| evals | local invariant and regression checks |
| reports | static HTML views over canonical files |

Workers can use lower-cost models when the task is routine. Operators should use
the strongest model and effort settings you choose for review, routing, and
closure. Large work is split into parts, and the same part can return to the
same worker session when that is safe.

## Evidence

### Replay Recovery Benchmark

Deterministic repo-state assay: 5 task shapes x 3 runs. The generated harness
is scaffolded from this public kit and initialized with `./init.sh` on every
run.

Measured scope: restart readiness after interruption. Not measured here: model
intelligence, hosted runtime latency, or final artifact quality.

The non-harness modes are reproducible baseline fixtures, not captured vendor
sessions. Score formula: `0.6 * artifact coverage + 0.4 * fact coverage`.

```sh
python3 benchmarks/replay_recovery/score.py --check-summary
```

| mode | runs | artifact coverage | fact coverage | status report | event count | score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| direct transcript | 15 | 0.100 | 0.125 | 0.000 | 0 | 0.110 |
| ad-hoc loop | 15 | 0.500 | 0.500 | 0.000 | 0 | 0.500 |
| generated harness | 15 | 1.000 | 0.875 | 1.000 | 7 | 0.950 |

The generated harness is slower and heavier. The gain is durable project state:
root state, team ownership, evaluator output, append-only events, status HTML,
and a restart path that survives the original session.

### Agentic Governance Benchmark

Deterministic local comparison: reference project surfaces for LangGraph,
CrewAI, OpenAI Agents SDK, Claude Code, a custom loop, and one generated harness.

Measured scope: project-level restart evidence, governance evidence, MCP
assurance, and dissent preservation. Not measured here: live model quality,
vendor service latency, token cost, or production runtime throughput.

The named framework rows are small reference surfaces written for this benchmark,
not full LangGraph, CrewAI, OpenAI Agents SDK, or Claude Code applications. The
rubric and baselines are authored in this repo. Treat this as a repo-state
assay, not an independent product ranking. `overall` is passed criteria divided
by 24.

```sh
python3 benchmarks/agentic_governance/score.py --check-summary
```

| surface | overall | restart | governance | runtime | files |
| --- | ---: | ---: | ---: | ---: | ---: |
| custom Python loop surface | 0.208 | 0.500 | 0.000 | 0.500 | 5 |
| LangGraph checkpoint surface | 0.417 | 0.800 | 0.133 | 1.000 | 9 |
| CrewAI flow surface | 0.542 | 0.800 | 0.333 | 1.000 | 11 |
| OpenAI Agents session surface | 0.500 | 0.800 | 0.267 | 1.000 | 9 |
| Claude Code project surface | 0.500 | 0.400 | 0.533 | 0.250 | 9 |
| generated harness | 0.958 | 0.900 | 1.000 | 0.750 | 150 |

The result is narrow but useful: runtime frameworks score higher on runtime
checkpoint semantics, while the generated harness scores higher on repo-local
governance, audit, and restart evidence. The larger file count is the cost of
that operating layer.

| track | baseline | generated harness |
| --- | ---: | ---: |
| MCP assurance | 0.300 permissive client | 1.000 |
| dissent preservation | 0.300 forced consensus fixture | 1.000 |

### Operational Resilience Policy Assay

Deterministic policy simulation for provider failover and human approval gates.
It does not call model providers, cloud runners, or external approval channels.
The baselines are synthetic controls authored in this repo, not competing
framework implementations. This is a policy-surface unit test for generated
harnesses.

```sh
python3 benchmarks/operational_resilience/score.py --check-summary
```

Provider failover policy surface:

| surface | score | completion policy | independent check policy |
| --- | ---: | ---: | ---: |
| single_vendor | 0.300 | 0.500 | 0.000 |
| retry_same_vendor | 0.350 | 0.625 | 0.000 |
| generated_harness_policy | 1.000 | 1.000 | 1.000 |

Approval gate policy surface:

| surface | score | false allow | false block | approval precision |
| --- | ---: | ---: | ---: | ---: |
| allow_all | 0.450 | 0.700 | 0.000 | 0.000 |
| block_all | 0.850 | 0.000 | 0.300 | 0.700 |
| generated_harness_policy | 1.000 | 0.000 | 0.000 | 1.000 |

The generated harness result is limited to these fixed scenarios. It does not
prove live failover accuracy, provider outage handling, or approval latency. It
verifies that generated projects contain model-routing and permission policies
before adapters are added.

### Runtime Persistence Smoke

Optional live dependency smoke. This one imports real packages through `uv` and
does not call LLM APIs.

```sh
uv run --python 3.12 \
  --with langgraph \
  --with crewai \
  --with openai-agents \
  python benchmarks/runtime_persistence/score.py --check-summary
```

Runtime package results:

| surface | score |
| --- | ---: |
| LangGraph memory checkpointer | 1.000 |
| CrewAI persisted flow | 0.900 |
| OpenAI Agents SQLite session | 1.000 |

Generated harness operating-layer smoke:

| surface | score |
| --- | ---: |
| generated harness restart evidence | 0.900 |

This confirms the intended boundary: runtime frameworks are strong at runtime
state persistence. The harness score is project restart evidence, not a runtime
reload primitive. The harness adds governance, cross-session handoff, policy,
reports, and evaluation structure around those runtimes.

### Website Example

Prompt:

```text
I want to build a sunglasses boutique website
```

<table>
  <tr>
    <td width="50%"><strong>Direct agent session</strong></td>
    <td width="50%"><strong>Generated harness loop</strong></td>
  </tr>
  <tr>
    <td><img src="assets/readme/sunglasses-codex-desktop.png" alt="Direct agent sunglasses site screenshot"></td>
    <td><img src="assets/readme/sunglasses-harness-desktop.png" alt="Harness generated sunglasses site screenshot"></td>
  </tr>
</table>

| generated artifacts | direct session | generated harness |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 | 27 |
| event records | 0 | 44 |
| restart handoff | no | yes |

These counts are process evidence. More files are not automatically better, and
this is not a claim that every harness-produced site will be visually better.
The screenshots show the artifact; the table shows the state left behind for
review and restart.

<details>
  <summary>Full page and mobile captures</summary>
  <table>
    <tr>
      <td width="50%"><strong>Direct full page</strong></td>
      <td width="50%"><strong>Harness full page</strong></td>
    </tr>
    <tr>
      <td width="50%"><img src="assets/readme/sunglasses-codex-desktop-full.png" alt="Direct full page sunglasses site screenshot"></td>
      <td width="50%"><img src="assets/readme/sunglasses-harness-desktop-full.png" alt="Harness generated full page sunglasses site screenshot"></td>
    </tr>
  </table>
  <table>
    <tr>
      <td width="50%"><strong>Direct mobile</strong></td>
      <td width="50%"><strong>Harness mobile</strong></td>
    </tr>
    <tr>
      <td width="50%"><img src="assets/readme/sunglasses-codex-mobile-full.png" alt="Direct mobile sunglasses site screenshot"></td>
      <td width="50%"><img src="assets/readme/sunglasses-harness-mobile-full.png" alt="Harness generated mobile sunglasses site screenshot"></td>
    </tr>
  </table>
</details>

### Date Normalization Regression

Challenge set: 36 public rows in
`benchmarks/date_normalization/cases.jsonl`. Each row contains an input phrase,
a reference date, locale assumptions, and the expected normalized date. This is
a regression fixture, not a hidden generalization benchmark.

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

| run | public fixture rows | accuracy | errors |
| --- | ---: | ---: | ---: |
| direct session | 36 | 83.3% | 6 |
| harness first pass | 36 | 72.2% | 10 |
| harness after feedback | 36 | 100.0% | 0 |

The first harness pass was worse. The useful behavior was the loop after
failure: failed cases were routed back into the same 36-row fixture, converted
into regression coverage, and reflected in the kit rules. This proves regression
capture, not generalization.

## Use When

- the project is larger than one answer
- multiple agents or sessions need shared state
- work needs planning, production, evaluation, and handoff
- failures should become reusable rules or eval cases
- another session should be able to resume from the repo alone

## Do Not Use When

- a one-file edit is enough
- speed matters more than traceability
- you already have durable execution and only need a runtime graph
- you cannot afford the extra governance files

## Limits

- This is a harness generator, not a hosted orchestration service
- It does not provide durable graph execution like a runtime framework
- The public benchmarks are small reproducible fixtures, not broad industry
  claims
- Account-specific posting, hosted dashboards, cloud runners, credentials, and
  private memory backends belong in project overlays

## Docs

- [Harness implementer manual](docs/HARNESS_IMPLEMENTER_MANUAL.md)
- [Operator manual](docs/OPERATOR_MANUAL.md)
- [Comparative survey](docs/COMPARATIVE_SURVEY_2026-05-24.md)
- [Benchmark report](docs/BENCHMARK_REPORT_2026-05-26.md)
- [Evaluation rubric](docs/EVALUATION_RUBRIC.md)
- [Optional extensions](docs/OPTIONAL_EXTENSIONS.md)

## 한국어

이 키트는 프로젝트 목표 하나를 받아 repo 안에 재개 가능한 agent 운영 구조를
생성한다

- 루트 상태 파일로 새 세션 재개
- operator worker evaluator 역할 분리
- shared context와 team context 기록
- events jsonl과 status html 생성
- 실패를 rule과 eval fixture로 되돌리는 루프
- public kit에는 개인 계정 연결, hosted dashboard, cloud runner,
  credential, private memory backend를 포함하지 않음
- framework 비교표는 실제 제품 순위가 아니라 이 repo에서 만든 작은
  reference surface 기준의 repo-state assay
- benchmark evidence는 영어 본문을 기준으로 유지하고 한국어는 동일한 claim
  boundary를 요약함

한 번의 답변보다 프로젝트 운영과 재개 가능성이 중요한 작업에 맞다. 단순한
파일 수정이나 이미 충분한 runtime graph가 있는 프로젝트에는 과하다.
