# Harness MCP Server Export

Purpose: expose read-only harness context to external tools without making MCP
or private tool memory authoritative.

This directory is a generated, dependency-free reference export. It starts
`UNVERIFIED` and read-only. Smoke it in the target MCP client before relying on
it.

## Tools

- `search_past_decisions`
- `get_capability_status`
- `get_current_task`
- `list_open_questions`

## Rules

- Read-only by default.
- External MCP transcripts are advisory until summarized into canonical files.
- Never expose secrets, credentials, or private data without explicit approval.
- Tool output is evidence for operators, not direct authority.
- Do not let MCP output bypass `feature_list.json`, task blueprints,
  evaluation gates, or human approval.

## Local Smoke

```sh
python3 harness/mcp_server/server.py --root . list-tools
python3 harness/mcp_server/server.py --root . call-tool get_capability_status --arguments '{}'
python3 harness/mcp_server/server.py --root . call-tool search_past_decisions --arguments '{"query":"operator"}'
```

## Real MCP Client Use

`server.py` is intentionally small so generated projects have a portable
starting point. If the target project needs a full MCP runtime, wrap the same
read-only tool functions in the client/runtime adapter approved for that
project and record smoke evidence in `CAPABILITY_REGISTRY.json`.
