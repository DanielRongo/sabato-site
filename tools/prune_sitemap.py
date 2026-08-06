#!/usr/bin/env python3
"""Remove URLs from sitemap.xml that must never be indexed.

A page carrying `noindex` while also sitting in the sitemap sends Google two
contradictory instructions: "here is a page worth indexing" and "do not index
it". The sitemap entry is the one to drop.

Currently that means the thank-you pages. They are post-conversion confirmation
screens; indexed, they can be entered directly from search, which fires a GA4
conversion for a visitor who never converted.

    python3 tools/prune_sitemap.py            # rewrite sitemap.xml
    python3 tools/prune_sitemap.py --check    # report only

publish.py's update_sitemap() only appends blog URLs, so it will not put these
back. If that ever changes, add the exclusions there too.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, "site", "sitemap.xml")

EXCLUDE = [
    "/thank-you-page",
    "/it/grazie",
    "/roi-calculator",   # unlisted by design; noindex, nothing links to it
    "/customers/",       # noindex until the customers approve public marketing use
    "/it/clienti/",
]


def main():
    check_only = "--check" in sys.argv
    src = open(SITEMAP, encoding="utf-8").read()
    entries = re.findall(r"<url>.*?</url>", src, re.S)
    if not entries:
        sys.exit("no <url> entries found - unexpected sitemap format")

    keep, dropped = [], []
    for e in entries:
        loc = re.search(r"<loc>(.*?)</loc>", e, re.S)
        path = re.sub(r"^https?://[^/]+", "", loc.group(1)).strip() if loc else ""
        if any(path == x or path.startswith(x) for x in EXCLUDE):
            dropped.append(path)
        else:
            keep.append(e)

    print(f"{len(entries)} URLs in sitemap")
    for d in dropped:
        print(f"   drop  {d}")
    if not dropped:
        print("   nothing to drop - sitemap already clean")
        return 0
    print(f"   keeping {len(keep)}")

    if check_only:
        return 0

    out = src
    for e in entries:
        if e not in keep:
            out = out.replace(e, "", 1)
    out = re.sub(r"\n\s*\n+", "\n", out)
    open(SITEMAP, "w", encoding="utf-8").write(out)
    print(f"wrote {SITEMAP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
