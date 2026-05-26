# Runtime Connectors

Status: disabled reference surfaces

Connectors are optional project-private adapters over file-backed harness
state. The public kit ships only disabled examples with no credentials and no
account target.

Rules:

- start `UNVERIFIED`
- deny network by default
- define allowed and denied payloads
- write audit events to `harness/events/events.jsonl`
- require smoke evidence before use
- include a disable path
- do not publish progress logs or private work records

Real connector code and secrets belong in a private overlay.
