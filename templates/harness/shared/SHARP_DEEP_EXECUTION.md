# Sharp Deep Execution

Default production mode is narrow and deep. This is a production constraint,
not permission to skip project planning.

## Rule

Do not develop widely and shallowly. First run enough planning runway to
understand the project shape, risks, deliverable map, and candidate slices. Then
approve the smallest valuable executable slice and take it through design,
production, debugging, evaluation, cross-evaluation, operator closure, context
update, and regulation review before starting the next production slice.

## Pre-Slice Planning Runway

Before a slice becomes active, planning must record:

- confirmed and rejected interpretations of the goal;
- material unknowns and human-decision blockers;
- candidate deliverables and verification surfaces;
- candidate slices, including deferred alternatives when ambiguity is material;
- whether design, research, domain review, or council input can invalidate the
  candidate slice.
- whether visualization is needed, and if so whether a task-local
  `VISUALIZATION_SPEC.md` is required before visualization production.

The first slice is a candidate until this runway and any required upstream
design/domain discovery approve it.

## Planning Requirements

Planning must define:

- the root `feature_list.json` item or new feature item that represents the
  approved active slice;
- the candidate slice set and the single approved active slice;
- why this slice is highest leverage now;
- explicit non-goals;
- definition of done;
- required design/spec work;
- required visualization spec work before any dashboard, timeline, graph, HTML
  external evidence view, manager view, or live status UI is built;
- required production work;
- required debugging/evaluation/cross-evaluation;
- evidence needed for operator closure;
- stop conditions;
- next-slice candidates that are explicitly deferred.

## Design Requirements

Design must make the active slice executable:

- states, screens, flows, artifacts, scenes, or outputs needed;
- responsive/layout/media behavior where applicable;
- edge cases that implementation must handle;
- validation path;
- evidence to capture.

If the slice includes visualization, design must first confirm the
pre-visualization information architecture, data contract, redaction model, and
acceptance criteria using `harness/templates/VISUALIZATION_SPEC.md`. Missing or
ambiguous visualization specification returns `SPEC_BLOCKED`.

## Advancement Rule

The next production slice may start only when the current slice is:

- `DONE`;
- `BLOCKED` with recorded reason and human/operator decision;
- `WARN` accepted by the human when material.

Discovery, inventory, or market/frontier scan may be broad, but production work
must return to one sharp/deep slice.

Feature state must mirror this advancement rule. Do not mark a feature
`passing` until the corresponding task closure evidence exists.

Before ending a session after any material gate, update or explicitly block:

- root `feature_list.json`;
- root `progress.md`;
- root `session-handoff.md`;
- current task packet or gate artifact;
- `harness/shared/WORKER_SESSION_REGISTRY.json` when worker ownership changed;
- `harness/events/events.jsonl`;
- local status report and viz export when available.

If any item cannot be updated, the gate is `BLOCKED` or `WARN`, not cleanly
complete.
