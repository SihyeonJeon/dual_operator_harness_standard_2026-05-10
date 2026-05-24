# Remote Adapter And Visualization Guide

## 한국어

이 문서는 인간이 직접 결정해야 하는 remote/viz/credential 경계를
정리합니다. worker는 이 결정 없이 외부 backend, cloud runner, remote
terminal, public connector를 활성화하면 안 됩니다.

### 이번 웹사이트 데모에도 같은가?

예. 원칙은 같습니다.

- `scripts/harnessctl.py report`가 만드는 `harness/reports/status.html`은
  내장 local compiled view입니다. 별도 backend 선택 없이 로컬 확인용으로
  사용할 수 있습니다.
- dashboard, timeline, graph, external report, live status UI, 외부 viz
  backend 연결은 task-local `VISUALIZATION_SPEC.md`가 먼저 backend,
  data contract, redaction, acceptance criteria를 확정해야 합니다.
- 외부 backend는 `events.jsonl`을 보내기 전에 human approval, bounded
  policy, credential lifecycle, smoke evidence가 필요합니다.

### 인간이 결정할 것

1. Viz backend 선택

   - `local_file`: 기본값. 네트워크 없음. `harnessctl.py viz-export`로
     `harness/reports/viz/`에 sanitized payload를 만듭니다.
   - external dashboard/SaaS/cloud/backend: 직접 선택하고, 목적과 공개 범위,
     보관 기간, private data 위험을 적습니다.

2. Cloud lane 선택

   - `harness/runtime/RUNNERS/*.json` 중 사용할 lane을 고릅니다.
   - `UNVERIFIED` 상태를 유지한 채 smoke를 먼저 수행합니다.
   - allowed commands, timeout, budget, network rule, kill procedure,
     audit path를 bounded policy로 적습니다.

3. Credential 관리

   - `.env`는 commit 금지입니다.
   - worker에게 secret 값을 주지 말고 credential id/scope만 줍니다.
   - `harness/shared/CREDENTIAL_LIFECYCLE.md`에 owner, scope, expiry,
     rotation, revocation trigger, audit event를 적습니다.

4. Smoke evidence

   - dry-run payload가 private data를 포함하지 않는지 확인합니다.
   - 외부 connector는 publish/send/write 없이 auth/schema/path만 증명합니다.
   - evidence path를 task artifact와 `events.jsonl`에 남깁니다.

5. Adapter 구현 승인

   - 실제 adapter 코드는 worker가 작성할 수 있습니다.
   - 인간은 backend, credential scope, bounded policy, smoke result를
     승인합니다.
   - adapter가 network write를 하려면 별도 human approval이 필요합니다.

### Worker에게 위임할 것

- `events.jsonl` -> viz backend adapter 구현
- `harnessctl.py report` UI 개선
- local dry-run payload 생성
- smoke evidence 파일 생성
- redaction tests
- README/external evidence 정리

### 금지

- spec 없이 dashboard/live UI/backend 연결 시작
- `.env` 내용 읽기 또는 로그/HTML/JSON에 기록
- human approval 없이 external post, deploy, outreach, network write 수행
- viz backend를 canonical memory로 취급

---

## English

This guide defines the human decision boundary for cloud runners, visualization
backends, credentials, and external adapters.

### Does the website demo follow the same rule?

Yes.

- `scripts/harnessctl.py report` generates a built-in local compiled view and
  needs no external backend selection.
- Dashboards, timelines, graphs, external reports, live status UIs, and external
  viz backends require a task-local `VISUALIZATION_SPEC.md` before production.
- External backends require human approval, bounded policy, credential lifecycle
  records, and smoke evidence before events can be pushed.

### Human Decisions

1. Choose the viz backend: default `local_file`, or an explicitly selected
   external backend.
2. Choose the cloud lane from `harness/runtime/RUNNERS/*.json`.
3. Record bounded policy: allowed commands, network rule, budget, timeout,
   audit path, and kill procedure.
4. Manage credentials through `harness/shared/CREDENTIAL_LIFECYCLE.md`; never
   commit `.env` or pass raw secrets into worker memory.
5. Review smoke evidence before changing any runner or adapter to verified.

Workers may implement deterministic adapter code and dry-run/smoke tooling, but
they must not activate network writes, publish externally, or treat external
views as canonical memory without operator and human approval.
