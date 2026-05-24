# Identity

Every actor must be attributable.

## Actor Classes

- human
- claude-code-operator
- codex-operator
- planning-worker
- design-worker
- coding-worker
- evaluation-worker
- hook
- mcp-server
- cloud-lane

## Rules

- Workers do not borrow operator identity.
- MCP servers do not borrow human identity.
- Tool calls must record actor id when the runtime exposes it.
- Production credentials must be scoped, revocable, and short-lived when
  available.
