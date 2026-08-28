# The Knowledge Taxonomy Pass — placing a claim in the topic graph

**For whom**: the agent holding extracted claims (`distillation.md`) that need a home.
**Answers**: "which node owns this concept, and what do I do when none does".
**Does not answer**: how claims are extracted (below — `distillation.md`) or what happens
when two claims disagree (below — `reconciliation.md`).

Why it exists: **a fact placed twice is a fact that will diverge.** Left alone, an agent
creates a new topic for every document it reads, no node owns the authoritative concept,
and the base accretes near-duplicates that answer the same question differently.

## 0. The graph, in one paragraph

`topics/<slug>.md`, one file per topic, **flat** — hierarchy lives in `parents:`
(a list: a topic may sit under several), never in the path, so inserting a parent above
ten existing nodes is an edit, not a file move. The graph grows **upward as well as
downward**. `topics/INDEX.md` (generated) is the router: slug, description, parents,
synonyms. Coverage state does not exist — `gaps:` inside a node says what that node
knows is missing, and nothing collects it.

## 1. Descend, do not scan

Placement is semantic judgement; no query performs it. What makes it affordable is the
abstraction hierarchy: read the top-level rows of `topics/INDEX.md`, pick the branch
whose description covers the claim's concept, repeat. Follow **every** parent listed —
a topic can be legitimately reachable from two branches, and descending only one is how
a duplicate gets created while the rules are obeyed. Synonyms are in the index precisely
so "listino" finds `pricing`. Open only the final candidates.

During a batch, the candidate set **includes what this run already created** — held in
memory, rebuilt at start by reading `topics/*.md` frontmatter (the files are the state;
a crash loses nothing a directory read does not restore). `topics/INDEX.md` is written
once, by `sdlc_check.py index`, at the end — never hand-appended mid-run.

## 2. Five verdicts

| Verdict | When | Action |
|---|---|---|
| **EXISTS** | a node owns the concept | reconcile the claim into it (`reconciliation.md`) |
| **INADEQUATE** | a node covers the area, the claim is finer-grained | deepen it, or create a child under it |
| **MISSING** | no node covers it | create under the nearest more-general node: slug, one-line `description:`, `parents:` |
| **GENERALIZES** | the concept sits **above** existing nodes | an **escalation trigger** — see §4 |
| **UNPLACED** | about no topic (document metadata, a signature, a procurement window) | `topics/unplaced.md` — a holding pen; nothing ranks or counts it |

**MISSING may only be declared after querying the graph.** An unread index can never
ground a MISSING verdict — otherwise the same thing gets built twice. The mechanical
side (double-owner check, near-duplicate warning) verifies afterwards; it does not
replace the descent.

## 3. Similar but perhaps not the same → sibling, never a merge

Create the node at the same level, set `related: <existing-slug>`, and write **one line
stating the distinction** ("distinct from `pricing` because it covers negotiated
exceptions, not list prices"). If that line cannot be written, they are the same concept
— go to reconciliation instead.

Why this direction: over-merging is the harmful error. One wrong merge contaminates
both topics' claims and propagates through every reference; a redundant sibling costs a
later merge. The deferral is only correct because merging **does** happen later: the
**canonicalization pass** — run at closure, or when the near-duplicate warning fires —
revisits `related:` pairs and either merges (tombstone the loser: `status: SUPERSEDED` +
`redirect_to:`, body emptied) or strengthens the distinction line.

## 4. GENERALIZES escalates; re-parenting is guarded

Re-parenting rewrites the graph's shape, and kb's Rule Zero makes hierarchy changes L3
(escalation triggers, `SKILL.md`): stop, declare, and treat it as its own unit — never a
side effect of placing one claim. A GENERALIZES that would create a **new root** also
stops for the practitioner: reframing the whole base is a decision, not a placement.

Before writing `parents:`, walk the target's ancestor chain; if the node itself appears,
**refuse** — a cycle detaches a subtree, and since descent is the only retrieval path, a
detached ring is invisible forever. The validator's `graph` check reports cycles and
unreachable nodes as errors, but the refusal at write time is what prevents them.

## 5. Tombstones, never deletion

A merged or renamed topic keeps its file: `status: SUPERSEDED`, `redirect_to: <slug>`,
body emptied. Inbound references resolve through it; a claim re-placed from an old
source lands on the survivor instead of resurrecting the dead slug.

## 6. The same descent, answer mode

The descent above also serves ANSWERING (`SKILL.md` §Topic Recall): when a reply would
assert facts about the project's domain, descend before answering from model memory.
Differences only — no placement verdicts, no writes; the descent stops at reading the
matched node's claims; coverage (found / not found) replaces the five verdicts; UNPLACED
does not exist when reading. Everything else applies unchanged: descend don't scan,
follow every parent, synonyms, tombstone redirects resolve to the survivor.
