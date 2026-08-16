#!/usr/bin/env python3
"""THE footer. One definition, both languages, every page.

    python3 footer.py            # print the English footer, for eyeballing
    python3 footer.py it         # print the Italian one

Import it instead: `from footer import footer_html`.

WHY THIS EXISTS
---------------
Before this, the footer was defined in three incompatible places:

  1. Framer's export - a <footer class="framer-PFscP ..."> on ~20 pages, holding
     relative hrefs (./pricing, ../terms) that resolve differently depending on
     how deep the page sits, a duplicated ENGLISH copy on /it/chi-siamo, and
     roughly 184px of empty spacers. 2,160px tall on a 390px phone.
  2. Eleven of our own templates, each carrying its own hand-pasted copy that
     shipped "/#usecases" placeholders and inert <span>s for industries.
  3. enhance.js, patching 1 and 2 at runtime - turning spans into links,
     retargeting hooks, repairing hrefs, forcing Italian pages back into the
     Italian site.

Every footer bug this session came from that split. So: generate the real markup
here, with real absolute hrefs, and let 1 be hidden by CSS and 2 be filled from
this file. Nothing left for 3 to repair.

SOURCE OF TRUTH: the USECASES_* and INDUSTRIES_* arrays in site/js/enhance.js,
which already drive the nav dropdowns. Parsed, not duplicated - the same reason
use_cases.py reads them. Add a page there and it appears here.

MOBILE: the two long columns are <details open>. Open is the shipped state, so
the markup a crawler sees always contains all 18 links - collapsing happens in
the browser, below 810px, and is presentation only. Chosen over rendering fewer
links on mobile because Google indexes mobile-first: whatever the phone version
omits is omitted from the index, and those 18 links are the internal linking
that got these pages crawled in the first place.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ENHANCE = os.path.join(ROOT, "site", "js", "enhance.js")

CAL = "https://cal.com/sabatoai/intro"
LINKEDIN = "https://www.linkedin.com/company/sabato-ai"
LOGO = "/fuc/images/KY1UqOX7zKeKJdbxTotIopeeZIU-f2557e25.png"
BACKED = "/fuc/images/V9nq776DtkEODcun83ayNz0liCU-28058054.webp"
LI_ICON = "/fuc/images/3vdzRTYV1XV6UUX6QKcsDIfU-e464e3f1.svg"
# width/height on the two brand images are the assets' TRUE intrinsic pixel
# sizes (logo 2080x278, backed 1496x132), not the display size. CSS sets the
# display width and leaves height:auto.
#
# They were 132x61 and 191x16, inherited from the old template, and neither
# matched its file. Because the images are loading="lazy" and the footer is
# below the fold, the browser reserves a box from the ATTRIBUTE ratio - so the
# logo held a 61px-tall slot, then collapsed to its real ~18px the instant it
# loaded. Scrolling into the footer made the whole brand block jump. Correct
# ratios mean the reserved box is right before the image arrives: no shift.
COPY = ("&copy; 2026 Sabato LTD - 71-75 Shelton Street, London (UK) - "
        "All rights reserved.")

COPY_EN = dict(
    home="/", tagline='The #1 managed Voice AI <br>for <span class="sb-nb">E-Commerce</span>.',
    backed="Backed by", company="Company", usecases="Workflows", industries="Industries",
    links=[("Home", "/"), ("Pricing", "/pricing"), ("About", "/about"),
           ("Contact us", "/contact"), ("Blog", "/blog")],
    product="Product", playbooks="Playbooks",
    demo="Book a Call", terms="Terms and Conditions", privacy="Privacy and Cookies",
    cookies="Cookie preferences",
    other_label="Italiano", other_href="/it", logo_alt="Sabato AI - Home",
    terms_href="/terms", privacy_href="/privacy-policy",
)
COPY_IT = dict(
    home="/it", tagline="La prima voice AI dedicata <br>esclusivamente all&rsquo;E-Commerce.",
    backed="Supportato da", company="Azienda", usecases="Flussi", industries="Settori",
    links=[("Home", "/it"), ("Prezzi", "/it/prezzi"), ("Chi Siamo", "/it/chi-siamo"),
           ("Contattaci", "/it/contatti"), ("Blog", "/it/blog")],
    product="Prodotto", playbooks="Playbook",
    demo="Prenota una call", terms="Termini e Condizioni", privacy="Privacy e Cookie",
    cookies="Preferenze cookie",
    other_label="English", other_href="/", logo_alt="Sabato AI - Home",
    # Real Italian pages since 7 Aug 2026 - these used to point at the English
    # originals, which is why the audit needed a cross-language exemption.
    terms_href="/it/termini-e-condizioni", privacy_href="/it/privacy-e-cookie",
)
LANGS = {"en": COPY_EN, "it": COPY_IT}


# The two long columns ship as <details OPEN>. That is the state a crawler sees
# and the state desktop wants, so neither needs JavaScript to be correct.
#
# This closes them on a narrow viewport. It is inline and sits immediately after
# the footer on purpose: an external or deferred script would run after first
# paint, so a phone would flash a 2,000px expanded footer and then snap shut.
# Inline and synchronous, it runs before the footer is painted.
#
# Safe to run here, unlike everything in enhance.js, because this footer is ours
# and lives outside React's root - there is no hydration to collide with.
# ...and on DESKTOP the summaries must not toggle at all. The CSS makes them
# LOOK like plain column headings (no marker, cursor: default), but <summary>
# stays a native toggle - so clicking "Use Cases" in the footer collapsed the
# whole column of links. Styling something inert does not make it inert.
# preventDefault on wide viewports does, and covers Enter/Space too, because
# the browser routes those through the same click activation. The resize
# handler re-opens everything at desktop width so a column collapsed on a
# phone cannot arrive closed when the same window is stretched wide.
COLLAPSE_SCRIPT = (
    '<script>(function(){try{'
    'var mq=window.matchMedia&&window.matchMedia("(max-width: 809px)");'
    'var d=document.querySelectorAll(".sb-footer details.sb-acc");var i;'
    'if(mq&&mq.matches)for(i=0;i<d.length;i++)d[i].removeAttribute("open");'
    'for(i=0;i<d.length;i++)(function(el){'
    'var s=el.querySelector("summary");if(!s)return;'
    's.addEventListener("click",function(e){'
    'if(!mq||!mq.matches)e.preventDefault();});'
    '})(d[i]);'
    'window.addEventListener("resize",function(){'
    'if(mq&&mq.matches)return;'
    'for(var j=0;j<d.length;j++)d[j].setAttribute("open","");});'
    '}catch(e){}})();</script>'
)


def _array(js, name):
    """(label, href) pairs from an array in enhance.js, in nav order."""
    m = re.search(re.escape(name) + r"\s*=\s*\[(.*?)\];", js, re.S)
    if not m:
        sys.exit(f"footer.py: could not find {name} in enhance.js - did the nav change?")
    # [^"]* not .*? - Italian entries carry an `aliases` field, and a lazy match
    # that required a closing brace ran on into the next entry.
    items = re.findall(r'label:\s*"([^"]*)"\s*,\s*href:\s*"([^"]*)"', m.group(1))
    if not items:
        sys.exit(f"footer.py: {name} parsed to nothing")
    return items


def nav_data(lang):
    js = open(ENHANCE, encoding="utf-8").read()
    suffix = "_IT" if lang == "it" else "_EN"
    return _array(js, "USECASES" + suffix), _array(js, "INDUSTRIES" + suffix)


def _li(label, href):
    # Labels come from enhance.js and may contain & or an apostrophe.
    return f'<li><a href="{href}">{html.escape(label, quote=False)}</a></li>'


def _column(title, items):
    """A collapsible column. <details open> so the shipped HTML is expanded."""
    lis = "".join(_li(l, h) for l, h in items)
    return (f'<details class="sb-col sb-acc" open>'
            f'<summary><span class="sb-h4">{title}</span></summary>'
            f'<ul>{lis}</ul></details>')


# ---------------------------------------------------------------------------
# FOOTER-ONLY SHORT LABELS. Daniel, 16 Aug: "I only wanted you to change them
# in the FOOTER menu so they fit into the space".
#
# Two different jobs: the header dropdown has a whole column and can afford the
# full name; a footer column has a sixth of the width and has to hold one line.
# So the short forms live HERE and nowhere else - enhance.js and playbook_data
# keep the real labels, which the header, the hubs and every cross-link use.
#
# KEYED ON HREF, not on the label: labels are editorial and get rewritten,
# hrefs are the identity of the page. Key this on text and the next rewording
# silently un-shortens the footer.
# ---------------------------------------------------------------------------
SHORT = {
    "en": {
        "/use-cases/cart-abandonment-recovery": "Cart Recovery",
        "/use-cases/qualify-and-collect-for-quote": "B2B Quote Collection",
        "/use-cases/checkout-summary-via-text": "WhatsApp Checkout",
        "/use-cases/back-in-stock-notification": "Back-in-Stock Alerts",
        "/playbooks/international-expansion": "Open New Markets",
    },
    "it": {
        "/it/casi-duso/recupero-carrelli-abbandonati": "Recupero Carrelli",
        "/it/casi-duso/riepilogo-checkout-via-messaggio": "Checkout su WhatsApp",
        "/it/casi-duso/feedback-post-consegna": "Feedback Consegna",
        "/it/playbook/espansione-internazionale": "Apri nuovi mercati",
        "/it/playbook/costi-assistenza": "Taglia i costi",
    },
}


def _short(lang, items):
    """Swap in the footer label where there is one. Everything else passes."""
    return [(SHORT[lang].get(h.rstrip("/"), l), h) for l, h in items]


def product_links(lang):
    """Every product page, from product_data - never a second hand-kept list."""
    from product_data import PRODUCTS, ORDER
    from product_data_it import PRODUCTS_IT, ORDER_IT
    src, order, base = ((PRODUCTS, ORDER, "/product/") if lang == "en"
                        else (PRODUCTS_IT, ORDER_IT, "/it/prodotto/"))
    return [(src[s]["chip"], base + s) for s in order]


def playbook_links(lang):
    """Every playbook, from playbook_data, same reason."""
    from playbook_data import PLAYBOOKS, ORDER
    from playbook_data_it import PLAYBOOKS_IT, ORDER_IT
    src, order, base = ((PLAYBOOKS, ORDER, "/playbooks/") if lang == "en"
                        else (PLAYBOOKS_IT, ORDER_IT, "/it/playbook/"))
    return [(src[s]["nav"], base + s) for s in order]


def footer_html(lang="en"):
    if lang not in LANGS:
        raise ValueError(f"footer.py: unknown language {lang!r}")
    c = LANGS[lang]
    ucs, inds = nav_data(lang)

    company = "".join(_li(l, h) for l, h in c["links"])
    company += (f'<li><a href="{CAL}" target="_blank" rel="noopener">'
                f'{c["demo"]}</a></li>')

    return (
      f'<footer class="sb-footer" data-lang="{lang}">'
        f'<div class="sb-shell">'
          f'<div class="sb-grid">'
            f'<div class="sb-brand">'
              f'<a href="{c["home"]}" aria-label="{c["logo_alt"]}">'
                f'<img class="sb-logo" src="{LOGO}" alt="Sabato AI logo" '
                f'width="2080" height="278" loading="lazy"></a>'
              f'<p class="sb-tagline">{c["tagline"]}</p>'
              f'<p class="sb-backed">{c["backed"]}</p>'
              f'<img class="sb-backed-img" src="{BACKED}" alt="ElevenLabs Grants" '
              f'width="1496" height="132" loading="lazy">'
            f'</div>'
            f'<div class="sb-col sb-col-static">'
              f'<span class="sb-h4">{c["company"]}</span><ul>{company}</ul>'
            f'</div>'
            + _column(c["product"], product_links(lang))
            + _column(c["playbooks"], _short(lang, playbook_links(lang)))
            + _column(c["usecases"], _short(lang, ucs))
            + _column(c["industries"], inds) +
          f'</div>'
          f'<div class="sb-bottom">'
            f'<p class="sb-copy">{COPY}</p>'
            f'<div class="sb-legal">'
              f'<a href="{c["terms_href"]}">{c["terms"]}</a>'
              f'<a href="{c["privacy_href"]}">{c["privacy"]}</a>'
              # Withdrawal has to be as easy as giving it (GDPR art. 7(3)), so
              # the banner is reachable from every page forever - not just once
              # on the first visit. consent.py listens for this attribute.
              f'<a href="#" data-sb-consent-open>{c["cookies"]}</a>'
              # data-lang-switch marks this as a deliberate cross-language link.
              # tools/audit_links.py and enhance.js both skip it - without the
              # marker the audit would report the switcher as a language leak,
              # which is the one thing it is not.
              f'<a href="{c["other_href"]}" data-lang-switch>{c["other_label"]}</a>'
              f'<a href="{LINKEDIN}" target="_blank" rel="noopener" '
              f'aria-label="Sabato AI on LinkedIn">'
              f'<img src="{LI_ICON}" alt="LinkedIn" width="20" height="20" '
              f'loading="lazy"></a>'
            f'</div>'
          f'</div>'
        f'</div>'
      f'</footer>'
      + COLLAPSE_SCRIPT
    )


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    out = footer_html(lang)
    ucs, inds = nav_data(lang)
    print(out)
    print(f"\n[{lang}] {len(ucs)} use cases, {len(inds)} industries, "
          f"{out.count('<a ')} links, {len(out)} bytes", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
