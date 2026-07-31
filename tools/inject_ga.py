#!/usr/bin/env python3
"""Put the Google Analytics 4 tag on every page, exactly once.

Run after every build:  python3 tools/inject_ga.py

Two things this has to handle, because the site has two DOM families:

1. Framer-exported pages (/, /it, /pricing, /about, /contact, ...) already ship
   a gtag pair — an init block early in <head> and the async loader just before
   </head> — wired to Framer's placeholder property G-499419803. That ID is
   malformed for GA4 (nine digits; GA4 wants ten alphanumerics after "G-"), so
   those pages have been reporting to nothing. We rewrite the ID in place
   rather than adding a second tag, which would double-count every pageview.

2. Authored pages (use-cases, industries, blog) and the templates that build
   them have no tag at all. They get the standard snippet inserted before
   </head>, fenced by a marker comment so re-runs are no-ops.

Templates are patched too — otherwise the next publish.py / industries.py run
silently strips the tag off every page it regenerates.
"""
import glob
import re
import sys

GA_ID = "G-BSK4KH9JJF"
OLD_IDS = ["G-499419803"]

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
        sys.exit("no HTML found — run this from the repo root")

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
    print("every page carries the tag exactly once")


if __name__ == "__main__":
    main()
