# Easy Orchestration Harness

[![CI](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml)

프로젝트 목표 하나로 멀티 에이전트 하네스를 만드는 도구

Codex와 Claude를 동등한 권한의 고정 `operator`로 두고, 프로젝트마다 필요한 `planning`, `design`, `production`, `evaluation`, `review` 흐름을 파일 기반으로 구성한다

웹사이트, 데이터 처리, 리서치, 운영 문서, 글쓰기처럼 결과물의 형태가 달라도 같은 방식으로 나누고, 검증하고, 다음 세션에서 이어갈 수 있게 만드는 것이 목적이다

| 같은 요청 | 일반 Codex `/goal` | 이 키트로 만든 하네스 |
| --- | --- | --- |
| 진행 방식 | 한 세션이 바로 제작 | 하네스 생성 후 operator가 작업 흐름을 운영 |
| 계획 | 대화 안에 남음 | PRD, anti PRD, 후보 작업, 승인 기록 |
| 작업 분리 | 단일 세션 중심 | operator, planner, worker, evaluator |
| 기억 | 채팅 의존 | shared context, team context, task packet |
| 검증 | 필요하면 수동으로 추가 | validator, eval, event log, status report |
| 재시작 | 사람이 다시 설명 | repo 파일만 읽고 이어가기 |

## 웹사이트 예시

프롬프트

```text
선글라스 편집숍을 만들고 싶다
```

<table>
  <tr>
    <td width="50%"><strong>Codex <code>/goal</code></strong></td>
    <td width="50%"><strong>Harness loop</strong></td>
  </tr>
  <tr>
    <td><img src="assets/readme/sunglasses-codex-desktop.png" alt="Direct Codex sunglasses site screenshot"></td>
    <td><img src="assets/readme/sunglasses-harness-desktop.png" alt="Harness generated sunglasses site screenshot"></td>
  </tr>
</table>

<details>
  <summary>전체 페이지와 모바일 캡처</summary>
  <p>위 이미지는 같은 1440x1100 viewport의 첫 화면이다. 아래에는 전체 페이지와 모바일 캡처를 접어 두었다.</p>
  <table>
    <tr>
      <td width="50%"><strong>Codex full page</strong></td>
      <td width="50%"><strong>Harness full page</strong></td>
    </tr>
    <tr>
      <td width="50%"><img src="assets/readme/sunglasses-codex-desktop-full.png" alt="Direct Codex full page sunglasses site screenshot"></td>
      <td width="50%"><img src="assets/readme/sunglasses-harness-desktop-full.png" alt="Harness generated full page sunglasses site screenshot"></td>
    </tr>
  </table>
  <table>
    <tr>
      <td width="50%"><strong>Codex mobile full page</strong></td>
      <td width="50%"><strong>Harness mobile full page</strong></td>
    </tr>
    <tr>
      <td width="50%"><img src="assets/readme/sunglasses-codex-mobile-full.png" alt="Direct Codex mobile full page sunglasses site screenshot"></td>
      <td width="50%"><img src="assets/readme/sunglasses-harness-mobile-full.png" alt="Harness generated mobile full page sunglasses site screenshot"></td>
    </tr>
  </table>
</details>

| 항목 | Codex `/goal` | Harness loop |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 README 중심 | 27 |
| event records | 0 | 44 |
| desktop and mobile screenshots | yes | yes |
| planning to operator closure | no | yes |
| restart handoff | no | yes |

Codex도 빠르게 쓸 만한 정적 사이트를 만들었다. 하네스 쪽은 더 무겁지만 이미지 자산, 역할별 기록, 검증 근거, 재시작 파일까지 같이 남겼다. 포트폴리오나 팀 작업처럼 결과물만큼 과정의 재현성이 중요한 경우에 차이가 난다

## 날짜 정규화 벤치마크

프롬프트

```text
기준 날짜 2026-05-25 월요일을 기준으로 한국어 업무 문장의 마감일 표현을 ISO 날짜로 정규화하는 offline CLI와 eval framework를 만든다
```

입출력

- input JSONL `{id,text}`
- output JSONL `{id,date}`
- 오늘, 내일, 이번주 요일, 다음주 요일, 다음달 영업일, 월말, 분기말, N일 후, N주 후, 명시적 날짜, 취소와 변경 표현 처리
- 날짜를 확정할 수 없으면 `UNKNOWN`

평가

- 각 방식은 자신이 만든 공개 정답셋에서는 모두 100% 통과
- 별도 challenge set 36개로 다시 채점
- challenge set에는 `내주`, `다다음 주`, `다음 달 말`, `분기 마지막 영업일`, `내일이 아니라 금요일`, `취소 후 재설정`, `요일 변경`, `6월 둘째 화요일` 같은 표현 포함

| 항목 | Codex `/goal` | Harness 1차 | Harness 피드백 후 |
| --- | ---: | ---: | ---: |
| 공개 정답셋 행 수 | 41 | 47 | 57 |
| 공개 정답셋 정확도 | 100.0% | 100.0% | 100.0% |
| challenge set 정확도 | 83.3% | 72.2% | 100.0% |
| challenge set 오류 수 | 6 | 10 | 0 |
| 실패 후 작업 재개 | no | 필요했음 | yes |
| 실패 케이스 회귀 테스트화 | no | no | yes |
| 키트 규칙 수정 | no | no | yes |
| 재시작 handoff | no | yes | yes |

재현

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

1차 결과는 direct Codex보다 낮았다. 차이는 실패를 처리하는 방식에서 나왔다. 외부 challenge 결과를 바로 정답처럼 섞지 않고, 새 피드백 작업으로 열고, 실패 케이스를 담당 파일과 평가셋에 반영한 뒤 다시 닫았다. 이 과정에서 공개 정답셋만으로 deterministic 작업을 통과 처리하지 않는 규칙도 키트에 추가했다

## 만들어지는 파일

```text
project/
  AGENTS.md
  CLAUDE.md
  feature_list.json
  progress.md
  session-handoff.md
  .claude/
  harness/
    operators/
    teams/
    shared/
    tasks/
    events/events.jsonl
    evals/
    reports/
    viz/
    broadcast/
    reviewers/
    runtime/
    mcp_server/
```

## 작동 방식

- `operator`는 검증된 모델 중 가장 강한 설정과 높은 reasoning effort 사용
- `worker`는 작업 난이도에 맞춰 더 낮은 모델과 effort 사용
- 큰 작업을 맡은 worker 세션은 같은 영역을 다시 열 때 재사용
- worker마다 수정 가능한 파일과 수정 금지 파일을 분리
- 기획 단계에서 후보 작업을 고른 뒤 좁고 깊게 진행
- 내부 작업 기록과 외부 공개 기록을 분리
- 공개 정답셋만으로 deterministic 품질을 통과 처리하지 않음
- challenge eval, 독립 리뷰, 명시적 WARN 중 하나 필요
- 실패와 반복 패턴은 failure ledger와 rule change log에 남김
- Markdown 지시는 단독 권위가 아니라 hook, validator, event, task packet으로 확인

## 시각화와 외부 기록

기본으로 제공되는 것

- `harness/events/events.jsonl`
- `python3 scripts/harnessctl.py report`
- `python3 scripts/harnessctl.py viz-export --backend local_file`
- `harness/reports/status.html`
- `harness/reports/viz/summary.json`

외부 backend 연동 전 정할 것

- task-local `VISUALIZATION_SPEC.md`
- 표시할 의사결정과 source artifacts
- redaction 기준
- update cadence
- credential lifecycle
- smoke evidence
- operator review

역할 기준

- bitmap image, product photo, hero image, mock photograph는 Codex image generation 담당
- diagram, timeline, dashboard information architecture는 Claude Code 담당
- public kit에서는 외부 publication connector를 켜지 않음
- social, blog, webhook, cloud, private RAG backend는 project overlay에서 연결

## 설치

```sh
git clone https://github.com/SihyeonJeon/easy-orchestration-harness.git
cd easy-orchestration-harness
python3 scripts/validate_kit.py
```

benchmark 재현

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

프로젝트 하네스 생성

```sh
python3 scripts/scaffold_harness.py \
  --target ../my-project \
  --goal "사용자가 원하는 프로젝트 목표"
```

생성한 프로젝트에서 시작

```sh
cd ../my-project
./init.sh
python3 scripts/harnessctl.py report
```

operator 세션에서 입력

```text
you are operator
```

## 권장 사용처

- 한 번의 답변보다 프로젝트 완수가 중요한 일
- 여러 agent가 계획, 제작, 평가, 수정 루프를 나눠야 하는 일
- 결과물뿐 아니라 판단 근거와 검증 기록이 필요한 일
- 웹, 앱, 데이터, 연구, 보고서, 운영, 교육, 콘텐츠처럼 domain이 고정되지 않은 일

## 비권장 사용처

- 한 파일의 짧은 수정
- 기록과 검증보다 속도가 중요한 일회성 작업
- 이미 LangGraph, CrewAI, custom runtime 안에서 durable execution만 필요한 경우

## 문서

- [Comparative survey](docs/COMPARATIVE_SURVEY_2026-05-24.md)
- [Evaluation rubric](docs/EVALUATION_RUBRIC.md)
- [Optional extensions](docs/OPTIONAL_EXTENSIONS.md)
- [Harness implementer manual](docs/HARNESS_IMPLEMENTER_MANUAL.md)
- [Operator manual](docs/OPERATOR_MANUAL.md)

## In English

Easy Orchestration Harness turns one project goal into a file-backed multi-agent harness

It keeps Codex and Claude as equal fixed operators, then lays out the project files for planning, worker ownership, shared memory, evaluation, visualization policy, external record boundaries, and restartable operation

It is not a replacement for LangGraph, CrewAI, OpenAI Agents SDK, Claude Code, or other runtimes. It is the governance and evidence layer around whichever agent runtime the project chooses

## Why

Direct agent sessions can produce strong outputs, but the operating history often stays inside chat

This kit makes the work inspectable

- what was planned
- what was rejected
- which worker owned which path
- what changed
- what was tested
- what remains risky
- how the next session resumes

## Results

Website demo

| Metric | Codex `/goal` | Harness loop |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 README focused | 27 |
| event records | 0 | 44 |
| planning to closure records | no | yes |

Date-normalization benchmark

| Metric | Codex `/goal` | Harness first pass | Harness after feedback |
| --- | ---: | ---: | ---: |
| visible golden rows | 41 | 47 | 57 |
| visible golden accuracy | 100.0% | 100.0% | 100.0% |
| challenge accuracy | 83.3% | 72.2% | 100.0% |
| challenge errors | 6 | 10 | 0 |
| feedback slice reopened | no | needed | yes |
| failures added as regression cases | no | no | yes |
| rule changed | no | no | yes |
| restart handoff | no | yes | yes |

The first harness result was not better. The useful behavior was the loop after failure. Challenge feedback reopened the work, routed accepted failures back into parser and eval files, converted them into regression cases, and then updated the kit rule

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

Then open an operator session and say

```text
you are operator
```

Reproduce the benchmark table

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

## Extension Model

Included by default

- local events and status report
- local visualization export
- broadcast draft queue
- reviewer packet descriptors
- read-only MCP export
- disabled cloud runner descriptors
- file-backed memory and optional backend contracts

Connected per project

- publication adapters
- reviewer models or services
- cloud execution lanes
- hosted visualization backends
- vector or graph memory backends
- credentials and account-specific policy

Every external connector starts disabled until bounded policy, credential lifecycle, smoke evidence, and operator review exist
