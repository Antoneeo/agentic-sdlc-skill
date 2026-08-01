# Signal Distillation & Verification Discipline

Signal Distillation replaces raw text dumping with contract-first, high-signal knowledge extraction. It operates in symbiosis with the `distill` skill discipline.

## Core Rules of Distillation

1. **Contract-First Writing**: Before writing or updating any non-trivial document, compile the text contract:
   - **Reader**: Who is consuming this document? (Agent, User, Specific Role).
   - **Action**: What decision or action will the reader take based on this document?
   - **Payload of Assertions**: What exact facts, constraints, and SOP steps are being asserted?
   - **Form**: What structure best conveys this signal? (Markdown table, numbered list, YAML frontmatter).
2. **Zero Speculation / Fact Verification**:
   - Every claim must trace back to a verifiable source (user prompt, primary document, inspected file, or explicit decision).
   - If information is unverified or speculative, mark it explicitly (`[unverified]` or `[requires user input]`) or omit it.
3. **Signal-to-Noise Ratio (Loss/Noise Gate)**:
   - Eliminate filler text, generic intros, pleasantries, and redundant explanations.
   - Keep only deterministic facts, decision logs, domain rules, and step-by-step SOP instructions.
4. **Lifecycle & Freshness Tagging**:
   - Every document must carry YAML frontmatter specifying `status: CURRENT` (or `SUPERSEDED`, `DRAFT`, `DEPRECATED`).
   - When new knowledge supersedes old knowledge, mark the old file `status: SUPERSEDED` and add `supersedes: <old_file.md>` to the new file.
