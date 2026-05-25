# Date Normalization Benchmark

공개 README의 정량 task 표를 재현하는 작은 회귀 fixture

목표

- 기준일 2026-05-25 월요일
- 한국어 업무 문장의 마감일 표현을 ISO 날짜로 정규화
- `UNKNOWN`은 불명확하거나 취소 후 재설정 없는 경우
- `내주`는 기준일 다음 주로 처리
- `다음달 첫 영업일`은 다음 달 1일부터 주말을 제외한 첫 날짜
- `다음달 마지막 영업일`은 다음 달 말일부터 주말을 제외하고 역산한 첫 날짜

실행

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

기준 결과

| run | correct | total | accuracy | errors |
| --- | ---: | ---: | ---: | ---: |
| codex_goal | 30 | 36 | 83.3% | 6 |
| harness_first_pass | 26 | 36 | 72.2% | 10 |
| harness_feedback_loop | 36 | 36 | 100.0% | 0 |

해석

- 첫 하네스 결과가 더 좋다는 주장이 아님
- 이 36행은 공개 회귀 fixture이며 hidden generalization benchmark가 아님
- 실패를 feedback slice로 다시 열어 수정하고 regression fixture로 승격하는 운영 루프 검증

## English

Small public regression fixture that reproduces the quantitative table in the public README

Run

```sh
python3 benchmarks/date_normalization/score.py --all --check-summary
```

The point is not that the first harness pass won

The 36 rows are public regression coverage, not a hidden generalization benchmark

The point is that the harness loop reopened failures, routed them into a follow-up slice, fixed them, and turned accepted failures into regression coverage
