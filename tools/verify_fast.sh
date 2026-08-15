#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# The fast gate. Checks ONLY the pages you name, in about two minutes instead
# of forty, so a page can be looked at while it is still being written.
#
# IT NEVER WRITES A RECEIPT, and it never will. tools/ship.sh compares a fresh
# digest of site/ against .deploy-receipt.json and refuses to push when they
# differ, so passing this proves a page is worth showing - not that it is
# shippable. Shipping still needs tools/verify.sh over everything.
#
#   bash tools/verify_fast.sh /product/agent-evaluation /it/prodotto/...
# ---------------------------------------------------------------------------
set -uo pipefail
cd "$(dirname "$0")/.."
[ $# -gt 0 ] || { echo "usage: bash tools/verify_fast.sh /path [/path ...]"; exit 2; }

PORT=8912
PAGES="$(printf "%s," "$@")"; PAGES="${PAGES%,}"
FAIL=0

echo "==> 1/5  footer is current with footer.py"
python3 tools/apply_footer.py >/dev/null 2>&1 || true
python3 tools/apply_footer.py --check >/dev/null 2>&1 || {
  echo "    footer drift - running apply_footer.py"; }

echo "==> 2/5  injectors (same order as the full gate: GA, marketing, consent)"
python3 tools/inject_ga.py      >/dev/null 2>&1 || FAIL=1
python3 tools/inject_reb2b.py   >/dev/null 2>&1 || FAIL=1
python3 tools/inject_consent.py >/dev/null 2>&1 || FAIL=1

echo "==> 3/5  serve the built site the way Netlify would"
pkill -f "serve_like_netlify.py $PORT" >/dev/null 2>&1 || true
sleep 1
python3 tools/serve_like_netlify.py "$PORT" >/tmp/verify_fast_server.log 2>&1 &
SERVER=$!
sleep 3

echo "==> 4/5  page sweep, link audit and phone render on: $PAGES"
python3 tools/postdeploy_check.py   "http://127.0.0.1:$PORT" "only:$PAGES" || FAIL=1
python3 tools/audit_links.py        "http://127.0.0.1:$PORT" "only:$PAGES" || FAIL=1
python3 tools/phone_render_audit.py "http://127.0.0.1:$PORT" "only:$PAGES" || FAIL=1

kill "$SERVER" >/dev/null 2>&1 || true

if [ "$FAIL" -ne 0 ]; then
  echo; echo "FAST CHECK FAILED - fix before asking anyone to look at it."
  exit 1
fi

echo
echo "==> 5/5  fast check passed on $# page(s)."
echo
echo "    NO RECEIPT WRITTEN, and none will be: shipping still needs the full"
echo "    sweep (tools/verify.sh). This only means the page is worth showing."
