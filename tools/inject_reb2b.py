#!/usr/bin/env python3
"""Put the RB2B visitor-identification tag on every page, exactly once.

Run after every build, right after inject_ga.py:

    python3 tools/inject_reb2b.py

Same shape as inject_ga.py, and for the same reasons:

  * Fenced by a marker comment, so a re-run replaces rather than stacks. Two
    copies of this snippet is not merely untidy - the loader guards on
    `window.reb2b`, so a second copy is dead weight on every page load forever.
  * TEMPLATES ARE PATCHED TOO. Without that, the next playbooks.py /
    publish.py / industries.py run silently strips the tag off every page it
    regenerates, and nobody notices until the dashboard is empty.
  * Self-verifies at the end and exits non-zero. A tag that is missing from
    nine pages is invisible until you go looking for traffic that never
    arrived.

Snippet supplied verbatim by Daniel, 12 Aug 2026. Do not "tidy" it - the
minified form is what RB2B publishes, and rewriting a third-party loader by
hand is how you end up debugging somebody else's vendor script at midnight.

WORTH KNOWING (from RB2B's own GDPR page, checked 12 Aug 2026): person-level
identification is US-only - "a US technology that fires on US soil, resolving
US data subjects" - and their database is built to exclude EU and UK residents.
On EU traffic this tag resolves nobody by design. It is still a third-party
script that runs before any consent is collected, which stacks on the same gap
GA4 already has here; the cookie-consent banner on the backlog covers both.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from consent import STORAGE_KEY, VERSION, MAX_AGE_DAYS  # noqa: E402

KEY = "5NRP9H3Q9YO1"

MARK_OPEN = "<!-- Marketing tag (Sabato) -->"
MARK_CLOSE = "<!-- /Marketing tag -->"

# The HTML markers say "Marketing tag", not the vendor's name. Nothing is being
# hidden - the loader URL is right there in the source - but there is no reason
# for view-source to advertise which identification vendor we buy from, and
# Daniel asked for the visitor-facing side to stay generic. This file, and the
# privacy policy, name them in full.
#
# DEFINED, NOT CALLED.
#
# RB2B identifies individual visitors, so it is marketing under any reading and
# cannot run before opt-in. Consent Mode is not an option here the way it is for
# GA4 - there is no cookieless mode for a vendor whose product IS the identity -
# so the loader simply does not execute until someone ticks Marketing.
#
# The vendor's own IIFE is preserved byte for byte inside the wrapper. It is
# their published minified form; rewriting a third-party loader by hand is how
# you end up debugging somebody else's script at midnight. All we do is stop
# calling it immediately and hand the trigger to consent.py, which invokes
# window.sbReb2b() on grant.
SNIPPET = (
    MARK_OPEN + "\n"
    '<script>window.sbReb2b=function(){'
    '!function(key) {if (window.reb2b) return;window.reb2b = {loaded: true};'
    'var s = document.createElement("script");s.async = true;'
    's.src = "https://ddwl4m2hdecbv.cloudfront.net/b/" + key + "/" + key + ".js.gz";'
    'document.getElementsByTagName("script")[0].parentNode.insertBefore(s, '
    'document.getElementsByTagName("script")[0]);}("' + KEY + '");};\n'
    '(function(){try{var c=JSON.parse(localStorage.getItem("' + STORAGE_KEY + '")'
    '||"null");if(c&&c.v===' + str(VERSION) + '&&c.marketing&&'
    '(Date.now()-Date.parse(c.ts))<' + str(MAX_AGE_DAYS) + '*864e5)'
    'window.sbReb2b();}catch(e){}})();</script>\n'
    + MARK_CLOSE + "\n"
)

BLOCK_RX = re.compile(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?",
                      re.DOTALL)

# LEGACY MARKERS, and why this list can only ever grow.
#
# Renaming MARK_OPEN on 12 Aug 2026 left the previous block on all 98 pages:
# the new regex could not see the old fence, so every page ended up with the
# tag twice. The self-check caught it - which is the entire reason it exists -
# but the lesson is that an idempotent injector's strip pattern is a contract
# with every copy it has ever written. Change the fence, keep the old one here
# forever, or the next rename does the same thing again.
LEGACY_RX = [
    re.compile(r"<!-- RB2B \(Sabato\) -->.*?<!-- /RB2B -->\n?", re.DOTALL),
]


def process(path):
    src = open(path, encoding="utf-8").read()
    out = BLOCK_RX.sub("", src)          # drop any previous copy, re-add fresh
    for rx in LEGACY_RX:                 # ...including copies under an old fence
        out = rx.sub("", out)
    if "</head>" not in out:
        return ("no-head", False)
    # AFTER the GA block, which inject_ga.py has already placed before </head>.
    # The loader does getElementsByTagName("script")[0] and dereferences its
    # parentNode, so it needs a script tag to exist. Its own tag satisfies that
    # even on a page with nothing else, but sitting after GA keeps the head in
    # a predictable order for anyone reading the source.
    out = out.replace("</head>", SNIPPET + "</head>", 1)
    if out != src:
        open(path, "w", encoding="utf-8").write(out)
        return ("injected", True)
    return ("injected", False)


def main():
    files = sorted(set(glob.glob("site/**/*.html", recursive=True) +
                       glob.glob("templates/*.html")))
    if not files:
        sys.exit("no HTML found - run this from the repo root")

    tally, changed = {}, 0
    for f in files:
        action, did = process(f)
        tally[action] = tally.get(action, 0) + 1
        changed += did

    for k in sorted(tally):
        print("  %s: %d" % (k, tally[k]))
    print("%d file(s) scanned, %d written, key = %s" % (len(files), changed, KEY))

    wrong = []
    for f in files:
        s = open(f, encoding="utf-8").read()
        if s.count(MARK_OPEN) != 1 or s.count(KEY) != 1:
            wrong.append((f, s.count(MARK_OPEN), s.count(KEY)))
    if wrong:
        print("\nTAG COUNT WRONG (marker, key):")
        for w in wrong:
            print("   ", w)
        sys.exit(1)
    print("every page carries the RB2B tag exactly once")


if __name__ == "__main__":
    main()
