# Knowledge Reconciliation Protocol

Applies when contradictory notes, conflicting SOPs, or outdated documentation are discovered in `ai_docs/`.

## Systematic Reconciliation Steps

1. **Identify the Contradiction / Conflict**:
   - Locate the exact files and sections that conflict (e.g. `doc_A.md` says X, `doc_B.md` says Y).
2. **Trace Primary Sources & Freshness**:
   - Inspect creation/modification dates and frontmatter `status` of both documents.
   - Determine which document represents the most recent or user-confirmed source of truth.
3. **Reconcile & Update**:
   - Update the authoritative document with the correct, reconciled information.
   - Mark the outdated document `status: SUPERSEDED` or `DEPRECATED`, adding `supersedes: <old_doc.md>` in the header of the new document.
4. **Re-index Knowledge Base**:
   - Run `python <skill_dir>/scripts/sdlc_check.py index` to update `ai_docs/INDEX.md` and refresh the router.
