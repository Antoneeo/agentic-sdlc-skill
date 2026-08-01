---
description: devPNT-generated data-entity doc. Snapshot 2026-07-02; regenerate via devPNT after structural changes.
status: CURRENT
---
<!-- devpnt:generated
  date: 2026-07-02T06:31:07
  generator: functional_docs_generator v1.0
  sources: (none)
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: d2ae755f57e59dee
-->

## Entities

| Entity | Python Classes | Key Attributes | Notes |
| :--- | :--- | :--- | :--- |
| User Profile | `User`, `UserProfile` | `id`, `username`, `email`, `bio`, `preferences` | Represents core system actors and their identity metadata. |
| Content Item | `Post`, `Comment` | `id`, `author_id`, `body`, `created_at` | Represents user-generated content entries. |
| Media Asset | `Image`, `Video` | `id`, `url`, `file_size`, `format` | Represents binary files linked to content or profiles. |

## Relations

User --1:N--> Post
User --1:N--> Comment
Post --1:N--> Comment
Post --1:N--> Media Asset