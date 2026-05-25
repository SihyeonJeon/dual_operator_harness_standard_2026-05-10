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

Then open your agent session in the generated project and use the operator entry
phrase:

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

Workers can use lower-cost models when the task is routine. Operators stay on
the strongest verified settings available for review, routing, and closure.
Large work is split into parts, and the same part can return to the same worker
session when that is safe.

## Evidence

### Recovery Fixture

This fixture measures restart readiness after an interrupted agent project. It
does not measure model intelligence or final output quality.

```sh
python3 benchmarks/replay_recovery/score.py --check-summary
```

| run | recovery artifacts | recoverable facts | event count | score |
| --- | ---: | ---: | ---: | ---: |
| direct session | 1/10 | 1/8 | 0 | 0.11 |
| generated harness | 10/10 | 7/8 | 7 | 0.95 |

The generated harness leaves restart files, machine-readable state, evaluator
output, event history, and a local status report. A direct transcript keeps much
less recoverable state unless the human creates that structure manually.

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

| metric | direct session | generated harness |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 | 27 |
| event records | 0 | 44 |
| restart handoff | no | yes |

These counts are process evidence, not a claim that every harness-produced site
will be visually better. The screenshots show the artifact; the table shows the
state left behind for review and restart.

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

### Date Normalization Fixture

This is a public regression fixture, not a hidden generalization benchmark.

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

| run | public fixture rows | accuracy | errors |
| --- | ---: | ---: | ---: |
| direct session | 36 | 83.3% | 6 |
| harness first pass | 36 | 72.2% | 10 |
| harness after feedback | 36 | 100.0% | 0 |

The first harness pass was worse. The useful behavior was the loop after
failure: failed cases were routed back into the task, converted into regression
coverage, and reflected in the kit rules.

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
- [Evaluation rubric](docs/EVALUATION_RUBRIC.md)
- [Optional extensions](docs/OPTIONAL_EXTENSIONS.md)

## Korean Summary

이 키트는 프로젝트 목표 하나를 받아 repo 안에 재개 가능한 agent 운영 구조를
생성한다

- 루트 상태 파일로 새 세션 재개
- operator worker evaluator 역할 분리
- shared context와 team context 기록
- events jsonl과 status html 생성
- 실패를 rule과 eval fixture로 되돌리는 루프
- public kit에는 개인 계정 연결이나 게시 기록 기능을 포함하지 않음

한 번의 답변보다 프로젝트 운영과 재개 가능성이 중요한 작업에 맞다. 단순한
파일 수정이나 이미 충분한 runtime graph가 있는 프로젝트에는 과하다.
