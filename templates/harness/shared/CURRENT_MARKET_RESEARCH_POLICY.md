# Current Market Research Policy

Status: generated policy for pre-planning current-state research

Before the operator approves an overall plan, planning must decide whether the
goal depends on the current market, current tools, current competitors, current
standards, current laws, current prices, current UX expectations, or current
public information.

If it does, current-state research is required before the plan. The research is
as-of the command date, not the model training date.

## Required When

- product, service, business, strategy, market, education, writing, design, or
  software work will be judged against current alternatives;
- the result includes recommendations, comparisons, trends, pricing, vendor
  choices, rules, public facts, or claims about what users expect now;
- the plan depends on what competitors, comparable products, tools, frameworks,
  platforms, regulations, or communities currently do.

## Not Required When

- the task is a purely local deterministic edit;
- the user explicitly provides the full source of truth and forbids external
  research;
- the environment is offline and the operator records a `NOT-RUN` risk.

## Minimum Evidence

- command date and research as-of date;
- source list or explicit `NOT-RUN` rationale;
- current alternatives or comparable references when relevant;
- findings that can change the plan, not generic background;
- planning decision impact: keep, change, add, remove, or ask human.

## Gate

Overall planning must not be treated as complete until one of these is true:

- `CURRENT_RESEARCH.json` exists for the active planning task with a `PASS`
  verdict;
- the planning artifact records `NOT-RUN` with risk and human/operator
  acceptance;
- the task is explicitly internal and deterministic with no current-state
  dependency.

Use:

```sh
python3 scripts/harnessctl.py current-research --task-id TASK --query "..." --source "..." --finding "..."
```

This helper records research evidence. It does not browse, buy data, or write
to external services.
