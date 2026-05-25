# Implementer File Map

This map tells the harness implementer which files are kit-level instructions,
and which files are copied into the generated harness.

## Kit-Level Files

- `IMPLEMENTER.md`: implementer entry point.
- `BOOTSTRAP.md`: scaffold procedure.
- `SPEC.md`: normative requirements for generated harnesses.
- `POLICY_LINTER.md`: validation requirements.
- `docs/HARNESS_IMPLEMENTER_MANUAL.md`: implementer role manual.
- `docs/CLOUD_VIZ_OPERATOR_GUIDE.md`: cloud/viz human decision guide source.
- `docs/OPTIONAL_EXTENSIONS.md`: public/private extension boundary.
- `docs/IMPLEMENTER_FILE_MAP.md`: this file.

## Template Files Copied Into Target Harness

- `templates/root/*`
  - includes root `.claude/` Claude Code adapter templates and
    `scripts/harnessctl.py`
- `templates/harness/shared/*`
- `templates/harness/mcp_server/*`
- `templates/harness/spec/*`
- `templates/harness/viz/*`
- `templates/harness/evals/*`
- `templates/harness/operators/*`
- `templates/harness/teams/*`
- `templates/harness/templates/*`
- `templates/harness/tasks/*`
- `templates/harness/runtime/*`
- `templates/harness/SCAFFOLDING_REPORT.md`
- `templates/harness/SCAFFOLDING_CHECKLIST.md`

## Machine Contracts

- `schemas/*.schema.json`
  - includes `viz-backends.schema.json` for `harness/viz/VIZ_BACKENDS.json`
  - includes `eval-suite.schema.json` for `harness/evals/golden_suite.json`
- `scripts/validate_harness.py`
- `scripts/implementer_hooks.py`
- generated root `scripts/harnessctl.py`

## Optional Helpers

- `scripts/scaffold_harness.py`
- `templates/input/INPUT_PACKET.md`
