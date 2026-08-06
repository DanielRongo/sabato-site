#!/usr/bin/env python3
"""Replace em and en dashes with plain hyphens across the site.

    python3 tools/dedash.py --dry     # report only
    python3 tools/dedash.py           # apply

Why: the long dash is a tell. Daniel's copy uses a plain hyphen.

Two rules, deliberately boring:

  1. A dash between two digits is a range -> "22-30", no spaces added.
  2. Every other dash becomes " - ", collapsing the spaces already around it,
     so "word—word", "word — word" and "word- —word" all land the same way.

The space-collapsing class is [ \\t] and NOT \\s. Inside the Framer bundles a
dash can sit at the end of a line inside a template literal; matching \\s would
swallow the newline and silently join two lines of copy.

Scope notes:

  - site/fuc/*.mjs and the search indexes are included. Framer pages are
    React-hydrated, so copy edited only in the HTML is thrown away on hydration
    and the page renders the old text. Bundles must be edited, then re-hashed
    with tools/rehash_edited_assets.py, which this script does NOT do for you.
  - Comments and docstrings in .py files are ours, not copy, but they are
    rewritten too. Keeping two conventions in one file invites the next edit to
    reintroduce the character.
  - site/old-pages is included: unlinked, but still served.
"""
import glob
import os
import re
import sys

# The same character arrives in four encodings. A literal-only sweep leaves the
# HTML entities in the industry templates and the \u2014 escapes in enhance.js
# rendering long dashes on pages that "passed".
ENCODED = re.compile(r"&mdash;|&ndash;|&#8212;|&#8211;|&#x201[34];|\\u201[34]", re.I)
RANGE = re.compile(r"(?<=\d)[—–](?=\d)")
OTHER = re.compile(r"[ \t]*[—–][ \t]*")
EXT = (".html", ".md", ".py", ".mjs", ".json", ".js", ".txt", ".xml")
SKIP = (".git/", "__pycache__", "tools/dedash.py",
        # Vendor code is not copy. React and Babel carry em dashes in their own
        # warning strings, and rewriting them changes the bytes the calculator
        # page pins with SRI integrity hashes - the scripts then refuse to load
        # and the app renders a blank #root. The calculator is also a delivered
        # artifact Daniel asked to keep byte-identical.
        "site/roi/", "site/roi-calculator.html")


def targets():
    for f in sorted(glob.glob("**/*", recursive=True)):
        if not os.path.isfile(f) or not f.endswith(EXT):
            continue
        if any(s in f for s in SKIP):
            continue
        yield f


def convert(text):
    text = ENCODED.sub("—", text)          # normalise, then apply the two rules
    text = RANGE.sub("-", text)
    text = OTHER.sub(" - ", text)
    # a dash sitting at the end of a line would otherwise gain a trailing space
    return text.replace(" - \n", " -\n")


def main():
    dry = "--dry" in sys.argv
    total = ranges = files = 0
    for f in targets():
        try:
            t = open(f, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        n = len(re.findall("[—–]", t)) + len(ENCODED.findall(t))
        if not n:
            continue
        r = len(RANGE.findall(t))
        out = convert(t)
        assert "—" not in out and "–" not in out and not ENCODED.search(out), f
        total += n
        ranges += r
        files += 1
        print("  %-58s %4d  (%d range%s)" % (f, n, r, "" if r == 1 else "s"))
        if not dry:
            open(f, "w", encoding="utf-8").write(out)
    print("\n%s %d dash(es) in %d file(s); %d were numeric ranges."
          % ("WOULD REPLACE" if dry else "replaced", total, files, ranges))
    if not dry:
        print("\nNext: rebuild (publish.py, industries.py, customers.py), then\n"
              "      python3 tools/rehash_edited_assets.py   # bundles changed")


if __name__ == "__main__":
    main()
