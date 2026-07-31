# The Knowledge Taxonomy Pass

Applies at L3, in phase 3, AFTER spec elicitation and BEFORE new knowledge documents or SOPs are drafted. It answers the key question: *does the knowledge base already contain the categories, entities, or SOPs this topic needs?*

Why it exists: **a document is not an isolated island of knowledge.** Left alone, an agent drafts a new document and duplicates concepts, entities, or rules that are already defined elsewhere in `ai_docs/` — so no single file owns the authoritative concept, updates are missed, and the knowledge base accretes conflicting information.

## 1. State the topic as Knowledge Domain Concepts, not as files

Write what knowledge concepts or SOPs are required — "customer onboarding procedure", "API authentication policy", "Q3 strategic goals". A concept names a domain subject. It names no specific file: that is the decoupling.

Two or three concepts are normal for a knowledge unit. State them under the `## Knowledge Taxonomy Ledger` heading.

## 2. Rule each concept against the Knowledge Base

One verdict per concept:

| Verdict | Meaning | What the row must carry |
|---|---|---|
| **EXISTS** | an existing document already owns this concept/SOP and covers the need | the file path, section, and the authoritative definition confirmed |
| **INADEQUATE** | a document owns the topic but is incomplete or outdated | the file path, and the specific gap or missing information |
| **MISSING** | no existing document covers this concept | the terms searched, the query tool used, and directories checked |

Read the `ai_docs/INDEX.md` and `ai_docs/reference/INDEX.md` (Guide Router) first — the inventory of what owns which concept.

## 3. Design missing knowledge units autonomously

When a concept is **MISSING**:
- Design it as an authoritative note or SOP guide in `ai_docs/reference/GUIDE_[topic].md` or `ai_docs/solutions/ANALYSIS_[topic].md`.
- Ensure it defines a single source of truth for that topic.
- Update `ai_docs/INDEX.md` upon completion using `sdlc_check.py index`.
