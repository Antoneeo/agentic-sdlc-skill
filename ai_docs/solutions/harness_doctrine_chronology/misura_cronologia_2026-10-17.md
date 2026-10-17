# Measurement: "what did we do this week" from documents alone (2026-10-17)

Read-only measurement, run on this machine's session scratchpad scripts (not shipped).
A = a field project on the knowledge lens (its name and file names are left out of this
public repository; counts and dates only). B = this repository (`ai_docs/`, branch
`feat/kb-site-spec`, `git --all`).

## 1. Dated records per place

| place | A | B |
|---|---|---|
| Diary: files / entries | 49 / 522 | 64 / 413 |
| entries starting with an ISO date | 432 (83%) | 244 (59%) |
| bullets under a dated heading | 64 | 53 |
| undated entries (paragraphs, headings, bullets) | 26 | 116 |
| distinct forms of a dated entry | 15 | 15 |
| non-ISO dates at the start of an entry | 0 | 0 |
| files with dates out of order | 6 (4 are SPEC) | 2 (+4 in reverse order) |
| REQUEST `### Rn — date` | 25/26 (one "R4-nota") | 47/47 |
| corpus/notes `date:` | 236/236 | – |
| sidecar `date:` | 304/304 | – |
| REVIEW_LOG dated rows | 56/56 | 204/204 (two table schemas) |
| HANDOFF `updated:` | 26/26 | 6/6 |
| dated ADRs | 1/2 (decisions live in RULING_/ELICITED_ notes) | 20/20 |

Free-text dates inside A's HANDOFF bodies: 229 ISO, 102 DD/MM, 34 "15 ottobre". 15 of
the 26 `next:` fields contain dates (21 DD/MM, 20 ISO).

## 2. Duplication

Verbatim copying (6 consecutive words) is low: `next:` repeated in the HANDOFF body ≤8%,
in the Diary ≤6%. The duplication is paraphrase, so no check sees it.
`next:` in A: median 500 characters, maximum 7,540, 24.9k in total over 26 workstreams;
in one case `next:` (2,074) is longer than its HANDOFF body (859). In B: median 127,
maximum 214.

## 3. Coverage of the last 7 days (unit × day from git log)

- A: 14 unit-days, 13 covered by a dated entry (one unit dated 16/10, committed 17/10).
  Gap: one unit whose only trace is a claim row; claim rows carry no date.
- B: 15 unit-days, 3 of audit_plan marking only excluded → 12. Covered in the places
  the F-072 spec lists: 6 (F-072, F-071/F-070, F-069, F-068, F-067, F-066 — the last
  dated 12/10, committed 13/10). Only in the prose of `project_notes`: 3 (release
  1.40.0, its registration, Course on latest). Only `updated:`: C-001 (15/10). Nothing:
  the viewer spike (SPIKE without dates), F1 (no ANALYSIS).

## 4. Reading

The problem is the form and the place, not the absence of dates: 15 forms of Diary
entry; `next:` used as a state summary in A; in B, work without an ANALYSIS (release,
fix, spike) leaves no dated entry where the doctrine says to look. Smallest change
suggested by the measurement (to be verified, not adopted as is): validate checks that
every Diary entry starts with one date format; `next:` holds only the next step, with a
length warning; work without an ANALYSIS leaves a dated line in `project_notes`.
