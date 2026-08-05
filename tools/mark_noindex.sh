#!/usr/bin/env bash
# Runs on Netlify's build machine for branch deploys and PR previews only.
# Never runs for production - see the contexts in netlify.toml.
#
# A branch deploy of a marketing site is a fully public, crawlable copy of the
# whole site on a *.netlify.app domain. Left alone, Google indexes it and you
# are competing with yourself for your own terms. This appends a catch-all
# X-Robots-Tag so every response on the preview says "do not index".
#
# Deliberately NOT touching robots.txt: a Disallow line stops crawlers fetching
# the page at all, which means they never see the noindex header and the URL can
# still surface. Same reasoning already recorded for /roi-calculator in HANDOFF.
set -euo pipefail

cat >> site/_headers <<'EOF'

# --- injected by tools/mark_noindex.sh on non-production deploys ---
/*
  X-Robots-Tag: noindex, nofollow
EOF

echo "noindex header appended for context: ${CONTEXT:-unknown} (branch: ${BRANCH:-unknown})"
