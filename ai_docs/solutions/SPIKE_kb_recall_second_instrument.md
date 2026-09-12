---
description: Negative spike — whether kb's recall needs a mandated text probe (and a claims inventory) to stop a false `kb: no coverage`. Two replays refuted the defect; the one real finding became the multi-slug verdict.
status: CURRENT
domain: code
---
# Spike: the recall's second instrument

## Question to answer
The recall's four verdicts all sit downstream of the semantic descent, and none
requires a second instrument. Does a descent that picks the wrong branch therefore
declare `kb: no coverage` on a corpus that holds the answer — a false negative
indistinguishable from genuine absence, after which the agent answers from model
memory?

## Time-box
2026-09-12, one session: a static read of the kb distribution, an assertion harness,
and two agent-level replays. `Level: L3 → reclassified` (see Consequences); router:
no match; lens code per `routing.md` step 3 (`sdlc_check.py` is build-consumed).
devPNT points at another project, so Standalone throughout.

## What was tried
**Static reading.** `SKILL.md` §Topic Recall, `taxonomy.md` §1/§6, `reconciliation.md`,
`distillation.md`, and the generated indexes in `scripts/sdlc_check.py`
(`kb_build_topic_index`, `kb_build_corpus_index`, `_kb_extra_validate`,
`kb_cmd_index`). Four text facts, all verified and all still true: the topic INDEX
carries four columns (slug, description, parents, synonyms); claims live inside
`topics/*.md` and no index addresses them; `kb: no coverage` is defined as "index
read, nothing fits"; `grep` appears in `guides.md` and `review.md` and never in the
recall.

**Vision Gate.** `VISION_kb_second_brain.md` (APPROVED) needs no amendment: a false
negative on a covered theme is a failure of its own success signal, and its Non-Goal
already declares the corpus "file-based, greppabile". The admission test placed the
two halves on different rows — the probe on **r14** (defect, purpose/actors/surface
unchanged, no new row), the claims inventory on **r7** (a user-visible ability under a
maintenance label: ruled fresh). The inventory's r2/r9 near-miss was disclosed per
**r8**, and its ceremony cost was priced, corrected and accepted by the owner —
then abandoned with the defect (below).

**The harness** (`harness_kb_recall_probe/probe.py`). Term-level measurements on a
fixture whose topic description shares no vocabulary with the question while a claim
inside answers it, plus a control fixture where the term IS in the description, plus
one invariant on the validator's freshness tuple. RED baseline recorded before any
edit.

**Two agent-level replays** (`replay_2026-09-12.md`). Fresh agent, no other context,
the current doctrine verbatim, a fixture KB by path, one practitioner question.
Neither subject was told what was expected, nor that a defect was under test.

## Answer / Outcome — the defect was NOT reproduced
Both replays returned the answering claim. Run 1 (vocabulary mismatch, one topic):
`kb: deployment → 3 claims cited`, citing the ruling and naming the supersession it
replaced. Run 2 (eight topics, the answering claim under `gdpr_compliance` while
`observability` — synonym `log`, carrying log claims — was the more plausible
branch): `kb: gdpr_compliance, observability → 2 claims cited`, three branches opened.

Three reasons the static reading was wrong, none visible without executing:

1. **The descent judges semantic coverage of concepts, not presence of terms.** A
   description that summarizes a topic still covers questions about the claims inside
   it. "The question's term is absent from the index row" measures vocabulary, never
   reachability — the harness's P2a says exactly that and no more.
2. **The descent is multi-branch by mandate.** `taxonomy.md` §1 requires following
   every parent and opening the final candidates, plural. A single wrong branch was
   never the shape of the act.
3. **The remedy is already emergent.** Run 2 executed
   `grep -rniE "retain|retention|conserv|SUPERSEDED|log" topics/` unprompted, as a
   cross-check for a contradicting claim. Mandating a probe would add doctrine bytes
   for a behaviour a capable subject performs on its own, on the corpus property the
   Vision already declares — which is what the "no ceremony ratchet" Non-Goal exists
   to refuse.

**One defect WAS reproduced, and it is not the one under test.** The four legal
verdicts assumed exactly one matched slug while the doctrine mandates descending every
candidate. Run 2 had to invent a form and said so: "the slug slot carries two slugs
because the descent legitimately matched two branches". A mandated act with no legal
way to declare its result is a contract gap.

## Consequences
- **Reclassified L3 → L2 and shipped as the multi-slug verdict form**: both
  node-naming verdicts now read `kb: <slug>[, <slug> …] → …`, with the reason on the
  record (which branches were opened is the part of the verdict a reader can check).
  Four legal values, unchanged — the repair is in the form, never a fifth value.
  Pinned by `scripts/test_kb_recall.py::test_the_verdict_form_admits_every_branch_the_descent_opened`,
  proven red against `HEAD` before the edit, and by the behavioural scenario
  `evals/scenarios/recall_verdict_names_every_branch.md`, whose fixture IS run 2's.
- **Abandoned: the mandated text probe and the claims inventory.** Neither ships. The
  harness carries no assertion for them: a probe pinning what was decided against is
  red by construction, which is a defect and not diligence.
- **Fixed in passing** (L1, and a prerequisite for this spike's own verification):
  `evals/run_behavioral.py` printed scenario text to a cp1252 console and died on
  `→` — so the shipped scenario `recall_descends_before_answering.md` had been
  un-runnable on a default Windows console since kb 1.7.0. stdout is now reconfigured
  to UTF-8 with `errors="replace"`.
- **Standing limits.** Two runs, one subject model, fixtures authored by the session
  that made the claim. The negative bounds the defect's frequency on those two shapes;
  it does not prove no shape reproduces it. Searching for a third fixture until one
  goes red was declined as rigging, on this project's own rule that a probe must be
  able to fail and a verdict is invalid on "found nothing".
- **Open, unrelated and untouched**: `SPIKE_kb_composition.md` (federated consultation
  of autonomous KBs) remains the standing kb design question.

Sources: `distributions/kb-agentic-skill/skills/kb-agentic-skill/{SKILL.md,taxonomy.md,reconciliation.md,distillation.md,scripts/sdlc_check.py,scripts/test_kb_recall.py,evals/run_behavioral.py}`;
`ai_docs/vision/features/VISION_kb_second_brain.md`; `ai_docs/vision/rulings.md`;
`ai_docs/solutions/harness_kb_recall_probe/{probe.py,replay_2026-09-12.md}`.
