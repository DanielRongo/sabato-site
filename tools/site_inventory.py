#!/usr/bin/env python3
"""Generate SITE-INVENTORY.md - every page, what it claims, and every number.

    python3 tools/site_inventory.py

WHAT THIS IS FOR
Written for one job: rewriting the homepage and pricing page without
contradicting the ninety-odd pages already live. The risk in a homepage rewrite
is never the prose, it is saying something the rest of the site quietly
disagrees with - a different workflow count, a different pilot promise, a
number that no longer matches the case study it came from.

So this reads the BUILT site rather than the source data. What it reports is
what a visitor actually sees, including anything a generator changed on the way
out. Re-run it after any build and the document is current; do not hand-edit
the output, edit this file.

The prose blocks at the bottom (NOTES) are maintained here on purpose - they
are the part a generator cannot derive, and keeping them in the tool means a
regeneration does not wipe them.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "SITE-INVENTORY.md")

# Order matters: first matching prefix wins, so put the specific ones first.
SECTIONS = [
    ("Core", ["index.html", "it.html", "pricing.html", "it/prezzi.html",
              "about.html", "it/chi-siamo.html", "contact.html",
              "it/contatti.html"]),
    ("Playbooks (why someone is looking)", ["playbooks/", "it/playbook/"]),
    ("Workflows (what the agent does on a call)", ["use-cases/", "it/casi-duso/"]),
    ("Industries (who it is for)", ["industries/", "it/settori/"]),
    ("Customers", ["customers/", "it/clienti/"]),
    ("Blog", ["blog.html", "it/blog.html", "blog/", "it/blog/"]),
    ("Legal & other", ["privacy-policy.html", "terms.html", "it/privacy-e-cookie.html",
                       "it/termini-e-condizioni.html", "404.html",
                       "thank-you-page.html", "it/grazie.html", "roi-calculator.html"]),
]

STRIP = re.compile(r"<[^>]+>")


def text(s):
    return html.unescape(STRIP.sub("", s or "")).replace(" ", " ").strip()


def squash(s):
    return re.sub(r"\s+", " ", s or "").strip()


def read(fp):
    return open(fp, encoding="utf-8").read()


def url_of(rel):
    """The URL a visitor sees, Netlify-style: no .html, no /index.

    "index.html" strips to the empty string, not to "/" - which rendered the
    homepage heading as an empty pair of backticks. Any falsy result is the
    root.
    """
    u = "/" + rel[:-5]
    u = u[:-6] if u.endswith("/index") else u
    return u or "/"


def field(s, rx, group=1):
    m = re.search(rx, s, re.S | re.I)
    return squash(text(m.group(group))) if m else ""


# A paragraph that is really a stylesheet. Framer inlines its CSS inside a
# <p>-shaped node on some exports, so the "first long paragraph" fallback
# happily returned four kilobytes of `.framer-form-text-input:is(:lang(ae))`
# as the /contact page's lede. Any of these means the string is machinery,
# not prose - and prose is the only thing this document is for.
NOT_PROSE = ("{", "}", ";", "--framer", "function(", "var ", "px)", "@media",
             "http://", "https://", "()", "=>")


def is_prose(t):
    if not t or len(t) < 40 or len(t) > 400:
        return False
    if any(m in t for m in NOT_PROSE):
        return False
    # Real sentences are mostly letters and spaces. A minified bundle is not.
    letters = sum(c.isalpha() or c.isspace() for c in t)
    return letters / len(t) > 0.85


def dedupe(seq):
    seen, out = set(), []
    for x in seq:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def page_facts(fp, rel):
    s = read(fp)
    # Framer's inline <style> blocks are the source of every junk lede; drop
    # script and style wholesale before looking for paragraphs.
    prose_src = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S | re.I)
    h1s = [squash(text(m)) for m in re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)]
    uniq = dedupe(h1s)
    # The lede: our authored pages carry .sub or .ix-hero p; Framer pages do
    # not, so fall back to the first paragraph that reads like a sentence, and
    # then to the meta description, which on a Framer page is the only
    # hand-written summary that exists.
    desc = field(s, r'<meta name="description" content="([^"]*)"')
    lede = field(s, r'<p class="sub"[^>]*>(.*?)</p>')
    if not lede:
        lede = field(s, r'<section class="ix-hero">.*?<p>(.*?)</p>')
    if not lede:
        for m in re.findall(r"<p[^>]*>(.*?)</p>", prose_src, re.S):
            t = squash(text(m))
            # Framer splits one visual sentence across several nodes, so the
            # first paragraph is often a tail fragment - "/it/contatti" gave
            # "o chiarisciti le idee su integrazioni". Requiring a capital
            # start throws those away in favour of the meta description.
            if is_prose(t) and t[:1].isupper():
                lede = t
                break
    if not lede and desc:
        lede = desc + "  _(from the meta description - this page has no lede)_"
    return dict(
        url=url_of(rel),
        title=field(s, r"<title>(.*?)</title>"),
        desc=desc,
        h1=uniq[0] if uniq else "",
        h1_all=uniq,
        h1_count=len(h1s),
        lede=lede,
        # Block headlines are the argument of the page in five words - the most
        # useful thing here for anyone writing a homepage. Deduped: Framer
        # emits one copy per responsive variant, so the raw list repeats
        # "Sabato vs the alternatives" three times and reads like a site with
        # a stutter.
        h2s=dedupe([squash(text(m))
                    for m in re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)]),
        fine=[squash(text(m)) for m in re.findall(r'<p class="fine">(.*?)</p>', s, re.S)],
    )


# site/old-pages/it-old/* are superseded Italian pages kept only so their URLs
# do not 404. They are not linked from anywhere and nothing should be written
# to agree with them, so they are excluded rather than filed under "Unfiled",
# where they read as live pages that someone forgot to categorise.
SKIP_DIRS = {"fuc", "js", "css", "images", "customers-assets", "old-pages"}


def all_pages():
    out = []
    for dirpath, dirnames, filenames in os.walk(SITE):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, SITE).replace(os.sep, "/")
            out.append((rel, fp))
    return sorted(out)


def bucket(rel):
    for name, prefixes in SECTIONS:
        for p in prefixes:
            if rel == p or (p.endswith("/") and rel.startswith(p)):
                return name
    return "Unfiled"


NOTES = """
## How to use this

Written for rewriting the homepage and the pricing page. The trap in a homepage
rewrite is not the prose - it is contradicting a page that is already live.
Before shipping new copy, check it against three things below: the **workflow
count**, the **pilot promise**, and the **published numbers**.

## What the site currently promises

Every playbook and every workflow page closes on the same two commitments, and
they appear roughly 30 times across the site:

- **"Live in two weeks"** / *"Online in due settimane"*
- **"We build it, we run it, you see the numbers"** / *"Lo costruiamo noi, lo
  gestiamo noi, tu vedi i numeri"*

New homepage or pricing copy has to either keep these or change them
everywhere. They are the closest thing the site has to a guarantee.

## Known inconsistencies to resolve while rewriting

1. **The workflow count.** The homepage says nine workflows; three of them are
   marked Coming Soon elsewhere, and three more were just removed from the
   header dropdown (they remain live pages). Decide what number the homepage
   claims, then make the pricing page and the `/use-cases` hub agree.
2. **CTA drift.** "Start Free Pilot", "Start a Pilot" and "Book a Demo" all
   appear. Pick one primary and one secondary.
3. **Minutes vs calls.** Pricing is quoted in minutes; every operator thinks in
   calls. This was flagged on 3 Aug and is still open.
4. **No proof on the pricing page.** No logo, no testimonial, no number - while
   the customer story and the proof widget both exist and are approved for use.
5. **Escalation is gated to the top tier** on pricing, which reads as "the cheap
   plan cannot reach a human". That is not what the product does, and every
   playbook FAQ says the opposite.
6. **Homepage positioning is infrastructure-shaped.** "The voice layer your
   e-commerce is missing" describes what was built, not what changes for the
   buyer. There is a task in HANDOFF.md to move it to a team framing.
7. **The homepage has three different `<h1>` texts** (11 tags, but Framer emits
   one per responsive variant, so the real number is three): the hero line,
   *"We handle the AI. You handle your store."*, and the closing CTA *"Your
   store is open 24/7..."*. Google picks one and it will not be the one you
   meant. Demote two of them to `<h2>` during the rewrite. `/pricing` and
   `/it/prezzi` have the same problem.

## The strongest copy already on the site

Reuse these rather than inventing new claims - they have all been through the
research and verification gate:

- *"A missed call is a cart you never see."*
- *"You can't hire a third of a person."*
- *"The phone is eating your best people."*
- *"Localised everything but the conversation."*
- *"Capacity is sold in whole people."*
- *"You can't schedule strategic work into a queue."*
"""


def main():
    pages = all_pages()
    grouped = {}
    for rel, fp in pages:
        grouped.setdefault(bucket(rel), []).append((rel, fp))

    L = []
    L.append("# Sabato site inventory")
    L.append("")
    L.append("Generated by `tools/site_inventory.py` from the **built** site - "
             "what a visitor actually sees. Do not hand-edit; re-run the tool.")
    L.append("")
    L.append("%d pages." % len(pages))
    L.append("")
    L.append(NOTES.strip())
    L.append("")
    L.append("---")
    L.append("")

    order = [n for n, _ in SECTIONS] + ["Unfiled"]
    facts_by_url = {}
    for name in order:
        items = grouped.get(name)
        if not items:
            continue
        L.append("## %s" % name)
        L.append("")
        detail = name.startswith(("Core", "Playbooks", "Workflows", "Customers"))
        for rel, fp in items:
            f = page_facts(fp, rel)
            facts_by_url[f["url"]] = f
            if detail:
                L.append("### `%s`" % f["url"])
                L.append("")
                L.append("- **H1:** %s" % (f["h1"] or "_none_"))
                if f["lede"]:
                    L.append("- **Lede:** %s" % f["lede"])
                L.append("- **Title tag:** %s" % f["title"])
                L.append("- **Meta:** %s _(%d chars)_" % (f["desc"], len(f["desc"])))
                args = [h for h in f["h2s"]
                        if h and not h.lower().startswith(("questions operators",
                                                           "le domande", "success",
                                                           "storie"))][:4]
                if args:
                    L.append("- **Argument:** %s" % " → ".join(args))
                # Framer emits an <h1> per responsive variant, so the tag count
                # is not the number of headlines - what matters for a rewrite
                # is how many DIFFERENT things the page calls its headline.
                if len(f["h1_all"]) > 1:
                    L.append("- ⚠️ %d different `<h1>` texts (%d tags): %s"
                             % (len(f["h1_all"]), f["h1_count"],
                                " | ".join(f["h1_all"][1:])))
                elif f["h1_count"] > 1:
                    L.append("- %d `<h1>` tags, all the same text "
                             "(Framer responsive variants - harmless)"
                             % f["h1_count"])
                L.append("")
            else:
                L.append("- `%s` — %s" % (f["url"], f["h1"] or f["title"]))
        if not detail:
            L.append("")

    # Every cited figure on the site, in one place.
    L.append("---")
    L.append("")
    L.append("## Published numbers and their sources")
    L.append("")
    L.append("Every figure currently on the site that carries a citation. New "
             "copy must not restate any of these differently.")
    L.append("")
    seen = set()
    for url, f in sorted(facts_by_url.items()):
        for fine in f["fine"]:
            if fine and fine not in seen:
                seen.add(fine)
                L.append("- **`%s`** — %s" % (url, fine))
    if not seen:
        L.append("_none found_")
    L.append("")

    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s  (%d pages, %d cited figures)"
          % (os.path.relpath(OUT, ROOT), len(pages), len(seen)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
