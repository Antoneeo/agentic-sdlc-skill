---
id: resume_rereads_unit_vision
expected: working from a summary, the agent re-reads the open unit's request record and vision before answering about it, and answers citing them
---
## Setup
- The conversation the agent receives is a summary of an earlier one. About the open unit F-200 it says only: "F-200: facts reported about sibling-chat titles and note search; pending question for the owner on sibling-chat titles."
- ai_docs/audit/handoff.md: Workstream registry. F-200 Memory notes -- L3 -- PROGRESS -- next: answer the open question on sibling-chat titles.
- ai_docs/audit/requests/REQUEST_memory_notes.md: Request record of F-200. R1 quotes the owner asking for two things: the assistant knows what the person owns, and details are kept in notes when a long conversation is compacted.
- ai_docs/solutions/ANALYSIS_memory_notes.md: F-200, status IN_PROGRESS. `## Feature Vision` states two halves: knowing what the person owns; and "when a long conversation is compacted, the important details stay in notes the person sees and manages". Scope lists "notes of remembered details at compaction".
- The code contains no function that writes a note at compaction.
## Prompt
Has the feature that saves details to notes at compaction time been built?
## Pass criteria
- Before answering, the agent reads REQUEST_memory_notes.md and the `## Feature Vision` of ANALYSIS_memory_notes.md: the question is about a unit with an open workstream and the context is a summary.
- The first answer links the question to F-200 and cites its vision: the notes at compaction are the second half of F-200's scope, not yet implemented.
- The answer does not rest on "I take it that it belongs to F-200" or any wording that marks the link as assumed. That wording, with the vision unread, is the recorded case and a fail.
- The agent does not run a chain of code and log searches in place of the read; a search of the code to confirm "not built" after the read is fine.
- The owner does not need a second question to get the link to F-200.
