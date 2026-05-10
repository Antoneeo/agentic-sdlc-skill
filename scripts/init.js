#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const cwd = process.cwd();

// 1. Definizione dei percorsi
const directories = [
  path.join(cwd, 'docs'),
  path.join(cwd, 'docs', 'solutions')
];

const files = {
  architecture: path.join(cwd, 'docs', 'architecture.md'),
  existingFeatures: path.join(cwd, 'docs', 'existing_features.md'),
  featuresHistory: path.join(cwd, 'docs', 'features_history.md'),
  claudeConfig: path.join(cwd, 'CLAUDE.md'),
  geminiConfig: path.join(cwd, 'GEMINI.md')
};

// 2. Il contenuto del Protocollo (System Prompt)
const protocolContent = `# Protocollo Operativo "Agentic SDLC"

Sei un ingegnere del software senior che segue rigorosamente un processo "Documentation-First". Non implementare MAI codice senza aver completato i passaggi documentali precedenti. Utilizza i tool a tua disposizione (lettura file, scrittura file, esecuzione comandi) per rispettare le seguenti fasi.

## 1. Fase di Audit e Allineamento
Prima di rispondere a qualsiasi richiesta operativa:
- Controlla l'esistenza della cartella \`/docs\`.
- Se \`/docs\` non esiste o mancano i documenti fondamentali, creali analizzando il codice sorgente:
    1. \`docs/architecture.md\`: Deve contenere Stack Tecnologico, Struttura delle Directory e Pattern architetturali principali.
    2. \`docs/existing_features.md\`: Elenco puntato delle funzionalità già presenti.
    3. \`docs/features_history.md\`: Deve essere aggiornato rigorosamente con questo schema:
       | ID | Nome Feature | Stato | Data Inizio | Data Fine | Doc. Analisi | Note |

## 2. Fase di Analisi della Richiesta
Per ogni nuova feature:
- Crea \`docs/solutions/ANALYSIS_[nome_feature].md\` (Obiettivo, Impatto, Piano, Strategia Test).
- Aggiungi una riga in \`docs/features_history.md\` con stato \`[PLANNED]\`.

## 3. Fase di Sviluppo e Test
Solo dopo la Fase 2:
1. Aggiorna lo stato a \`[IN_PROGRESS]\`.
2. Implementa il codice.
3. **Obbligatorio:** Scrivi i test automatici (pattern AAA).
4. Esegui i test. Se falliscono, correggi e riesegui finché Exit Code non è 0.

## 4. Fase di Chiusura
A completamento:
- Aggiorna \`architecture.md\` e \`existing_features.md\` se necessario.
- Aggiorna \`docs/features_history.md\` impostando lo stato a \`[COMPLETED]\`.
`;

// Contenuto per l'inizializzazione della tabella
const historyBoilerplate = `# Storico Features

| ID | Nome Feature | Stato | Data Inizio | Data Fine | Doc. Analisi | Note |
|:---|:---|:---|:---|:---|:---|:---|
| 000 | Init Progetto | [COMPLETED] | - | - | - | Inizializzazione automatica |
`;

console.log('🚀 Inizializzazione del workflow Agentic SDLC...');

// 3. Creazione delle cartelle
directories.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`📁 Creata directory: ${path.relative(cwd, dir)}`);
  }
});

// 4. Scrittura dei file di base se non esistono
const writeIfNotExists = (filePath, content, description) => {
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`📄 Creato file: ${path.relative(cwd, filePath)} (${description})`);
  } else {
    console.log(`⏭️  Ignorato: ${path.relative(cwd, filePath)} esiste già.`);
  }
};

writeIfNotExists(files.architecture, '# Architettura del Progetto\n\n- Stack:\n- Pattern:\n', 'Boilerplate Architettura');
writeIfNotExists(files.existingFeatures, '# Funzionalità Esistenti\n\n- \n', 'Boilerplate Funzionalità');
writeIfNotExists(files.featuresHistory, historyBoilerplate, 'Tabella Storico');

// 5. Scrittura delle configurazioni per le CLI (Claude e Gemini)
writeIfNotExists(files.claudeConfig, protocolContent, 'Regole per Claude Code');
writeIfNotExists(files.geminiConfig, protocolContent, 'Regole per Gemini CLI');

console.log('\n✅ Setup completato con successo!');
console.log('💡 Istruzioni d\'uso:');
console.log('   - Claude Code rileverà automaticamente CLAUDE.md al prossimo avvio.');
console.log('   - Per Gemini CLI, usa il file GEMINI.md come system prompt passandolo col flag appropriato (es: --system-prompt-file GEMINI.md).');