#!/usr/bin/env python3
"""Category glyphs for the hero live-call card.

One 24x24 lime line-glyph per industry, so a visitor knows which vertical they
are on before reading a word. Written as SVG code, like every other graphic on
the site: flat, geometric, palette-only, no raster.

Drawn on a 24x24 grid with a 2px stroke so all nine share a weight - a mixed
set of stroke widths is the fastest way to make a glyph family look bought
rather than designed.
"""

_L = 'rgb(204,255,0)'
_W = '<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'


def _g(paths):
    return _W % (_L, paths)


ICONS = {
    # wall-mounted split unit with airflow
    "home-improvement": _g(
        '<rect x="3" y="4" width="18" height="7" rx="2"/>'
        '<line x1="6" y1="8" x2="14" y2="8"/>'
        '<path d="M7 15c1.6 1.6 3.2 1.6 4.8 0"/>'
        '<path d="M11 19c1.6 1.6 3.2 1.6 4.8 0"/>'),
    # brake disc with hub and vent holes
    "automotive-parts": _g(
        '<circle cx="12" cy="12" r="8.5"/>'
        '<circle cx="12" cy="12" r="3"/>'
        '<line x1="12" y1="3.5" x2="12" y2="6"/>'
        '<line x1="12" y1="18" x2="12" y2="20.5"/>'
        '<line x1="3.5" y1="12" x2="6" y2="12"/>'
        '<line x1="18" y1="12" x2="20.5" y2="12"/>'),
    # chip with pins
    "electronics-tech": _g(
        '<rect x="7" y="7" width="10" height="10" rx="1.5"/>'
        '<line x1="10" y1="3.5" x2="10" y2="7"/><line x1="14" y1="3.5" x2="14" y2="7"/>'
        '<line x1="10" y1="17" x2="10" y2="20.5"/><line x1="14" y1="17" x2="14" y2="20.5"/>'
        '<line x1="3.5" y1="10" x2="7" y2="10"/><line x1="3.5" y1="14" x2="7" y2="14"/>'
        '<line x1="17" y1="10" x2="20.5" y2="10"/><line x1="17" y1="14" x2="20.5" y2="14"/>'),
    # armchair
    "furniture-home": _g(
        '<path d="M5 11V8a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v3"/>'
        '<path d="M3.5 12.5a1.8 1.8 0 0 1 3.6 0V16h9.8v-3.5a1.8 1.8 0 0 1 3.6 0V18H3.5z"/>'
        '<line x1="6" y1="18" x2="6" y2="20.5"/><line x1="18" y1="18" x2="18" y2="20.5"/>'),
    # leaf on a stem
    "outdoor-garden": _g(
        '<path d="M12 21V11"/>'
        '<path d="M12 11c0-4.4 3-7.5 8-8 .4 5.4-2.6 8.4-8 8z"/>'
        '<path d="M12 15c-3.6 0-6-2.2-6.4-6 4 .3 6.4 2.6 6.4 6z"/>'),
    # t-shirt
    "fashion-apparel": _g(
        '<path d="M8.5 3.5 5 5.2 3.5 9.5l3 1.3V20.5h11V10.8l3-1.3L19 5.2l-3.5-1.7"/>'
        '<path d="M8.5 3.5a3.5 3.5 0 0 0 7 0"/>'),
    # heart
    "health-wellness": _g(
        '<path d="M12 20.2 4.6 13a4.6 4.6 0 0 1 6.5-6.5l.9.9.9-.9A4.6 4.6 0 0 1 19.4 13z"/>'),
    # dumbbell
    "sports-fitness": _g(
        '<line x1="9" y1="12" x2="15" y2="12"/>'
        '<rect x="4.5" y="8.5" width="4" height="7" rx="1.2"/>'
        '<rect x="15.5" y="8.5" width="4" height="7" rx="1.2"/>'
        '<line x1="2.5" y1="10.5" x2="2.5" y2="13.5"/>'
        '<line x1="21.5" y1="10.5" x2="21.5" y2="13.5"/>'),
    # hex nut with bolt
    "industrial-b2b": _g(
        '<path d="M12 3.2 19 7.1v7.8L12 18.8 5 14.9V7.1z"/>'
        '<circle cx="12" cy="11" r="3.2"/>'),
}
