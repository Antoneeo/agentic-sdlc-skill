---
description: Why the D-UC / use-case grounding gate is two mechanical checks (product-name buckets + benefit-trace), verified by a light independent review that PRECEDES but does not replace the human.
status: CURRENT
---
# ADR: Use-case grounding gate — a light review that precedes, not replaces, the human

**Status:** Accepted
**Date:** 2026-08-05
**Task ref:** owner feedback session 2026-08-05 (post-1.23.0 Interface Contract release)

## Context
The S2A2 chain grounds its BOTTOM in real source — the E-ISP blast-radius mandate forces
`find_symbol_usages`/`get_call_sites` enumeration against the actual codebase. Its TOP, the
`D-UC` / use-cases, was grounded in nothing. An author could propose use-cases naming actors,
surfaces or capabilities the project does not have, or needs the Vision never asked for, and
nothing caught it until the E-ISP tried and failed to map impact — the most expensive place to
discover it, after D-IC, P-TM and E-ISP have all built on the fiction. The owner named the gap:
"è fondamentale che UC debba avere grounding sul sistema per non proporre cose che non fanno
parte dell'obiettivo della vision e che non sono presenti nel progetto."

Two things had to be decided: (a) WHAT the gate checks — an open-ended "is it grounded?" invites
a vibe review; (b) WHO enforces it — the human alone, or an independent AI pass.

## Decision
A tight **two-check** gate on the `D-UC` / use-cases, and nothing else: (1) every product name
resolves to exactly one bucket — EXISTS (the product's own term for a real thing), NEW (declared),
or METAPHOR (illustrative only, never an interface element); a name in no bucket invents system
reality that is not there. (2) every use-case traces to a Vision / M-VISION benefit; one that
traces to nothing is drift. Both read the use-case TEXT, so both are falsifiable predicates a
reviewer can verify — not a judgement call.

Enforcement: an **independent light review runs FIRST and does not replace the human** — AI
review, then the owner's own. The user-need judgement (is this the right need / actor / UX?) stays
the owner's; the light pass rules only on the two grounding predicates. Landed in both the skill
(the moment-1 design review; `review.md` use-case-grounding clause; owning definition in
`templates.md` `## Use Cases / User Needs`; cited in `SKILL.md` §3) and devPNT (§4.5 scope
extended to `D-UC` grounding-only; `devpnt-tech-reviewer-light` gains a D-UC checklist).

## Alternatives considered
- **Open-ended "ground the use-cases" gate** — rejected: unfalsifiable, becomes a vibe review.
  The owner compressed it to two mechanical checks ("due cose e nient'altro").
- **Human-owned only, no independent reviewer** — first chosen, then rejected on the owner's
  correction: an AI light pass catches ungrounded names / untraced use-cases mechanically before
  the human spends attention, and the two checks ARE verifiable (grep the real name; read the
  M-VISION), so they suit a light reviewer. It precedes, never replaces, the human.
- **Bring the whole D-UC into the independent review** — rejected: the user-need JUDGEMENT stays
  human-owned (§4.5 keeps M-VISION/D-UC judgement with the human); only the two grounding
  predicates enter the review, never the need itself.

## Consequences
- **Pro:** the funnel's top is grounded before D-IC binds it, P-TM assesses it and E-ISP maps it;
  invented scope and vision drift are caught at the cheapest point; the human still owns the need.
- **Con / risk:** one more light-tier pass on the `D-UC`; the EXISTS check depends on the reviewer
  verifying the product's real terms against source (a few reads). Sized to the change — two
  checks, no blanket conformance theater elsewhere.
