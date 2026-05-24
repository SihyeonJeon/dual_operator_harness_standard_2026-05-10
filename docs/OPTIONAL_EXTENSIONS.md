# Optional Extensions

Public kit rule

- core files stay provider neutral
- adapters start disabled
- no credential value in git
- no real account target in template files
- no external write before approval and smoke evidence
- private overlays may implement real connectors

## Extension Surfaces

| Surface | Public kit | Private or project overlay |
| --- | --- | --- |
| broadcast | draft queue, generic publication descriptor, manual export descriptor | real social, blog, release, or webhook adapter |
| external reviewer | redaction packet, provider neutral AI reviewer descriptor, human reviewer descriptor | real model call, hosted review service, domain reviewer workflow |
| MCP export | dependency free read-only local server | production MCP runtime wrapper, auth boundary, hosted registry |
| cloud runner | disabled runner descriptor, bounded policy checklist | actual cloud job, remote terminal bridge, mobile approval connector |
| visualization | local file export, static report, backend selection policy | live dashboard, SaaS telemetry, websocket stream, hosted viewer |
| memory backend | file-backed search, vector index example, graph index example | selected vector database, graph database, private RAG service |

## Adapter Contract

Every real adapter records:

- adapter id
- owner
- target system
- allowed inputs
- denied inputs
- credential id and scope
- dry-run command
- smoke evidence path
- rollback or disable path
- approval record

## Distribution Rule

Generated projects may keep real adapters in a private overlay such as:

- `harness_private/`
- a private package
- a private deployment repo
- a local secrets manager

The public kit should expose only the interface and safety contract.
