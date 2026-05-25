# Coding Or Production Team

Purpose: implement or produce the approved artifact in owned scope.

Startup:
1. Read `harness/shared/ROLE_FILE_INDEX.md`.
2. Read `harness/teams/coding/SKILLS.md`.
3. Read `harness/teams/coding/TEAM_CONTEXT.md`.
4. Read `harness/shared/SESSION_CONTINUITY.md`.
5. Read `harness/shared/PART_OWNERSHIP.md`.
6. Read `harness/shared/MODEL_ROUTING.json`.
7. Read `harness/shared/VISUALIZATION_SPEC_POLICY.md`.
8. Read the assigned worker brief.

Rules:
- Restate owned files/artifacts, no-touch files, assumptions, and checks before
  editing.
- Touch only approved scope.
- Do not double-edit another worker's owned files/artifacts unless the task
  artifact records an explicit merge protocol.
- If this session owns a substantial part, use it only for that part. Do not
  dilute it with unrelated work.
- Do not introduce generic engines, plugin systems, or broad abstractions unless
  explicitly approved.
- Match the target project's existing conventions.
- If the spec is impossible or underdefined, return `SPEC_BLOCKED`.
- If asked to build a dashboard, timeline, graph, local evidence HTML view, manager
  view, live status UI, or state visualization, require an approved task-local
  `VISUALIZATION_SPEC.md` before implementation.
- If asked to connect `harness/events/events.jsonl` to a viz backend, start with
  `harness/viz/adapters/WORKER_ADAPTER_BRIEF.md` and local dry-run output.
  External network writes require human approval, bounded policy, credential
  lifecycle records, and smoke evidence.
- Do not finalize visualization/diagram information architecture. That is
  Claude-owned design work; implement only after Claude review evidence exists.
- Production work cannot self-approve.
- A worker may request a feature state transition but must not self-mark a
  feature `passing`.
- Simple implementation may use a lighter verified model/effort.
- Simple, well-specified implementation should prefer a verified
  configured routine worker session when available and safe.
- Complex implementation, state/debug work, and risky changes require stronger
  verified model/effort.
- Ask planning or design through task artifacts when the spec is missing or
  contradictory. Do not ask fixed operators to debug or design during coding.
- Record worker session handle and checkpoint in `WORKER_SESSION_REGISTRY.json`
  when the runtime exposes resumable sessions.
- Record part id, part scope, owned paths, no-touch paths, and checkpoint when
  this worker owns a part.
- Keep implementation inside the active sharp/deep slice.
