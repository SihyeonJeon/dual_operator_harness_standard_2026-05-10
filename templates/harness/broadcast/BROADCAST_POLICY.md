# Broadcast Policy

Purpose: convert approved internal evidence into external-facing drafts without
turning external channels into canonical memory or automatic authority.

## Default State

- Broadcast is a draft system by default.
- Automatic external publish is denied.
- Connectors start `UNVERIFIED` until target-project smoke evidence exists.
- Network writes, public posts, releases, outreach, submissions, and external
  evidence updates require explicit human approval.
- Operators may create drafts after task closure. Workers may not publish.

## Internal And External Boundary

Internal records remain canonical in:

- `feature_list.json`
- `progress.md`
- `session-handoff.md`
- `harness/shared/`
- `harness/tasks/`
- `harness/events/events.jsonl`

External-channel artifacts live under `harness/broadcast/` as draft, approval,
or publication records. They are not canonical project memory until an operator
summarizes the relevant decision or outcome back into internal records.

## Draft Queue

SessionEnd, Stop, or task-close hooks may create entries in
`harness/broadcast/DRAFT_QUEUE.md` and draft files under
`harness/broadcast/drafts/`.

Recommended draft types:

- Korean blog draft
- English blog draft
- release note draft
- short social post draft
- external evidence summary

Every draft must name:

- source task id or trace id;
- source internal evidence paths;
- target audience;
- redaction status;
- approval status;
- generic connector id, if any;
- publication denial or approval evidence.

## Human Approval

No connector may publish from an unapproved draft. Approval evidence must record:

- approving human or delegated approver;
- approved channel;
- approved scope;
- approved date;
- material redactions;
- rollback or correction path when applicable.

## Redaction

Drafts must remove or mask:

- secrets, tokens, credentials, customer-private data, private messages, and
  internal-only paths;
- unverifiable claims;
- unsupported benchmark or competitor claims;
- regulated-domain recommendations not approved for publication;
- names, accounts, or personal data without permission.

## Connector Policy

Connector JSON files in the public kit are examples only. Real channel
adapters belong in a project-private overlay or a generated project after the
project records target, scope, smoke evidence, rollback path, and approval.

Side-effecting connectors must be represented in `TOOL_REGISTRY.json` with a
side-effect class of `network_write` or `external_action` and an approval policy
that is stricter than `not_required_scoped`.

## Event Requirements

Create an observability event for:

- draft created;
- draft approved;
- draft rejected;
- connector smoke passed or failed;
- publication attempted;
- publication completed;
- correction, takedown, or rollback.

## Do Not

- Do not publish from hidden chat context.
- Do not treat external likes, comments, or reviewer output as canonical memory
  until summarized into internal files.
- Do not let broadcast urgency bypass planning, evaluation, human review, or
  redaction.
- Do not auto-post by default.
