---
description: devPNT-generated map of the package's external interfaces. Snapshot 2026-06-13; regenerate via devPNT after structural changes.
status: CURRENT
---
<!-- devpnt:generated
  date: 2026-06-13T05:23:51
  generator: functional_docs_generator v1.0
  sources: ai_docs
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: 518eb3e8ee5a5050
-->

## Agentic SDLC Communication Interface
- Name: Agentic SDLC Control Interface
- Direction: bidirectional
- Authentication: required (runtime token validation)
- Message Format: stdio
- Module: sdlc_check.py

## MCP Protocol Interface
- Name: Model Context Protocol Interface
- Direction: bidirectional
- Authentication: required (runtime capability handshake)
- Message Format: JSON-RPC
- Module: antigravity_skills_guide.md

## SSE Event Stream Interface
- Name: Server-Sent Events Interface
- Direction: inbound
- Authentication: required (connection handshake)
- Message Format: WebSocket frames
- Module: antigravity_skills_guide.md