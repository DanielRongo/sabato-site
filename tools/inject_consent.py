#!/usr/bin/env python3
"""Put the cookie consent banner on every page, exactly once.

    python3 tools/inject_consent.py

Runs in the gate after inject_ga.py and inject_reb2b.py, because it is the
thing that flips those two on. Same marker-fenced, idempotent, self-verifying
shape as both.

BEFORE </body>, NOT </head>. The banner is a fixed-position sibling that sits
after Framer's React root - never inside it. Markup inserted into that tree is
silently deleted at hydration, which is the bug that cost a day on the proof
widget. Being last in <body> also means the markup never blocks first paint.

Language is chosen by path, the same rule footer.py uses: /it and /it/* are
Italian, everything else English. Get this wrong and an Italian visitor is
asked for consent in English, which is not consent that a regulator would
recognise as informed.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from consent import consent_html  # noqa: E402

MARK_OPEN = "<!-- Consent (Sabato) -->"
MARK_CLOSE = "<!-- /Consent -->"

BLOCK_RX = re.compile(re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?",
                      re.DOTALL)

# Standalone tools with no site chrome. The ROI calculator is unlisted and
# carries noindex; it still sets no cookies of its own, and the GA tag it does
# carry is gated by the same Consent Mode default as everywhere else - but a
# banner on a bare React tool page has nothing to sit against, so it is skipped
# deliberately rather than by accident.
SKIP = {"site/roi-calculator.html"}


def lang_of(path):
    rel = path.replace(os.sep, "/")
    rel = rel[len("site/"):] if rel.startswith("site/") else rel
    return "it" if rel == "it.html" or rel.startswith("it/") else "en"


def process(path):
    src = open(path, encoding="utf-8").read()
    out = BLOCK_RX.sub("", src)
    rel = path.replace(os.sep, "/")
    if rel in SKIP:
        # Strip any copy a previous run left, then leave it alone.
        if out != src:
            open(path, "w", encoding="utf-8").write(out)
            return ("skipped", True)
        return ("skipped", False)
    if "</body>" not in out:
        return ("no-body", False)
    block = MARK_OPEN + "\n" + consent_html(lang_of(path)) + "\n" + MARK_CLOSE + "\n"
    out = out.replace("</body>", block + "</body>", 1)
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
    print("%d file(s) scanned, %d written" % (len(files), changed))

    wrong = []
    for f in files:
        s = open(f, encoding="utf-8").read()
        want = 0 if f.replace(os.sep, "/") in SKIP else 1
        if s.count(MARK_OPEN) != want or s.count('id="sb-consent"') != want:
            wrong.append((f, s.count(MARK_OPEN), want))
        # A banner in the wrong language is worse than none: it is consent the
        # visitor cannot be said to have understood.
        elif want and ('data-lang="%s"' % lang_of(f)) not in s:
            wrong.append((f, "wrong-lang", lang_of(f)))
    if wrong:
        print("\nBANNER WRONG (file, got, want):")
        for w in wrong:
            print("   ", w)
        sys.exit(1)
    print("every page carries the banner exactly once, in its own language")


if __name__ == "__main__":
    main()
