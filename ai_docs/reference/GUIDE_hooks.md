---
description: Consult before changing hook installation, ownership, Codex event normalization or client diagnostics.
status: CURRENT
source_kind: code
source: F-091 hook implementation on baseline 74c1833f, captured 2026-11-04
distilled_from: ai_docs/reference/.sources/hooks-c44cdcbf.md
source_hash: c44cdcbf3fd4830f52bbf8f6b0848c9233e7aadbfcec39813e94ef87815b6cc6
topics: [hooks, installation, codex]
---
# Guide: hook lifecycle and event interpretation

For a maintainer locating the authoritative component before editing. This guide maps
implemented contracts; acceptance evidence belongs to ANALYSIS_codex_hooks and its
harness. It does not certify client trust or native execution.

## Installation owner
[source: hooks-c44cdcbf.md#postinstall]
[source: hooks-c44cdcbf.md#init]
[source: hooks-c44cdcbf.md#wirecodexhook]
[source: hooks-c44cdcbf.md#hookhandler]
[source: hooks-c44cdcbf.md#hooksources]

`scripts/lib.js` owns client paths, hook profiles, markers and merging. The main
postinstall wires four Codex user-level handlers after skill copy. Init configures
orientation only, reusing the user-level writer. Claude takes its original branch;
its settings target and commands stay unchanged. Sibling Node installers keep their
own scope: never replace their lib.js wholesale with this package's copy.

[source: hooks-c44cdcbf.md#consent-label]

Each generated Codex handler carries a distinct statusMessage explaining its purpose; the installed desktop also uses it as the consent-row title.

Codex uses CODEX_HOME/hooks.json and absolute installed-validator paths. JSON/TOML
user and current-project sources are inspected before writing. Existing runtime-equivalent (event/matcher/type/complete argv),
disabled, removed, malformed or unverifiable configurations are preserved and
reported. Inspecting a definition is not proof it is trusted or executing.

## Ownership and removal
[source: hooks-c44cdcbf.md#removeglobalhookentries]
[source: hooks-c44cdcbf.md#decodehookinvocation]

Each hook keeps its per-target opt-out marker. Reinstall never repairs a removal
silently, including deletion of an entire recorded TOML file. Cleanup decodes the fixed invocation and removes entries only when their
validator belongs to a removed skill root, including marker-listed historical
targets. Foreign commands remain. Explicit preuninstall is documented because npm
versions can skip the lifecycle callback. No trust store is edited.

## Runtime boundary
[source: hooks-c44cdcbf.md#wrapper]
[source: hooks-c44cdcbf.md#hook-edits]
[source: hooks-c44cdcbf.md#transcript-events]
[source: hooks-c44cdcbf.md#shell-read-paths]
[source: hooks-c44cdcbf.md#-codex-literal-calls]

The fixed wrapper carries base64 JSON argv, uses the same interpreter for the
validator and preserves stdout/JSON deny while normalizing child exit status.
Two PreToolUse handlers mean two wrappers plus two validators per native patch.
The wrapper cannot repair an absent interpreter. Command definitions require
human trust and local orchestration; native execution is a separate acceptance gate.

`hook_edits` accepts complete native apply_patch syntax, keeps all Add/Update/Delete
paths and both Move paths, and rejects unknown/incomplete carriers as a whole.
The existing verdict/constraints rules then inspect each edit. Recall shares a
15-line output budget; it never issues permissionDecision or allow.

`transcript_events` preserves Claude records and normalizes recognized Codex
assistant output_text and tool calls. User/tool/reasoning content cannot declare
a router. Historical host cwd/workdir resolve literal Get-Content/cat read hints.
Only the bounded literal exec wrapper grammar is recognized; no JavaScript or shell
input is executed. Unknown carriers stay fail-open and retain written duties.

## Diagnosis and preservation
[source: hooks-c44cdcbf.md#-codex-hook-config]
[source: hooks-c44cdcbf.md#-orient-hook-commands]
[source: hooks-c44cdcbf.md#-orient-entry-live]

Orientation inspects Codex user hooks.json/config.toml and project sources, labels
the client explicitly and resolves the known wrapper. A configured/resolvable
validator is not a trusted hook. Policy, malformed sources and execution environment
can prevent dispatch despite a valid definition. Observable disabling is applied across Codex sources; disabled handlers/groups are excluded. Malformed sources are unverified. Duplicate messages count configured definitions, never delivered copies.

Before changing this area read F-091 P1–P6 in ANALYSIS_codex_hooks and F-085 P1–P10 in
ANALYSIS_working_model: single path resolver, attributed cleanup, per-hook markers,
Claude semantics, read-only/context-only recall, no allow, bounded parsing and
identical shared Python copies remain binding.

## Preservation constraints

Unreleased F-091 constraints; the authoritative table remains in the ANALYSIS.

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `scripts/lib.js::CLIENTS`, `scripts/lib.js::skillTarget` | postinstall, init, preuninstall, test_clients | Un solo resolver dei percorsi; nessuna anticipazione della migrazione F-082. | E1; text_references.txt  [source: solutions/ANALYSIS_codex_hooks.md#P1] |
| P2 | `scripts/lib.js::wireGlobalOrientHook`, `scripts/lib.js::wireOrientHook`, `scripts/lib.js::removeGlobalOrientHooks` | postinstall/test_clients; init/test_clients; preuninstall/test_clients rispettivamente | Opt-out per target, preservazione delle configurazioni altrui, firme pubbliche retrocompatibili. | E1; text_references.txt  [source: solutions/ANALYSIS_codex_hooks.md#P2] |
| P3 | `scripts/lib.js::wireGlobalRemindHook`, `scripts/lib.js::wireGlobalVerdictHook`, `scripts/lib.js::wireGlobalRecallHook`, `scripts/lib.js::removeGlobalCommandHooks` | postinstall/test_clients; preuninstall/test_clients per remove | Marker distinti; nessun raddoppio o ampliamento del permesso; uninstall attribuito per root. | Test clients esistenti; text_references.txt  [source: solutions/ANALYSIS_codex_hooks.md#P3] |
| P4 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::transcript_facts`, `skills/agentic-sdlc-skill/scripts/sdlc_core.py::transcript_work` | verdict_reason; constraints_hook_context; relativi test diretti | Claude conserva il proprio comportamento; user/tool output non diventano dichiarazioni assistant. | E2, E5; text_references.txt  [source: solutions/ANALYSIS_codex_hooks.md#P4] |
| P5 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::_orient_hook_commands`, `skills/agentic-sdlc-skill/scripts/sdlc_core.py::orient_wiring`, `skills/agentic-sdlc-skill/scripts/sdlc_core.py::orient_hook_state` | orient_wiring/orient_hook_state; cmd_orient/print_orient_hook_note; test_session_start/test_skill_invariants | La diagnosi distingue client, assenza, morto e non verificabilità; nessuna attestazione di trust. | E3; text_references.txt  [source: solutions/ANALYSIS_codex_hooks.md#P5] |
| P6 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py` e copie esplicitate nella mappa | entry point software, KB, marketing e Course | Copie condivise identiche; entry point+core+knowledge sufficienti senza nuovi file runtime obbligatori. | Contratti delle entry point; futura prova hash sulle quattro copie  [source: solutions/ANALYSIS_codex_hooks.md#P6] |
