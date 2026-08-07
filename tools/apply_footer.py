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
from cta import cta_html, PAGES as CTA_PAGES  # noqa: E402
from header import header_html  # noqa: E402

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
    r'\s*'                                        # see the insert comment below
    r'(?:<section class="sb-cta".*?</section>)?\s*'
    r'<footer class="sb-footer".*?</footer>'
    r'(?:\s*<script>\(function\(\)\{try\{.*?\}\)\(\);</script>)?'
    r'\s*', re.S)
THEIRS_OLD = re.compile(r'<footer class="site-footer".*?</footer>\s*', re.S)
# Our header + its inline menu script, and the templates' old hand-pasted one.
OURS_HDR = re.compile(
    r'\s*<header class="sb-header".*?</header>'
    r'(?:\s*<script>\(function\(\)\{var h=document\.querySelector.*?</script>)?'
    r'\s*', re.S)
THEIRS_HDR = re.compile(r'\s*<header class="site-header".*?</header>\s*', re.S)

# Framer's closing CTA, identified by its headline because the section's class
# hash differs on every page (framer-10d8oh2 on /it and nothing like it
# elsewhere). Marked at build time so the stylesheet has one stable hook.
CTA_HEADLINES = ("Your store is open 24/7", "Il tuo store")
LEGACY_MARK = "data-sb-legacy-cta"


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*)>")

# The component root Framer wraps this CTA in. "CTA Section" on most pages;
# /about has no <section> at all and roots it on a "Container" instead.
ROOT_NAMES = ('data-framer-name="CTA Section"', 'data-framer-name="Container"')
# Framer's header root. Stable across every page, unlike the CTA's.
FRAMER_HEADER = 'header.framer-wv5hx'


def _ancestors_at(html_text, offset):
    """[(tag_start, tag_name, attrs)] of every element open at `offset`.

    A real (small) tokenizer rather than rfind("<section"): on /about the CTA has
    no enclosing <section>, and on other pages a naive backwards search lands on
    a sibling that already closed. Getting this wrong hides the wrong half of
    the page, so it is worth the 20 lines.
    """
    stack = []
    for m in TAG.finditer(html_text):
        if m.start() >= offset:
            break
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if closing:
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][1] == name:
                    del stack[k:]
                    break
        elif name not in VOID and not attrs.rstrip().endswith("/"):
            stack.append((m.start(), name, attrs))
    return stack


CLASS_RE = re.compile(r'class="([^"]*)"')
# Eats the indentation too. Leave it behind and each run re-inserts at a
# slightly different offset, so --check reports drift forever.
STYLE_TAG = re.compile(r'[ \t]*<style data-sb-legacy-cta>.*?</style>\n?', re.S)


def legacy_cta_classes(html_text):
    """Framer's OWN class on the root of each closing-CTA variant.

    Keyed on Framer's class, not on an attribute we add. Stamping our own
    attribute was the first attempt and it failed: React re-renders these nodes
    at hydration and strips anything we put on them - three of eight pages lost
    it. Framer's own class always comes back, because React is the thing putting
    it there.
    """
    found = []
    for needle in CTA_HEADLINES:
        i = html_text.find(needle)
        while i != -1:
            for _start, _name, attrs in reversed(_ancestors_at(html_text, i)):
                if any(r in attrs for r in ROOT_NAMES):
                    m = CLASS_RE.search(attrs)
                    if m:
                        # framer-xxxxx is the generated one; the rest are shared
                        # presets that other components use too.
                        for cls in m.group(1).split():
                            if cls.startswith("framer-") and cls not in found:
                                found.append(cls)
                                break
                    break
            i = html_text.find(needle, i + len(needle))
    return found


def hide_legacy_cta_css(html_text):
    """Return the page with a <style> hiding Framer's CTA on THIS page."""
    html_text = STYLE_TAG.sub("", html_text)          # idempotent
    classes = legacy_cta_classes(html_text)
    if not classes:
        return html_text, 0
    sel = ", ".join("." + c for c in sorted(classes))
    tag = f'<style data-sb-legacy-cta>{sel}{{display:none !important}}</style>'
    if "</head>" not in html_text:
        return html_text, 0
    return html_text.replace("</head>", f"  {tag}\n</head>", 1), len(classes)


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


def apply_to(html, lang, rel):
    """Return the page with exactly one sb-footer and the stylesheet linked."""
    new_footer = footer_html(lang)
    # Only the pages Framer put a closing CTA on. Our generated pages already
    # end with their own page-specific <section class="cta-band">.
    block = (cta_html(lang) if rel in CTA_PAGES else "") + new_footer

    # Idempotency: strip any CTA+footer we previously installed before adding one.
    html = OURS.sub("", html)
    # And retire the old hand-pasted template footer if this page still has one.
    html = THEIRS_OLD.sub("", html)
    if CSS_LINK not in html:
        if "</head>" in html:
            html = html.replace("</head>", f"  {CSS_LINK}\n</head>", 1)
        else:
            return None, "no </head>"
    # AFTER the stylesheet link, always. Doing it before meant run 1 produced
    # <style><link> and run 2 produced <link><style> - byte-different output for
    # identical input, so --check flagged drift on every page forever.
    html, _ = hide_legacy_cta_css(html)

    html = OURS_HDR.sub("\n", html)
    html = THEIRS_HDR.sub("\n", html)
    m = re.search(r"<body[^>]*>", html)
    if not m:
        return None, "no <body>"
    # First thing in <body>, BEFORE Framer's React root - same reason the footer
    # goes after it. Anything inside that root gets re-rendered at hydration.
    html = html[:m.end()] + "\n" + header_html(lang) + html[m.end():]

    if "</body>" in html:
        # Leading \n matters. OURS starts with `\s*`, so stripping also eats the
        # newline before the footer; inserting without one meant run N and run
        # N+1 produced different bytes forever and --check reported drift on
        # every generated page. With it, the output is a fixed point.
        html = html.replace("</body>", f"\n{block}\n</body>", 1)
    else:
        return None, "no </body>"
    return html, None


def main():
    check = "--check" in sys.argv
    written, problems, skipped = 0, [], 0

    for full, rel in pages():
        src = open(full, encoding="utf-8").read()
        out, err = apply_to(src, lang_of(rel), rel)
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
