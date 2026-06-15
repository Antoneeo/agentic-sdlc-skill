# Enforcement meccanico (opzionale, consigliato per i team)

Le regole a livello di prompt dipendono dalla disciplina del modello e degradano con contesti lunghi, compaction e istruzioni concorrenti. Tre livelli di garanzia crescente:

## 1. Validazione interattiva (default, nessun setup)

L'agente esegue alla chiusura (Fase 5) un solo gate:

```
python "<dir_skill>/scripts/sdlc_check.py" check
```

(`check` = validate + stale in un comando.) Exit code ≠ 0 ⇒ la feature non si dichiara chiusa. È il livello minimo previsto dalla skill.

## 2. Check in CI (consigliato per i team)

Copia `scripts/sdlc_check.py` nel repository (es. `tools/sdlc_check.py`) e aggiungi alla pipeline:

```
python tools/sdlc_check.py validate
```

Effetto: indice non rigenerato, frontmatter invalidi, sezione sicurezza mancante o stati incoerenti **bloccano la pipeline** invece di affidarsi alla memoria dell'agente. Funziona perché i documenti viaggiano nello stesso PR del codice (regola di Fase 5).

Nota: la copia nel repo è quella autoritativa per la CI; aggiornala quando aggiorni la skill.

## 3. Hook PreToolUse (gate sulle scritture)

Blocca Edit/Write su percorsi protetti quando nessuna `ANALYSIS_*.md` è `IN_PROGRESS`. In `.claude/settings.json` del progetto:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python \"C:\\Users\\<utente>\\.claude\\skills\\agentic-sdlc\\scripts\\sdlc_check.py\" gate --hook --protected \"src/auth;src/crypto\""
          }
        ]
      }
    ]
  }
}
```

Semantica: exit code 2 + messaggio su stderr ⇒ la scrittura viene bloccata e il messaggio è mostrato all'agente, che deve creare l'ANALYSIS (Fase 3) prima di riprovare.

**Avvertenze d'uso:**
- Il gate è volutamente grossolano: applicato a tutto `src/` bloccherebbe anche i task L1/L2 legittimi previsti dal Triage. Usalo **solo su directory security-critical** (`--protected "src/auth;src/crypto"`), dove "mai senza analisi" è la policy desiderata.
- I percorsi in `--protected` sono prefissi relativi alla radice del progetto, separati da `;`.
- `ai_docs/`, `tests/` e `test/` sono sempre esclusi dal blocco.
- L'hook assume che la working directory sia la radice del progetto (comportamento standard degli hook di Claude Code).
