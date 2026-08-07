#!/usr/bin/env python3
"""Build the four legal pages from legal/*.md.

    python3 legal.py

  legal/terms.en.md    -> site/terms.html
  legal/terms.it.md    -> site/it/termini-e-condizioni.html
  legal/privacy.en.md  -> site/privacy-policy.html
  legal/privacy.it.md  -> site/it/privacy-e-cookie.html

WHY THE ENGLISH PAGES ARE REBUILT TOO
-------------------------------------
They were Framer exports. Keeping them there while adding Italian versions would
have meant the same document living in two systems, and the Italian one drifting
the first time either changed - the exact failure this repo has hit three times.
Legal pages are pure prose with no interactivity, so they are the easiest thing
on the site to own outright.

TWO CORRECTIONS TO THE LIVE ENGLISH TEXT, approved by Daniel 7 Aug 2026:
  * the privacy policy said account data is retained "plus the period required
    by Spanish tax law". Sabato LTD is registered in England and Wales and the
    terms are governed by English law. Now reads UK tax law.
  * the registered address was printed as "1-75, Shelton Street" - the 7 was
    missing. The footer has always said 71-75.
Both were template leftovers. They are corrected in English and translated
correctly into Italian.

The cookie policy also gained a section covering THIS WEBSITE and GA4. It
previously described only the Shopify app and dashboard, while the marketing
site has been setting a _ga cookie all along. The policy now says so plainly.
Blocking that cookie until consent is the separate banner task.

NOT LEGAL ADVICE. This is a translation and a factual correction of documents
Daniel already had, not new drafting. An Italian-facing business should have the
result read by a lawyer.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "legal")
SITE = os.path.join(ROOT, "site")
TPL = os.path.join(ROOT, "templates", "legal.html")

# source -> (output path, url path, sibling url in the other language)
PAGES = [
    ("terms.en.md",   "terms.html",                        "/terms",                    "en"),
    ("terms.it.md",   "it/termini-e-condizioni.html",      "/it/termini-e-condizioni",  "it"),
    ("privacy.en.md", "privacy-policy.html",               "/privacy-policy",           "en"),
    ("privacy.it.md", "it/privacy-e-cookie.html",          "/it/privacy-e-cookie",      "it"),
]
PAIRS = {
    "/terms": "/it/termini-e-condizioni",
    "/it/termini-e-condizioni": "/terms",
    "/privacy-policy": "/it/privacy-e-cookie",
    "/it/privacy-e-cookie": "/privacy-policy",
}


def front_matter(text):
    """`key: value` lines above the first blank line."""
    head, _, body = text.partition("\n\n")
    fm = {}
    for line in head.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body.strip()


def inline(s):
    """**bold**, [text](url) and bare emails. Everything else is escaped.

    Escaping happens FIRST, so HTML entities written in the source come out
    literal - "&nbsp;" renders as the five characters "&nbsp;". Use the real
    character instead. The privacy pages shipped a visible "&nbsp;·&nbsp;" in
    their date line before this was noticed.
    """
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\">])\b([\w.+-]+@[\w.-]+\.\w+)\b",
               r'<a href="mailto:\1">\1</a>', s)
    return s


def to_html(body):
    """A deliberately small markdown subset: ##, ###, -, and paragraphs."""
    out, buf = [], []

    def flush():
        if buf:
            out.append("    <p>" + inline(" ".join(buf)) + "</p>")
            buf.clear()

    lines = body.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln:
            flush()
        elif ln.startswith("### "):
            flush(); out.append("    <h3>" + inline(ln[4:]) + "</h3>")
        elif ln.startswith("## "):
            flush(); out.append("    <h2>" + inline(ln[3:]) + "</h2>")
        elif ln.startswith("- "):
            flush()
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append("      <li>" + inline(lines[i][2:].strip()) + "</li>")
                i += 1
            out.append("    <ul>\n" + "\n".join(items) + "\n    </ul>")
            continue
        else:
            buf.append(ln)
        i += 1
    flush()
    return "\n".join(out)


def mark_switcher(note_html, lang):
    """Tag the note's cross-language link as a deliberate switcher.

    Each legal page ends with a line pointing at its sibling in the other
    language. That is the same kind of link as the footer's language switcher,
    so it carries the same marker - otherwise tools/audit_links.py counts it as
    a language leak, which is precisely what it is not. It flagged all eight of
    them the first time these pages were built, which is the audit working.
    """
    def add(m):
        href = m.group(1)
        other = "it" if lang == "en" else "en"
        target = "it" if href.startswith("/it/") or href == "/it" else "en"
        return (f'<a href="{href}" data-lang-switch>' if target == other
                else f'<a href="{href}">')
    return re.sub(r'<a href="([^"]+)">', add, note_html)


def build():
    tpl = open(TPL, encoding="utf-8").read()
    written = 0
    for src, out_rel, url, lang in PAGES:
        path = os.path.join(SRC, src)
        if not os.path.exists(path):
            sys.exit(f"legal.py: missing {path}")
        fm, body = front_matter(open(path, encoding="utf-8").read())
        alt = PAIRS[url]
        page = (tpl
                .replace("{{LANG}}", lang)
                .replace("{{SEO_TITLE}}", html.escape(fm["seo_title"], quote=False))
                .replace("{{DESCRIPTION}}", html.escape(fm["description"], quote=False))
                .replace("{{PATH}}", url)
                .replace("{{ALT_EN}}", url if lang == "en" else alt)
                .replace("{{ALT_IT}}", url if lang == "it" else alt)
                .replace("{{OG_LOCALE}}", "it_IT" if lang == "it" else "en_US")
                .replace("{{EYEBROW}}", html.escape(fm["eyebrow"], quote=False))
                .replace("{{H1}}", html.escape(fm["h1"], quote=False))
                .replace("{{DATES}}", inline(fm["dates"]))
                .replace("{{NOTE}}", mark_switcher(inline(fm["note"]), lang))
                .replace("{{BODY}}", to_html(body)))
        dest = os.path.join(SITE, out_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(page)
        print(f"  {lang}  {url:28} <- legal/{src}  ({len(page):,} bytes)")
        written += 1
    return written


def main():
    n = build()
    print(f"\n{n} legal page(s) built")
    return 0


if __name__ == "__main__":
    sys.exit(main())
