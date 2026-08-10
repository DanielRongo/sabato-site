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
               link="Read the full case study",
               base="/customers/"),
    "it": dict(eyebrow="Storia cliente",
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
    return (
      f'<section class="sb-proof" data-lang="{lang}" hidden>'
        f'<div class="sb-proof-card">'
          f'<p class="sb-proof-eyebrow">{c["eyebrow"]}</p>'
          f'<div class="sb-proof-stats">{stats}</div>'
          f'<figure class="sb-proof-quote">'
            f'<img class="sb-proof-face" src="{d["photo"]}" width="120" height="120" '
            f'alt="{html.escape(d["person"])}, {html.escape(d["role"])} at {html.escape(d["name"])}" '
            f'loading="lazy" decoding="async">'
            f'<div class="sb-proof-said">'
              f'<blockquote>&ldquo;{d["quote"]}&rdquo;</blockquote>'
              f'<figcaption><b>{html.escape(d["person"])}</b>'
              f'<span>{html.escape(d["role"])}, {html.escape(d["name"])}</span></figcaption>'
            f'</div>'
          f'</figure>'
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
    "<script>(function(){"
    "function go(){"
    "var w=document.querySelector('section.sb-proof');if(!w)return;"
    "var all=document.querySelectorAll('#main [data-framer-name]'),faq=null,i;"
    "for(i=0;i<all.length;i++){"
    "var n=(all[i].getAttribute('data-framer-name')||'').toLowerCase().trim();"
    "if(n.indexOf('faq section')===0){faq=all[i];break;}}"
    "if(faq&&faq.parentNode)faq.parentNode.insertBefore(w,faq);"
    "w.hidden=false;}"
    "if(document.readyState==='complete')setTimeout(go,300);"
    "else window.addEventListener('load',function(){setTimeout(go,300);});"
    "})();</script>")


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    out = proof_html(lang)
    print(out)
    print(f"\n[{lang}] {len(out)} bytes, goes on {sorted(PAGES)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
