# Agent Loader

Easy Orchestration Harness is a standard kit for generating a dual-operator,
multi-agent orchestration harness for any project type.

Always load order:

1. `IMPLEMENTER.md` when creating a project-local harness
2. `BOOTSTRAP.md`
3. `SPEC.md`
4. `docs/HARNESS_IMPLEMENTER_MANUAL.md` when acting as harness implementer
5. `docs/OPERATOR_MANUAL.md` when acting as an operator or writing operator files
6. `POLICY_LINTER.md` before claiming a scaffold is valid
7. `manifest.json` when checking public source split integrity

Use `templates/`, `schemas/`, and `scripts/validate_harness.py` as the
executable implementation layer.

If `dist/reassembled.md` exists, do not load it by default. It is a bundle
artifact for one-file distribution and integrity checks, not the normal
operating context.

If the user supplies only two inputs, interpret them as:

- this kit;
- project goal.

If prior information and constraints are also supplied, treat them as optional
scaffolding context. If not supplied, write `UNKNOWN` instead of inventing them.

If either input leaves a material operator decision ambiguous, ask the user a
focused question before encoding that decision as governance.
