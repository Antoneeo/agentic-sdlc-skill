# The Hybrid Seam — coexistence with devPNT (marketing lens)

**For whom**: the agent working a marketing engagement where the `devpnt_*` tools
are available and point at this project.
**Answers**: "which mode am I in, and who owns what when both authorities are live".
**Does not answer**: the process itself — the engagement triage, the SOSTAC
phases, the gates and the evidence discipline are `SKILL.md`'s, identical in both
modes.

Moved out of `SKILL.md` by F-052 so a Standalone session stops paying for a seam
it cannot reach. **The content below is unchanged**: a relocation, not a rewrite.

<!-- moved-block-sha256: b9b19d58a104e858f38460065160a61e64a6cd6f64f92c1bbf47fbf534d25ef6 -->
### Hybrid in symbiosis with devPNT

Use this mode when the `devpnt_*` tools are available and point at the current project.

Authoritative hierarchy:
1. **devPNT M-VISION**: strategic beacon of the plan cycle. Before strategy or tactics, read it and verify benefits, success signals, scope-in and non-goals.
2. **devPNT Master Plan**: the marketing roadmap; milestones are plan cycles (a quarter, a launch, a market entry).
3. **devPNT Action Plan**: the nine phases of the active engagement as tactical nodes.
4. **devPNT governed artifacts**: the marketing artifact set (table below).
5. **Local `mkt_docs/`**: readable context, Standalone fallback, evidence ledger home, shadow/mirror when useful.

### Ownership matrix (the Hybrid seam)

The skill owns the **process** (triage, phases, gates, lifecycle); devPNT owns the **machinery** (governed storage, versioned proposals, review wiring). The marketing artifacts occupy the same governance slots the software artifacts occupy in the sibling skill:

| Artifact | Standalone master | Hybrid master (devPNT slot) | Mirror rule |
|---|---|---|---|
| Marketing vision | `vision/MKT_VISION.md` | M-VISION (`milestone_vision_<slug>`) | filesystem copy is a shadow; DB wins |
| ICP & Personas | `strategy/ICP_PERSONAS.md` | `mkt_icp_personas` (D-UC slot) | shadow `SHADOW_[doc_key]_vX.Y.md` |
| Threat map | `strategy/THREAT_MAP.md` | `mkt_threat_map` (P-TM slot) | shadow |
| Objectives | `strategy/OBJECTIVES.md` | `mkt_objectives` | shadow |
| Strategy | `strategy/STRATEGY.md` | `mkt_strategy` (E-ISP slot) | shadow, exported BEFORE tactics work |
| Tactical plan | `tactics/TACTICAL_PLAN.md` | `mkt_tactical_plan` (E-TDD slot) | shadow, exported BEFORE action phase |
| Measurement plan | `tactics/MEASUREMENT_PLAN.md` | `mkt_measurement_plan` (E-TP slot) | shadow |
| Evidence ledger | `research/evidence_ledger.md` | `research/evidence_ledger.md` — **filesystem-first even in Hybrid** | validator needs it on disk; devPNT may reference, never copies |
| Final plan + one-pager | `deliverables/` | assembled from ACCEPTED artifact versions | PDF via `devpnt_generate_document_pdf` when available |
| Handoff | `audit/handoff.md` | `audit/handoff.md` | always filesystem |

Hybrid rules:
- devPNT is the governed source for plans and strategy artifacts; do not create a second truth in `mkt_docs/`.
- The skill stays autonomous: if devPNT is not there, switch to Standalone without losing capability.
- If the user request, the local vision and the M-VISION diverge, stop and make the conflict explicit.
- Never auto-accept devPNT proposals: present the preview and wait for explicit confirmation.
- Where the local devPNT protocol imposes stricter gates (vision creation/amendment gates, independent review gates), follow them: they are the same discipline this skill encodes.
