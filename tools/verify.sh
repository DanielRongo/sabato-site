#!/usr/bin/env bash
# Full pre-deploy gate. RUNS IN THE CLAUDE CLOUD CONTAINER ONLY.
#
# postdeploy_check.py drives Playwright at /opt/pw-browsers/chromium, which
# exists in the Claude container and not on a Mac - and the Mac side of the
# Cowork bridge has no network, so it cannot install it either. That is why
# verification lives here and pushing lives there.
#
#   bash tools/verify.sh              # build, sweep the local copy, write receipt
#   bash tools/verify.sh <url>        # also sweep a deployed URL (staging/prod)
#
# On success it writes .deploy-receipt.json recording the exact site/ digest that
# passed. tools/ship.sh on the Mac refuses to push unless the digest still
# matches, so an unverified edit cannot slip out to Netlify.
set -euo pipefail

cd "$(dirname "$0")/.."
PORT=8909
REMOTE_URL="${1:-}"

echo "==> 1/5  rehash any edited immutable assets under site/fuc/"
# LANDMINE: rehash_edited_assets.py with no argument defaults its diff base to
# the repo's FIRST commit, so on a fresh clone it treats every asset ever touched
# as "edited" and renames hundreds of files. Its "already fresh" guard cannot
# save you either - it compares a sha256 prefix against Framer's own hash scheme,
# which never matches. So: only run it when site/fuc/ actually has uncommitted
# changes, and always diff against origin/main (what is live), never the epoch.
if [ -n "$(git status --porcelain -- site/fuc/)" ]; then
  git fetch origin --quiet 2>/dev/null || true
  BASE_REF="origin/main"
  git rev-parse --verify --quiet "$BASE_REF" >/dev/null || BASE_REF="HEAD"
  echo "    changes detected under site/fuc/ - rehashing against $BASE_REF"
  python3 tools/rehash_edited_assets.py "$BASE_REF"
else
  echo "    no uncommitted changes under site/fuc/ - skipping (correct: nothing to rehash)"
fi

echo
echo "==> 2/5  inject GA4 (must be the last thing that touches HTML)"
python3 tools/inject_ga.py

echo
echo "==> 3/5  serve the built site the way Netlify would"
python3 tools/serve_like_netlify.py "$PORT" &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
sleep 2

echo
echo "==> 4/5  Playwright sweep against http://127.0.0.1:$PORT"
if ! python3 tools/postdeploy_check.py "http://127.0.0.1:$PORT"; then
  echo
  echo "GATE FAILED - no receipt written. Nothing is safe to push." >&2
  exit 1
fi

echo
echo "==> 4a/5  cold-load footer clicks (regression, 6 Aug 2026)"
# The sweep above clicks links that enhance.js has already wired, so it cannot
# see the bug where footer links are dead on a first visit and alive after a
# reload. This test reverts the wiring first and only then clicks.
if ! python3 tools/test_footer_clicks.py "http://127.0.0.1:$PORT"; then
  echo
  echo "GATE FAILED - no receipt written. Nothing is safe to push." >&2
  exit 1
fi

if [ -n "$REMOTE_URL" ]; then
  echo
  echo "==> 4b/5  Playwright sweep against $REMOTE_URL"
  # A Cowork cloud container cannot reach the public internet from Chromium -
  # egress is proxied to package registries only, so sabato.ai, *.netlify.app
  # and everything else fail with ERR_TUNNEL_CONNECTION_FAILED. Probe first, so
  # a network wall is never mistaken for a broken website.
  if ! python3 - "$REMOTE_URL" <<'PROBE'
import sys
from playwright.sync_api import sync_playwright
url = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    pg = b.new_page()
    try:
        pg.goto(url, wait_until="domcontentloaded", timeout=20000)
    except Exception as e:
        print(str(e).splitlines()[0][:120]); b.close(); sys.exit(1)
    b.close()
PROBE
  then
    echo
    echo "CANNOT REACH $REMOTE_URL from this container." >&2
    echo "This is almost certainly the sandbox egress wall, NOT a broken site." >&2
    echo "Verify a DEPLOYED url with Claude in Chrome (runs in Daniel's own" >&2
    echo "browser) or have Daniel look. The local sweep above is the real gate." >&2
    exit 1
  fi
  if ! python3 tools/postdeploy_check.py "$REMOTE_URL"; then
    echo
    echo "DEPLOYED SITE FAILED at $REMOTE_URL" >&2
    exit 1
  fi
fi

kill $SERVER_PID 2>/dev/null || true

echo
echo "==> 5/5  write .deploy-receipt.json"
DIGEST="$(python3 tools/site_digest.py)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo unknown)"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
cat > .deploy-receipt.json <<EOF
{
  "site_digest": "$DIGEST",
  "verified_at": "$STAMP",
  "head_at_verify": "$COMMIT",
  "local_sweep": "pass",
  "remote_sweep": "${REMOTE_URL:-not-run}",
  "verified_by": "claude cowork - tools/verify.sh"
}
EOF
cat .deploy-receipt.json
echo
echo "GATE PASSED. Safe to run tools/ship.sh on the Mac."
