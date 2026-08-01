<!-- devpnt:generated
  date: 2026-07-09T05:29:50
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
| rpc.py | stdio server | python rpc.py | Standard input/output communication bridge |
| library.py | importable module | import library | Data models and utility functions |