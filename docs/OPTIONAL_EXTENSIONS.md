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
| publication or social channel | not scaffolded | real social, blog, release, or webhook adapter |
| private review workflow | not scaffolded | real model call, hosted review service, domain reviewer workflow |
| MCP export | dependency free read-only local server | production MCP runtime wrapper, auth boundary, hosted registry |
| cloud runner | disabled runner descriptor, bounded policy checklist | actual cloud job, remote terminal bridge, mobile approval connector |
| visualization | local file export, static report, backend selection policy | live dashboard, SaaS telemetry, websocket stream, hosted viewer |
| memory backend | file-backed search, vector index example, graph index example | selected vector database, graph database, private RAG service |
| chat approval connector | disabled Discord approval example with denied publication payloads | real bot, webhook, mobile approval bridge, private credential overlay |
| browser/device validation | policy requires Playwright or equivalent evidence for interactive UI | real Playwright project, device farm, visual regression service |
| additional LLM or agent surface | `AGENT_PROVIDER_OVERRIDES.json` records requested surfaces as `UNVERIFIED` candidates | real Gemini, Cursor, OpenAI Agents SDK, local LLM, hosted model, or private tool runner smoke-tested in the project |

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

The public kit exposes the local harness and safety contract. Account-specific
publication, outreach, and private review workflows stay outside the public
repository.
