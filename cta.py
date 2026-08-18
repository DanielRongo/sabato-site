#!/usr/bin/env python3
"""THE closing CTA band - the green card that closes the eight Framer pages.

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
# Framer's line-art flourish inside the card. Natural size 1040x1410; the card
# renders it 440x467 with object-fit:cover, so the attributes carry the real
# intrinsic size and CSS does the sizing (same rule as the footer logo).
DECOR = "/fuc/images/gwJojp6ALd65GvULe61l4AVkc-d2211afa.png"

# Exactly the pages Framer shipped this band on, verified by grepping for the
# headline. Kept explicit rather than "every Framer page" so adding a page does
# not silently gain a second closing CTA.
PAGES = {
    "index.html", "about.html", "contact.html", "pricing.html",
    "it.html", "it/prezzi.html", "it/chi-siamo.html", "it/contatti.html",
}

# Copy WAS Framer's verbatim. It is not any more: on 18 Aug 2026 the headline
# became "Your best people shouldn't be reading tracking numbers", which is the
# line Daniel picked for the close, and the body lost "Live in two weeks" - a
# claim he killed for undervaluing the work.
#
# THIS BAND IS ON EIGHT PAGES, not just the homepage (see PAGES). The headline
# had to work on /about and /pricing too, which is why it argues about the job
# rather than about this page. The body deliberately does NOT say "the four
# numbers above": the hero with the numbers exists only on / and /it.
COPY = {
    "en": dict(
        eyebrow="Get Started",
        # NOTE the space before <br>. On phones the CSS hides the <br> so the
        # headline can wrap naturally, and without that space the two sentences
        # collide into "24/7.Your phone line". On desktop a space before a line
        # break collapses to nothing, so the wide layout is unaffected.
        h2="Your best people shouldn't be <br>reading tracking numbers.",
        # <br> is Framer's break - it balances the two lines. Hidden on phones
        # (see the CSS), where the copy wraps naturally.
        body=("Pre-configured AI voice workflows for e-commerce, connected to your "
              "catalog and fully managed. <br>Book a call, or talk to our agent "
              "right now."),
        btn="Book a Call",
    ),
    "it": dict(
        eyebrow="Inizia ora",
        h2="I tuoi migliori non dovrebbero <br>leggere numeri di tracking.",
        body=("Workflow vocali AI preconfigurati per l&rsquo;e-commerce, collegati al tuo "
              "catalogo e completamente gestiti. <br>Prenota una call, oppure parla "
              "con il nostro agente adesso."),
        btn="Prenota una call",
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
          f'<div class="sb-cta-eyebrow-row">'
          f'<span class="sb-cta-eyebrow">{html.escape(c["eyebrow"], quote=False)}</span>'
          f'</div>'
          f'<h2 class="sb-cta-h2">{c["h2"]}</h2>'
          f'<p class="sb-cta-body">{c["body"]}</p>'
          f'<a class="sb-cta-btn" href="{CAL}" target="_blank" rel="noopener">'
          f'{html.escape(c["btn"], quote=False)}</a>'
          f'<img class="sb-cta-decor" src="{DECOR}" alt="" aria-hidden="true" '
          f'width="1040" height="1410" loading="lazy">'
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
