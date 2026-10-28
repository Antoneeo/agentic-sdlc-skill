// Region mirror (F-070): keep a named region of one Markdown document equal to a
// subsection of a version's section in a Markdown release record.
//
// Dev-only, like the tests beside it: absent from every package.json `files`.
// Stdlib only. Line endings: inputs are read as LF; a write keeps the target's own
// endings, and comparisons ignore the difference, so a CRLF checkout and an LF
// export of the same commit agree.
//
//   extractSubsection(record, version, title) -> {status: 'found', body}
//                                              | {status: 'absent'}   (missing or empty)
//                                              | {status: 'error', reason}
//   syncRegion(doc, name, content)  -> {status: 'agrees'|'differs', text} | {status: 'error', reason}
//   writeRegion(file, name, content[, fsImpl]) -> {status: 'agrees'|'written'|'error', reason?}
//
// A region is every line between the whole-line bounds `<!-- NAME:begin -->` and
// `<!-- NAME:end -->`; empty content leaves the two bounds on consecutive lines.

const fs = require('fs');
const path = require('path');

const toLf = (text) => text.replace(/\r\n/g, '\n');

// One entry per Markdown heading outside code fences: {level, text, index}.
// A fence closes only on the character that opened it, at least as long, alone on
// its line (CommonMark): a ``` line inside a ~~~ block is content.
function headings(lines) {
  const out = [];
  let fence = null;
  lines.forEach((line, index) => {
    const f = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(line);
    if (f && !fence) { fence = f[1]; return; }
    if (f && fence && f[1][0] === fence[0] && f[1].length >= fence.length && !f[2].trim()) {
      fence = null;
      return;
    }
    const m = !fence && /^(#{1,6}) (.*?)\s*$/.exec(line);
    if (m) out.push({ level: m[1].length, text: m[2], index });
  });
  return out;
}

// The lines below heading `h`, up to the next heading of level <= maxLevel.
function bodyAfter(lines, hs, h, maxLevel) {
  const next = hs.find((o) => o.index > h.index && o.level <= maxLevel);
  return lines.slice(h.index + 1, next ? next.index : lines.length);
}

function trimBlank(lines) {
  let a = 0;
  let b = lines.length;
  while (a < b && !lines[a].trim()) a += 1;
  while (b > a && !lines[b - 1].trim()) b -= 1;
  return lines.slice(a, b);
}

function extractSubsection(record, version, title) {
  const lines = toLf(record).split('\n');
  const hs = headings(lines);
  const sections = hs.filter((h) => {
    const m = h.level === 2 && /^\[([^\]]+)\]/.exec(h.text);
    // `[Unreleased]` holds work no version has shipped yet: it answers for none.
    return m && m[1] === version && !/^unreleased\b/i.test(m[1]);
  });
  if (sections.length === 0) return { status: 'error', reason: `no section "## [${version}]"` };
  if (sections.length > 1) return { status: 'error', reason: `ambiguous: ${sections.length} sections "## [${version}]"` };
  const section = sections[0];
  const end = hs.find((o) => o.index > section.index && o.level <= 2);
  const inside = hs.filter((o) => o.index > section.index && (!end || o.index < end.index));
  const subs = inside.filter((o) => o.level === 3 && o.text === title);
  if (subs.length > 1) return { status: 'error', reason: `ambiguous: ${subs.length} "### ${title}" in [${version}]` };
  if (subs.length === 0) return { status: 'absent' };
  const body = trimBlank(bodyAfter(lines, hs, subs[0], 3));
  return body.length ? { status: 'found', body: body.join('\n') } : { status: 'absent' };
}

function bounds(name) {
  return [`<!-- ${name}:begin -->`, `<!-- ${name}:end -->`];
}

// Every line with its own terminator, so a write touches no line outside the region.
function splitKeep(text) {
  const parts = text.split(/(\r?\n)/);
  const lines = [];
  for (let i = 0; i < parts.length; i += 2) lines.push({ text: parts[i], eol: parts[i + 1] || '' });
  return lines;
}

function syncRegion(doc, name, content) {
  const lines = splitKeep(doc);
  const [open, close] = bounds(name);
  const opens = lines.flatMap((l, i) => (l.text.trim() === open ? [i] : []));
  const closes = lines.flatMap((l, i) => (l.text.trim() === close ? [i] : []));
  if (opens.length !== 1 || closes.length !== 1 || closes[0] < opens[0]) {
    return { status: 'error', reason: `region bounds for "${name}" missing, duplicated or out of order` };
  }
  const wanted = content ? toLf(content).split('\n') : [];
  const current = lines.slice(opens[0] + 1, closes[0]).map((l) => l.text);
  if (current.length === wanted.length && current.every((l, i) => l === wanted[i])) {
    return { status: 'agrees', text: doc };
  }
  // New lines take the opening bound's ending: the region keeps the file's own style.
  const eol = lines[opens[0]].eol || '\n';
  const join = (ls) => ls.map((l) => l.text + l.eol).join('');
  return {
    status: 'differs',
    text: join(lines.slice(0, opens[0] + 1)) + wanted.map((l) => l + eol).join('') + join(lines.slice(closes[0])),
  };
}

// Whole or not at all: a temporary file beside the target, renamed over it; any
// failure removes the temporary file before reporting.
function writeRegion(file, name, content, fsImpl = fs) {
  const r = syncRegion(fsImpl.readFileSync(file, 'utf8'), name, content);
  if (r.status !== 'differs') return r;
  const tmp = path.join(path.dirname(file), `.${path.basename(file)}.${process.pid}.tmp`);
  try {
    fsImpl.writeFileSync(tmp, r.text);
    fsImpl.renameSync(tmp, file);
  } catch (e) {
    try { fsImpl.unlinkSync(tmp); } catch (_) { /* never created */ }
    return { status: 'error', reason: `cannot write ${file}: ${e.code || e.message}` };
  }
  return { status: 'written' };
}

module.exports = { extractSubsection, syncRegion, writeRegion };
