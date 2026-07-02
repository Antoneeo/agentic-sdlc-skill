---
description: devPNT-generated data-entity doc. Snapshot 2026-05-10, predates the 1.5/1.6 restructuring: regenerate before trusting.
status: DEPRECATED
---
<!-- devpnt:generated
  date: 2026-05-10T06:55:42
  generator: functional_docs_generator v1.0
  sources: (none)
  model: GoogleGemini/gemini-3.1-flash-lite-preview
  summary_hash: d2ae755f57e59dee
-->

## Entities

| Entity | Python Classes | Key Attributes | Notes |
| :--- | :--- | :--- | :--- |
| User Profile | `User`, `UserProfile` | `id`, `username`, `email`, `bio` | Core identity and profile data for system actors. |
| Content Item | `Post`, `Comment` | `id`, `author_id`, `body`, `created_at` | Primary user-generated data objects. |
| Media Asset | `Image`, `Video` | `id`, `url`, `file_size`, `mime_type` | Stored binary content linked to users or posts. |

## Relations

User --1:N--> Post
User --1:N--> Comment
Post --1:N--> Comment
Post --1:N--> Media Asset