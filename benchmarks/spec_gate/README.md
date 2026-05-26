# Spec Gate Regression Guard

This self-check verifies that generated harnesses keep planning gates in front
of sharp/deep production work.

The script includes three deterministic surfaces:

- `direct_session`: prompt captured and production file started
- `ad_hoc_brief`: manual brief with goal, risks, tasks, and progress
- `generated_harness`: a real harness scaffolded from this public kit and
  initialized with `./init.sh`

The first two are authored controls, not neutral external baselines. They are
kept in the script to prevent the guard from becoming a pure path-existence
smoke test with no contrast.

Criteria:

- goal intake
- workstream and risk profile
- PRD or equivalent brief
- anti-PRD or failure-mode note
- policy against vague-goal production
- candidate slice gate
- worker brief contract
- part-owner worker reuse
- evaluator gate
- no production before planning runway
- local visibility
- operator closure

This is a planning-gate surface regression guard, not a model-quality,
final-artifact, or neutral framework comparison benchmark.

```sh
python3 benchmarks/spec_gate/score.py --check-summary
```

| generated scaffold checks | failed | conformance |
| ---: | ---: | ---: |
| 12 | 0 | 100% |
