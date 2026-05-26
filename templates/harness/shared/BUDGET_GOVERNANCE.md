# Budget Governance

Status: public-safe policy and local enforcement surface

Every dispatched task must carry a `BUDGET.json` before worker execution.
Every runner descriptor must carry a budget policy and kill procedure. A task
without a budget is not ready for dispatch.

## Required Task Budget Fields

- `task_id`
- `token_cap`
- `time_cap_minutes`
- `cost_cap_usd`
- `warning_threshold_percent`
- `kill_threshold_percent`
- `kill_procedure`
- `escalation.event_type`

Unknown commercial caps must stay `UNKNOWN` or `project_defined_before_dispatch`
until the operator records an explicit decision. Do not silently invent caps.

## Usage Event Fields

Budget-related events use these fields in `harness/events/events.jsonl`:

- `token_used`
- `time_elapsed_minutes`
- `cost_used_usd`
- `budget_percent`
- `budget_status`

Expected event types:

- `budget.ok`
- `budget.warning`
- `budget.kill_required`
- `budget.escalation_required`

## Local Check

Use the local control surface whenever a runner has observed token, time, or
cost counters:

```sh
python3 scripts/harnessctl.py budget-check \
  --task-id F0-PLANNING-RUNWAY \
  --time-elapsed-minutes 120
```

If observed usage reaches the warning threshold, the command writes a
`budget.warning` event. If observed usage reaches the kill threshold, the
command writes `budget.kill_required` and the configured escalation event, then
returns a non-zero exit code so a runner can stop dispatch.

## Enforcement Boundary

The public kit cannot read every provider's private token meter by itself. A
runner adapter must pass observed counters into `budget-check`. The generated
harness still enforces the structure: missing budgets, missing runner kill
procedures, missing event fields, and missing budget-check support fail local
validation.

## Operator Rules

- budget increase requires operator escalation
- cost or paid API budget increase requires human approval unless the project
  has a written pre-approval
- timeout or kill procedures must leave a checkpoint and handoff note
- workers must not continue after `budget.kill_required`
- budget failures feed `FAILURE_LEDGER.md` and future eval fixtures
