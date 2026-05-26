# Easy Orchestration Harness

[![CI](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A file-backed harness generator for restartable agent projects

It turns one project goal into a repo-local operating layer for Claude Code,
Codex, Cursor, LangGraph apps, CrewAI flows, OpenAI Agents SDK apps, or custom
agent loops. The generated project has explicit operator and worker roles,
shared state, event logs, evaluation fixtures, status reports, and a restart
path that survives the original conversation.

## Why This Exists

Strong agent sessions still lose project state when the useful context lives
only in chat memory.

This kit writes the operating state into the project:

- goal, constraints, unknowns, and acceptance criteria
- operator, evaluator, and worker responsibilities
- owned paths and no-touch paths for each work packet
- shared context, team context, and handoff notes
- append-only event records and local HTML status reports
- failed cases converted into rules and regression fixtures
- restart instructions for the next session

## Quick Start

```sh
git clone https://github.com/SihyeonJeon/easy-orchestration-harness.git
cd easy-orchestration-harness

python3 scripts/scaffold_harness.py \
  --target ../my-project \
  --goal "your project goal"

cd ../my-project
./init.sh
python3 scripts/harnessctl.py report
```

Open the generated project in your agent tool and let it read `AGENTS.md`.

```text
you are operator
```

To verify the public kit itself:

```sh
python3 scripts/validate_kit.py
```

## What It Generates

```text
project/
  AGENTS.md
  CLAUDE.md
  README.md
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
    reports/viz/
    runtime/
    mcp_server/
```

## Operating Model

| Layer | What it gives the project |
| --- | --- |
| harness implementer | converts a goal into project-local operating files |
| operator | routes work, reviews gates, decides closure |
| worker teams | handle planning, design, production, and evaluation lanes |
| part ownership | sends the same part back to the same worker session when safe |
| hooks and validators | enforce lifecycle checks beyond markdown instructions |
| executable helpers | generate context packs, worker briefs, task packets, model routes, and software feedback evidence |
| event log | records task, gate, and eval evidence as append-only state |
| status report | renders canonical state into local HTML and JSON |
| MCP export | exposes read-only local project state for compatible tools |

Workers can use cheaper models for routine packets. Operators should use the
strongest model and effort setting available for review, routing, and closure.
The kit does not force one vendor or runtime.

Generated routing policy names `sonnet`, `haiku`, and
`gpt-5.3-codex-spark` as routine-task aliases when they are available and
verified in the local environment. Operators still keep the strongest verified
model and effort for routing, review, and closure.

Token saving is handled through bounded context packs, part-owner session
reuse, a four-plugin cap with a `caveman` compression slot, and compact
agent-to-agent packets that cite evidence paths instead of forwarding full
transcripts.

Repeatable domain-neutral steps are executable through `scripts/harnessctl.py`:
`context-pack`, `worker-brief`, `model-route`, `task-packet`, and
`software-feedback`. The remaining markdown files describe judgment boundaries
and project-specific reasoning rather than asking agents to manually repeat
stable mechanics.

## How It Differs From Runtime Frameworks

Easy Orchestration Harness is not a graph runtime. It is the operating layer
around agent tools and runtimes.

| Dimension | Runtime frameworks | Easy Orchestration Harness |
| --- | --- | --- |
| execution | graph, flow, session, checkpoint | repo-local project operating system |
| adoption | application code integration | scaffold into any project directory |
| operators | usually app-defined | fixed dual-operator protocol with dissent preservation |
| worker routing | usually runtime or app policy | part ownership, worker reuse, model and effort tiering |
| restart | runtime state or chat history | files, events, status report, handoff, eval output |
| governance | app-specific | generated policies, hooks, validators, and task packets |
| evidence | traces or logs | event log, local HTML report, benchmark fixtures |
| safety boundary | provider or app guardrails | MCP trust, permission policy, credential lifecycle, budget caps |
| software feedback | usually project-defined | lint/static checks, runtime smoke, Playwright or equivalent browser/device evidence, UI/UX/layout review |

Use LangGraph, CrewAI, OpenAI Agents SDK, Claude Code, Codex, or custom loops
for execution when they fit. Use this kit when the project needs durable
operating state across sessions, tools, and agent roles.

## Use It For

- work that is larger than one answer
- projects that need multiple agent sessions or tools
- planning, production, evaluation, and handoff as separate phases
- repeatable restart after an interrupted session
- turning failures into rules, tests, and eval fixtures

## Do Not Use It For

- a one-file edit
- a disposable prototype where traceability does not matter
- replacing a runtime graph or checkpoint system
- projects that cannot tolerate extra governance files

## Evidence

Public fixtures were last updated on 2026-05-26. They are small reproducible
regression checks, not broad industry rankings.

| Fixture | Scope | Current result |
| --- | --- | --- |
| requirements traceability | generated harness requirements reflected in public-safe files | 189/189 checks |
| spec gate | planning surfaces before production work | 12/12 checks |
| static visualization | local status HTML, JSON, sanitized event export | 12/12 checks |
| replay recovery | file-only restart surface across 10 task shapes | generated harness 1.000, controls 0.110 and 0.500 |
| bilingual README parity | Korean and English generated-project operating sections | 14/14 checks |
| budget governance | task caps, runner kill procedures, local budget-check event surface | covered in traceability and generated validator |
| software feedback | coding work requires lint/runtime/browser evidence policy and executable evidence packet | generated policy, runner, and validator surface |
| cloud runner policy | disabled-by-default remote descriptors and policy docs | 10/10 descriptor, 10/10 policy |
| date normalization loop | failed cases captured into the next regression pass | 83.3% direct, 72.2% first pass, 100.0% after feedback |

Detailed commands, scope boundaries, and comparison tables are in
[Benchmarks](docs/BENCHMARKS.md) and the dated
[benchmark report](docs/BENCHMARK_REPORT_2026-05-26.md).

## Website Example

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

| Process residue | Direct session | Generated harness |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 | 27 |
| event records | 0 | 44 |
| restart handoff | no | yes |

The screenshots show one artifact comparison. The counts show what state was
left behind for review and restart. More files are not automatically better;
the point is that the second run leaves an operating record another session can
use.

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

## Limits

- this is a harness generator, not a hosted orchestration service
- it does not provide durable graph execution by itself
- runtime frameworks remain useful for checkpointing, graph execution, tracing,
  and provider integrations
- public benchmarks are deterministic fixtures with stated boundaries
- live token, cost, latency, and model-variance benchmarks are Phase 2 work
- account-specific publishing, hosted dashboards, cloud jobs, credentials, and
  private memory backends belong in project overlays

## Docs

- [Docs index](docs/README.md)
- [Harness implementer manual](docs/HARNESS_IMPLEMENTER_MANUAL.md)
- [Operator manual](docs/OPERATOR_MANUAL.md)
- [Benchmarks](docs/BENCHMARKS.md)
- [Phase 2 benchmark roadmap](docs/PHASE2_BENCHMARK_ROADMAP.md)
- [Requirement traceability](docs/REQUIREMENT_TRACEABILITY_2026-05-26.md)
- [Evaluation rubric](docs/EVALUATION_RUBRIC.md)
- [Optional extensions](docs/OPTIONAL_EXTENSIONS.md)

## 한국어

Easy Orchestration Harness는 프로젝트 목표 하나를 받아 재개 가능한 agent
운영 구조를 repo 안에 생성하는 키트다.

생성되는 프로젝트는 operator, worker, evaluator 역할을 분리하고, 공유
콘텍스트와 팀 콘텍스트, 이벤트 로그, 로컬 status report, eval fixture,
handoff 파일을 남긴다. 다음 세션은 이전 대화를 읽지 않아도 repo에 남은
상태로 작업을 이어갈 수 있다.

### 빠른 시작

```sh
git clone https://github.com/SihyeonJeon/easy-orchestration-harness.git
cd easy-orchestration-harness

python3 scripts/scaffold_harness.py \
  --target ../my-project \
  --goal "프로젝트 목표"

cd ../my-project
./init.sh
python3 scripts/harnessctl.py report
```

그 다음 생성된 프로젝트에서 agent tool을 열고 `AGENTS.md`를 읽게 한 뒤
다음처럼 시작한다.

```text
you are operator
```

### 적합한 작업

- 한 번의 답변보다 긴 프로젝트
- 여러 agent session 또는 여러 도구가 함께 다루는 프로젝트
- 기획, 제작, 평가, 인수인계를 분리해야 하는 작업
- 중단 후 repo 상태만 보고 재개해야 하는 작업
- 실패 사례를 rule과 regression fixture로 되돌려야 하는 작업

### 공개 버전의 경계

- 개인 계정 자동 게시 기능 없음
- 활성 cloud runner 없음
- hosted dashboard 없음
- credential 없음
- private memory backend 없음
- 공개 benchmark는 작은 재현 fixture이며 업계 전체 순위가 아님

세부 검증 결과는 [Benchmarks](docs/BENCHMARKS.md)와
[Requirement traceability](docs/REQUIREMENT_TRACEABILITY_2026-05-26.md)에
정리되어 있다.
