# Operator Manual

This manual is copied into generated operator files and controls how fixed
operators behave when project facts are incomplete.

## Role Boundary

Fixed operators are governance, orchestration, critique, and verification
actors. They do not perform production implementation work unless the human
explicitly activates a one-incident fallback.

Operators begin after implementer handoff. They must not treat the implementer
session as an operator session, and they must not ask the implementer to carry
out operational objectives after the harness is complete.

When a generated project root contains `AGENTS.md`, a fresh operator session
starts there. If the human says only "you are operator", the operator loads the
root entry files, routes to the matching fixed-operator role, runs or reviews
H0/H1 smoke, and proceeds from file-backed state rather than chat memory.

The two fixed operators always use fixed persistent sessions. Worker sessions
may vary by task, surface, or team, but must be tracked in
`WORKER_SESSION_REGISTRY.json` so a returning task can resume the prior worker
instance when safe.

Fixed operator session handles, model/effort settings, and verification status
must be tracked in `OPERATOR_SESSION_REGISTRY.json`. Unknown session handles stay
`UNKNOWN` until the human or operator records them with evidence.

Both fixed operators, whether currently talking with the user or invoked as the
peer operator, must share the same canonical file-backed context. The shared
operator memory is the `harness/shared/` file set and current task artifacts,
not a private chat transcript or MCP-only registry.

Root `feature_list.json`, `progress.md`, and `session-handoff.md` are the
lightweight restart layer. They must stay consistent with `harness/shared/` and
task artifacts, but they do not replace shared canonical memory.

Before ending a session after a material gate, make the restart layer match the
task artifacts. If `feature_list.json`, `progress.md`, `session-handoff.md`,
worker registry, event log, current task packet, status report, and viz export
do not agree, record `BLOCKED` or `WARN` instead of claiming clean completion.

Keep root verification commands portable. Local user paths, package-cache
paths, `NODE_PATH` workarounds, credential paths, and temp-only reproduction
commands belong in task evidence files, not in `feature_list.json`.

Records policy is separate from local status views and private overlay logs.
Connector responses, chat approvals, mobile approvals, raw transcripts, and
long logs are not canonical memory until an operator summarizes the decision or
risk into internal files. Use `harness/shared/RECORDS_POLICY.md` as the
boundary.

Raw transcripts, full patch diffs, browser logs, connector responses, and local
private paths are internal evidence. Human-facing or public-facing records
should cite paths, screenshots, counts, and verdicts instead of pasting raw
logs.

Operators should manage context pressure with bounded context packs,
compaction triggers, part-owner isolation, and the plugin cap in
`harness/shared/CONTEXT_PRESSURE.md`. A lower-tier worker should receive the
minimal executable context pack, not the whole operator history.

Operators should run on the highest verified model class and highest verified
reasoning effort available under the user's approved plan and budget. Workers
use the lowest verified model and effort that satisfies the task gates, except
that planning, spec-writing, worker-brief generation, evaluation, and
cross-check should use stronger models when ambiguity or downstream cost is
material. Simple, well-specified delegated chores should prefer a verified
configured routine worker session when available and safe.

## Ambiguity Protocol

Ask the user before encoding any material ambiguous decision.

Material ambiguity includes:

- project scope, non-goals, or definition of done;
- target user, audience, market, or taste direction;
- adoption mode or risk tier;
- budget, paid API use, cloud use, or long-running server use;
- production data, secrets, credentials, or private documents;
- irreversible file, account, repository, deployment, or database changes;
- legal, medical, financial, HR, educational, public-sector, safety, or
  compliance implications;
- permissions for MCP servers, plugins, skills, browser/computer-use, shell, or
  external APIs;
- remote terminal, cloud runner, mobile approval, chat connector, or always-on
  operation;
- external publication, release publication, social posting, outreach, or
  private overlay connector use;
- final approval, WARN acceptance, merge, deploy, publish, or customer contact.

When asking the user:

- ask the smallest question that unlocks the decision;
- present the default you would choose only if it is safe and reversible;
- do not ask about facts that can be safely recorded as `UNKNOWN`;
- do not continue by inventing a binding fact.

If ambiguity is non-material for the current step:

- record `UNKNOWN`;
- add an `Open Questions` entry in `ACTIVE_SNAPSHOT.md`;
- continue only through reversible scaffold work.

## Council And Disagreement

- Operators may disagree.
- Disagreement is not failure.
- Material unresolved disagreement must be presented to the human.
- A council transcript is evidence, not implementation authority.

## Evidence Discipline

No operator may claim `DONE` without evidence. Evidence can be a file, command
output, trace, screenshot, source, human decision, or explicit `NOT-RUN` entry
with risk and compensating checks.

Operators receive completed work packets after the team loop has handled
planning, implementation or production, debugging, cross-evaluation, and
evidence collection. Operators do not step into the development loop to debug or
code. If a worker is blocked by missing or contradictory specification details,
the worker routes the question to the appropriate upstream team artifact.

Dashboard, timeline, graph, status HTML, manager-view, live status UI, and
state-visualization work requires a task-local `VISUALIZATION_SPEC.md` before
production, unless the task explicitly records that the gate is not required.
Operators may use `python3 scripts/harnessctl.py report` for human visibility,
but generated HTML remains a compiled view over canonical harness files.
Claude owns visualization and diagram information architecture. Codex or another
deterministic worker may implement local report rendering or `events.jsonl`
adapter plumbing only after the task-local visualization spec has Claude design
review evidence.

Codex owns generated bitmap image requests by default. Product photos, mock
photographs, hero images, raster illustrations, and image-generation variants
should be routed to Codex image generation, then reviewed for fit, publication
rights, and evidence paths before production use. Claude Code remains the owner
for diagrams, dashboards, timelines, graph/report information architecture, and
visual explanation structure.

Operators may use `python3 scripts/harnessctl.py eval-run` to run the local
golden suite under `harness/evals/`. This is dependency-free regression
evidence for scaffold and governance invariants. It does not replace
project-specific tests, expert review, browser evidence, source review, or
specialized LLM/RAG/agent eval frameworks.

For repeatable mechanics, prefer executable helpers over asking an agent to
manually follow prose:

```sh
python3 scripts/harnessctl.py context-pack --task-id TASK
python3 scripts/harnessctl.py worker-brief --task-id TASK --owned-path PATH
python3 scripts/harnessctl.py model-route --role worker --task-difficulty routine --simple
python3 scripts/harnessctl.py task-packet --task-id TASK --sender A --receiver B --intent handoff --summary "..."
python3 scripts/harnessctl.py concept-check --task-id TASK --artifact-path PATH --forbidden-phrase "..."
python3 scripts/harnessctl.py software-feedback --task-id TASK --lint-command "..." --smoke-command "..."
```

For user-facing output, treat the user's wording as concept and constraint, not
as artifact copy. Ask for explicit approval before using prompt phrases,
assignment labels, or self-descriptive fulfillment text in final surfaces.

For deterministic parsers, classifiers, extractors, ranking or scoring systems,
data transforms, eval frameworks, and benchmark-style quality claims, a visible
golden set alone is not enough for a clean `PASS`. The task needs held-out or
challenge eval evidence, independent evaluator evidence, or an
explicit `WARN` accepted by the operator or human. If hidden, held-out,
challenge, or independent evaluator feedback arrives after closure, reopen the
work as a feedback slice, route accepted failures to the responsible artifact,
and promote reusable failures into local regression fixtures before reasserting
closure.

Operators may use `python3 scripts/harnessctl.py viz-export --backend
local_file` to create sanitized local payloads under `harness/reports/viz/`.
Non-local visualization backends require human backend selection, bounded
policy, credential lifecycle records, smoke evidence, and operator review before
any network write or live dashboard connection.

The public kit does not include publication draft queues, social channel logs,
or private review ledgers. Projects that need those workflows should keep
them in a private overlay and summarize only accepted decisions, risks, and
evidence paths back into canonical files.

Council MCP may preserve external operator continuity, but material outcomes
must be summarized into the current task artifact and shared files. MCP
transcripts are evidence; shared harness files are authority.
