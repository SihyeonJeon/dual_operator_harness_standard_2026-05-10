# Easy Orchestration Harness

Dual operator multi-agent orchestration harness architecture 생성 키트

목표 하나를 프로젝트별 운영 하네스로 바꾸는 키트

Codex와 Claude를 동등한 고정 operator로 두고 planning, design, production, evaluation, operator review를 파일 기반으로 운영

웹 개발, LLM eval, 리서치, 운영, 글쓰기, 데이터 워크플로처럼 산출물 형태가 달라도 같은 구조로 분해, 협업, 교차 검증, 재시작 가능

| 같은 목표 | 일반 Codex `/goal` | 이 키트로 생성한 하네스 |
| --- | --- | --- |
| 운영 방식 | 한 세션이 바로 제작 | implementer가 하네스 생성, operator가 팀 구성과 루프 운영 |
| 계획 | 대화 안에 묻힘 | PRD, anti PRD, candidate slice, approval gate |
| 분업 | 단일 세션 중심 | fixed operator, planning, design, coding, evaluation worker |
| 메모리 | 채팅 의존 | shared context, team context, task packet, handoff |
| 검증 | 선택 사항 | validator, eval suite, event trace, status report |
| 재시작 | 사람이 재구성 | repo 파일만 읽고 이어가기 |

## 웹 개발 비교

실험 입력

```text
선글라스 편집숍을 만들고 싶다
```

<table>
  <tr>
    <td width="50%"><strong>Codex session <code>/goal</code></strong></td>
    <td width="50%"><strong>Generated harness loop</strong></td>
  </tr>
  <tr>
    <td><img src="assets/readme/sunglasses-codex-desktop.png" alt="Direct Codex sunglasses site screenshot"></td>
    <td><img src="assets/readme/sunglasses-harness-desktop.png" alt="Harness generated sunglasses site screenshot"></td>
  </tr>
</table>

<details>
  <summary>전체 페이지와 모바일 캡처</summary>
  <p>첫 표는 같은 1440x1100 viewport의 첫 화면 비교입니다. 아래는 전체 페이지와 모바일 전체 페이지입니다.</p>
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
| planning, design, coding, evaluation, operator closure | no | yes |
| restart handoff | no | yes |

해석

- direct Codex도 빠르게 완성도 있는 정적 사이트를 만들었음
- 하네스 루프는 더 무겁지만 실제 제품 이미지 자산, 역할별 산출물, 검증 기록, 재시작 상태까지 남겼음
- 포트폴리오나 팀 작업처럼 결과물뿐 아니라 과정과 품질 판단 근거가 필요한 경우 하네스 쪽이 더 강함

## 어려운 정량 task 비교

실험 입력

```text
기준 날짜 2026-05-25 월요일을 기준으로 한국어 업무 문장의 마감일 표현을 ISO 날짜로 정규화하는 offline CLI와 eval framework를 만든다
```

입력 계약

- JSONL input `{id,text}`
- JSONL output `{id,date}`
- 오늘, 내일, 이번주 요일, 다음주 요일, 다음달 영업일, 월말, 분기말, N일 후, N주 후, 명시적 날짜, 취소와 변경 표현 처리
- 알 수 없거나 취소 후 재설정 없는 행은 `UNKNOWN`

평가 방식

- 각 방식이 만든 visible golden set은 자기 검증으로 통과
- 별도 held out challenge set 36개로 재평가
- challenge set은 `내주`, `다다음 주`, `다음 달 말`, `분기 마지막 영업일`, `내일이 아니라 금요일`, `취소 후 재설정`, `요일 변경`, `6월 둘째 화요일` 같은 visible set 바깥 표현 포함

| 항목 | Codex `/goal` | Harness first pass | Harness feedback loop |
| --- | ---: | ---: | ---: |
| visible golden rows | 41 | 47 | 57 |
| visible golden accuracy | 100.0% | 100.0% | 100.0% |
| held out challenge accuracy | 83.3% | 72.2% | 100.0% |
| held out errors | 6 | 10 | 0 |
| feedback slice reopened | no | needed | yes |
| accepted failures promoted to regression fixtures | no | no | yes |
| rule change produced | no | no | yes |
| restart handoff | no | yes | yes |

해석

- 초회 harness 결과는 direct Codex보다 낮았음
- 이 실패가 핵심 신호였음
- operator가 외부 challenge 결과를 canonical memory로 바로 섞지 않고 F2 feedback slice로 요약, 라우팅, 수정, 재평가
- accepted hidden failures를 local regression fixture로 승격
- 키트 자체에도 held out challenge eval gate를 추가
- direct `/goal`은 빠른 산출물에는 강하지만 실패 이후의 운영 규율, 재개 가능한 task state, rule evolution은 자동으로 남기지 않음
- 이 데모의 차이는 첫 산출물 우열이 아니라 실패를 발견한 뒤 구조적으로 정확도를 끌어올리는 능력

## 생성되는 구조

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

핵심 규율

- operator는 항상 최고 모델과 높은 effort 기준
- worker는 task 난이도와 위험도에 따라 모델과 effort를 낮춰 비용 절약
- 큰 part를 맡은 worker session은 해당 part가 다시 열릴 때 재호출
- worker마다 owned paths와 no touch paths를 명시
- planning runway 이후 sharp and deep 실행
- 내부 콘텍스트와 외부 채널 기록 분리
- visible golden set만으로 deterministic quality claim을 passing 처리하지 않음
- held out challenge eval, independent reviewer, accepted WARN 중 하나 필요
- 실패와 성공은 failure ledger, rule change log, regulation evolution으로 누적
- MD 지시는 단독 권위가 아니라 hook, validator, event, task packet으로 확인

## 시각화와 외부 기록

기본 제공

- `harness/events/events.jsonl`
- `python3 scripts/harnessctl.py report`
- `python3 scripts/harnessctl.py viz-export --backend local_file`
- `harness/reports/status.html`
- `harness/reports/viz/summary.json`

외부 backend 연결 조건

- task-local `VISUALIZATION_SPEC.md` 먼저 작성
- 표시할 의사결정, source artifacts, redaction, update cadence 확정
- Claude Code가 dashboard, timeline, diagram, report information architecture 검토
- worker가 `events.jsonl` to backend adapter 구현
- bounded policy, credential lifecycle, smoke evidence, operator review 통과

자산 생성 규율

- bitmap image, product photo, hero image, mock photograph는 Codex image generation 담당
- diagram, timeline, dashboard information architecture는 Claude Code 담당
- 외부 publication connector는 public kit 안에서 활성화하지 않음
- 실제 social, blog, webhook, cloud, private RAG backend는 project overlay에서 연결

## 설치와 사용

```sh
git clone https://github.com/SihyeonJeon/easy-orchestration-harness.git
cd easy-orchestration-harness
python3 scripts/validate_kit.py
```

프로젝트 하네스 생성

```sh
python3 scripts/scaffold_harness.py \
  --target ../my-project \
  --goal "사용자가 원하는 프로젝트 목표"
```

생성된 프로젝트에서 시작

```sh
cd ../my-project
./init.sh
python3 scripts/harnessctl.py report
```

operator session에서 입력

```text
you are operator
```

## 언제 쓰는가

- 한 번의 답변보다 프로젝트 완수가 중요한 작업
- 여러 agent가 계획, 제작, 평가, 수정 루프를 나눠야 하는 작업
- 산출물뿐 아니라 판단 근거, 검증 기록, 재시작 가능성이 필요한 작업
- 웹, 앱, 데이터, 연구, 보고서, 운영, 교육, 콘텐츠처럼 domain이 고정되지 않은 작업

맞지 않는 경우

- 한 파일의 짧은 수정
- 기록과 검증보다 속도가 중요한 일회성 작업
- 이미 LangGraph, CrewAI, custom runtime 안에서 durable execution만 필요한 경우

## 관련 문서

- [Comparative survey](docs/COMPARATIVE_SURVEY_2026-05-24.md)
- [Evaluation rubric](docs/EVALUATION_RUBRIC.md)
- [Optional extensions](docs/OPTIONAL_EXTENSIONS.md)
- [Harness implementer manual](docs/HARNESS_IMPLEMENTER_MANUAL.md)
- [Operator manual](docs/OPERATOR_MANUAL.md)

## English

Easy Orchestration Harness turns one project goal into a project-local dual-operator multi-agent harness

It keeps Codex and Claude as equal fixed operators, then generates the files needed for planning, worker ownership, shared memory, evaluation, visualization policy, external record boundaries, and restartable operation

The kit is not a replacement for LangGraph, CrewAI, OpenAI Agents SDK, Claude Code, or other runtimes

It is the governance and evidence layer around whichever agent runtime the project chooses

## Why It Exists

Direct agent sessions can produce strong outputs, but the operating history often stays inside chat

This kit makes the work inspectable

- what was planned
- what was rejected
- which worker owned which path
- what changed
- what was tested
- what remains risky
- how the next session resumes

## Demo Results

Website demo

| Metric | Codex `/goal` | Harness loop |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 README focused | 27 |
| event records | 0 | 44 |
| planning to closure records | no | yes |

Quantitative challenge demo

Korean business deadline normalization CLI and eval framework

| Metric | Codex `/goal` | Harness first pass | Harness feedback loop |
| --- | ---: | ---: | ---: |
| visible golden rows | 41 | 47 | 57 |
| visible golden accuracy | 100.0% | 100.0% | 100.0% |
| held out challenge accuracy | 83.3% | 72.2% | 100.0% |
| held out errors | 6 | 10 | 0 |
| feedback slice reopened | no | needed | yes |
| accepted failures promoted to regression fixtures | no | no | yes |
| rule change produced | no | no | yes |
| restart handoff | no | yes | yes |

The first harness result was not better

The useful behavior was the loop after failure

External challenge feedback was summarized into a new F2 slice, routed back to parser and eval artifacts, converted into regression fixtures, rerun, and then promoted into kit governance as a held out challenge eval gate

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

## Public Extension Model

Included by default

- local events and status report
- local visualization export
- broadcast draft queue
- reviewer packet descriptors
- read-only MCP export
- disabled cloud runner descriptors
- file-backed memory and optional backend contracts

Connected per project

- real publication adapters
- real reviewer models or services
- cloud execution lanes
- hosted visualization backends
- vector or graph memory backends
- credentials and account-specific policy

Every external connector starts disabled until bounded policy, credential lifecycle, smoke evidence, and operator review exist
