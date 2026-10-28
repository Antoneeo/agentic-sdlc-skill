#!/usr/bin/env node
// F-070 probe: a stand-in for `npm` so publish_all.bat can run with nothing sent
// anywhere. Put this folder first on PATH (npm.cmd calls this file).
//   NPM_STUB_REGISTRY=all   every local version is "already on the registry"
//   NPM_STUB_REGISTRY=none  nothing is on the registry
//   NPM_STUB_LOG=<file>     every call is appended there, one line each
// `publish` never reaches a network: it is only logged.
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const log = process.env.NPM_STUB_LOG;
if (log) fs.appendFileSync(log, `${process.cwd()} :: ${args.join(' ')}\n`);
const onRegistry = process.env.NPM_STUB_REGISTRY === 'all';

function pkgField(field) {
  const pkg = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'package.json'), 'utf8'));
  const value = field.split('.').reduce((o, k) => (o == null ? undefined : o[k]), pkg);
  return value === undefined ? '{}' : JSON.stringify(value);
}

if (args[0] === 'pkg' && args[1] === 'get') {
  console.log(pkgField(args[2]));
} else if (args[0] === 'view') {
  if (!onRegistry) process.exit(1);
  const spec = args[1];
  const at = spec.lastIndexOf('@');
  if (args[2] === 'version' && at > 0) console.log(spec.slice(at + 1));
  else if (args[2] && args[2].startsWith('dist-tags.')) console.log(JSON.parse(pkgField('version')));
} else if (args[0] === 'publish') {
  console.log('[stub] publish logged, nothing sent');
} else {
  process.exit(1);
}
