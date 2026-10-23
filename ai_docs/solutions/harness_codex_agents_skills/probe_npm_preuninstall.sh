#!/usr/bin/env bash
# F-075 probe E9: does `npm uninstall -g` run a package's `preuninstall` script?
# A throwaway package is packed (`npm pack`, as the registry serves it), installed into
# a temp prefix, then uninstalled; nothing global is touched. Each step is asserted, so
# a failed install cannot masquerade as "not run".
# Control: `npm run preuninstall` must create the marker (the script itself works).
set -u
S=$(mktemp -d); mkdir -p "$S/pkg" "$S/prefix"
# The marker path reaches the script through the environment (npm passes it on), in
# the native form node expects (Git Bash paths are not valid for Windows node).
export F075_MARK="$S/ran"
NATIVE_S="$S"
if command -v cygpath >/dev/null; then F075_MARK=$(cygpath -w "$S/ran"); NATIVE_S=$(cygpath -w "$S"); fi
cat > "$S/pkg/package.json" <<'JSON'
{"name":"f075-preun-probe","version":"1.0.0","scripts":{"preuninstall":"node -e \"require('fs').writeFileSync(process.env.F075_MARK,'x')\""}}
JSON
echo "npm $(npm --version)"
fail() { echo "INVALID: $1"; rm -rf "$S"; exit 2; }
TGZ=$(cd "$S/pkg" && npm pack --silent 2>/dev/null | tail -1)
[ -f "$S/pkg/$TGZ" ] || fail "npm pack produced no tarball"
npm i -g --prefix "$NATIVE_S/prefix" --no-audit --no-fund "$NATIVE_S/pkg/$TGZ" >/dev/null 2>&1 || fail "install failed"
present() { find "$S/prefix" -maxdepth 3 -name f075-preun-probe | head -1; }
[ -n "$(present)" ] || fail "package not present in the prefix after install"
npm uninstall -g --prefix "$NATIVE_S/prefix" f075-preun-probe >/dev/null 2>&1 || fail "uninstall failed"
[ -z "$(present)" ] || fail "package still present after uninstall"
if [ -f "$S/ran" ]; then echo "uninstall: PREUNINSTALL RAN"; else echo "uninstall: PREUNINSTALL NOT RUN"; fi
(cd "$S/pkg" && npm run preuninstall >/dev/null 2>&1)
if [ -f "$S/ran" ]; then echo "control: script runs when invoked directly"; else echo "control: FAILED (probe invalid)"; fi
rm -rf "$S"
