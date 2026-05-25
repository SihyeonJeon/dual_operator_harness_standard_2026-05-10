# Dual Operator Multi Agent Orchestration Harness Kit

[![CI](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/SihyeonJeon/easy-orchestration-harness/actions/workflows/ci.yml)

프로젝트 목표 하나로 파일 기반 멀티 에이전트 하네스를 만드는 키트

Codex와 Claude를 동등한 고정 `operator`로 두고, 프로젝트마다 필요한 `planning`, `design`, `production`, `evaluation`, `review` 흐름을 생성한다

웹사이트, 데이터 처리, 리서치, 운영 문서, 글쓰기처럼 결과물의 형태가 달라도 같은 방식으로 나누고, 검증하고, 다음 세션에서 이어갈 수 있게 만드는 것이 목적이다

| 구분 | 직접 Codex Claude 세션 | LangGraph CrewAI 같은 런타임 | 이 키트 |
| --- | --- | --- | --- |
| 주 역할 | 산출물 생성 | agent graph와 runtime 실행 | 프로젝트별 운영 구조 생성 |
| 계획 기록 | 대화 안에 남기 쉬움 | 직접 구현 필요 | PRD anti PRD 후보 slice 승인 기록 |
| 작업 분리 | 사람이 계속 지시 | framework 코드로 구성 | operator team worker evaluator 파일 생성 |
| 기억 | 세션 문맥 중심 | runtime memory 중심 | shared context team context task packet |
| 검증 | 사람이 별도 추가 | framework별 tracing eval 연동 | validator eval event log status report |
| 재시작 | 사람이 다시 설명 | checkpoint 구현 방식에 의존 | repo 파일만 읽고 operator 재개 |
| 적합한 위치 | 빠른 단발 작업 | 제품 런타임과 durable execution | agent를 어떻게 나눠 굴릴지 정하는 governance layer |

## 웹사이트 예시

프롬프트

```text
선글라스 편집숍을 만들고 싶다
```

<table>
  <tr>
    <td width="50%"><strong>직접 Codex 세션</strong></td>
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

| 항목 | 직접 Codex 세션 | Harness loop |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 README 중심 | 27 |
| event records | 0 | 44 |
| desktop and mobile screenshots | yes | yes |
| operator closure record | no | yes |
| restart handoff | no | yes |

Codex도 빠르게 쓸 만한 정적 사이트를 만들었다. 하네스 쪽은 더 무겁지만 이미지 자산, 역할별 기록, 검증 근거, 재시작 파일까지 같이 남겼다. 포트폴리오나 팀 작업처럼 결과물만큼 과정의 재현성이 중요한 경우에 차이가 난다

## 날짜 정규화 벤치마크

프롬프트

```text
2026-05-25 월요일을 기준으로 한국어 업무 문장의 마감일 표현을 ISO 날짜로 정규화하는 offline CLI와 eval framework를 만든다
```

입출력

- input JSONL `{id,text}`
- output JSONL `{id,date}`
- 오늘, 내일, 이번주 요일, 다음주 요일, 주 지칭 표현, 다음달 첫 영업일과 마지막 영업일, 월말, 분기말, N일 후, N주 후, 월 서수 요일, 명시적 날짜, 취소와 변경 표현 처리
- 날짜를 확정할 수 없으면 `UNKNOWN`

평가 기준

- 같은 공개 평가 파일 `benchmarks/date_normalization/cases.jsonl`
- 36개 한국어 업무 문장과 기대 ISO 날짜
- 포함 표현 `내주`, `다다음 주`, `다음 달 말`, `분기 마지막 영업일`, `내일이 아니라 금요일`, `취소 후 재설정`, `요일 변경`, `6월 둘째 화요일`
- 각 방식의 예측 파일은 `benchmarks/date_normalization/predictions/`
- 이 36행은 공개 회귀 fixture이며 일반화 성능을 주장하는 hidden benchmark가 아님

| 항목 | 직접 Codex 세션 | Harness 1차 | Harness 피드백 후 |
| --- | ---: | ---: | ---: |
| 공개 평가 파일 | 36 rows | 36 rows | 36 rows |
| 정확도 | 83.3% | 72.2% | 100.0% |
| 오류 수 | 6 | 10 | 0 |
| 실패 케이스 회귀 테스트화 | no | no | yes |
| 키트 규칙 수정 | no | no | yes |
| 재현 명령 | yes | yes | yes |

재현

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

1차 결과는 직접 Codex 세션보다 낮았다. 이 결과를 숨기지 않고 피드백 작업으로 열어 실패 케이스를 담당 규칙과 평가 파일에 반영했다. 그 뒤 공개 회귀 fixture 36개 기준 100%를 확인했고, deterministic 작업은 보이는 예시만으로 통과 처리하지 않는 규칙을 키트에 추가했다

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
    runtime/
    mcp_server/
```

## 작동 방식

- `operator`는 검증된 모델 중 가장 강한 설정과 높은 reasoning effort 사용
- `worker`는 작업 난이도에 맞춰 더 낮은 모델과 effort 사용
- 작업을 큰 토막으로 나누고 같은 토막은 같은 worker 세션이 다시 맡도록 기록
- worker마다 수정 가능한 파일과 수정 금지 파일을 분리
- 기획 단계에서 후보 작업을 고른 뒤 좁고 깊게 진행
- 내부 작업 기록과 로컬 리포트 뷰를 분리
- deterministic 품질 주장은 별도 평가 파일, 독립 평가, 명시적 WARN 중 하나 필요
- 실패와 반복 패턴은 failure ledger와 rule change log에 남김
- Markdown 지시는 단독 권위가 아니라 hook, validator, event, task packet으로 확인

## 시각화와 로컬 기록

기본으로 제공되는 것

- `harness/events/events.jsonl`
- `python3 scripts/harnessctl.py report`
- `python3 scripts/harnessctl.py viz-export --backend local_file`
- `harness/reports/status.html`
- `harness/reports/viz/summary.json`

비로컬 backend 연동 전 정할 것

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
- public kit에는 게시 draft queue, social connector, private review ledger를 넣지 않음
- cloud runner, hosted viz, private RAG backend는 project overlay에서 연결

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

It keeps Codex and Claude as equal fixed operators, then lays out the project files for planning, worker ownership, shared memory, evaluation, visualization policy, local record policy, and restartable operation

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

| Metric | Direct Codex session | Harness loop |
| --- | ---: | ---: |
| site files | 3 | 8 |
| generated bitmap assets | 0 | 5 |
| task evidence files | 1 README focused | 27 |
| event records | 0 | 44 |
| operator closure records | no | yes |

Date-normalization benchmark

| Metric | Direct Codex session | Harness first pass | Harness after feedback |
| --- | ---: | ---: | ---: |
| public evaluation rows | 36 | 36 | 36 |
| accuracy | 83.3% | 72.2% | 100.0% |
| errors | 6 | 10 | 0 |
| failures added as regression cases | no | no | yes |
| rule changed | no | no | yes |

The first harness result was not better. The useful behavior was the loop after failure. The 36 rows are a public regression fixture, not a hidden generalization benchmark. The failed cases were routed back into the task, converted into regression coverage, and then reflected in the kit rule

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
- read-only MCP export
- disabled cloud runner descriptors
- file-backed memory and optional backend contracts

Private or project overlay

- cloud execution lanes
- hosted visualization backends
- vector or graph memory backends
- credentials and account-specific policy

The public kit does not scaffold account-specific posting, social channel logs, publication ledgers, or connector response logs
