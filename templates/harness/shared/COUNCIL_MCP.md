# Council MCP

Default council bridge:

- script: `UNKNOWN_COUNCIL_MCP_SERVER`
- transport: stdio
- project binding: `--project-root <target-project>`
- external operator: `codex_operator`
- external operator sandbox: read-only
- external operator session: persistent per project

## Required Activation

1. Register the MCP server with an absolute target project root.
2. Call `project_info`.
3. Confirm `project_root` exactly matches the active project.
4. Call `list_operators`.
5. Run a read-only `convene_external -> continue_external -> conclude_external`
   smoke.
6. Record evidence under `harness/tasks/H1-COUNCIL-SMOKE/evidence/`.
7. Mark the `council` MCP entry in `MCP_TRUST.json` as approved only after
   smoke passes.

## Authority Boundary

Council MCP may be used for:

- advisory peer reasoning;
- material decision review;
- disagreement surfacing;
- context revival;
- closure challenge;
- transcripted council state.

Council MCP must not be used for:

- code-writing;
- production file edits;
- worker dispatch;
- merge;
- deploy;
- launch approval;
- bypassing team evaluation.

## Shared Context Rule

Both fixed operators must share the same file-backed operator context:

- `harness/shared/ACTIVE_SNAPSHOT.md`
- `harness/shared/PROJECT_PROFILE.json`
- `harness/shared/HARNESS_CONFIG.json`
- `harness/shared/CONTEXT.md`
- `harness/shared/MEMORY.md`
- `harness/shared/FAILURE_LEDGER.md`
- `harness/shared/RULE_CHANGE_LOG.md`
- current task artifacts

The council MCP stores registry/transcript files under its own project-keyed
directory for continuity. Those files are not the canonical project memory.
After each material council meeting, copy or summarize the outcome into the
current task artifact and shared context when it changes decisions.

## Required Meeting Artifact

For material council meetings, create:

`harness/tasks/{task-id}/COUNCIL_MEETING.md`

Minimum fields:

- agenda;
- current conversation operator;
- peer operator;
- shared context version or date;
- opening position;
- peer response;
- agreements;
- disagreements;
- decision;
- outcome: `converged | partial | disagreement`;
- context/rule updates required.
