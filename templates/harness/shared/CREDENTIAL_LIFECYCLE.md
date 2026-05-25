# Credential Lifecycle

Default: no secret access.

Credentials are human-owned. Workers receive credential ids and scopes, not raw
secret values. `.env` files, token values, connector responses, and account
secrets must not be committed, copied into reports, or summarized into canonical
project records.

For viz backend adapters, cloud lanes, deploys, remote terminal, mobile
approval, chat connectors, or private overlay adapters, record a lifecycle entry
here before any worker is allowed to use credentials.

## Required Fields For Any Approved Credential

- credential id:
- owner:
- actor:
- scope:
- source:
- issued at:
- expires at:
- rotation rule:
- revocation trigger:
- audit event:

## Revocation Triggers

- incident response activation;
- MCP/tool compromise;
- worker scope violation;
- secret leakage in trace/log/memory;
- human request;
- project completion.
