#!/usr/bin/env python3
"""Stamp site/js/enhance.js with a content-hash query string everywhere.

enhance.js is what injects the footer Blog link, the Use Cases dropdown and the
click interceptor. It is referenced by a bare, unversioned path, so a browser
holding an old copy keeps running old behaviour indefinitely - the user sees a
site that is missing features the repo clearly contains, and nothing on our side
reproduces it. (This is the same class of bug as the immutable /fuc/ cache, but
worse: /fuc/ files are at least hash-named by Framer.)

Rewrites every `/js/enhance.js` reference (any existing ?v= is replaced) to
`/js/enhance.js?v=<sha256[:10]>` across site/**.html and templates/**.html, so
a changed file is always a changed URL. Run after editing enhance.js, before
deploying:

    python3 tools/version_enhance.py
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "site", "js", "enhance.js")
REF = re.compile(r'(?P<path>(?:\.{0,2}/)?(?:js/)?enhance\.js)(?:\?v=[A-Za-z0-9]+)?')


def main():
    if not os.path.exists(TARGET):
        print("enhance.js not found", file=sys.stderr)
        return 1
    digest = hashlib.sha256(open(TARGET, "rb").read()).hexdigest()[:10]

    touched = 0
    for base in ("site", "templates"):
        for dirpath, _, files in os.walk(os.path.join(ROOT, base)):
            for fn in files:
                if not fn.endswith(".html"):
                    continue
                fp = os.path.join(dirpath, fn)
                try:
                    t = open(fp, encoding="utf-8").read()
                except UnicodeDecodeError:
                    continue
                if "enhance.js" not in t:
                    continue
                new = REF.sub(lambda m: f'{m.group("path")}?v={digest}', t)
                if new != t:
                    open(fp, "w", encoding="utf-8").write(new)
                    touched += 1

    print(f"enhance.js -> ?v={digest}   ({touched} file(s) updated)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
