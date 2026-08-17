#!/usr/bin/env python3
"""THE homepage hero - the black card with the headline and the call numbers.

    python3 hero.py                 # print the English one
    python3 hero.py it              # Italian
    python3 hero.py --preview       # allow placeholder numbers (mockups only)

Import it: `from hero import hero_html, PAGES`.

WHY THIS EXISTS
---------------
Two reasons, one structural and one a plain bug.

Structural: the four callable numbers have to live in the hero, and the hero is
inside React's root (#main). Writing into that tree during hydration is the
fault that broke every footer link on this site for two weeks. The only safe
place for our markup is outside the root - which is where the header, the
closing CTA and the footer already live. So the hero joins them: Framer's is
hidden by CSS keyed on its OWN attribute, ours is emitted right after the
header by tools/apply_footer.py.

The wave: Framer's hero card carries `padding: 50px 40px 591px` on desktop and
`32px 40px 302px` on phones, and an absolutely-positioned <video> sits IN that
reserved space - the looping wave. It is `preload="none"` with no poster, and
this container's Chromium has no H.264 decoder, so in a headless screenshot it
renders as a black rectangle on a black card. The first version of this file
read that as dead padding and deleted the whole thing. It was not dead. Never
conclude "empty" from a render that cannot decode the asset - check the markup.

So the video is rebuilt here too, in normal flow instead of absolute
coordinates, at the sizes Framer gives it: 1360x552 on desktop, 350x260 on a
phone, object-fit: fill (it stretches - that is Framer's choice, kept).

WHAT IS COPIED VERBATIM: the eyebrow, the headline and both subhead paragraphs,
in both languages. This is a layout rebuild, not a rewrite - same policy as
cta.py.

GEOMETRY, measured off Framer at 1440px and 390px before anything was replaced:

    Hero Section wrapper  padding 16px 40px 0   radius 24px 24px 0 0  (phone: 0 20px)
    black card            eyebrow sits 88px below the card top        (phone: 70px)
    wave video            full card width, 552px tall, 44px above the card bottom
                                                       (phone: 260px tall, 13px)
    content column        max-width 1280, centred
    h1                    Satoshi 700, 72px/82.8px, tracking -2px     (phone: 36px/41.4px)
    subhead               Satoshi 400, 20px/34px                      (phone: 18px/30.6px)
    subhead column        644px on /, 800px on /it - Framer sizes it per language
    eyebrow row           white pill, radius 322px, padding 4px 20px 4px 8px, gap 8px
    "New" badge           rgb(255,43,43), radius 76px, padding 0 16px, 12px

THE NUMBERS ARE A HARD GATE. hero_html() raises if NUMBERS are still
placeholders, and tools/apply_footer.py asks that question in a preflight
before build.py runs a single generator - so a refusal changes nothing on disk
instead of leaving the site half-built. Preview renders pass
allow_placeholder=True; the build never does.
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Only the two homepages. Every other page keeps its own hero.
PAGES = {"index.html", "it.html"}

# The recording Framer had behind the lime play button. Same asset in both
# languages - it is an English call, which is worth fixing eventually; the
# Italian hero never had a player at all.
SAMPLE_CALL = "/fuc/assets/FEuwqrQUga0mEuonuv8aRlsCG8.mp3"

# The looping wave that closes the hero. Desktop only, by CSS alone.
#
# It was briefly JS-armed - no src in the markup, set from data-src when
# (min-width: 810px) matched - to stop phones fetching 4.2MB. That version
# never played. On staging, in a real Chrome, the element sat at
# networkState=LOADING with readyState=0 and zero bytes fetched, and an
# explicit load() did nothing; awaiting play() hung the renderer for 45
# seconds. Reproduced twice on cold loads.
#
# So: a plain src and a plain autoplay, which is the path browsers are actually
# built for, and display:none below 810px. Chrome will not autoplay a
# display:none element, so with preload="metadata" a phone pays for a few KB of
# headers rather than the whole file - most of the saving, none of the risk.
# muted + playsinline are what make autoplay legal at all; drop either and the
# wave is a black box on every iPhone.
WAVE = "/fuc/assets/zjPqfnxlo8A7anHbrHHt6WNQQ.mp4"

# ---------------------------------------------------------------------------
# The four numbers.
#
# PLACEHOLDER = True means "not real yet". Leave it True and the build refuses,
# rather than publishing a number that rings somebody else's phone.
# ---------------------------------------------------------------------------
PLACEHOLDER = False

# Real, from Daniel, 9 Aug 2026. tel: is E.164 exactly as provisioned; the
# display string is the same digits grouped the way each country writes them
# (London 020, Naples 081, Balearic 871, US NANP) - a number a reader cannot
# parse at a glance is a number they do not dial.
NUMBERS = [
    # (code, label EN,       label IT,      display,             tel:)
    ("gb", "United Kingdom", "Regno Unito", "+44 20 3893 2636",  "+442038932636"),
    ("us", "United States",  "Stati Uniti", "+1 754 208 0610",   "+17542080610"),
    ("it", "Italia",         "Italia",      "+39 081 1818 1316", "+3908118181316"),
    ("es", "España",         "Spagna",      "+34 871 073 084",   "+34871073084"),
]

# Regional-indicator pairs, written as escapes so the file stays ASCII.
# Flat rounded SVG, not emoji - same reason as the header switcher: Windows
# renders regional-indicator pairs as the letters in a box.
def _flag(uid, body):
    return ('<svg class="sb-cflag" viewBox="0 0 30 20" width="18" height="12" '
            'aria-hidden="true" focusable="false">'
            f'<defs><clipPath id="cf-{uid}"><rect width="30" height="20" rx="3"/></clipPath></defs>'
            f'<g clip-path="url(#cf-{uid})">{body}</g></svg>')


FLAG = {
    "gb": _flag("gb",
        '<rect width="30" height="20" fill="#012169"/>'
        '<path d="M0 0l30 20M30 0L0 20" stroke="#f1f2f1" stroke-width="4.4"/>'
        '<path d="M0 0l30 20M30 0L0 20" stroke="#c8102e" stroke-width="2.2"/>'
        '<path d="M15 0v20M0 10h30" stroke="#f1f2f1" stroke-width="6.6"/>'
        '<path d="M15 0v20M0 10h30" stroke="#c8102e" stroke-width="3.8"/>'),
    "us": _flag("us",
        '<rect width="30" height="20" fill="#f1f2f1"/>'
        '<path d="M0 1.5h30M0 4.6h30M0 7.7h30M0 10.8h30M0 13.9h30M0 17h30" '
        'stroke="#b31942" stroke-width="1.55"/>'
        '<rect width="13" height="10.8" fill="#0a3161"/>'),
    "it": _flag("it",
        '<rect width="10" height="20" fill="#009246"/>'
        '<rect x="10" width="10" height="20" fill="#f1f2f1"/>'
        '<rect x="20" width="10" height="20" fill="#ce2b37"/>'),
    "es": _flag("es",
        '<rect width="30" height="20" fill="#aa151b"/>'
        '<rect y="5" width="30" height="10" fill="#f1bf00"/>'),
}

# ---------------------------------------------------------------------------
# THE HERO CHIP. Replaces the white "New / Integration with Shopify" pill.
# Daniel, 16 Aug: "I don't like the pill - propose another design even if that
# means completely revamping it", then: "I love the pill that includes both
# Shopify and Zapier, keep that".
#
# Three things were wrong with the old one and only one was visual:
#   - a WHITE SLAB with a RED badge on a black hero: the loudest object on the
#     page, spending all that attention on the word "New".
#   - "New" ages, and nothing will remember to remove it.
#   - it went NOWHERE. The most-looked-at element above the fold was not a link.
# ---------------------------------------------------------------------------
SHOPIFY_MARK = (
    '<svg class="sb-chip-mark" viewBox="0 0 24 27" width="15" height="17" '
    'aria-hidden="true" focusable="false">'
    '<path d="M18.6 4.9a.3.3 0 0 0-.25-.25c-.1 0-2.1-.15-2.1-.15s-1.4-1.4-1.55-1.55c-.15-.15-.45-.1-.56-.07 0 0-.3.1-.78.25A5.5 5.5 0 0 0 12.98 1 3 3 0 0 0 10.5.02C8.6.08 6.72 1.45 5.2 3.9 4.14 5.6 3.33 7.75 3.1 9.4c-2.2.68-3.73 1.16-3.77 1.17-1.1.35-1.14.38-1.28 1.42C-2.06 12.77 0 26.9 0 26.9l15.2 2.6 6.6-1.63S18.62 5.07 18.6 4.9z" '
    'fill="#95BF47" transform="translate(2.4 -1.6) scale(.86)"/>'
    '<path d="M14.2 3.13c-.28.08-.6.18-.95.29 0-.66-.09-1.58-.4-2.37 1 .19 1.48 1.3 1.35 2.08z" fill="#5E8E3E"/>'
    '<path d="M11.9 8.9s-.86-.46-1.9-.46c-1.55 0-1.63.97-1.63 1.21 0 1.33 3.46 1.84 3.46 4.95 0 2.45-1.55 4.02-3.64 4.02-2.5 0-3.79-1.56-3.79-1.56l.67-2.22s1.32 1.14 2.44 1.14c.73 0 1.03-.58 1.03-1 0-1.74-2.84-1.82-2.84-4.66 0-2.4 1.72-4.72 5.2-4.72 1.34 0 2 .38 2 .38l-1 3.02z" fill="#fff"/></svg>')

ZAPIER_MARK = (
    '<svg class="sb-chip-mark" viewBox="0 0 24 24" width="13" height="13" '
    'aria-hidden="true" focusable="false">'
    '<path d="M13 2.5 4.5 13.5H11l-.8 8 8.3-11h-6.3z" fill="#ff4f00"/></svg>')

COPY = {
    "en": dict(
        badge="New",
        chip_a="Shopify", chip_b="Zapier", chip_c="+ 8,500 apps",
        chip_href="/product/integrations-webhooks",
        chip_aria="How Sabato connects to your systems",
        tag="Integration with Shopify",
        # The lime eyebrow carries the category so the headline does not have
        # to. Both lines of the h1 are hand-broken: the sentence is a pair and
        # letting the browser wrap it anywhere else breaks the parallel.
        eyebrow="Managed Voice AI for e-commerce",
        h1="You grow the store. <br>We run the phone line.",
        sub1=("Sabato puts a managed voice agent on your support line, built for "
              "e-commerce and retail, wired into your catalog and your order system, "
              "speaking every language you sell in. We build it, we run it, we "
              "improve it every day. Your team gets its time back."),
        sub2="",
        hand="call it right now &mdash; it picks up",
        reveal="Show number",
        call="Call now",
        listen="or listen to a sample call",
    ),
    "it": dict(
        badge="Novit&agrave;",
        chip_a="Shopify", chip_b="Zapier", chip_c="+ 8.500 app",
        chip_href="/it/prodotto/integrations-webhooks",
        chip_aria="Come Sabato si collega ai tuoi sistemi",
        tag="Integrazione con Shopify",
        eyebrow="Voice AI gestita per l&rsquo;e-commerce",
        h1="Tu fai crescere lo store. <br>Al telefono ci pensiamo noi.",
        sub1=("Sabato mette un agente vocale gestito sulla tua linea di assistenza, "
              "pensato per e-commerce e retail, collegato al catalogo e al sistema "
              "ordini, che parla tutte le lingue in cui vendi. Lo costruiamo, lo "
              "gestiamo, lo miglioriamo ogni giorno. Il tuo team si riprende il suo tempo."),
        sub2="",
        hand="chiamalo adesso &mdash; risponde",
        reveal="Mostra numero",
        call="Chiama ora",
        listen="oppure ascolta una chiamata di esempio",
    ),
}

# Adds .sb-js to the section, which is what switches the numbers from "shown"
# to "masked". Doing it from script rather than in the markup means the masking
# only ever happens when the code that can unmask them is running - JS off, or
# the script erroring, leaves four readable numbers rather than four dead
# buttons. Inline and tiny, like the header menu and the footer accordion,
# because this markup lives outside React's root and a separate file would be a
# third request for ten lines.
REVEAL_SCRIPT = (
    "<script>(function(){"
    "var s=document.querySelector('section.sb-hero');if(!s)return;"
    "s.classList.add('sb-js');"
    "s.addEventListener('click',function(e){"
    "var t=e.target;if(!t||!t.closest)return;"
    "var a=t.closest('.sb-hero-num');if(!a)return;"
    # Only the lime CALL NOW line dials. Everything else on the card toggles.
    "if(t.closest('.sb-hero-call'))return;"
    # e.detail is 0 for a click synthesised by Enter or Space. A keyboard user
    # cannot aim at CALL NOW - it is a <span> inside the anchor, and nesting a
    # second focusable there would be invalid markup - so on an already-open
    # card the keyboard path dials instead of toggling: Enter reveals, Enter
    # again calls.
    "if(a.classList.contains('is-open')&&e.detail===0)return;"
    "e.preventDefault();a.classList.toggle('is-open');});"
    "})();</script>")


PHONE_GLYPH = (
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M6.6 2.8h3.1l1.6 4-2 1.2a11.3 11.3 0 0 0 4.7 4.7l1.2-2 4 1.6v3.1'
    'a1.6 1.6 0 0 1-1.7 1.6A15.8 15.8 0 0 1 5 6.1a1.6 1.6 0 0 1 1.6-1.7Z" '
    'stroke="currentColor" stroke-width="2.1" stroke-linejoin="round"/></svg>')


def _cards(lang):
    """One anchor per country, number masked until the first click.

    The number is in the markup and in the href from the start - it is only
    visually masked - so a reader with JS off gets it without any interaction,
    and aria-label carries it to a screen reader. The two-step (reveal, then
    dial) exists for the mouse and touch path, where a single tap on a tel:
    link would otherwise start a call before the number was ever shown. Once a
    card is open it stays open: collapsing it again when another is opened
    loses state for no reason.

    Three rows: country, then the number (masked), then the CALL NOW button
    under it. The third row is always in the layout and only its visibility
    changes, so the card is the same height open or closed and nothing jumps
    when you tap. The country label stays put now rather than being swapped out,
    which matters once two cards are open at once.

    CALL NOW is the only thing that dials. On a phone that is a plain click on a
    plain tel: link, untouched by the handler, so the OS dialler opens the way it
    would from any other link.
    """
    idx = 1 if lang == "en" else 2
    reveal = COPY[lang]["reveal"]
    call = COPY[lang]["call"]
    out = []
    for row in NUMBERS:
        code, disp, tel = row[0], row[3], row[4]
        label = html.escape(row[idx], quote=False)
        out.append(
            f'<a class="sb-hero-num" href="tel:{tel}" data-cc="{code}" '
            f'aria-label="{html.escape(row[idx])} {html.escape(disp)}">'
            f'<span class="sb-hero-cc">{FLAG[code]} {label}</span>'
            f'<span class="sb-hero-slot">'
            f'<span class="sb-hero-no">{html.escape(disp, quote=False)}</span>'
            f'<span class="sb-hero-reveal" aria-hidden="true">{reveal}</span>'
            f'</span>'
            f'<span class="sb-hero-call" aria-hidden="true">{PHONE_GLYPH}{call}</span>'
            f'</a>')
    return "".join(out)


def hero_html(lang="en", allow_placeholder=False):
    if lang not in COPY:
        raise ValueError(f"hero.py: unknown language {lang!r}")
    if PLACEHOLDER and not allow_placeholder:
        raise SystemExit(
            "hero.py: NUMBERS are still placeholders.\n"
            "  Put the four real numbers in NUMBERS, set PLACEHOLDER = False,\n"
            "  and rebuild. Refusing to publish a phone number that is not ours.")
    c = COPY[lang]
    return (
      f'<section class="sb-hero" data-lang="{lang}">'
        f'<div class="sb-hero-card">'
          f'<div class="sb-hero-inner">'
            f'<a class="sb-hero-chip" href="{c["chip_href"]}" '
            f'aria-label="{c["chip_aria"]}">'
              f'<span class="sb-chip-seg">{SHOPIFY_MARK}<b>{c["chip_a"]}</b></span>'
              f'<i class="sb-chip-sep"></i>'
              f'<span class="sb-chip-seg">{ZAPIER_MARK}<span>{c["chip_b"]}</span></span>'
              f'<i class="sb-chip-sep"></i>'
              f'<span class="sb-chip-more">{c["chip_c"]}</span>'
              f'<span class="sb-chip-arrow">&rarr;</span>'
            f'</a>'
            f'<span class="sb-hero-eyebrow">{c["eyebrow"]}</span>'
            f'<h1 class="sb-hero-h1">{c["h1"]}</h1>'
            f'<p class="sb-hero-sub">{c["sub1"]}</p>'
            + (f'<p class="sb-hero-sub">{c["sub2"]}</p>' if c["sub2"] else "") +
            f'<p class="sb-hero-hand">{c["hand"]}</p>'
            f'<div class="sb-hero-nums">{_cards(lang)}</div>'
            f'<a class="sb-hero-listen" href="{SAMPLE_CALL}" target="_blank" rel="noopener">'
              f'<span class="sb-hero-tri"></span>{c["listen"]}</a>'
          f'</div>'
          f'<video class="sb-hero-wave" src="{WAVE}" autoplay loop muted '
          f'playsinline preload="metadata" aria-hidden="true" tabindex="-1"></video>'
        f'</div>'
      f'</section>'
      f'{REVEAL_SCRIPT}'
    )


def main():
    args = sys.argv[1:]
    preview = "--preview" in args
    langs = [a for a in args if not a.startswith("-")]
    lang = langs[0] if langs else "en"
    out = hero_html(lang, allow_placeholder=preview)
    print(out)
    print(f"\n[{lang}] {len(out)} bytes, goes on {sorted(PAGES)}"
          + ("   PLACEHOLDER NUMBERS" if PLACEHOLDER else ""), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
