# Bilingual README Parity Guard

Deterministic local guard for generated project README files.

It checks whether the generated Korean and English sections carry the same
operating surface: goal, bootstrap commands, operator entry, worker roles,
planning policy, part-owner reuse, records policy, visualization boundary, MCP
and remote boundaries, file inventory, and public/private boundary.

This is not a native fluency benchmark, translation quality benchmark, or live
LLM evaluation. The two non-harness rows are authored controls.

## Run

```sh
python3 benchmarks/bilingual_readme_parity/score.py --check-summary
```

## Expected Summary

| surface | passed | failed | total | score |
| --- | ---: | ---: | ---: | ---: |
| korean_only | 2 | 12 | 14 | 0.143 |
| bilingual_summary | 5 | 9 | 14 | 0.357 |
| generated_harness | 14 | 0 | 14 | 1.000 |

## Limit

The guard verifies structural parity and terminology carry-over. It does not
decide whether Korean wording is natural, persuasive, or publication-ready.
