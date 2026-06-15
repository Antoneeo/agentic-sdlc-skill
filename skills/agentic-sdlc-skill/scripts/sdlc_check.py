#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validatore meccanico per la skill Agentic SDLC.

Comandi:
  check      gate unico di chiusura: validate + stale in un solo comando (exit 1 se uno dei due fallisce)
  validate   verifica la coerenza strutturale di ai_docs/ (exit 1 se errori)
  index      rigenera gli indici generati: strategic/features_history.md (dai frontmatter
             delle ANALYSIS_*.md) e ai_docs/INDEX.md (manifest dei documenti canonici)
  stale      elenca le aree modificate dopo l'ultima analisi registrata in audit_plan.md (exit 1 se presenti)
  mark       registra percorsi come ANALYZED con riferimento corrente (hash git, altrimenti timestamp UTC)
  gate       hook PreToolUse: blocca scritture su percorsi protetti senza ANALYSIS IN_PROGRESS (exit 2)

Solo libreria standard (Python >= 3.8). Compatibile Windows e POSIX.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

VALID_STATES = {"PLANNED", "IN_PROGRESS", "COMPLETED", "CANCELLED"}
VALID_LEVELS = {"L1", "L2", "L3", "SPIKE"}
VISION_FILES = ("project_vision.md", "roadmap.md", "principles.md")
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
             "dist", "build", ".idea", ".vs", "ai_docs"}
INDEX_HEADER = ("<!-- GENERATO da sdlc_check.py index - non modificare a mano. "
                "Fonte di verita': frontmatter dei file ANALYSIS_*.md -->")
MANIFEST_HEADER = ("<!-- GENERATO da sdlc_check.py index - non modificare a mano. "
                   "Fonte di verita': gli header dei documenti canonici in ai_docs/. -->")
# Directory i cui .md sono documenti canonici durevoli: vengono manifestati in INDEX.md.
# audit/ e solutions/ restano discovery-by-grep (sessione / process artifact), non manifestati.
MANIFEST_DIRS = ("vision", "reference", "architecture", "functional", "strategic")
# Stati riconosciuti: doc canonici (CURRENT/SUPERSEDED/...), vision (DRAFT/APPROVED),
# ADR (Accepted/Proposed/Rejected). Unione, per non dare falsi avvisi su convenzioni gia' in uso.
CANONICAL_STATES = {"CURRENT", "SUPERSEDED", "DRAFT", "DEPRECATED",
                    "APPROVED", "ACCEPTED", "PROPOSED", "REJECTED"}
GENERATED_DOCS = {"features_history.md", "INDEX.md"}  # generati: mai entrate del manifest
MTIME_GRACE = timedelta(seconds=2)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ----------------------------------------------------------------- utilità

def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_project_root(start=None):
    cur = Path(start or os.getcwd()).resolve()
    for p in [cur] + list(cur.parents):
        if (p / "ai_docs").is_dir():
            return p
    return cur


def read_text(path):
    # utf-8-sig: scarta un eventuale BOM iniziale (file autorati su Windows) cosi'
    # il frontmatter '---' a riga 0 resta riconoscibile; legge utf-8 normale altrimenti.
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_iso(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def norm_text(s):
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def load_frontmatter(lines):
    meta = {}
    if not lines or lines[0].strip() != "---":
        return meta
    for line in lines[1:60]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            meta[m.group(1).strip().lower()] = m.group(2).strip()
    return meta


def list_analyses(root):
    """Ritorna [(path, frontmatter, testo)] per le ANALYSIS_*.md (shadow escluse)."""
    sol = root / "ai_docs" / "solutions"
    out = []
    if not sol.is_dir():
        return out
    for p in sorted(sol.glob("ANALYSIS_*.md")):
        text = read_text(p)
        if "SHADOW" in text[:200]:
            continue
        out.append((p, load_frontmatter(text.splitlines()), text))
    return out


def iter_files(target):
    if target.is_file():
        yield target
        return
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            yield Path(dirpath) / name


# ---------------------------------------------------------------------- git

def git_available(root):
    try:
        r = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                           cwd=str(root), capture_output=True, text=True, timeout=10)
        return r.returncode == 0 and r.stdout.strip() == "true"
    except Exception:
        return False


def git_head(root):
    try:
        r = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"],
                           cwd=str(root), capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def git_has_changes(root, rel_path):
    """True se ci sono modifiche tracked/untracked sotto rel_path."""
    try:
        rel = rel_path.replace("\\", "/")
        r = subprocess.run(["git", "status", "--porcelain", "--", rel],
                           cwd=str(root), capture_output=True, text=True, timeout=30)
        return r.returncode == 0 and bool(r.stdout.strip())
    except Exception:
        return False


def git_changed_since(root, ref, rel_path):
    """File cambiati (tracked + untracked) sotto rel_path rispetto a ref. None se ref non risolvibile."""
    try:
        r = subprocess.run(["git", "diff", "--name-only", ref, "--", rel_path],
                           cwd=str(root), capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            return None
        changed = [l.strip() for l in r.stdout.splitlines() if l.strip()]
        r2 = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", rel_path],
                            cwd=str(root), capture_output=True, text=True, timeout=30)
        if r2.returncode == 0:
            changed += [l.strip() for l in r2.stdout.splitlines() if l.strip()]
        return sorted(set(changed))
    except Exception:
        return None


# -------------------------------------------------------------------- index

def build_index(root):
    rows = []
    for p, meta, _ in list_analyses(root):
        rows.append((
            meta.get("id", "?"),
            meta.get("feature", p.stem.replace("ANALYSIS_", "")),
            meta.get("livello", ""),
            meta.get("stato", "?"),
            meta.get("data_inizio", ""),
            meta.get("data_fine", ""),
            "solutions/" + p.name,
        ))
    rows.sort(key=lambda r: r[0])
    lines = [INDEX_HEADER,
             "# Storico Funzionalita' (generato)",
             "",
             "| ID | Feature | Livello | Stato | Inizio | Fine | Doc |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines) + "\n"


# riga "Status:"/"Stato:" nel corpo (con o senza ** **), prefisso che precede la descrizione
_STATUS_LINE = re.compile(r"^\**\s*(?:status|stato)\s*\**\s*:\s*\**\s*([A-Za-z][\w-]*)", re.I)
# righe puramente di metadati da saltare quando si sceglie la descrizione di fallback
_META_LINE = re.compile(r"^\**\s*(date|data|task ref|version|versione|owner|autore|branch|agente|created|creato|updated|aggiornato)\b", re.I)


def extract_doc_meta(path):
    """(title, description, status, supersedes) di un doc canonico.

    Riconosce DUE convenzioni di header: il frontmatter YAML-lite
    (description/status/supersedes/title) e la riga in corpo `**Status:** X`
    (usata da ADR e doc legacy). In fallback deduce il titolo dal primo '# H1'
    e la descrizione dalla prima riga di prosa, saltando le righe di metadati.
    """
    text = read_text(path)
    lines = text.splitlines()
    meta = load_frontmatter(lines)
    body = lines
    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 60)):
            if lines[i].strip() == "---":
                body = lines[i + 1:]
                break

    title = meta.get("title", "")
    if not title:
        for line in body:
            m = re.match(r"^#\s+(.*)$", line)
            if m:
                title = m.group(1).strip()
                break
    title = title or path.stem

    status = meta.get("status", "").upper()
    if not status:
        for line in body[:25]:
            m = _STATUS_LINE.match(line.strip())
            if m:
                status = m.group(1).upper()
                break

    desc = meta.get("description", "")
    if not desc:
        for line in body:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("<!--") or _META_LINE.match(s):
                continue
            if s.startswith(">"):
                s = s.lstrip(">").strip()
            m = _STATUS_LINE.match(s)
            if m:
                # "Status: X — descrizione": tieni la parte dopo lo status; se vuota, salta
                rest = s[m.end():].strip(" *—–-:.")
                if not rest:
                    continue
                s = rest
            if s:
                desc = s
                break
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) > 160:
        desc = desc[:157].rstrip() + "..."
    return title, desc, status, meta.get("supersedes", "").strip()


def list_canonical_docs(root):
    """[(rel_to_ai_docs, path, (title, desc, status, supersedes))] per i doc canonici."""
    ai = root / "ai_docs"
    out = []
    for d in MANIFEST_DIRS:
        base = ai / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            if p.name in GENERATED_DOCS or p.name == "README.md":
                continue
            out.append((p.relative_to(ai).as_posix(), p, extract_doc_meta(p)))
    return out


def build_manifest(root):
    docs = list_canonical_docs(root)
    lines = [MANIFEST_HEADER,
             "# Indice documenti `ai_docs/` (generato)",
             "",
             "Manifest completo dei documenti canonici. Per la priorita' di lettura (must-read)",
             "vedi il `README.md` curato a mano. Lo storico delle ANALYSIS e' in",
             "`strategic/features_history.md`. `audit/` e `solutions/` sono discovery-by-grep,",
             "non manifestate qui."]
    by_dir = {}
    for rel, _, meta in docs:
        by_dir.setdefault(rel.split("/", 1)[0], []).append((rel, meta))
    for top in MANIFEST_DIRS:
        rows = by_dir.get(top)
        if not rows:
            continue
        lines += ["", f"## {top}/", "",
                  "| Documento | Stato | Descrizione |", "|---|---|---|"]
        for rel, (title, desc, status, _sup) in rows:
            d = (desc or title).replace("|", "\\|")
            lines.append(f"| `{rel}` | {status or '-'} | {d} |")
    return "\n".join(lines).rstrip() + "\n"


def cmd_index(root):
    hist = root / "ai_docs" / "strategic" / "features_history.md"
    hist.parent.mkdir(parents=True, exist_ok=True)
    hist.write_text(build_index(root), encoding="utf-8")
    print(f"[ok] indice ANALYSIS rigenerato: {hist}")
    # INDEX.md solo se esistono doc canonici: niente manifest vuoto su progetti minimali
    if list_canonical_docs(root):
        manifest = root / "ai_docs" / "INDEX.md"
        manifest.write_text(build_manifest(root), encoding="utf-8")
        print(f"[ok] manifest documenti rigenerato: {manifest}")
    else:
        print("[info] nessun documento canonico: INDEX.md non generato")
    return 0


# ----------------------------------------------------------------- validate

def cmd_validate(root):
    errors, warnings = [], []
    ai = root / "ai_docs"
    if not ai.is_dir():
        print(f"[info] {ai} non esiste: nulla da validare (progetto senza documentazione SDLC).")
        return 0

    # Vision: presenza e dichiarazione di stato
    for name in VISION_FILES:
        f = ai / "vision" / name
        if not f.is_file():
            warnings.append(f"vision/{name} mancante")
            continue
        head = "\n".join(read_text(f).splitlines()[:12])
        m = re.search(r"Stato:\s*(DRAFT|APPROVED)", head)
        if not m:
            errors.append(f"vision/{name}: manca 'Stato: DRAFT|APPROVED' nelle prime righe")
        elif m.group(1) == "DRAFT":
            warnings.append(f"vision/{name} in stato DRAFT: non e' autorita' di gating, da far validare all'utente")

    # ANALYSIS: frontmatter e sezioni obbligatorie
    seen_ids = {}
    analyses = list_analyses(root)
    for p, meta, text in analyses:
        rel = "solutions/" + p.name
        if not meta:
            errors.append(f"{rel}: frontmatter assente")
            continue
        fid = meta.get("id")
        if not fid:
            errors.append(f"{rel}: campo 'id' mancante")
        elif fid in seen_ids:
            errors.append(f"{rel}: id '{fid}' duplicato (gia' usato in {seen_ids[fid]})")
        else:
            seen_ids[fid] = rel
        stato = meta.get("stato", "")
        if stato not in VALID_STATES:
            errors.append(f"{rel}: stato '{stato}' non valido ({'/'.join(sorted(VALID_STATES))})")
        if not meta.get("data_inizio"):
            errors.append(f"{rel}: 'data_inizio' mancante")
        if stato == "COMPLETED" and not meta.get("data_fine"):
            errors.append(f"{rel}: COMPLETED senza 'data_fine'")
        livello = meta.get("livello")
        if livello and livello.upper() not in VALID_LEVELS:
            warnings.append(f"{rel}: livello '{livello}' non riconosciuto ({'/'.join(sorted(VALID_LEVELS))})")
        if "## Sicurezza" not in text:
            errors.append(f"{rel}: sezione '## Sicurezza e Threat Model' mancante (obbligatoria)")
        for sec in ("## Obiettivo", "## Vision della Feature", "## Impatto", "## Piano d'Azione", "## Strategia di Test", "## Diario"):
            if sec not in text:
                warnings.append(f"{rel}: sezione '{sec}' mancante")

    # Indice generato allineato
    hist = ai / "strategic" / "features_history.md"
    if analyses:
        if not hist.is_file():
            errors.append("strategic/features_history.md mancante: esegui 'sdlc_check.py index'")
        elif norm_text(read_text(hist)) != norm_text(build_index(root)):
            errors.append("strategic/features_history.md non allineato alle ANALYSIS: esegui 'sdlc_check.py index'")

    # Manifest dei documenti canonici allineato (Poka-Yoke: file non indicizzato = chiusura sporca)
    docs = list_canonical_docs(root)
    manifest = ai / "INDEX.md"
    if docs:
        if not manifest.is_file():
            errors.append("ai_docs/INDEX.md mancante: esegui 'sdlc_check.py index'")
        elif norm_text(read_text(manifest)) != norm_text(build_manifest(root)):
            errors.append("ai_docs/INDEX.md non allineato ai documenti canonici: esegui 'sdlc_check.py index'")

    # Lifecycle dei documenti canonici: status dichiarato + coerenza supersedes
    canon_status = {rel: meta[2] for rel, _, meta in docs}
    for rel, _, (title, desc, status, supersedes) in docs:
        if not status:
            warnings.append(f"{rel}: manca 'status:' nell'header (CURRENT/SUPERSEDED/DRAFT/DEPRECATED)")
        elif status not in CANONICAL_STATES:
            warnings.append(f"{rel}: status '{status}' non riconosciuto ({'/'.join(sorted(CANONICAL_STATES))})")
        if supersedes:
            base = os.path.basename(supersedes)
            for other, ost in canon_status.items():
                if (other == supersedes or other.endswith("/" + supersedes)
                        or os.path.basename(other) == base) and ost == "CURRENT":
                    warnings.append(f"{other}: ancora CURRENT ma superseduto da {rel} (impostare status: SUPERSEDED)")

    # Handoff: intestazione e freschezza
    hand = ai / "audit" / "handoff.md"
    if hand.is_file():
        m = re.search(r"Data:\s*(\d{4}-\d{2}-\d{2})", read_text(hand))
        if not m:
            warnings.append("audit/handoff.md senza intestazione 'Data: YYYY-MM-DD'")
        else:
            try:
                stamp = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                age = (datetime.now(timezone.utc) - stamp).days
                if age > 14:
                    warnings.append(f"audit/handoff.md ha {age} giorni: trattarlo come storico, non come stato corrente")
            except ValueError:
                warnings.append("audit/handoff.md: data non interpretabile")

    for w in warnings:
        print(f"[warn]  {w}")
    for e in errors:
        print(f"[ERROR] {e}")
    print(f"\nValidazione: {len(errors)} errori, {len(warnings)} avvisi.")
    return 1 if errors else 0


# ------------------------------------------------------------- audit_plan

def parse_audit_plan(root):
    f = root / "ai_docs" / "audit" / "audit_plan.md"
    rows, lines = [], []
    if f.is_file():
        lines = read_text(f).splitlines()
        for i, line in enumerate(lines):
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            if cells[0].lower() == "percorso" or set(cells[0]) <= set("-: "):
                continue
            rows.append({
                "line": i,
                "path": cells[0],
                "stato": cells[1].upper(),
                "ref": cells[2] if len(cells) > 2 else "",
                "note": cells[3] if len(cells) > 3 else "",
            })
    return f, lines, rows


def cmd_stale(root):
    f, _, rows = parse_audit_plan(root)
    if not rows:
        print(f"[info] nessuna riga in {f}: niente da controllare "
              "(audit non inizializzato, oppure modalita' Hybrid dove la mappatura e' delegata a devPNT).")
        return 0
    use_git = git_available(root)
    stale = []
    for row in rows:
        if row["stato"] != "ANALYZED":
            continue
        rel, ref = row["path"], row["ref"]
        target = root / rel
        if not target.exists():
            print(f"[warn]  {rel}: percorso inesistente")
            continue
        changed = []
        if use_git and re.fullmatch(r"[0-9a-fA-F]{7,40}", ref or ""):
            res = git_changed_since(root, ref, rel.replace("\\", "/"))
            if res is None:
                print(f"[warn]  {rel}: ref git '{ref}' non risolvibile, impossibile valutare")
                continue
            changed = res
        else:
            ts = parse_iso(ref)
            if ts is None:
                print(f"[warn]  {rel}: riferimento '{ref}' non interpretabile (ne' hash git ne' ISO UTC)")
                continue
            for fp in iter_files(target):
                mtime = datetime.fromtimestamp(fp.stat().st_mtime, tz=timezone.utc)
                if mtime > ts + MTIME_GRACE:
                    changed.append(str(fp.relative_to(root)).replace("\\", "/"))
        if changed:
            stale.append((rel, changed))

    if not stale:
        print("[ok] nessuna area analizzata risulta modificata dopo l'ultima analisi.")
        return 0
    print("Aree modificate dopo l'ultima analisi registrata:")
    for rel, changed in stale:
        print(f"  {rel}  ({len(changed)} file)")
        for c in changed[:10]:
            print(f"    - {c}")
        if len(changed) > 10:
            print(f"    ... e altri {len(changed) - 10}")
    print("\nDopo la ri-analisi, registra con: sdlc_check.py mark <percorso>")
    return 1


def cmd_mark(root, paths):
    f, lines, rows = parse_audit_plan(root)
    use_git_ref = git_available(root) and not any(
        git_has_changes(root, raw.replace("\\", "/").rstrip("/")) for raw in paths
    )
    ref = git_head(root) if use_git_ref else utc_now_iso()
    by_path = {r["path"].replace("\\", "/").rstrip("/"): r for r in rows}

    if not lines:
        lines = ["# Piano di Audit", "",
                 "| Percorso | Stato | Riferimento | Note |",
                 "|---|---|---|---|"]
        rows = []

    def row_text(path, note):
        return f"| {path} | ANALYZED | {ref} | {note} |"

    appended = []
    for raw in paths:
        key = raw.replace("\\", "/").rstrip("/")
        display = key + ("/" if (root / key).is_dir() else "")
        existing = by_path.get(key)
        if existing:
            lines[existing["line"]] = row_text(existing["path"], existing["note"])
            print(f"[ok] {existing['path']} -> ANALYZED ({ref})")
        else:
            appended.append(row_text(display, ""))
            print(f"[ok] {display} aggiunto come ANALYZED ({ref})")

    if appended:
        insert_at = (max(r["line"] for r in rows) + 1) if rows else len(lines)
        lines[insert_at:insert_at] = appended

    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


def cmd_check(root):
    print("===== validate =====")
    rc_v = cmd_validate(root)
    print("\n===== stale =====")
    rc_s = cmd_stale(root)
    print(f"\ncheck: {'PULITO' if not (rc_v or rc_s) else 'NON PULITO'} "
          f"(validate rc={rc_v}, stale rc={rc_s})")
    return 1 if (rc_v or rc_s) else 0


# --------------------------------------------------------------------- gate

def cmd_gate(args):
    file_path = args.file or ""
    if args.hook:
        try:
            # bytes -> utf-8-sig: il payload degli hook e' JSON UTF-8 a prescindere
            # dalla code page della console; '-sig' scarta il BOM (pipe da PowerShell)
            raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
            payload = json.loads(raw)
            file_path = (payload.get("tool_input") or {}).get("file_path") or ""
        except Exception:
            return 0  # input non interpretabile: non bloccare
    if not file_path:
        return 0
    root = Path(args.root).resolve() if args.root else find_project_root()
    try:
        rel = str(Path(file_path).resolve().relative_to(root)).replace("\\", "/")
    except ValueError:
        return 0  # fuori dal progetto: non di competenza del gate
    if rel.startswith(("ai_docs/", "tests/", "test/")):
        return 0
    protected = [p.strip().replace("\\", "/").rstrip("/")
                 for p in (args.protected or "").split(";") if p.strip()]
    if not protected:
        return 0
    if not any(rel == p or rel.startswith(p + "/") for p in protected):
        return 0
    for _, meta, _ in list_analyses(root):
        if meta.get("stato") == "IN_PROGRESS":
            return 0
    sys.stderr.write(
        f"[sdlc gate] '{rel}' e' in un percorso protetto ma nessuna ANALYSIS_*.md e' IN_PROGRESS. "
        "Crea o riattiva l'analisi (Fase 3 di agentic-sdlc) prima di modificare questo file.\n")
    return 2


# --------------------------------------------------------------------- main

def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", help="radice del progetto (default: risale fino a trovare ai_docs/)")

    ap = argparse.ArgumentParser(prog="sdlc_check.py",
                                 description="Validatore meccanico per Agentic SDLC")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", parents=[common], help="gate di chiusura: validate + stale in un solo comando")
    sub.add_parser("validate", parents=[common], help="verifica coerenza di ai_docs/")
    sub.add_parser("index", parents=[common], help="rigenera features_history.md + ai_docs/INDEX.md")
    sub.add_parser("stale", parents=[common], help="aree modificate dopo l'ultima analisi")
    mp = sub.add_parser("mark", parents=[common], help="registra percorsi come ANALYZED")
    mp.add_argument("paths", nargs="+", help="percorsi relativi alla radice del progetto")
    gp = sub.add_parser("gate", parents=[common], help="hook PreToolUse (exit 2 = blocca)")
    gp.add_argument("--hook", action="store_true", help="leggi il payload JSON dell'hook da stdin")
    gp.add_argument("--file", help="percorso file da valutare (alternativa a --hook)")
    gp.add_argument("--protected", default="", help="prefissi protetti separati da ';' (es. \"src/auth;src/crypto\")")

    args = ap.parse_args(argv)
    if args.cmd == "gate":
        return cmd_gate(args)

    root = Path(args.root).resolve() if args.root else find_project_root()
    if args.cmd == "check":
        return cmd_check(root)
    if args.cmd == "validate":
        return cmd_validate(root)
    if args.cmd == "index":
        return cmd_index(root)
    if args.cmd == "stale":
        return cmd_stale(root)
    if args.cmd == "mark":
        return cmd_mark(root, args.paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
