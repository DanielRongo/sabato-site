#!/usr/bin/env python3
"""THE proof widget - Creative Cables' first month, face, quote and the link.

    python3 proof.py           # print the English one
    python3 proof.py it        # Italian

Import it: `from proof import proof_html, PAGES`.

WHY IT IS BUILT THIS WAY
------------------------
Daniel wants it immediately before the FAQ section on /, /pricing and /about.
That position is inside Framer's React root, and React will not tolerate a
stranger there: a probe div inserted at build time directly before
<section data-framer-name="Faq Section"> was GONE by the time hydration
finished - silently reconciled away, no error, no trace. Measured, not assumed.

So the markup is emitted at the end of <body>, outside the root, where the rest
of our components live. It is therefore in the served HTML - crawlers and
previews see the quote and the numbers without running a line of script. A
seven-line inline script then MOVES that one node in front of the FAQ section
after load, which is safe because hydration has already finished by then.

If the script never runs, the widget simply stays where it is, above the
footer. Wrong position, still readable, still linked - the failure mode is
cosmetic rather than blank.

DATA COMES FROM customer_data.py. The quote, the three first-month figures, the
name, the role and the photo are the same strings the case study renders, so
the homepage cannot drift from the page it links to. `approved` is checked at
build time: this widget refuses to render for a customer who has not signed off.
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from customer_data import CUSTOMERS                      # noqa: E402
import customer_data_it as _it                           # noqa: E402

CUSTOMERS_IT = next(getattr(_it, n) for n in dir(_it) if n.isupper())

SLUG = "creative-cables"

# Every page Daniel asked for, both languages. Clima Convenienza is not here:
# its approval is still pending and `approved` would block it anyway.
PAGES = {"index.html", "pricing.html", "about.html",
         "it.html", "it/prezzi.html", "it/chi-siamo.html"}

# Framer names it "Faq Section" on / and /about and "FAQ Section" on /pricing.
# The script matches case-insensitively for exactly that reason - the same class
# of trap as the CTA section that ships with a trailing space in its name.
ANCHOR = "faq section"

COPY = {
    "en": dict(eyebrow="Customer story",
               h2="Success stories",
               sub="What happened in the first month on the line - measured on "
                   "real calls, not modelled.",
               link="Read the full case study",
               base="/customers/"),
    "it": dict(eyebrow="Storia cliente",
               h2="Storie di successo",
               sub="Cosa è successo nel primo mese sulla linea - misurato su "
                   "chiamate vere, non stimato.",
               link="Leggi il caso studio completo",
               base="/it/clienti/"),
}


def _data(lang):
    src = CUSTOMERS if lang == "en" else CUSTOMERS_IT
    d = src[SLUG]
    # `promotable`, not `approved`. Approved means their own page is signed off.
    # Promotable means we may put their name and numbers on OUR homepage, which
    # is a different and larger permission - see the header of customer_data.py.
    if not d.get("promotable"):
        raise SystemExit(f"proof.py: {SLUG} is not promotable - refusing to render")
    return d


def proof_card(lang="en"):
    """The head + card markup shared by both placements."""
    if lang not in COPY:
        raise ValueError(f"proof.py: unknown language {lang!r}")
    c, d = COPY[lang], _data(lang)
    stats = "".join(
        f'<div class="sb-proof-stat">'
        f'<span class="sb-proof-num">{html.escape(v, quote=False)}</span>'
        f'<span class="sb-proof-lab">{lab}</span></div>'
        for v, lab, _note in d["results"][:3])
    # ORDER: person first, numbers second. Daniel asked for the face and the
    # quote to outrank the metrics, and the DOM order is what carries that -
    # not just the type sizes. It also reads better to a screen reader and to a
    # crawler, both of which take the source order literally: a human being
    # vouching for us, then the evidence backing him up.
    # The customer's own logo rides the attribution line, right-aligned opposite
    # the name. That pairing is the whole point: "Marco Logreco, Head of
    # E-Commerce" and the Creative Cables mark are one statement of who is
    # speaking, so they belong on one line rather than at opposite ends of the
    # card. Falls back to the eyebrow if a customer has no white knockout.
    # width AND height, both. With only a height attribute the box measures ZERO
    # wide until the lazy image actually decodes, so the flex row lays out around
    # a phantom and the mark snaps into place on load - which is exactly the
    # "logo is not aligned properly" you can see on a cold visit. 110x34 is the
    # 633x196 source at its rendered height.
    mark = (f'<img class="sb-proof-logo" src="{d["logo_white"]}" '
            f'alt="{html.escape(d["name"])}" width="110" height="34" '
            f'loading="lazy" decoding="async">'
            if d.get("logo_white") else "")
    return (
        f'<div class="sb-proof-head">'
          f'<h2>{c["h2"]}</h2><p>{c["sub"]}</p>'
        f'</div>'
        f'<div class="sb-proof-card">'
          f'<div class="sb-proof-quote">'
            f'<img class="sb-proof-face" src="{d["photo"]}" width="260" height="260" '
            f'alt="{html.escape(d["person"])}, {html.escape(d["role"])} at {html.escape(d["name"])}" '
            f'loading="lazy" decoding="async">'
            f'<div class="sb-proof-said">'
              f'<blockquote>&ldquo;{d["quote"]}&rdquo;</blockquote>'
              f'<div class="sb-proof-by">'
                f'<p class="sb-proof-who"><b>{html.escape(d["person"])}</b>'
                f'<span>{html.escape(d["role"])}, {html.escape(d["name"])}</span></p>'
                f'{mark}'
              f'</div>'
            f'</div>'
          f'</div>'
          f'<div class="sb-proof-stats">{stats}</div>'
          f'<a class="sb-proof-cta" href="{c["base"]}{SLUG}">{c["link"]}'
          f'<span aria-hidden="true"> &rarr;</span></a>'
        f'</div>')


def proof_html(lang="en"):
    """Homepage placement: emitted at end of <body>, moved before the FAQ."""
    return (f'<section class="sb-proof" data-lang="{lang}" hidden>{proof_card(lang)}</section>'
            f'{MOVE_SCRIPT}')


def proof_inline_html(lang="en"):
    """The SAME widget, for a page that owns its own layout.

    Byte-identical card markup to the homepage version - same head, same card,
    same classes, so it inherits every rule in footer.css and cannot drift into
    a lookalike. Two differences, both structural rather than visual:

      * `sb-proof-inline` in the class list, and no `data-lang="x" hidden`.
        tools/apply_footer.py strips `<section class="sb-proof"` - an exact
        match including the closing quote - so a second class in that attribute
        is what keeps this copy from being deleted on the next build. It is a
        load-bearing class name, not decoration.
      * No move script. There is no Framer FAQ to slide in front of on an
        authored page; the section is already exactly where it belongs.

    The logo still has to be aligned to the end of the quote, so that one piece
    of the script comes along under its own marker.
    """
    c, d = COPY[lang], _data(lang)
    _ = c, d                     # validation side effects: unknown lang, approval
    card = proof_card(lang)
    return (f'<section class="sb-proof sb-proof-inline" data-lang="{lang}">{card}</section>'
            f'{INLINE_FIT_SCRIPT}')


# Moves the widget in front of the FAQ section AFTER hydration. Runs on `load`,
# not DOMContentLoaded: Framer is still reconciling at DOMContentLoaded and a
# node inserted then is removed again, which is the whole reason this script
# exists rather than the markup simply being emitted in place.
MOVE_SCRIPT = (
    "<script data-sb-proof>(function(){var W=null,F=null;"
    # W and F hold the widget and its FAQ anchor in a CLOSURE, and go() runs
    # three times: React can delete the moved node in a late reconcile exactly
    # the way it deleted the build-time probe, and once it has, a re-query finds
    # nothing to put back.
    "function go(){"
    "var w=W||document.querySelector('section.sb-proof');if(!w)return;W=w;"
    "var all=document.querySelectorAll('#main [data-framer-name]'),faq=null,i;"
    "for(i=0;i<all.length;i++){"
    "var n=(all[i].getAttribute('data-framer-name')||'').toLowerCase().trim();"
    "if(n.indexOf('faq section')===0){faq=all[i];break;}}"
    "if(faq){F=faq;if(faq.parentNode&&w.nextElementSibling!==faq)"
    "faq.parentNode.insertBefore(w,faq);}"
    "w.hidden=false;ord();}"
    # THE PHONE BUG, 11 Aug: at its phone breakpoint Framer lays #main out as a
    # flex column and positions sections with CSS `order` (hero 1 ... faq 10) -
    # DOM position stops mattering. Our widget had no order, so it defaulted to
    # 0 and flex sorted it to the top of the page, directly after the hero.
    # Desktop keeps every order at 0, which is why every DOM-based check
    # passed while phones showed it in the wrong place. Copying the FAQ's own
    # computed order makes the two a tie, and flex breaks ties by DOM order -
    # where we are already immediately before the FAQ. Re-applied on resize,
    # because the order values change per breakpoint.
    "function ord(){if(!W||!F)return;"
    "var o=getComputedStyle(F).order;"
    "if(W.style.order!==o)W.style.order=o;}"
    "function arm(){var d=[300,1500,4000],i;"
    "for(i=0;i<d.length;i++)setTimeout(go,d[i]);}"
    "if(document.readyState==='complete')arm();"
    "else window.addEventListener('load',arm);"
    "addEventListener('resize',ord);"
    "})();</script>")


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    out = proof_html(lang)
    print(out)
    print(f"\n[{lang}] {len(out)} bytes, goes on {sorted(PAGES)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())


# Aligns the logo to the end of the quote's longest rendered line - the same
# measurement the homepage widget does, minus the moving. Its own attribute,
# because apply_footer strips `<script data-sb-proof>` exactly.
INLINE_FIT_SCRIPT = (
    "<script data-sb-proof-inline>(function(){"
    "function fit(){"
    "var w=document.querySelector('section.sb-proof-inline');if(!w)return;"
    "var q=w.querySelector('blockquote'),by=w.querySelector('.sb-proof-by');"
    "if(!q||!by)return;by.style.width='';"
    "if(innerWidth<768)return;"
    "var r=document.createRange();r.selectNodeContents(q);"
    "var rects=r.getClientRects(),m=0,i;"
    "for(i=0;i<rects.length;i++){if(rects[i].width>1&&rects[i].right>m)m=rects[i].right;}"
    "var l=q.getBoundingClientRect().left;"
    "if(m>l+40)by.style.width=Math.ceil(m-l)+'px';}"
    "if(document.readyState!=='loading')fit();"
    "else document.addEventListener('DOMContentLoaded',fit);"
    "addEventListener('load',fit);addEventListener('resize',fit);"
    "if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);"
    "})();</script>")
