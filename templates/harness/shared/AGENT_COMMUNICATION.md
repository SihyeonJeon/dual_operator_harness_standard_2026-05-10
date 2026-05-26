# Agent Communication

Status: generated policy for token-efficient agent coordination

Agents communicate through small task packets and canonical files, not through
long hidden chat transcripts.

## Message Shape

Use this shape for worker updates, evaluator feedback, operator routing, and
handoff notes:

```json
{
  "task_id": "UNKNOWN",
  "part_id": "UNKNOWN",
  "sender": "UNKNOWN",
  "receiver": "UNKNOWN",
  "intent": "status | question | feedback | handoff | decision",
  "summary": "one short paragraph",
  "evidence_paths": ["harness/tasks/..."],
  "requested_action": "UNKNOWN",
  "stop_if_unanswered": false
}
```

When available, generate this packet with:

```sh
python3 scripts/harnessctl.py task-packet --task-id TASK --sender A --receiver B --intent handoff --summary "..."
```

This keeps the packet shape stable and records an event in `events.jsonl`.

## Token Rules

- send paths and verdicts before prose
- cite source files instead of pasting large content
- summarize command output and keep full logs in task evidence
- use one current task packet as the main communication surface
- update team `TEAM_CONTEXT.md` only with durable lessons
- update `harness/shared/CONTEXT.md` only with cross-team decisions
- do not forward a full operator conversation to lower-tier workers
- do not send one worker's unrelated context to another worker
- compact before dispatching routine workers

## Routing Rules

- worker questions about unclear scope go to planning through the task artifact
- visual/UI quality questions go to design through the task artifact
- implementation blockers go to production or debugging through the task artifact
- verification failures go to evaluation and then back to exactly one owner
- operator sessions receive completed work packets, not raw worker chatter

## Part-Owner Rule

The worker that owns a substantial part may be resumed for that same part. That
same warm session should not be reused for unrelated parts. If the session is
unavailable, the replacement worker loads the context pack and prior checkpoint
instead of the whole historical conversation.
