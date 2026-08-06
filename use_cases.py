#!/usr/bin/env python3
"""Build the use-case index pages: /use-cases and /it/casi-duso.

    python3 use_cases.py

Why this exists: the nav has two dropdowns. The industries one ends in an "all"
link pointing at /industries, a real hub. The use-cases one pointed at
"/#usecases" - an anchor on the homepage - because no hub had ever been built.
Nine use-case pages existed with no index, reachable only through footer links
and that dropdown.

SOURCE OF TRUTH, deliberately:

  * order and labels come from the USECASES arrays in site/js/enhance.js, which
    already drive the nav dropdown. Duplicating them into a new data file would
    create the second owner that has bitten this repo twice already.
  * each card's line comes from that use-case page's own <h1>. Those headlines
    are the best copy on the site ("The carts your recovery emails never bring
    back") and they already exist - there is no reason to write them twice.

So adding a use-case page and adding it to enhance.js is enough: re-run this and
its card appears. Nothing to keep in sync by hand.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
CAL = "https://cal.com/sabatoai/intro"

LANGS = {
    # USECASES_EN / USECASES_IT are the real arrays; plain USECASES is only the
    # `IT ? ... : ...` alias, so matching on it finds the ternary, not the data.
    "en": dict(array="USECASES_EN", tpl="use-case-index.html",
               out=os.path.join(SITE, "use-cases", "index.html"), pages=os.path.join(SITE, "use-cases")),
    "it": dict(array="USECASES_IT", tpl="use-case-index-it.html",
               out=os.path.join(SITE, "it", "casi-duso", "index.html"),
               pages=os.path.join(SITE, "it", "casi-duso")),
}


def dropdown_items(array_name):
    """(label, href) pairs from enhance.js, in nav order."""
    js = open(os.path.join(SITE, "js", "enhance.js"), encoding="utf-8").read()
    m = re.search(re.escape(array_name) + r"\s*=\s*\[(.*?)\];", js, re.S)
    if not m:
        sys.exit(f"could not find {array_name} in enhance.js - did the nav change?")
    # [^"]* rather than .*? - entries may carry extra fields (the Italian ones
    # have `aliases`), so requiring a closing brace after href made the lazy
    # match run on into the next entry and produce a mangled href.
    items = re.findall(r'label:\s*"([^"]*)"\s*,\s*href:\s*"([^"]*)"', m.group(1))
    if not items:
        sys.exit(f"{array_name} found but no label/href pairs parsed")
    return items


def page_headline(href):
    """The <h1> of the use-case page this card links to."""
    fp = os.path.join(SITE, href.lstrip("/") + ".html")
    if not os.path.exists(fp):
        return None, f"missing page {fp}"
    s = open(fp, encoding="utf-8").read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if not m:
        return None, f"no <h1> in {href}"
    return html.unescape(re.sub("<[^>]+>", "", m.group(1))).strip(), None


def build(lang):
    cfg = LANGS[lang]
    cards, problems = "", []
    items = dropdown_items(cfg["array"])
    for label, href in items:
        head, err = page_headline(href)
        if err:
            problems.append(err)
            continue
        cards += (f'<a class="ix-card" href="{href}">'
                  f'<h3>{html.escape(label, quote=False)}</h3>'
                  f'<p class="ix-lead">{html.escape(head, quote=False)}</p></a>')

    # Every page in the directory must appear, or the hub silently under-lists
    # and we are back to pages nobody can reach.
    on_disk = {f[:-5] for f in os.listdir(cfg["pages"])
               if f.endswith(".html") and f != "index.html"}
    linked = {h.rsplit("/", 1)[-1] for _, h in items}
    missing = on_disk - linked
    if missing:
        problems.append(f"pages not in the {cfg['array']} nav array: {sorted(missing)}")

    tpl = open(os.path.join(ROOT, "templates", cfg["tpl"]), encoding="utf-8").read()
    page = tpl.replace("{{CARDS}}", cards).replace("{{CAL}}", CAL)
    os.makedirs(os.path.dirname(cfg["out"]), exist_ok=True)
    open(cfg["out"], "w", encoding="utf-8").write(page)
    return len(items), cfg["out"], problems


def main():
    bad = 0
    for lang in LANGS:
        n, out, problems = build(lang)
        rel = os.path.relpath(out, ROOT)
        print(f"  {lang}: {n} card(s) -> {rel}")
        for p in problems:
            print(f"     PROBLEM: {p}")
            bad += 1
    if bad:
        print(f"\n{bad} problem(s)", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
