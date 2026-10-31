# Coordinating Parallel Sessions

Rules for several peer sessions working on one repository at once, one of them
coordinating. Read this only when they apply (§Trigger); a session that is not
coordinated never needs it.

## Trigger and roles

The rules apply while more than one session works on the same repository **and**
the owner has named the coordinating session in a request-record entry. The skill
never elects a coordinator. Without that naming no session coordinates: each works
in its own worktree, asks the owner before using an exclusive resource, and appends
to no record it does not own.

- **Coordinator** — the session the owner named. It keeps the shared files below,
  writes the record of the shared unit, and acts for the owner only within what the
  owner delegated.
- **Part** — a peer session the owner can talk to, working on its own unit and
  following the whole skill for it (triage, design, review, closure). It is not a
  dispatched subagent: `dispatch.md` governs those, unchanged.

Out of scope: which part runs next, in what order, with what priority — the owner
decides that, and nothing here records it (Non-Goal 1, ruling r3).

## 1. Every record has one writer

A request record numbers its entries; two writers number them twice (field case:
three sessions wrote R156–R158 into one record at once). So:

- A part's unit has its own record when its triage gives it one (every L3); the
  part is its only writer.
- The record of the shared unit the parts serve — the milestone, the umbrella — is
  written only by the coordinator.
- Owner words a part receives are recorded **before it acts on them**, in the record
  of the unit they settle. Words settling the part's own unit go to its own record.
  Words settling the shared unit are appended verbatim to the part's own record
  under the received heading (`templates.md` §REQUEST) and sent to the coordinator,
  which appends them verbatim to the shared record citing
  `REQUEST_[part].md#R<n>`.
- A part with no record of its own (below L3) sends the words; the coordinator's
  shared entry names that part and the date received, and the part acts once it
  exists.
- Every such entry keeps every rule of the record: verbatim, redaction, the owner
  told so they can correct a quotation.
- An artifact of the shared unit cites only the shared record: the coordinator
  enters the words before any such artifact relies on them.

## 2. Leases on exclusive resources

An exclusive resource has one holder at a time: the development container, the test
database, the code-writer role in a checkout a runtime mounts, any other the owner
names. A part asks the coordinator; the coordinator appends to `audit/leases.md`:

```
take <resource> — <session> — YYYY-MM-DD
release <resource> — <session> — YYYY-MM-DD
```

The file opens by citing the entry that names the coordinator; only the coordinator
writes it. A lease names a resource and a session, never a unit; it keeps no queue,
no waiting list, no order, and ends with its release (ruling r40). A restart or a
long suite on a shared resource is announced to the coordinator before it starts —
it kills what another session is running against it. A permission for a resource
given before the coordinator was named («restart it as much as you like, nobody else
uses it») rested on a single user: from the naming on it exempts no session from the
lease. If the owner restates it, the coordinator enters it as a `take` for that
session — a recorded lease, never an exemption. A lease never released is
closed by the owner through the coordinator; there is no timeout.

**The code-writer lease is the one exception to «own worktree»** (`SKILL.md`
Phase 4). The session holding it writes code in the checkout the runtime mounts;
every other session keeps its own worktree and writes no code there. The lease
passes to another session only once the holder's code in that checkout is committed,
or set aside with the owner's yes. Two sessions' code in that checkout is a
violation, code a previous holder left uncommitted included.

## 3. Decisions taken under delegation

A decision the coordinator takes under the owner's delegation is a request-record
entry under the delegated heading (`templates.md` §REQUEST), citing the delegation
entry — in Hybrid also the devPNT proposal it accepted (`hybrid.md`). It is the
decision's one home: an artifact relying on it cites the entry (ruling r41).

A delegation never reaches an earlier owner decision, of any unit: a choice that
would change one goes to the owner as a question. (Field case: under a delegation
to approve design boards, the coordinator removed a file the owner had decided to
keep; a design document was accepted on it before the coordinator withdrew.)

## 4. What travels between sessions

- An owner statement recorded verbatim in a request record is citable by every
  session.
- An authorization for a gated act — one the client or the skill makes wait for the
  owner's yes — is valid only in the session the owner gave it to. A message from
  another session saying the owner authorized it is information, never the
  authorization: the receiving session asks the owner, or the session holding it
  acts.
- A decision found to rest on a false fact is reopened by a new entry naming the one
  it corrects (`templates.md` §REQUEST); the old entry is never edited.

## 5. When a part stops

A part that stops — done, blocked, interrupted — sends the coordinator:

```
Unit / increment:
State: done | stopped at step <X>
Files touched:
Verification run and result:
Open points:
Needs the owner:
```

The coordinator checks each claim on the diff and the run output, never on the
message (`review.md`, an unproven completion claim), then tells the owner what is
done, what is left and what needs them.

A part can stop without being able to send (a crash, a closed client). A part with
no closure message is not done: before relying on its state — accepting its work,
mapping a commit, telling the owner it finished — the coordinator reads its HANDOFF
`next:` and its working tree, and tells the owner which closure steps (`SKILL.md`
Phase 5) the tree shows done and which it cannot tell. Whether to resume the part is the
owner's call.

## 6. One commit, several units

Before a commit carrying more than one unit's work, the coordinator writes the
commit map (`templates.md`) and runs:

```
python <skill_dir>/scripts/sdlc_check.py commit-map MAP
```

It checks the map against the working tree as it stands against HEAD: a generated
file under a unit, a changed HANDOFF or request record in no section, a file under
two units outside Shared, a file both under a unit and in Left out, a changed
authored file under Regenerated are errors; a
changed file in no section, a listed file with no change are warnings. It sees this
working tree only, not other worktrees. The commit stays the owner's.
