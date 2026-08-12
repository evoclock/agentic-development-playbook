# 05 — Optional read-only MCP context

## Purpose

Explain how a small, reviewed Model Context Protocol (MCP) source could provide
read-only context to an agent. MCP is optional and is not part of the default
router demonstration.

## Boundary

Do not register or run an MCP server during the default supervised demo. A
separate approval must identify the server source, tools, permissions, network
access, data paths, tests, and stopping point.

MCP is a transport and tool boundary. It does not make returned context
authoritative, grant approval, prove provenance, or replace direct inspection
of the repository.

## Review before registration

Before any approved live test:

1. read the complete server source and tests;
2. confirm every operation is read-only;
3. confirm context paths are fixed and cannot escape the approved scope;
4. confirm unknown operations fail safely;
5. inspect network and subprocess behaviour;
6. verify the protocol and tool schemas;
7. record the decision in the existing task receipt.

Do not register a server merely because an agent requests it.

## Protocol checks

A minimal initialization request has this shape:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
```

The server must return a valid JSON-RPC result with only the reviewed
capabilities. Test discovery, valid calls, invalid-item errors, and JSON-lines
framing before allowing an agent to use the server.

## Safe use

Use MCP only to locate reviewed context. Inspect the actual source, task
contract, tests, and evidence directly before making a decision.

Stop if:

- the server requests a write operation;
- the server makes an unexpected network request;
- a tool accepts an unrestricted path;
- returned context conflicts with tracked files;
- a proposed change exceeds the approved task scope.

The security-review skill and public-safety hook remain active boundaries around
any approved integration.
