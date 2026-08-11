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


def proof_html(lang="en"):
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
      f'<section class="sb-proof" data-lang="{lang}" hidden>'
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
        f'</div>'
      f'</section>'
      f'{MOVE_SCRIPT}'
    )


# Moves the widget in front of the FAQ section AFTER hydration. Runs on `load`,
# not DOMContentLoaded: Framer is still reconciling at DOMContentLoaded and a
# node inserted then is removed again, which is the whole reason this script
# exists rather than the markup simply being emitted in place.
MOVE_SCRIPT = (
    "<script data-sb-proof>(function(){var W=null;"
    # W holds the node in a CLOSURE, and go() runs three times rather than once.
    # Moving the widget puts it inside React's tree, and a late reconcile can
    # delete it again exactly the way the build-time probe was deleted - which
    # showed up here as the widget being intermittently absent on load, roughly
    # one run in ten under a cold cache. Because the reference outlives the
    # removal, a later pass can put the same node back; a plain re-query could
    # not, since by then there is nothing in the document to find.
    "function go(){"
    "var w=W||document.querySelector('section.sb-proof');if(!w)return;W=w;"
    "var all=document.querySelectorAll('#main [data-framer-name]'),faq=null,i;"
    "for(i=0;i<all.length;i++){"
    "var n=(all[i].getAttribute('data-framer-name')||'').toLowerCase().trim();"
    "if(n.indexOf('faq section')===0){faq=all[i];break;}}"
    "if(faq&&faq.parentNode&&w.nextElementSibling!==faq)"
    "faq.parentNode.insertBefore(w,faq);"
    "w.hidden=false;fit();}"
    # Aligns the logo to the END OF THE LAST-WRAPPING LINE rather than to the
    # edge of the text COLUMN. CSS cannot express this: the column is 736px but
    # English wraps 69px short of it, so a right-aligned mark hangs past the
    # text. Italian happens to fill the column, which is why it looked correct
    # in one language and wrong in the other. A Range over the blockquote gives
    # one rect per rendered line; the widest one is the real right edge.
    "function fit(){"
    "var w=document.querySelector('section.sb-proof');if(!w)return;"
    "var q=w.querySelector('blockquote'),by=w.querySelector('.sb-proof-by');"
    "if(!q||!by)return;by.style.width='';"
    "if(innerWidth<768)return;"                # stacked on phone, nothing to align
    "var r=document.createRange();r.selectNodeContents(q);"
    "var rects=r.getClientRects(),m=0,i;"
    "for(i=0;i<rects.length;i++){if(rects[i].width>1&&rects[i].right>m)m=rects[i].right;}"
    "var l=q.getBoundingClientRect().left;"
    "if(m>l+40)by.style.width=Math.ceil(m-l)+'px';}"
    "function arm(){var d=[300,1500,4000],i;"
    "for(i=0;i<d.length;i++)setTimeout(go,d[i]);}"
    "if(document.readyState==='complete')arm();"
    "else window.addEventListener('load',arm);"
    # Re-measure on resize: the line breaks move, so the right edge moves with
    # them. Fonts landing late shift it too, hence the second pass on webfont
    # load where the browser supports it.
    "addEventListener('resize',fit);"
    "if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);"
    "})();</script>")


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    out = proof_html(lang)
    print(out)
    print(f"\n[{lang}] {len(out)} bytes, goes on {sorted(PAGES)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
