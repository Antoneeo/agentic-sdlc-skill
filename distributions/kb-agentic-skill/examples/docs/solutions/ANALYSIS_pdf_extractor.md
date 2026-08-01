# Analisi della Feature: PDF Text Extractor EXE

## Obiettivo
- Creare un'applicazione portabile (.exe) per Windows.
- Estrarre testo da file PDF.
- Integrazione opzionale di AI per gestire PDF scannerizzati o complessi.
- Semplicità d'uso e portabilità (singolo file eseguibile).

## Impatto
- **Nuove dipendenze:** `pdf-parse` (estrazione testo), `pkg` o `nexe` (per la creazione dell'eseguibile), `openai` o `ollama` (opzionale per l'AI).
- **Nuovi file:** `src/pdf_extractor.js`, `src/ai_helper.js`, `package.json` (per l'applicazione).
- **Integrazioni:** Eventuale API key per AI (da gestire con variabili d'ambiente).

## Piano d'Azione
1. [ ] Definizione dello stack tecnologico specifico per l'eseguibile (Node.js + pkg).
2. [ ] Implementazione della logica di estrazione testo PDF standard (pdf-parse).
3. [ ] Implementazione del layer AI opzionale (fallback per OCR/testo complesso).
4. [ ] Creazione dello script di build per generare l'eseguibile Windows (.exe).
5. [ ] Scrittura dei test automatici (Pattern AAA).

## Strategia di Test
- **Test unitari:** Mock dei file PDF per verificare l'estrazione del testo.
- **Test d'integrazione:** Verifica del flusso completo (caricamento PDF -> estrazione -> output).
- **Test di build:** Conferma che l'eseguibile venga generato correttamente.
- **Esempi attesi:** 
    - Input: `test.pdf` (testo selezionabile) -> Output: stringa di testo corretta.
    - Input: `image.pdf` (scannerizzato) -> Output: richiesta AI/OCR.
