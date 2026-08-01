<!-- devpnt:generated
  date: 2026-07-08T11:36:16
  generator: functional_docs_generator v1.0
  sources: ai_docs
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: 52a1bf1145267a4e
-->

## MCP (Model Context Protocol)
- Name: Model Context Protocol
- Direction: bidirectional
- Authentication: none
- Message Format: JSON-RPC
- Module: functional/external_interfaces.md

## SSE (Server-Sent Events)
- Name: Server-Sent Events Transport
- Direction: outbound
- Authentication: none
- Message Format: JSON-RPC / SSE
- Module: functional/external_interfaces.md

## Stdio Transport
- Name: Standard I/O Communication
- Direction: bidirectional
- Authentication: none
- Message Format: stdio
- Module: functional/external_interfaces.md

## npm Registry Interface
- Name: npm Registry API
- Direction: outbound
- Authentication: 2FA/Token
- Message Format: REST
- Module: reference/GUIDE_release.md

## Git Versioning Interface
- Name: Git Remote Protocol
- Direction: outbound
- Authentication: SSH/HTTPS
- Message Format: binary
- Module: reference/GUIDE_release.md