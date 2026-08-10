#!/usr/bin/env python3
"""THE brand-logo band - the black strip of partner logos under the hero.

    python3 logos.py            # print the English one
    python3 logos.py it         # Italian (identical markup; kept for symmetry)

Import it: `from logos import logos_html, PAGES`.

WHY THIS EXISTS
---------------
It closes the seam. Our hero card and Framer's logo band are two halves of one
black slab, and they were inset by different amounts: Framer runs three
responsive variants and the first hero rebuild reproduced one of them, so above
1440px the card kept widening while the band stopped at 1360 and the join
showed a step. Owning both halves means one rule sets the width of both -
see the shared selectors in site/css/footer.css. The seam cannot drift again
because there is nothing left to drift against.

It is also the pilot for the seven Framer sections still on the homepage. If
this pattern holds - hide theirs by data-framer-name, emit ours before React's
root, verify with tools/visual_diff.py - the rest follow.

MEASURED OFF FRAMER, at 1440 and 390:

    band card      radius 0 0 24px 24px, #000, same width rule as the hero card
    padding        74px 40px desktop, 32px 20px phone   (180px / 96px tall)
    viewport       32px tall, overflow hidden
    item           [logo][gap][1px x 20px line], gap 32px desktop / 20px phone
    line colour    rgb(248, 244, 241)
    speed          50px/s at BOTH breakpoints - Framer's 43s desktop and 20.06s
                   phone durations are the same speed over different content
                   widths, which is why the durations here are per-breakpoint

THE MARQUEE IS CSS, NOT JS. Framer drives it with a Web Animations ticker over
four copies of the list. Two copies and a translateX(-50%) keyframe give the
same seamless loop with no runtime, and honour prefers-reduced-motion, which
Framer's version does not.
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# The two homepages, and ONLY those.
#
# /pricing and /it/prezzi also carry something Framer calls "Brand Logos", but
# it is a different instance: 39px tall, 1200 wide, sitting mid-page with no
# hero above it. Shipping this 180px black band there put a hero-sized slab at
# the very top of the pricing page. tools/visual_diff.py caught it on its first
# real run - +157px of page height on a page this change had no business
# touching. If that strip is ever rebuilt it needs its own module and its own
# measurements.
PAGES = {"index.html", "it.html"}

# In Framer's order. Sizes are the rendered sizes, which for these files are the
# intrinsic ones except OpenAI (400x104 scaled to 104x27) and Telnyx (116x28
# squashed to 116x24 - Framer's choice, kept, because changing it would change
# the look). Framer gives every one of them alt="Logo"; real names cost nothing
# and are what a screen reader or an image search actually needs.
LOGOS = [
    ("zy54O3FOzcr0mnSvdOoSxqDD0-eab126d3.png",   99, 27, "OpenAI"),
    ("1IvwouzNYdt7lTiFas45b7QzgA-eca0d577.webp", 124, 24, "Deepgram"),
    ("Fs5hS48wxwuagBC7H1l6RnwNk-d1a6967d.png",   116, 24, "Google Gemini"),
    ("BeLHRYc79GbBZMVsNpi3laMZ2OA-43cb69ca.png",  91, 27, "Twilio"),
    ("DnXU6OH0H2Ic0bs54VdXl8akN0-a74c4db8.png",  104, 27, "Telnyx"),
    ("ZLfNjO9rPDa2rr4fMSSxHxkUSU-721d21cb.png",  150, 19, "ElevenLabs"),
]

BASE = "/fuc/images/"


def _items(copy):
    """One pass of the six logos.

    copy=2 is the duplicate that makes translateX(-50%) loop seamlessly. It is
    aria-hidden so the list is not announced twice, and its images carry empty
    alt for the same reason.
    """
    dup = copy == 2
    hidden = ' aria-hidden="true"' if dup else ''
    out = []
    for f, w, h, name in LOGOS:
        alt = "" if dup else html.escape(name)
        out.append(
            f'<li class="sb-logos-item"{hidden}>'
            f'<img src="{BASE}{f}" width="{w}" height="{h}" alt="{alt}" '
            f'loading="lazy" decoding="async">'
            f'<span class="sb-logos-line"></span>'
            f'</li>')
    return "".join(out)


def logos_html(lang="en"):
    if lang not in ("en", "it"):
        raise ValueError(f"logos.py: unknown language {lang!r}")
    return (
      f'<section class="sb-logos" data-lang="{lang}">'
        f'<div class="sb-logos-card">'
          f'<div class="sb-logos-viewport">'
            f'<ul class="sb-logos-track">{_items(1)}{_items(2)}</ul>'
          f'</div>'
        f'</div>'
      f'</section>'
    )


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    out = logos_html(lang)
    print(out)
    print(f"\n[{lang}] {len(out)} bytes, {len(LOGOS)} logo(s) x2, "
          f"goes on {sorted(PAGES)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
