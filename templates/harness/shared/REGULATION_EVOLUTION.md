# Regulation Evolution

The harness improves by turning success and failure records into better role
files, skills, templates, schemas, and checks.

## Editable Governance Surfaces

Operators may update these files as governance work:

- operator `AGENT.md`
- operator `SKILLS.md`
- team `AGENT.md`
- team `SKILLS.md`
- team `TEAM_CONTEXT.md`
- shared policies
- templates
- schemas
- linter/doctor rules
- eval fixtures

## Evidence Required

Every regulation change must cite at least one of:

- failure ledger entry;
- evaluation report;
- cross-evaluation report;
- repeated worker confusion;
- successful pattern worth preserving;
- user correction;
- council decision.

## Rule Change Record

Every accepted rule change must be recorded in `RULE_CHANGE_LOG.md` with:

- changed surface;
- change class;
- evidence path;
- reviewer or operator;
- rollback note when authority, permission, safety, cost, compliance,
  merge/deploy, or human-approval behavior changes.

## Change Classes

Class A: mechanical clarification

- typo, broken link, missing reference, clearer load order;
- may be applied by the current operator;
- must be logged in `RULE_CHANGE_LOG.md`.

Class B: role or team behavior refinement

- updates to `AGENT.md`, `SKILLS.md`, `TEAM_CONTEXT.md`, templates, or eval
  wording based on evidence;
- may be applied by an operator after independent operator review or recorded
  cross-check;
- must be logged with evidence.

Class C: authority, permission, safety, cost, compliance, merge/deploy, or
human-approval change

- requires dual-operator agreement and explicit human approval;
- must include rollback notes.

## Mandatory Post-Task Review

At the end of each substantial task, before moving to the next sharp/deep slice:

1. Review failures, warnings, `NOT-RUN` gates, worker questions, and successful
   reusable patterns.
2. Decide whether any role file, skill file, template, schema, or linter rule
   should change.
3. Apply Class A/B changes when allowed.
4. Escalate Class C changes to the human.
5. Record the change or "no change" decision in `RULE_CHANGE_LOG.md`.
