---
id: F-002
feature: Agentic SDLC vNext
status: COMPLETED
level: L3
start_date: 2026-06-13
end_date: 2026-06-13
---
# Analisi della Feature: Agentic SDLC vNext

## Obiettivo
- Evolvere la skill `agentic-sdlc` mantenendo il nome pubblico esistente.
- Integrare triage proporzionale, Vision a stato graduato, validazione meccanica e support file installabili.
- Rendere esplicita la simbiosi con devPNT senza ridurre la capacita' Standalone.

## Vision della Feature
- Documento guida: `ai_docs/vision/features/VISION_agentic_sdlc_vnext.md`.
- La feature realizza il beneficio di una skill autonoma ma capace di elevarsi quando devPNT e' presente.
- In Standalone, `ai_docs/` resta fonte di verita' locale.
- In Hybrid, devPNT governa `M-VISION`, Master Plan, Action Plan e artefatti versionati.
- Non-obiettivo: rendere devPNT obbligatorio per usare la skill.

## Impatto
- Modifica `skills/agentic-sdlc-skill/SKILL.md`.
- Aggiunge support file installati nella skill runtime: `templates.md`, `ENFORCEMENT.md`, `scripts/sdlc_check.py`.
- Aggiorna `scripts/postinstall.js` e `scripts/preuninstall.js` per coprire Gemini oltre a Claude e Codex.
- Aggiorna `scripts/init.js` e i template in `references/`.
- Aggiorna protocolli generati, README, CHANGELOG e metadata di versione.
- Migra i documenti locali minimi per rendere verificabile il nuovo validatore.

## Sicurezza e Threat Model
- Superficie filesystem: gli installer copiano file nelle directory utente delle skill. Mitigazione: solo copia ricorsiva da cartella package controllata, senza esecuzione di contenuti copiati.
- Superficie hook: `sdlc_check.py gate` puo' essere usato come hook, ma resta opzionale e limitato a percorsi protetti configurati dall'utente.
- Superficie devPNT: la skill usa devPNT come governance quando disponibile, ma non deve inventare stato o auto-accettare proposte.

## Piano d'Azione
- [x] Analizzare v1, v2 e percorso di installazione effettivo.
- [x] Integrare la skill vNext mantenendo il nome `agentic-sdlc`.
- [x] Portare support file nella directory runtime della skill.
- [x] Aggiornare installer per Claude, Codex e Gemini.
- [x] Aggiornare init, template e documentazione pacchetto.
- [x] Eseguire validazioni tecniche.

## Strategia di Test
- `node --check scripts/init.js`
- `node --check scripts/postinstall.js`
- `node --check scripts/preuninstall.js`
- `python -m py_compile skills/agentic-sdlc-skill/scripts/sdlc_check.py`
- `python skills/agentic-sdlc-skill/scripts/sdlc_check.py validate --root .`
- `npm pack --dry-run --json`

## Diario / Stato Corrente
- 2026-06-13: Analisi avviata. Decisione: integrare vNext come evoluzione di `agentic-sdlc`, non come skill parallela `agentic-sdlc-v2`.
- 2026-06-13: Implementazione completata. Check Node, Python, validatore SDLC e `npm pack --dry-run` superati; il dry-run include i support file runtime.
