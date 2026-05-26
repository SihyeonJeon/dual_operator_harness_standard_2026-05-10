# {{PROJECT_NAME}}

## 한국어

목표

```text
{{PROJECT_GOAL}}
```

### 시작

```sh
./init.sh
python3 scripts/validate_harness.py .
python3 scripts/harnessctl.py report
python3 scripts/harnessctl.py eval-run
python3 scripts/harnessctl.py budget-check --task-id F0-PLANNING-RUNWAY --time-elapsed-minutes 1
python3 scripts/harnessctl.py context-pack --task-id H0-LOCAL-SMOKE
python3 scripts/harnessctl.py worker-brief --task-id H0-LOCAL-SMOKE --owned-path PATH
python3 scripts/harnessctl.py model-route --role worker --task-difficulty routine --simple
python3 scripts/harnessctl.py task-packet --task-id H0-LOCAL-SMOKE --sender A --receiver B --intent handoff --summary "summary"
python3 scripts/harnessctl.py current-research --task-id H0-LOCAL-SMOKE --query "current alternatives" --source "SOURCE" --finding "finding"
python3 scripts/harnessctl.py cross-feedback --task-id H0-LOCAL-SMOKE --producer A --reviewer B --verdict PASS --feedback "feedback"
python3 scripts/harnessctl.py concept-check --task-id H0-LOCAL-SMOKE --artifact-path PATH --forbidden-phrase "prompt phrase"
python3 scripts/harnessctl.py software-feedback --task-id H0-LOCAL-SMOKE --lint-command "..." --smoke-command "..."
```

### operator 진입

```text
you are operator
```

### 운영 축

- Codex Claude Code 동등 fixed operator
- operator 생산 작업 기본 금지
- planning runway 우선
- sharp deep slice 승인 후 production
- worker model effort task difficulty routing
- simple task aliases sonnet haiku gpt-5.3-codex-spark when verified
- executable model-route helper applies routing policy
- BUDGET.json token time cost cap and budget-check kill surface
- routine worker configured low cost model 가능
- part owner session same part reuse
- token saving agent communication via bounded task packets
- context-pack worker-brief task-packet helpers reduce repeated prompt context
- current-research records command-date market/comparable evidence before overall planning
- cross-feedback records independent feedback before operator closure
- concept-check catches prompt wording leakage in user-facing artifacts
- CONCEPT_TRANSLATION_POLICY.md separates user request from artifact copy
- shared context canonical
- team context memory
- VISUALIZATION_SPEC.md 승인 전 dashboard timeline graph live status UI 금지
- Claude visualization information architecture owner
- events jsonl local first
- 외부 viz backend human approval policy credential smoke evidence 필요
- status html compiled view
- harness eval run local regression
- software feedback policy lint runtime Playwright UI UX layout
- software-feedback helper writes evidence packet
- RECORDS_POLICY.md local canonical record policy
- public kit no external posting scaffold
- MCP read only context export
- remote mobile cloud denied by default
- disabled Discord approval connector example only no publication adapter

### 파일

- `AGENTS.md`
- `CLAUDE.md`
- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `guide_for_human.md`
- `scripts/harnessctl.py`
- `harness/shared`
- `harness/operators`
- `harness/teams`
- `harness/tasks`
- `harness/viz`
- `harness/evals`
- `harness/mcp_server`
- `harness/runtime`
- `harness/shared/BUDGET_GOVERNANCE.md`
- `harness/shared/AGENT_COMMUNICATION.md`
- `harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md`
- `harness/shared/CROSS_FEEDBACK_LOOP.md`
- `harness/shared/CONCEPT_TRANSLATION_POLICY.md`
- `harness/shared/SOFTWARE_FEEDBACK_POLICY.md`
- `harness/events/events.jsonl`
- `harness/reports/status.html`

## English

Goal

```text
{{PROJECT_GOAL}}
```

### Start

```sh
./init.sh
python3 scripts/validate_harness.py .
python3 scripts/harnessctl.py report
python3 scripts/harnessctl.py eval-run
python3 scripts/harnessctl.py budget-check --task-id F0-PLANNING-RUNWAY --time-elapsed-minutes 1
python3 scripts/harnessctl.py context-pack --task-id H0-LOCAL-SMOKE
python3 scripts/harnessctl.py worker-brief --task-id H0-LOCAL-SMOKE --owned-path PATH
python3 scripts/harnessctl.py model-route --role worker --task-difficulty routine --simple
python3 scripts/harnessctl.py task-packet --task-id H0-LOCAL-SMOKE --sender A --receiver B --intent handoff --summary "summary"
python3 scripts/harnessctl.py current-research --task-id H0-LOCAL-SMOKE --query "current alternatives" --source "SOURCE" --finding "finding"
python3 scripts/harnessctl.py cross-feedback --task-id H0-LOCAL-SMOKE --producer A --reviewer B --verdict PASS --feedback "feedback"
python3 scripts/harnessctl.py concept-check --task-id H0-LOCAL-SMOKE --artifact-path PATH --forbidden-phrase "prompt phrase"
python3 scripts/harnessctl.py software-feedback --task-id H0-LOCAL-SMOKE --lint-command "..." --smoke-command "..."
```

### Operator Entry

```text
you are operator
```

### Operating Axes

- equal fixed Codex Claude Code operators
- operators avoid production work by default
- planning runway first
- production after approved sharp deep slice
- worker model effort task difficulty routing
- simple task aliases sonnet haiku gpt-5.3-codex-spark when verified
- executable model-route helper applies routing policy
- BUDGET.json token time cost caps and budget-check kill surface
- routine worker configured low cost model when verified
- part owner session same part reuse
- token-saving agent communication through bounded task packets
- context-pack worker-brief task-packet helpers reduce repeated prompt context
- current-research records command-date market/comparable evidence before overall planning
- cross-feedback records independent feedback before operator closure
- concept-check catches prompt wording leakage in user-facing artifacts
- CONCEPT_TRANSLATION_POLICY.md separates user request from artifact copy
- shared context canonical
- team context memory
- VISUALIZATION_SPEC.md before dashboard timeline graph live status UI
- Claude visualization information architecture owner
- events jsonl local first
- external viz backend human approval policy credential smoke evidence required
- status html compiled view
- harness eval run local regression
- software feedback policy lint runtime Playwright UI UX layout
- software-feedback helper writes evidence packet
- RECORDS_POLICY.md local canonical record policy
- public kit no external posting scaffold
- MCP read only context export
- remote mobile cloud denied by default
- disabled Discord approval connector example only no publication adapter

### Files

- `AGENTS.md`
- `CLAUDE.md`
- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `guide_for_human.md`
- `scripts/harnessctl.py`
- `harness/shared`
- `harness/operators`
- `harness/teams`
- `harness/tasks`
- `harness/viz`
- `harness/evals`
- `harness/mcp_server`
- `harness/runtime`
- `harness/shared/BUDGET_GOVERNANCE.md`
- `harness/shared/AGENT_COMMUNICATION.md`
- `harness/shared/CURRENT_MARKET_RESEARCH_POLICY.md`
- `harness/shared/CROSS_FEEDBACK_LOOP.md`
- `harness/shared/CONCEPT_TRANSLATION_POLICY.md`
- `harness/shared/SOFTWARE_FEEDBACK_POLICY.md`
- `harness/events/events.jsonl`
- `harness/reports/status.html`
