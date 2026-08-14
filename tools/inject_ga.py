#!/usr/bin/env python3
"""Put the Google Analytics 4 tag on every page, exactly once.

Run after every build:  python3 tools/inject_ga.py

Two things this has to handle, because the site has two DOM families:

1. Framer-exported pages (/, /it, /pricing, /about, /contact, ...) already ship
   a gtag pair - an init block early in <head> and the async loader just before
   </head> - wired to Framer's placeholder property G-499419803. That ID is
   malformed for GA4 (nine digits; GA4 wants ten alphanumerics after "G-"), so
   those pages have been reporting to nothing. We rewrite the ID in place
   rather than adding a second tag, which would double-count every pageview.

2. Authored pages (use-cases, industries, blog) and the templates that build
   them have no tag at all. They get the standard snippet inserted before
   </head>, fenced by a marker comment so re-runs are no-ops.

Templates are patched too - otherwise the next publish.py / industries.py run
silently strips the tag off every page it regenerates.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from consent import STORAGE_KEY, VERSION, MAX_AGE_DAYS  # noqa: E402

GA_ID = "G-BSK4KH9JJF"
OLD_IDS = ["G-499419803"]

# ---------------------------------------------------------------------------
# Google Consent Mode v2, defaulted to DENIED.
#
# This is the half that makes the banner mean anything. Without it GA4 sets its
# _ga cookie the moment the page loads and the banner is decoration - prior
# consent is the whole requirement, and a banner shown after the fact is
# written evidence that we knew.
#
# It goes in FIRST, immediately after <head>, and it does not touch the tag
# itself. gtag() only pushes onto window.dataLayer, so defining it early and
# queueing the default means our denial is the first thing in the queue no
# matter where the loader or the config call ends up - which matters, because
# the Framer pages carry their own gtag pair roughly 200KB before </head> and
# we do not want to be surgically editing their generated bundle.
#
# Denied is not off: GA4 still sends cookieless pings, so traffic volume and
# page popularity survive a refusal. That was Daniel's call over blocking the
# script outright, on the grounds that otherwise the analytics only ever show
# the subset who accepted, with no way to size the gap.
#
# A returning visitor's stored choice is read here so their acceptance applies
# to the very first pageview rather than the second.
# ---------------------------------------------------------------------------
CM_OPEN = "<!-- Consent Mode (Sabato) -->"
CM_CLOSE = "<!-- /Consent Mode -->"
CONSENT_DEFAULT = (
    CM_OPEN + "\n"
    '<script>window.dataLayer=window.dataLayer||[];'
    'function gtag(){dataLayer.push(arguments);}'
    '(function(){var a="denied",m="denied";try{'
    'var c=JSON.parse(localStorage.getItem("' + STORAGE_KEY + '")||"null");'
    'if(c&&c.v===' + str(VERSION) + '&&(Date.now()-Date.parse(c.ts))<'
    + str(MAX_AGE_DAYS) + '*864e5){a=c.analytics?"granted":"denied";'
    'm=c.marketing?"granted":"denied";}}catch(e){}'
    'gtag("consent","default",{ad_storage:m,ad_user_data:m,'
    'ad_personalization:m,analytics_storage:a,functionality_storage:"granted",'
    'security_storage:"granted",wait_for_update:500});})();</script>\n'
    + CM_CLOSE + "\n"
)
# The leading \n? matters. The block is inserted as "\n" + CONSENT_DEFAULT, so a
# strip pattern that does not also eat that newline leaves one behind on every
# run - a blank line per file per gate, growing forever, and a 108-file diff
# every time even when nothing changed. Caught 14 Aug by reading a diff that
# should have been empty.
CM_RX = re.compile(r"\n?" + re.escape(CM_OPEN) + r".*?" + re.escape(CM_CLOSE) + r"\n?",
                   re.DOTALL)
HEAD_OPEN_RX = re.compile(r"<head\b[^>]*>", re.IGNORECASE)

MARK_OPEN = "<!-- GA4 (Sabato) -->"
MARK_CLOSE = "<!-- /GA4 -->"

SNIPPET = f"""{MARK_OPEN}
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
{MARK_CLOSE}
"""

BLOCK_RX = re.compile(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?",
                      re.DOTALL)


def process(path):
    """Return (action, changed) for one HTML file."""
    src = open(path, encoding="utf-8").read()
    out = src

    # Consent default first, always - strip and re-add so re-runs are no-ops
    # and so the block stays at the very top of <head> if anything ever
    # inserts above it.
    out = CM_RX.sub("", out)
    m = HEAD_OPEN_RX.search(out)
    if m:
        out = out[:m.end()] + "\n" + CONSENT_DEFAULT + out[m.end():]

    # Framer pages: rewrite the placeholder ID wherever it appears.
    retagged = 0
    for old in OLD_IDS:
        if old in out:
            retagged += out.count(old)
            out = out.replace(old, GA_ID)

    already_native = f"gtag/js?id={GA_ID}" in out and MARK_OPEN not in out

    if already_native:
        # A Framer page we just retagged (or one that already carried the right
        # ID). Strip any snippet we may have added on an earlier run so the tag
        # is never present twice.
        out = BLOCK_RX.sub("", out)
        action = "retagged" if retagged else "native"
    else:
        out = BLOCK_RX.sub("", out)          # drop the old copy, re-add fresh
        if "</head>" not in out:
            return ("no-head", False)
        out = out.replace("</head>", SNIPPET + "</head>", 1)
        action = "injected"

    if out != src:
        open(path, "w", encoding="utf-8").write(out)
        return (action, True)
    return (action, False)


def main():
    files = sorted(set(glob.glob("site/**/*.html", recursive=True) +
                       glob.glob("templates/*.html")))
    if not files:
        sys.exit("no HTML found - run this from the repo root")

    tally = {}
    changed = 0
    for f in files:
        action, did = process(f)
        tally[action] = tally.get(action, 0) + 1
        changed += did

    for k in sorted(tally):
        print(f"  {k}: {tally[k]}")
    print(f"{len(files)} file(s) scanned, {changed} written, tag = {GA_ID}")

    # Fail loudly rather than shipping a page that counts every visit twice.
    dupes = []
    for f in files:
        s = open(f, encoding="utf-8").read()
        if s.count(f"gtag/js?id={GA_ID}") != 1 or s.count(f"'{GA_ID}'") != 1:
            dupes.append((f, s.count(f"gtag/js?id={GA_ID}"), s.count(f"'{GA_ID}'")))
    if dupes:
        print("\nTAG COUNT WRONG (loader, config):")
        for d in dupes:
            print("   ", d)
        sys.exit(1)

    # The consent default must exist exactly once AND come before the first
    # config call. Ordering is the whole point - a denial queued after the
    # config has already run is a cookie already set.
    bad_order = []
    for f in files:
        s = open(f, encoding="utf-8").read()
        if s.count(CM_OPEN) != 1:
            bad_order.append((f, "count", s.count(CM_OPEN)))
            continue
        cfg = s.find("'%s'" % GA_ID)
        if cfg != -1 and s.find(CM_OPEN) > cfg:
            bad_order.append((f, "consent-after-config", cfg))
    if bad_order:
        print("\nCONSENT DEFAULT WRONG:")
        for d in bad_order:
            print("   ", d)
        sys.exit(1)
    print("every page carries the tag exactly once, behind a denied-by-default "
          "consent state")


if __name__ == "__main__":
    main()
