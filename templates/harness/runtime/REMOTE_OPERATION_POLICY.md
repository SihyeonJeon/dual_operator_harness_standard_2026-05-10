# Remote Operation Policy

Status: template

Remote terminal control, cloud workers, mobile approvals, chat connectors, and
always-on lanes are disabled until explicitly approved and smoked.

## Allowed Shape

Remote operation must be a bounded connector over file-backed harness state:

- approved project root;
- explicit runner identity;
- least-privilege credentials;
- allowed command/tool list;
- budget and timeout;
- audit log path;
- approval channel;
- stop/kill procedure;
- smoke evidence.

Runner descriptors live under `harness/runtime/RUNNERS/`. They are the only
approved opt-in path for local, Claude Code, Codex, remote/cloud, or future
runner surfaces. Every descriptor starts `UNVERIFIED`, denies network by
default, and must record audit path plus smoke evidence before production use.

Use `harness/runtime/CLOUD_VIZ_OPERATOR_GUIDE.md` when selecting a cloud lane,
visualization backend, credential scope, or adapter implementation path.

## Denied By Default

- unrestricted shell or terminal relay;
- unbounded cloud agent loops;
- mobile approval messages that mutate state without writing an approval packet;
- secret access without credential lifecycle approval;
- network writes, public posting, outreach, deploy, payment, contract, or account
  action without explicit human approval and smoke evidence.

## Mobile Approval Rule

Mobile or external chat approval is a communication surface, not authority by
itself. A material approval must be written into a durable approval packet or
task artifact before agents act on it.

## External Evidence And Status Views

Static HTML reports may be shared only after redaction rules are checked. Public
evidence output requires an explicit sharing decision and must not expose
private traces, secrets, customer data, internal deliberation, or unapproved
claims.

External visualization backends are remote operation surfaces. The default
`local_file` viz backend writes sanitized payloads locally only. Any backend
that performs network writes requires human approval, bounded policy, credential
lifecycle records, smoke evidence, and a rollback or disable path.
