#!/usr/bin/env python3
"""Install the one footer (footer.py) on every page under site/.

    python3 tools/apply_footer.py            # write
    python3 tools/apply_footer.py --check    # report drift, change nothing

Runs LAST in build.py, after every generator, because it is the only step
allowed to own footer markup.

TWO KINDS OF PAGE, HANDLED DIFFERENTLY
--------------------------------------
Framer-exported pages carry <footer class="framer-PFscP ...">. That node is NOT
removed: Framer ships the footer in its JS bundle too, so deleting it from the
HTML makes React re-insert it AND re-render the surrounding tree on the
mismatch - the exact fault that broke every footer link on this site. It is left
untouched and hidden by site/css/footer.css. Ours is appended at the end of
<body>, OUTSIDE React's root, where hydration cannot reach it.

Our own generated pages had a hand-pasted <footer class="site-footer"> in each
of eleven templates. Those are replaced wholesale by the generated one.

Both get <link rel="stylesheet" href="/css/footer.css"> in <head>.

IDEMPOTENT. Run it twice and the second run reports 0 written - that is asserted
by the test at the bottom of build.py's gate. A patcher that is not idempotent
is how content got duplicated on every build in this repo before.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from footer import footer_html  # noqa: E402

SITE = os.path.join(ROOT, "site")
CSS_LINK = '<link rel="stylesheet" href="/css/footer.css">'

# Pages with no footer by design. old-pages/ is a parked copy of the pre-migration
# site; it is not linked from anywhere and must not be touched.
SKIP_DIRS = {"fuc", "old-pages", "js", "css"}

# The trailing \s* is load-bearing. Without it the newline this script inserts
# before </body> survives the strip, a fresh one is added, and every run grows
# the file by a byte - so --check would report drift forever and the "run it
# twice and nothing changes" guarantee would be a lie.
OURS = re.compile(
    r'<footer class="sb-footer".*?</footer>'
    r'(?:\s*<script>\(function\(\)\{try\{.*?\}\)\(\);</script>)?'
    r'\s*', re.S)
THEIRS_OLD = re.compile(r'<footer class="site-footer".*?</footer>\s*', re.S)


def lang_of(rel):
    return "it" if rel == "it.html" or rel.startswith("it/") else "en"


def pages():
    for dirpath, dirnames, filenames in os.walk(SITE):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                yield full, os.path.relpath(full, SITE).replace(os.sep, "/")


def apply_to(html, lang):
    """Return the page with exactly one sb-footer and the stylesheet linked."""
    new_footer = footer_html(lang)

    # Idempotency: strip any footer we previously installed before adding one.
    html = OURS.sub("", html)
    # And retire the old hand-pasted template footer if this page still has one.
    html = THEIRS_OLD.sub("", html)

    if CSS_LINK not in html:
        if "</head>" in html:
            html = html.replace("</head>", f"  {CSS_LINK}\n</head>", 1)
        else:
            return None, "no </head>"

    if "</body>" in html:
        html = html.replace("</body>", f"{new_footer}\n</body>", 1)
    else:
        return None, "no </body>"
    return html, None


def main():
    check = "--check" in sys.argv
    written, problems, skipped = 0, [], 0

    for full, rel in pages():
        src = open(full, encoding="utf-8").read()
        out, err = apply_to(src, lang_of(rel))
        if err:
            problems.append(f"{rel}: {err}")
            continue
        if out == src:
            skipped += 1
            continue
        if not check:
            open(full, "w", encoding="utf-8").write(out)
        written += 1

    verb = "would change" if check else "written"
    print(f"  {written} {verb}, {skipped} already current")
    for p in problems:
        print(f"     PROBLEM: {p}")

    if check and written:
        print("\nFooter drift: run python3 tools/apply_footer.py", file=sys.stderr)
        return 1
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
