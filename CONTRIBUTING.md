# Contributing

This repository is a public harness generator. Keep public source portable,
credential-free, and reproducible.

## Before a PR

```sh
python3 scripts/validate_kit.py
git diff --check
```

## Public Claim Rules

- benchmark claims need a command, fixture path, result, and scope boundary
- generated-project behavior should be covered by `scripts/validate_kit.py`
- private account automation must stay outside public source
- credential values, local private logs, and active cloud targets must not be
  committed
- README claims should link to benchmark or traceability docs

## New Adapters

Adapters should start disabled by default and include:

- owner
- allowed inputs
- denied inputs
- credential scope description
- dry-run command
- smoke evidence path
- rollback or disable path
- approval policy

Real credentials and account targets belong in a private project overlay, not
in this repository.
