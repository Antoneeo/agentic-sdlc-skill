# Portability — carrying knowledge between projects

**For whom**: the agent moving a subgraph out of one project or into another.
**Answers**: "what travels, what refuses to travel, and what an import may decide".
**Does not answer**: where a claim's concept belongs (`taxonomy.md` — import *uses* that
pass, it does not replace it) or how a disagreement is settled (`reconciliation.md`).

## 1. What a bundle is

A directory mirroring the docs-root layout:

```
<bundle>/
  MANIFEST.md            kb_bundle: 1, source_project, topics, per-artifact sha256
  topics/<slug>.md
  corpus/given/<name>    + <name>.meta.md   (+ the .txt extraction, when there is one)
  corpus/notes/<name>.md
```

The layout is mirrored **on purpose**. Claim `source` cells are docs-root-relative, so
nothing is rewritten on import — and because `kb_claim_id` hashes
`path#locator#qty` with the text excluded, the same artifact cited at the same span
mints **the same id in every project**. De-duplication is therefore mechanical, not a
judgement call, and importing the same bundle twice is a provable no-op.

## 2. Export is a closure, not a selection

You choose topics; the export decides what must travel with them.

- **Every artifact a selected claim cites**, plus its sidecar and its stored extraction.
  A claim whose source cannot be reopened is model knowledge arriving by another route —
  the validator would reject it in the target, and correctly.
- **Every row a `CONTESTED` row points at.** The symmetry check refuses a set that lost
  half its members, so a partial export ships a tree that cannot pass its own checks.
  When a partner row lives in an unselected topic, that topic is **added and reported** —
  never dropped, never silently.

If a conflict partner resolves to no row at all, the export **refuses**: exporting a
broken set is worse than exporting nothing.

## 3. Import is additive, and decides nothing

`import` writes files. It does not place concepts, merge bodies, or settle disagreements.

- **Never overwrites a topic.** A slug that already exists is reported and skipped: two
  projects using the word `pricing` may mean two different things, and that judgement is
  the placement pass's (`taxonomy.md`, five verdicts, `owns:` against double placement).
- **Never deletes.** The doctrine is tombstones over deletion; an additive import has no
  business removing anything.
- **All or nothing.** The whole plan is computed before a byte is written. An import that
  half-applies leaves a tree whose checks fail and whose owner cannot tell what landed.

It refuses on: a missing or unmarked `MANIFEST.md`; a path that escapes the docs root; an
artifact whose name matches an existing one **with different bytes** (content-addressed
names must mean equal content — a mismatch means one of the two is lying about its
origin); an incomplete conflict set; a dangling `supersedes:`.

After importing, run `check`. The import is deliberately not a validator.

## 4. Knowledge crosses; authority does not

`RULING` means *the fact you know and the corpus does not*, with a `basis:` you gave. It
is the only thing that settles a `CONTESTED` set. A ruling from another project carries
another owner's decision, and importing it unchanged would make that decision binding
here without anyone here granting it — the machine deciding, which reconciliation
refuses everywhere else.

So an imported ruling arrives as **`prov: IMPORTED`** (owner ruling, 2026-08-03):

- its text, span and original `basis:` travel **verbatim** — the knowledge is not lost,
  and pretending it is a `DERIVED` synthesis would make the row lie about where it came
  from;
- its note carries `imported_from:`, and the validator refuses an `IMPORTED` row without
  it: unnamed, the class says nothing and the row is a `RULING` with the label filed off;
- **it cannot supersede a local row.** The validator errors on `SUPERSEDED <id>` when
  that id is `IMPORTED`.

**Re-ratification** is one act: read it, write your own note with your own `basis:`, and
set the row's `prov` to `RULING`. That is you deciding, which is the only thing that ever
settles anything here.

## 5. Triage

Exporting is L1 — it writes nothing into the corpus and changes no knowledge. Importing
is **L3**: a source enters the corpus and nodes are created, which is the L3 definition
in Rule Zero, and the bundle is external input, which is never L1 whatever its size.
