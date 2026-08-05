#!/usr/bin/env python3
"""Deterministic fingerprint of everything that gets deployed.

Two machines have to agree on this number: the Claude cloud container that runs
the Playwright gate, and Daniel's Mac that runs the push. So it is written in
python3 (present on both) rather than shell - macOS has `shasum`, Linux has
`sha256sum`, and they are not interchangeable.

    python3 tools/site_digest.py          # print the digest of site/

The digest covers file paths AND contents under site/. Rename a file, change a
byte, add a page: the digest moves. That is the whole point - tools/ship.sh
compares it against the digest recorded in .deploy-receipt.json and refuses to
push anything Claude did not actually verify.
"""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

# Noise that Finder and Netlify sprinkle around; never part of what we ship.
IGNORE_NAMES = {".DS_Store"}
IGNORE_DIRS = {".git", "__pycache__"}


def digest(root=SITE):
    if not os.path.isdir(root):
        sys.exit(f"no site/ directory at {root} - run from the repo")
    h = hashlib.sha256()
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS)
        for fn in sorted(filenames):
            if fn in IGNORE_NAMES:
                continue
            paths.append(os.path.join(dirpath, fn))
    for p in sorted(paths):
        rel = os.path.relpath(p, root)
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        h.update(b"\0")
    return h.hexdigest(), len(paths)


if __name__ == "__main__":
    d, n = digest()
    if "-v" in sys.argv:
        print(f"{d}  ({n} files under site/)")
    else:
        print(d)
