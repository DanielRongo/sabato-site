#!/usr/bin/env python3
"""THE header. One definition, both languages, every page.

    python3 header.py            # print the English header
    python3 header.py it         # Italian

Import it: `from header import header_html`.

WHY THIS EXISTS
---------------
Same story as the footer and the closing CTA: Framer's header was the last block
on the site still laid out with its own absolute geometry, and it had the same
class of bug. Measured on /it, the Italian CTA button is 201px wide against
170px in English - so between roughly 768px and 1199px the button starts at
x=602 while "Contatti" runs to x=622, overlapping it by 20px, with the language
flag rendered INSIDE the button's text. That is backlog item #18, and no amount
of nudging Framer's numbers fixes it for both languages at once.

This one is a flex row. Nothing overlaps because nothing is positioned.

WHAT CHANGED ON PURPOSE
-----------------------
The hamburger now takes over below 1024px, not below 810px. Framer kept the full
nav down to 768px, which is precisely where the Italian labels stop fitting: at
768 the shell has 644px of content width and the Italian nav alone needs 315px
plus a 132px logo plus a 201px button. It does not fit, in any arrangement, so
showing it was always going to overlap. Between 1024 and 1199 the nav stays but
tightens (24px gaps, 32px shell padding), which Italian clears with room to
spare.

The other change: our own generated pages previously had NO mobile navigation at
all - the template's rule was literally `.nav-links { display: none }` under
810px, with no menu to replace it. Every page now gets the same working menu.

GEOMETRY: read off Framer with getComputedStyle, not from a screenshot.
  desktop  wrapper max-width 1200, padding 16px 30px, sticky
           shell 1140x88, radius 24px, white, padding 16px 70px
           logo 132px, nav 16px/500 Satoshi, gap 48px
           button 170x51, lime #CCFF00, radius 100px, padding 12px 30px, 16px/700
  phone    shell 330x60, radius 24px, logo 117px, burger 21x21
"""
import html
import os
import sys

from footer import nav_data   # same enhance.js arrays the footer reads
from playbook_data import PLAYBOOKS, ORDER            # the trigger half of the menu
from playbook_data_it import PLAYBOOKS_IT, ORDER_IT
from product_data import PRODUCTS, ORDER as PR_ORDER
from product_data_it import PRODUCTS_IT, ORDER_IT as PR_ORDER_IT

ROOT = os.path.dirname(os.path.abspath(__file__))
CAL = "https://cal.com/sabatoai/intro"
LOGO = "/fuc/images/UTATYXc6NipXQRoxyaGHHfHSyA4-f2557e25.png"

# (label, href, dropdown) - dropdown is "uc", "ind" or None.
#
# PRODUCT, added 14 Aug. Daniel's call: its own top-level item rather than a
# fifth column in a dropdown he had already called overcrowded. It is a fourth
# taxonomy - Use Cases is what the agent DOES, Industries is WHO it is for,
# Playbooks is WHY you are looking, Product is WHAT YOU BUY - and a fourth axis
# does not fit inside a menu built for two.
#
# It points at the one product page that exists. When the second lands it needs
# a /product hub and a dropdown, exactly like the other two: a top-level label
# reading "Product" that opens a single deep page is honest at one page and
# misleading at three. Do not add the other four to this menu without building
# the hub first - that is how the /use-cases hub went unbuilt for months.
NAV = {
    # Daniel, 16 Aug: "we don't want more than 5 master menu items in the
    # header, otherwise it gets crowded in width", grouped the way he proposed:
    #   PRODUCT   = what you buy  -> Platform + Workflows (what it makes)
    #   USE CASES = does it fit   -> Playbooks + Industries
    # Contact leaves the nav: there is a Contact button now, and a link plus a
    # button to the same page is one of those things nobody notices until they
    # count.
    "en": [("Product", "/product/voice-agent-builder", "pr"),
           ("Use Cases", "/use-cases", "uc"),
           ("About", "/about", None), ("Pricing", "/pricing", None)],
    "it": [("Prodotto", "/it/prodotto/voice-agent-builder", "pr"),
           ("Casi d\u2019uso", "/it/casi-duso", "uc"),
           ("Chi Siamo", "/it/chi-siamo", None), ("Prezzi", "/it/prezzi", None)],
}
ALL_LABEL = {"en": {"uc": "All workflows", "ind": "All industries",
                    "pb": "All playbooks", "pr": ""},
             "it": {"uc": "Tutti i flussi", "ind": "Tutti i settori",
                    "pb": "Tutti i playbook", "pr": ""}}
# PRODUCT has no "all" link because it has no hub yet. Empty string skips the
# link rather than rendering one that points at nothing.
PB_HUB = {"en": "/playbooks", "it": "/it/playbook"}
IND_HUB = {"en": "/industries", "it": "/it/settori"}
UC_HUB = {"en": "/use-cases", "it": "/it/casi-duso"}
COL_HEAD = {"en": {"uc": "Workflows", "pb": "Playbooks",
                   "pr": "Platform", "ind": "Industries"},
            "it": {"uc": "Flussi", "pb": "Playbook",
                   "pr": "Piattaforma", "ind": "Settori"}}
PB_BASE = {"en": "/playbooks/", "it": "/it/playbook/"}

# HIDDEN FROM THE DESKTOP DROPDOWN ONLY. Daniel, 13 Aug: the menu was
# overcrowded once the playbook column arrived, so three workflows come out of
# it - but the PAGES stay, and so do their links in the footer, on the
# /use-cases hub, on every industry page and in the sitemap. This is a menu
# decision, not a deprecation.
#
# Keyed on the URL's last segment, in BOTH languages, rather than on the label:
# labels are editorial and get rewritten, slugs are the identity of the page.
# Filtering by English label would have silently left all three in the Italian
# menu, which is precisely the sort of half-applied change this repo keeps
# catching after the fact.
MENU_HIDE = {
    "cart-abandonment-recovery", "recupero-carrelli-abbandonati",
    "checkout-summary-via-text", "riepilogo-checkout-via-messaggio",
    "post-delivery-feedback", "feedback-post-consegna",
    # Daniel, 16 Aug: three industries out of the DROPDOWN as redundant - "but
    # keep them everywhere else". Same rule as the three workflows above: the
    # pages stay, and so do their links in the footer, on /industries, on every
    # cross-link and in the sitemap. This is a menu decision, not a
    # deprecation, and it is keyed on slug in both languages for the same
    # reason - labels get rewritten, slugs are the page.
    "outdoor-garden", "giardino-outdoor",
    "sports-fitness", "sport-fitness",
    "industrial-b2b", "industria-b2b",
}


def _menu_visible(items):
    return [(l, h) for l, h in items
            if h.rstrip("/").rsplit("/", 1)[-1] not in MENU_HIDE]


def product_items(lang):
    """(label, href) for every product page that exists.

    Read from product_data, exactly like playbook_items reads playbook_data, so
    a new product page appears in the menu the moment it is written. A second
    hand-kept list is a second thing to forget - that lesson is already written
    into the function below.
    """
    src, order, base = ((PRODUCTS, PR_ORDER, "/product/") if lang == "en"
                        else (PRODUCTS_IT, PR_ORDER_IT, "/it/prodotto/"))
    return [(src[s]["chip"], base + s) for s in order]


def playbook_items(lang):
    """(label, href) for every playbook that exists.

    Read from playbook_data, so a new playbook appears in the menu the moment it
    is written. The use-case half of this menu already learned that lesson: its
    items come from the enhance.js arrays rather than a second hand-kept list,
    because a second list is a second thing to forget.
    """
    src, order, base = ((PLAYBOOKS, ORDER, PB_BASE["en"]) if lang == "en"
                        else (PLAYBOOKS_IT, ORDER_IT, PB_BASE["it"]))
    return [(src[s]["nav"], base + s) for s in order]
FLAG = {
    # Rounded flat SVG, not emoji. Emoji flags are a lottery: Windows draws
    # them as the letters "GB" and "IT" in a box, and the other platforms all
    # draw a different shape. Daniel, 16 Aug: "replace with a rounded flat
    # higher quality version".
    "it": ('<svg class="sb-flag" viewBox="0 0 30 20" width="24" height="16" '
           'aria-hidden="true" focusable="false">'
           '<defs><clipPath id="fr-it"><rect width="30" height="20" rx="3.2"/></clipPath></defs>'
           '<g clip-path="url(#fr-it)">'
           '<rect width="10" height="20" fill="#009246"/>'
           '<rect x="10" width="10" height="20" fill="#f1f2f1"/>'
           '<rect x="20" width="10" height="20" fill="#ce2b37"/></g></svg>'),
    "gb": ('<svg class="sb-flag" viewBox="0 0 30 20" width="24" height="16" '
           'aria-hidden="true" focusable="false">'
           '<defs><clipPath id="fr-gb"><rect width="30" height="20" rx="3.2"/></clipPath></defs>'
           '<g clip-path="url(#fr-gb)">'
           '<rect width="30" height="20" fill="#012169"/>'
           '<path d="M0 0l30 20M30 0L0 20" stroke="#f1f2f1" stroke-width="4.4"/>'
           '<path d="M0 0l30 20M30 0L0 20" stroke="#c8102e" stroke-width="2.2"/>'
           '<path d="M15 0v20M0 10h30" stroke="#f1f2f1" stroke-width="6.6"/>'
           '<path d="M15 0v20M0 10h30" stroke="#c8102e" stroke-width="3.8"/></g></svg>'),
}


COPY = {
    # Daniel, 16 Aug: "'Start free pilot' is wording that should disappear -
    # people don't appreciate free stuff". Two buttons instead of one slab: a
    # quiet way to reach us, and the thing we want clicked.
    "en": dict(home="/", btn="Book a Call", ghost="Contact", ghost_href="/contact",
               demo="Book a Call",
               other="/it", other_flag=FLAG["it"], other_label="Italiano",
               menu="Open menu", close="Close menu", logo_alt="Sabato AI - Home"),
    "it": dict(home="/it", btn="Prenota una call", ghost="Contatti",
               ghost_href="/it/contatti", demo="Prenota una call",
               other="/", other_flag=FLAG["gb"], other_label="English",
               menu="Apri il menu", close="Chiudi il menu", logo_alt="Sabato AI - Home"),
}

# Toggling the menu is 12 lines, so it is inlined rather than adding a request.
# Safe to run inline, unlike anything in enhance.js: this header is ours and
# sits outside React's root, so there is no hydration to collide with.
MENU_SCRIPT = (
    '<script>(function(){'
    'var h=document.querySelector(".sb-header");if(!h)return;'
    'var b=h.querySelector(".sb-burger"),p=h.querySelector(".sb-panel");'
    'if(!b||!p)return;'
    'function set(o){h.classList.toggle("sb-open",o);'
    'b.setAttribute("aria-expanded",o?"true":"false");'
    'document.documentElement.style.overflow=o?"hidden":"";}'
    'b.addEventListener("click",function(e){e.preventDefault();'
    'set(!h.classList.contains("sb-open"));});'
    'p.addEventListener("click",function(e){if(e.target.closest("a"))set(false);});'
    'document.addEventListener("keydown",function(e){if(e.key==="Escape")set(false);});'
    'addEventListener("resize",function(){if(innerWidth>=1024)set(false);});'
    '})();</script>'
)


def lang_of(rel):
    return "it" if rel == "it.html" or rel.startswith("it/") else "en"


def _plain_links(lang):
    """Flat list - used by the mobile panel, where dropdowns make no sense.

    Playbooks are appended rather than nested. On a phone the whole point of this
    panel is that everything is one tap away, and a page reachable only through a
    hover menu does not exist on a phone at all.
    """
    out = "".join(f'<a href="{h}">{html.escape(l, quote=False)}</a>'
                  for l, h, _ in NAV[lang])
    out += "".join(f'<a href="{h}">{html.escape(l, quote=False)}</a>'
                   for l, h in playbook_items(lang))
    return out


def _col(lang, head, items, all_label, all_href):
    """One column of a dropdown: a heading, its links, its own hub link."""
    lis = "".join(f'<a href="{h}">{html.escape(l, quote=False)}</a>'
                  for l, h in items)
    if all_label:
        lis += (f'<a class="sb-dd-all" href="{all_href}">'
                f'{html.escape(all_label, quote=False)}</a>')
    return (f'<span class="sb-dd-col">'
            f'<span class="sb-dd-head">{html.escape(head, quote=False)}</span>'
            f'{lis}</span>')


def _desktop_nav(lang):
    """Nav with two two-column dropdowns.

    data-uc-dropdown is asserted by tools/postdeploy_check.py on four pages. It
    stays on the OUTER span - moving it into a column would keep the check
    green while quietly changing what it guards.
    """
    ucs, inds = nav_data(lang)
    H, A = COL_HEAD[lang], ALL_LABEL[lang]
    out = []
    for label, href, kind in NAV[lang]:
        esc = html.escape(label, quote=False)
        if not kind:
            out.append(f'<a href="{href}">{esc}</a>')
            continue
        if kind == "pr":
            body = (_col(lang, H["pr"], product_items(lang), A["pr"], href)
                    + _col(lang, H["uc"], _menu_visible(ucs), A["uc"], UC_HUB[lang]))
        else:
            body = (_col(lang, H["pb"], playbook_items(lang), A["pb"], PB_HUB[lang])
                    + _col(lang, H["ind"], _menu_visible(inds), A["ind"],
                           IND_HUB[lang]))
        dd = f'<span class="sb-dd sb-dd-2col" data-uc-dropdown="{kind}">{body}</span>'
        out.append(f'<span class="sb-nav-item">'
                   f'<a href="{href}" aria-haspopup="true">{esc}</a>{dd}</span>')
    return "".join(out)


def header_html(lang="en"):
    if lang not in COPY:
        raise ValueError(f"header.py: unknown language {lang!r}")
    c = COPY[lang]
    return (
      f'<header class="sb-header" data-lang="{lang}">'
        f'<div class="sb-hdr-shell">'
          f'<a class="sb-hdr-logo" href="{c["home"]}" aria-label="{c["logo_alt"]}">'
            f'<img src="{LOGO}" alt="Sabato AI" width="2080" height="278"></a>'
          f'<nav class="sb-hdr-nav" aria-label="Main">'
            + _desktop_nav(lang) +
          f'</nav>'
          f'<span class="sb-hdr-cta">'
            f'<a class="sb-hdr-flag" href="{c["other"]}" data-lang-switch '
            f'aria-label="{c["other_label"]}">{c["other_flag"]}</a>'
            f'<a class="sb-hdr-btn sb-hdr-ghost" href="{c["ghost_href"]}">'
            f'{html.escape(c["ghost"], quote=False)}</a>'
            f'<a class="sb-hdr-btn" href="{CAL}" target="_blank" rel="noopener">'
            f'{html.escape(c["btn"], quote=False)}</a>'
          f'</span>'
          f'<button class="sb-burger" type="button" aria-expanded="false" '
          f'aria-controls="sb-menu" aria-label="{c["menu"]}">'
          f'<span></span><span></span></button>'
        f'</div>'
        f'<div class="sb-panel" id="sb-menu">'
          f'<div class="sb-panel-inner">'
            + _plain_links(lang) +
            f'<a href="{CAL}" target="_blank" rel="noopener">'
            f'{html.escape(c["demo"], quote=False)}</a>'
            f'<a class="sb-hdr-flag" href="{c["other"]}" data-lang-switch>'
            f'{c["other_flag"]}</a>'
          f'</div>'
        f'</div>'
      f'</header>'
      + MENU_SCRIPT
    )


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    out = header_html(lang)
    print(out)
    print(f"\n[{lang}] {len(out)} bytes, {len(NAV[lang])} nav links", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
