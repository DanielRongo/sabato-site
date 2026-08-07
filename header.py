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

ROOT = os.path.dirname(os.path.abspath(__file__))
CAL = "https://cal.com/sabatoai/intro"
LOGO = "/fuc/images/UTATYXc6NipXQRoxyaGHHfHSyA4-f2557e25.png"

# (label, href, dropdown) - dropdown is "uc", "ind" or None.
NAV = {
    "en": [("Use Cases", "/use-cases", "uc"), ("Industries", "/industries", "ind"),
           ("Pricing", "/pricing", None), ("About", "/about", None),
           ("Contact", "/contact", None)],
    "it": [("Casi d'uso", "/it/casi-duso", "uc"), ("Settori", "/it/settori", "ind"),
           ("Prezzi", "/it/prezzi", None), ("Chi Siamo", "/it/chi-siamo", None),
           ("Contatti", "/it/contatti", None)],
}
ALL_LABEL = {"en": {"uc": "All use cases", "ind": "All industries"},
             "it": {"uc": "Tutti i casi d'uso", "ind": "Tutti i settori"}}
COPY = {
    "en": dict(home="/", btn="Start Free Pilot", demo="Book a Demo",
               other="/it", other_flag="\U0001F1EE\U0001F1F9", other_label="Italiano",
               menu="Open menu", close="Close menu", logo_alt="Sabato AI - Home"),
    "it": dict(home="/it", btn="Inizia il Pilota Gratuito", demo="Prenota una Demo",
               other="/", other_flag="\U0001F1EC\U0001F1E7", other_label="English",
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
    """Flat list - used by the mobile panel, where dropdowns make no sense."""
    return "".join(f'<a href="{h}">{html.escape(l, quote=False)}</a>'
                   for l, h, _ in NAV[lang])


def _desktop_nav(lang):
    """Nav with the two dropdowns.

    data-uc-dropdown is not decoration: tools/postdeploy_check.py asserts it on
    /, /pricing, /about and /contact. enhance.js used to inject these onto
    Framer's nav; that pass is now inert, so the markup has to carry them. The
    gate caught their absence the first time this header shipped, which is
    exactly what it is for.

    Items come from the same enhance.js arrays the footer parses, so adding a
    use-case page still updates nav, footer and hub together.
    """
    ucs, inds = nav_data(lang)
    out = []
    for label, href, kind in NAV[lang]:
        esc = html.escape(label, quote=False)
        if not kind:
            out.append(f'<a href="{href}">{esc}</a>')
            continue
        items = ucs if kind == "uc" else inds
        lis = "".join(f'<a href="{h}">{html.escape(l, quote=False)}</a>'
                      for l, h in items)
        lis += (f'<a class="sb-dd-all" href="{href}">'
                f'{html.escape(ALL_LABEL[lang][kind], quote=False)}</a>')
        out.append(
            f'<span class="sb-nav-item">'
            f'<a href="{href}" aria-haspopup="true">{esc}</a>'
            f'<span class="sb-dd" data-uc-dropdown="{kind}">{lis}</span>'
            f'</span>')
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
            f'<a class="sb-hdr-flag" href="{c["other"]}" data-lang-switch '
            f'aria-label="{c["other_label"]}">{c["other_flag"]}</a>'
          f'</nav>'
          f'<a class="sb-hdr-btn" href="{CAL}" target="_blank" rel="noopener">'
          f'{html.escape(c["btn"], quote=False)}</a>'
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
