#!/usr/bin/env bash
# The push half of the bridge. RUN THIS ON THE MAC, in your own Terminal.
#
#   ./tools/ship.sh staging "what changed"    # -> origin/staging -> preview deploy
#   ./tools/ship.sh live                      # -> fast-forward main -> production
#   ./tools/ship.sh status                    # what is verified, what is pending
#
# Claude never runs this and never holds a credential. It edits files, runs the
# Playwright gate in its cloud container, and leaves .deploy-receipt.json behind.
# This script checks that receipt still describes the site/ tree on disk. If you
# or Claude touched anything afterwards, the digest moves and the push is
# refused - that is the safety, so resist --force unless you know why.
set -euo pipefail

cd "$(dirname "$0")/.."

SITE_NAME="delicate-valkyrie-20e427"   # Netlify site; change here if it ever moves
SITE_ID="68487802-e2a9-46b4-bb09-e26aa077d9ad"
PROD_URL="https://sabato.ai"           # Netlify's primary URL is the apex, not www
STAGING_URL="https://staging--${SITE_NAME}.netlify.app"

MODE="${1:-status}"
MSG="${2:-}"
FORCE="${FORCE:-0}"

red()  { printf '\033[31m%s\033[0m\n' "$*"; }
grn()  { printf '\033[32m%s\033[0m\n' "$*"; }
ylw()  { printf '\033[33m%s\033[0m\n' "$*"; }

receipt_ok() {
  [ -f .deploy-receipt.json ] || return 1
  local recorded current
  recorded="$(python3 -c 'import json;print(json.load(open(".deploy-receipt.json"))["site_digest"])' 2>/dev/null)" || return 1
  current="$(python3 tools/site_digest.py)"
  [ "$recorded" = "$current" ]
}

require_receipt() {
  if receipt_ok; then
    grn "receipt matches site/ - this tree was verified by Claude"
    python3 -c 'import json;r=json.load(open(".deploy-receipt.json"));print("   verified at",r["verified_at"],"| remote sweep:",r["remote_sweep"])'
    return 0
  fi
  red "REFUSING: site/ does not match .deploy-receipt.json"
  if [ ! -f .deploy-receipt.json ]; then
    echo "   No receipt at all. Ask Claude to run tools/verify.sh in its container."
  else
    echo "   The site changed after Claude verified it. Re-verify before pushing."
  fi
  echo "   Override with: FORCE=1 ./tools/ship.sh $MODE \"$MSG\""
  [ "$FORCE" = "1" ] || exit 1
  ylw "FORCE=1 set - pushing unverified. On your head."
}

case "$MODE" in
  status)
    echo "branch:  $(git rev-parse --abbrev-ref HEAD)"
    echo "remote:  $(git config --get remote.origin.url)"
    echo
    echo "working tree:"
    git status --short || true
    echo
    echo "site digest: $(python3 tools/site_digest.py)"
    if receipt_ok; then grn "receipt: MATCHES - safe to ship"; else red "receipt: stale or missing - verify before shipping"; fi
    echo
    echo "staging: $STAGING_URL"
    echo "live:    $PROD_URL"
    ;;

  staging)
    [ -n "$MSG" ] || { red "need a message: ./tools/ship.sh staging \"what changed\""; exit 1; }
    require_receipt
    git fetch origin --quiet
    # Work always lands on staging first; main is only ever fast-forwarded to it.
    if [ "$(git rev-parse --abbrev-ref HEAD)" != "staging" ]; then
      echo "switching to staging (carrying your working changes)"
      git checkout staging
    fi
    git add -A
    if git diff --cached --quiet; then
      ylw "nothing to commit - pushing existing commits only"
    else
      git commit -m "$MSG"
    fi
    git push origin staging
    grn "pushed to staging."
    echo "Netlify branch deploy: $STAGING_URL"
    echo "Ask Claude to sweep that URL before you run: ./tools/ship.sh live"
    ;;

  live)
    require_receipt
    git fetch origin --quiet
    if ! git diff --quiet || ! git diff --cached --quiet; then
      red "working tree is dirty. Ship to staging first."; exit 1
    fi
    if [ "$(git rev-parse staging)" != "$(git rev-parse origin/staging)" ]; then
      red "local staging and origin/staging differ. Push staging first."; exit 1
    fi
    git checkout main
    # --ff-only means production is byte-identical to what staging deployed.
    # If this refuses, main has commits staging does not - reconcile deliberately.
    if ! git merge --ff-only staging; then
      red "main cannot fast-forward to staging. Someone committed straight to main."
      echo "   Rebase staging onto main, re-verify, then try again."
      git checkout staging
      exit 1
    fi
    git push origin main
    git checkout staging
    grn "live. Netlify is building production now."
    echo "$PROD_URL"
    ;;

  *)
    echo "usage: ./tools/ship.sh [status|staging \"msg\"|live]"; exit 1 ;;
esac
