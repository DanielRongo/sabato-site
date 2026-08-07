#!/usr/bin/env python3
"""THE closing CTA band - the green "Your store is open 24/7" card.

    python3 cta.py            # print the English one
    python3 cta.py it         # Italian

Import it: `from cta import cta_html, PAGES`.

WHY THIS EXISTS
---------------
Framer exported this band as a <section position:absolute> with pixel
coordinates baked in - `top: 10366px` on desktop, `top: 12216.8px` on phone,
plus transforms like translate(-720px, 0) and an inner block at
`top: -870px; margin-top: -118px`.

Measured on /it at 390px: the section's own box sat at y=12000 while its inner
content rendered at y=11061 - 939px ABOVE its own parent, straight on top of the
FAQ. On desktop it left a dead ~900px gap before the footer. Absolute
coordinates only hold while every pixel above them is unchanged, and they had
not been true for a while.

So it is rebuilt here in normal flow: a centred card with a CSS gradient, no
absolute positioning, no magic numbers. It sits directly above the footer
because tools/apply_footer.py emits the two together.

WHERE IT GOES: only the pages Framer put it on (PAGES below). Our generated
pages - use cases, industries, blog, customers - already close with their own
page-specific <section class="cta-band">, which is a better CTA than a generic
one because it names the thing the reader just read about. Two closing CTAs
stacked would be worse than either.

The gradient is a CSS linear-gradient sampled from Framer's background JPG
(#F7FD47 -> #2BFE41, left to right), so there is one fewer image to load and no
1440x900 raster stretched across a card of a different shape.
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CAL = "https://cal.com/sabatoai/intro"

# Exactly the pages Framer shipped this band on, verified by grepping for the
# headline. Kept explicit rather than "every Framer page" so adding a page does
# not silently gain a second closing CTA.
PAGES = {
    "index.html", "about.html", "contact.html", "pricing.html",
    "it.html", "it/prezzi.html", "it/chi-siamo.html", "it/contatti.html",
}

# Copy is Framer's, verbatim - this is a layout rebuild, not a rewrite.
COPY = {
    "en": dict(
        eyebrow="Get Started",
        # NOTE the space before <br>. On phones the CSS hides the <br> so the
        # headline can wrap naturally, and without that space the two sentences
        # collide into "24/7.Your phone line". On desktop a space before a line
        # break collapses to nothing, so the wide layout is unaffected.
        h2="Your store is open 24/7. <br>Your phone line should be too.",
        body=("Pre-configured AI voice workflows for e-commerce. Connected to your "
              "catalog. Fully managed. Live in two weeks. Book a call or talk to our "
              "AI right now."),
        btn="Start Free Pilot",
    ),
    "it": dict(
        eyebrow="Inizia ora",
        h2="Il tuo store &egrave; aperto 24/7. <br>Anche il tuo telefono dovrebbe esserlo.",
        body=("Workflow vocali AI preconfigurati per l&rsquo;e-commerce. Collegati al tuo "
              "catalogo. Completamente gestiti. Operativi in due settimane. Prenota una "
              "call o parla con la nostra AI adesso."),
        btn="Inizia il Pilota Gratuito",
    ),
}


def lang_of(rel):
    return "it" if rel == "it.html" or rel.startswith("it/") else "en"


def cta_html(lang="en"):
    if lang not in COPY:
        raise ValueError(f"cta.py: unknown language {lang!r}")
    c = COPY[lang]
    return (
      f'<section class="sb-cta" data-lang="{lang}">'
        f'<div class="sb-cta-card">'
          f'<span class="sb-cta-eyebrow">{html.escape(c["eyebrow"], quote=False)}</span>'
          f'<h2 class="sb-cta-h2">{c["h2"]}</h2>'
          f'<p class="sb-cta-body">{c["body"]}</p>'
          f'<a class="sb-cta-btn" href="{CAL}" target="_blank" rel="noopener">'
          f'{html.escape(c["btn"], quote=False)}</a>'
        f'</div>'
      f'</section>'
    )


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    out = cta_html(lang)
    print(out)
    print(f"\n[{lang}] {len(out)} bytes, goes on {len(PAGES)} page(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
