---
description: devPNT-generated entry-point doc. Snapshot 2026-07-02; regenerate via devPNT after structural changes.
status: CURRENT
---
<!-- devpnt:generated
  date: 2026-07-02T06:31:03
  generator: functional_docs_generator v1.0
  sources: (none)
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: a5ebe0ef17a7bcfa
-->

| Entry Point | Type | Invocation | Initializes |
| :--- | :--- | :--- | :--- |
| cli.py | CLI | python cli.py --root /path | Core engine and configuration |
| server.py | HTTP server | python server.py --port 8080 | Web framework and API routes |
| worker.py | daemon | python worker.py --queue jobs | Background task processor |
| transport.py | stdio server | node transport.js | Standard I/O communication channel |
| plugin.py | importable module | import plugin | Plugin registration system |