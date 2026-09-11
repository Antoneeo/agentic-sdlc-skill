# The Hybrid Seam — coexistence with devPNT

**For whom**: the agent working a project where the `devpnt_*` tools are available
and point at this project.
**Answers**: "which mode am I in, who owns what when both authorities are live,
and how do the two vocabularies map onto each other".
**Does not answer**: the process itself — triage, the phases, the gates and the
write triggers are `SKILL.md`'s, and they are identical in both modes.

Moved out of `SKILL.md` by F-051 so a Standalone session stops paying for a seam
it cannot reach. **The content below is unchanged**: this file is a relocation,
not a rewrite.

<!-- moved-block-sha256: f11e6d5b9cd4710849fa9d3701f16ff0da39f2d163e8ffdb8adbff6a119b3614 -->
### Hybrid in symbiosis with devPNT

Use this mode when the `devpnt_*` tools are available and point at the current project.

Authoritative hierarchy:
1. **devPNT M-VISION**: strategic beacon of the milestone. Before design or code, read it and verify benefits, success signals, scope-in and non-goals.
2. **devPNT Master Plan**: strategic roadmap and milestones.
3. **devPNT Action Plan**: current tactical work for the active goal.
4. **devPNT governed artifacts**: `D-UC`, `P-TM`, `E-ISP`, `E-TDD`, `E-TP`, ADR.
5. **Local `ai_docs/`**: readable context, Standalone fallback, local handoff or shadow/mirror when useful.

Hybrid rules:
- devPNT is the governed source for plans and artifacts; do not create a second truth in `ai_docs/`.
- The skill stays autonomous: if devPNT is not there, switch to Standalone without losing capability.
- If the user request, the local Vision and the M-VISION diverge, stop and make the conflict explicit.
- Do not create or modify milestones without respecting the M-VISION.
- Never auto-accept devPNT proposals: present the preview and wait for explicit confirmation.
- If the local devPNT protocol imposes stricter bootstrap, plans or gates, follow them.

## Coexistence with devPNT (the Hybrid seam)

This section is the single authoritative answer to "who owns what" when both the
skill and devPNT are active. The skill owns the **process** (triage, phases, Vision
Gate, lifecycle); devPNT owns the **machinery** (governed storage, versioned
proposals, semantic analysis, independent reviewers). devPNT strengthens the
process; it never replaces it.

### Ownership matrix

| Artifact | Standalone master | Hybrid master | Mirror rule |
|---|---|---|---|
| Product vision | `vision/project_vision.md` | `vision/project_vision.md` (product scope) | devPNT KL vision is regenerated from it, never edited independently |
| Milestone vision | `vision/roadmap.md` milestones | devPNT M-VISION | `roadmap.md` may reference the M-VISION key; it never restates its content |
| Feature design | `solutions/ANALYSIS_[feature].md` | devPNT E-ISP/E-TDD (+ D-UC/P-TM) | shadow exported from the ACCEPTED DB version as `SHADOW_[doc_key]_vX.Y.md`; on divergence the DB wins and the shadow is regenerated |
| Plans | `## Action Plan` inside the ANALYSIS | devPNT Master/Action Plan | none |
| Feature state | ANALYSIS frontmatter `status` | Action Plan node status | mapping table below; at closure both must move together |
| ADR | `architecture/` (canonical dir) | devPNT DB (`adr_YYYY-MM-DD_slug`) | optional filesystem shadow `SHADOW_adr_*` exported at closure for grep-ability |
| Audit / freshness | `audit/audit_plan.md` + `stale`/`mark` | devPNT KL coverage + summary status | run `check --hybrid` (skips audit-plan staleness) |
| Design review (pre-implementation) | `review.md` moment 1, on the ANALYSIS | devPNT §4.5 gate on `E-ISP`/`E-TDD` | same slot, richer backend — run ONE of them, never both |
| *(mode is per unit of change, not per project)* | a Hybrid-capable project may work one feature Standalone: the slot follows the ARTIFACT the design lives in, and the mode is declared in that artifact. `validate --hybrid` suppresses the Standalone design-review backstop, since devPNT owns the slot there | | |
| Review log | `audit/reviews/REVIEW_LOG.md` | devPNT `REVIEW_LOG.md` (same path) | always filesystem |
| Operative guides | `ai_docs/reference/` | `ai_docs/reference/` — **filesystem-first even in Hybrid** | devPNT bootstrap may point at their index; it never copies their content |
| Handoff | `audit/handoff.md` | `audit/handoff.md` | always filesystem |

### Triage equivalence (one threshold, two vocabularies)

devPNT's "significance threshold" and the skill's triage are the SAME test. Do not
run two classifications:

| Skill triage | devPNT equivalent | Governed artifacts |
|---|---|---|
| L1 Trivial | trivial exempt | none |
| L2 Small | localized obvious edit | none — but see escalation |
| L3 Significant | governed unit of change | D-UC/P-TM/E-ISP/E-TDD per the devPNT trigger policy |
| Spike | exempt (non-mergeable) | `SPIKE_[topic].md` only |

Escalation triggers (any one of these makes it L3, in BOTH vocabularies): touches
more than one module, changes a public API/contract/message format, changes a data
model or state machine, has a security surface, risks duplicating existing logic,
or the design choice is non-obvious. An L2 that trips one of these is not an L2.

### Feature state mapping

| ANALYSIS frontmatter | devPNT plan node |
|---|---|
| PLANNED | READY (or BLOCKED / ON_HOLD while waiting) |
| IN_PROGRESS | PROGRESS |
| COMPLETED | DONE |
| CANCELLED | CANCELLED |

Closure discipline: never mark the node DONE while the shadow/ANALYSIS still says
IN_PROGRESS, or vice versa. They move in the same closure step.

### Shadow discipline (Hybrid)

- Shadow filename: `SHADOW_[doc_key]_vX.Y.md`, first line
  `<!-- SHADOW generated from devPNT (doc_key vX.Y) - do not edit by hand -->`.
  Never save a shadow under an `ANALYSIS_*` name: that name means "authoritative
  Standalone document" and the validator treats it as such.
- **Export the approved E-TDD shadow BEFORE implementation** (not only at closure).
  It gives context-free subagents their design input, unlocks `gate --hybrid`, and
  guarantees the filesystem fallback if devPNT becomes unavailable mid-feature.
- At closure, refresh all shadows from the accepted DB versions.

### Validator in Hybrid

Pass `--hybrid` explicitly (never auto-detected — an explicit flag beats a guessed
mode): `check --hybrid` and `stale --hybrid` skip audit-plan staleness (mapping is
delegated to devPNT/KL) — guide-drift checking still runs (`ai_docs/reference/`
is filesystem-first even in Hybrid, see the ownership matrix above); `gate --hybrid`
also unlocks on the presence of an E-TDD shadow in `solutions/` (the Hybrid design
gate) instead of requiring an IN_PROGRESS ANALYSIS.
