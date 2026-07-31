#!/usr/bin/env python3
"""Sabato industry landing pages.

Builds site/industries/<slug>.html from the per-industry data below, using the
same shell, tokens and class vocabulary as the use-case pages so the family
reads as one site.

    python3 industries.py

Design decisions worth knowing before editing:

* The variable across industries is WHICH WORKFLOWS DOMINATE, not the noun.
  High-consideration categories call before buying (sizing, fitment, quote);
  low-consideration categories call after (WISMO, returns, back-in-stock).
  That is what keeps nine pages from being one page, and it keeps every page
  consistent with our own published argument that nobody phones before buying
  a t-shirt.
* Every question row names the actual field that answers it. If a row could be
  copied to another industry unchanged, it does not belong on the page.
* Four CTAs, not two: hero, after the questions table, after the transcript,
  and the closing band. The transcript is the belief peak and previously had no
  door next to it.
* `proof` renders only where it is true. No invented logos, no illustrative
  customer names.
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
BASE = "https://www.sabato.ai"
CAL = "https://cal.com/sabatoai/intro"

# --------------------------------------------------------------------------
# Per-industry content. Everything category-specific lives here.
# --------------------------------------------------------------------------
from industry_data import INDUSTRIES
from industry_icons import ICONS

ORDER = list(INDUSTRIES.keys())

FOOTER_INDUSTRIES = [
    ("Home Improvement", "/industries/home-improvement"),
    ("Automotive &amp; Parts", "/industries/automotive-parts"),
    ("Electronics &amp; Tech", "/industries/electronics-tech"),
    ("Furniture &amp; Home", "/industries/furniture-home"),
    ("Outdoor &amp; Garden", "/industries/outdoor-garden"),
    ("Fashion &amp; Apparel", "/industries/fashion-apparel"),
    ("Health &amp; Wellness", "/industries/health-wellness"),
    ("Sports &amp; Fitness", "/industries/sports-fitness"),
    ("Industrial &amp; B2B", "/industries/industrial-b2b"),
]


# --------------------------------------------------------------------------
# SVG category scenes — flat, geometric, palette only. Written as code so they
# scale, restyle from tokens and weigh a few KB. No raster, no photography.
# --------------------------------------------------------------------------
SCENES = {
"hvac": ("A wall-mounted unit sized against a floor plan and a climate zone",
  '''<rect x="44" y="60" width="200" height="180" rx="8" fill="none" stroke="rgb(18,10,11)" stroke-width="3"/>
  <line x1="44" y1="150" x2="150" y2="150" stroke="rgb(18,10,11)" stroke-width="3"/>
  <line x1="150" y1="150" x2="150" y2="240" stroke="rgb(18,10,11)" stroke-width="3"/>
  <text x="60" y="98" class="s-b">120 m&#178;</text><text x="60" y="120" class="s-s">single floor</text>
  <rect x="300" y="76" width="150" height="46" rx="10" fill="rgb(18,10,11)"/>
  <rect x="316" y="92" width="118" height="4" rx="2" fill="rgb(204,255,0)"/>
  <path d="M310 140 q40 26 80 0" fill="none" stroke="rgb(204,255,0)" stroke-width="4" stroke-linecap="round"/>
  <path d="M330 170 q40 26 80 0" fill="none" stroke="rgb(204,255,0)" stroke-width="4" stroke-linecap="round" opacity=".6"/>
  <path d="M350 200 q40 26 80 0" fill="none" stroke="rgb(204,255,0)" stroke-width="4" stroke-linecap="round" opacity=".3"/>''',
  "SIZED AT", "12 kW", ["climate zone E", "ceiling 2.7 m"]),

"auto": ("A vehicle registration decoded to the correct brake disc",
  '''<rect x="44" y="86" width="196" height="58" rx="10" fill="none" stroke="rgb(18,10,11)" stroke-width="3"/>
  <rect x="44" y="86" width="34" height="58" rx="10" fill="rgb(0,153,255)"/>
  <text x="96" y="126" class="s-b" font-size="24">BD16 ZKP</text>
  <text x="44" y="176" class="s-s">2016 Golf 2.0 TDI &#183; built 03/2016</text>
  <text x="44" y="200" class="s-s">post-facelift</text>
  <circle cx="368" cy="150" r="62" fill="none" stroke="rgb(18,10,11)" stroke-width="4"/>
  <circle cx="368" cy="150" r="22" fill="rgb(18,10,11)"/>
  <circle cx="368" cy="106" r="5" fill="rgb(204,255,0)"/><circle cx="368" cy="194" r="5" fill="rgb(204,255,0)"/>
  <circle cx="324" cy="150" r="5" fill="rgb(204,255,0)"/><circle cx="412" cy="150" r="5" fill="rgb(204,255,0)"/>''',
  "FITS", "312 mm", ["vented front disc", "not the 288"]),

"electronics": ("Two display outputs compared against a laptop port specification",
  '''<rect x="44" y="72" width="210" height="130" rx="10" fill="rgb(18,10,11)"/>
  <rect x="44" y="202" width="210" height="12" rx="4" fill="rgb(18,10,11)" opacity=".55"/>
  <rect x="62" y="90" width="120" height="6" rx="3" fill="rgb(204,255,0)"/>
  <rect x="62" y="106" width="80" height="6" rx="3" fill="rgba(248,244,241,.3)"/>
  <line x1="266" y1="138" x2="336" y2="138" stroke="rgb(204,255,0)" stroke-width="4"/>
  <line x1="266" y1="170" x2="336" y2="170" stroke="rgb(227,226,226)" stroke-width="4"/>
  <rect x="344" y="96" width="112" height="70" rx="8" fill="none" stroke="rgb(18,10,11)" stroke-width="3"/>
  <text x="352" y="138" class="s-b" font-size="17">4K 60Hz</text>
  <rect x="344" y="182" width="112" height="70" rx="8" fill="none" stroke="rgb(227,226,226)" stroke-width="3"/>
  <text x="352" y="224" class="s-s" font-size="17">4K 30Hz</text>''',
  "REQUIRES", "TB4", ["two 4K at 60 Hz", "96 W passthrough"]),

"furniture": ("A packed sofa measured against a doorway and a turning staircase",
  '''<path d="M60 236 V96 h70 v40 h-40 v100" fill="none" stroke="rgb(18,10,11)" stroke-width="3"/>
  <path d="M130 136 h64 v100" fill="none" stroke="rgb(227,226,226)" stroke-width="3"/>
  <text x="60" y="76" class="s-s">landing turn</text>
  <rect x="250" y="126" width="196" height="76" rx="8" fill="rgb(18,10,11)"/>
  <line x1="348" y1="126" x2="348" y2="202" stroke="rgb(204,255,0)" stroke-width="4"/>
  <text x="250" y="228" class="s-s">packed &#183; 2 boxes &#183; legs separate</text>
  <line x1="250" y1="112" x2="446" y2="112" stroke="rgb(204,255,0)" stroke-width="3"/>
  <text x="250" y="102" class="s-b" font-size="14">205 cm</text>''',
  "FITS", "205 cm", ["two boxes", "legs detach"]),

"industrial": ("A trade account recognised, with contract pricing at a quantity break",
  '''<path d="M116 62 176 96 v68 l-60 34 -60 -34 V96z" fill="none" stroke="rgb(18,10,11)" stroke-width="4"/>
  <circle cx="116" cy="130" r="24" fill="rgb(18,10,11)"/>
  <text x="44" y="234" class="s-s">M10 &#215; 40 &#183; A4-316</text>
  <rect x="230" y="76" width="216" height="52" rx="8" fill="none" stroke="rgb(227,226,226)" stroke-width="2"/>
  <text x="248" y="108" class="s-s" font-size="15">1&#8211;99 &#183; &#163;1.18</text>
  <rect x="230" y="140" width="216" height="52" rx="8" fill="rgb(204,255,0)"/>
  <text x="248" y="172" class="s-b" font-size="15">200+ &#183; &#163;0.94</text>
  <text x="230" y="222" class="s-s">Harlow Engineering &#183; contract price</text>''',
  "CERTIFIED", "3.1", ["EN 10204", "batch document"]),

"outdoor": ("A plot area matched to a cutting width, with a restock date pending",
  '''<path d="M52 210 h180 v-56 h-60 v-44 h-120z" fill="none" stroke="rgb(18,10,11)" stroke-width="3"/>
  <text x="70" y="184" class="s-b">800 m&#178;</text>
  <text x="70" y="206" class="s-s">slope at rear</text>
  <rect x="278" y="128" width="150" height="54" rx="10" fill="rgb(18,10,11)"/>
  <circle cx="308" cy="192" r="16" fill="none" stroke="rgb(18,10,11)" stroke-width="4"/>
  <circle cx="398" cy="192" r="16" fill="none" stroke="rgb(18,10,11)" stroke-width="4"/>
  <line x1="278" y1="112" x2="428" y2="112" stroke="rgb(204,255,0)" stroke-width="3"/>
  <text x="278" y="102" class="s-b" font-size="14">46 cm</text>''',
  "RESTOCK", "18th", ["sit-on mower", "callback booked"]),

"health": ("A subscription schedule with one delivery skipped",
  '''<rect x="44" y="76" width="196" height="164" rx="12" fill="none" stroke="rgb(18,10,11)" stroke-width="3"/>
  <line x1="44" y1="116" x2="240" y2="116" stroke="rgb(18,10,11)" stroke-width="3"/>
  <circle cx="88" cy="152" r="14" fill="rgb(227,226,226)"/>
  <circle cx="142" cy="152" r="14" fill="none" stroke="rgb(18,10,11)" stroke-width="3" stroke-dasharray="4 4"/>
  <circle cx="196" cy="152" r="14" fill="rgb(204,255,0)"/>
  <text x="74" y="196" class="s-s" font-size="12">sent</text>
  <text x="122" y="196" class="s-s" font-size="12">skipped</text>
  <text x="176" y="196" class="s-s" font-size="12">next</text>
  <rect x="286" y="96" width="160" height="124" rx="12" fill="rgb(18,10,11)"/>
  <rect x="308" y="126" width="116" height="6" rx="3" fill="rgb(204,255,0)"/>
  <rect x="308" y="146" width="86" height="6" rx="3" fill="rgba(248,244,241,.32)"/>
  <rect x="308" y="166" width="100" height="6" rx="3" fill="rgba(248,244,241,.32)"/>''',
  "NEXT CHARGE", "3rd", ["one skipped", "new address saved"]),

"sports": ("A packed rower measured for a doorway and a two-person carry",
  '''<rect x="44" y="132" width="216" height="46" rx="8" fill="rgb(18,10,11)"/>
  <line x1="44" y1="116" x2="260" y2="116" stroke="rgb(204,255,0)" stroke-width="3"/>
  <text x="44" y="106" class="s-b" font-size="14">218 cm packed</text>
  <text x="44" y="206" class="s-s">44 kg &#183; one box</text>
  <path d="M320 96 v140" stroke="rgb(18,10,11)" stroke-width="3"/>
  <path d="M420 96 v140" stroke="rgb(18,10,11)" stroke-width="3"/>
  <text x="330" y="86" class="s-s" font-size="12">standard doorway</text>
  <circle cx="352" cy="166" r="13" fill="rgb(204,255,0)"/><circle cx="390" cy="166" r="13" fill="rgb(204,255,0)"/>''',
  "DELIVERY", "2-person", ["room of choice", "assembly added"]),

"fashion": ("A parcel tracked through carrier events to a pickup point",
  '''<rect x="48" y="96" width="120" height="100" rx="10" fill="rgb(18,10,11)"/>
  <line x1="108" y1="96" x2="108" y2="196" stroke="rgb(204,255,0)" stroke-width="5"/>
  <line x1="188" y1="146" x2="470" y2="146" stroke="rgb(227,226,226)" stroke-width="4"/>
  <line x1="188" y1="146" x2="386" y2="146" stroke="rgb(204,255,0)" stroke-width="4"/>
  <circle cx="188" cy="146" r="11" fill="rgb(204,255,0)"/>
  <circle cx="287" cy="146" r="11" fill="rgb(204,255,0)"/>
  <circle cx="386" cy="146" r="11" fill="rgb(204,255,0)"/>
  <circle cx="470" cy="146" r="11" fill="none" stroke="rgb(18,10,11)" stroke-width="3" stroke-dasharray="4 4"/>
  <text x="176" y="186" class="s-s" font-size="11">picked</text>
  <text x="262" y="186" class="s-s" font-size="11">in transit</text>
  <text x="348" y="186" class="s-b" font-size="11">held at depot</text>
  <text x="446" y="186" class="s-s" font-size="11">pickup</text>''',
  "REROUTED", "400 m", ["pickup point", "code sent by text"]),
}


def scene(kind):
    """Flat geometric SVG per category. One layout law across all nine: the
    situation on the left, the resolved answer in a dark card on the right —
    so the family reads as one system rather than nine separate drawings."""
    alt, body, lbl, big, notes = SCENES[kind]
    ns = "".join(
        f'<text x="524" y="{192 + i*22}" class="s-n">{n}</text>'
        for i, n in enumerate(notes))
    return (f'<svg class="scene" viewBox="0 0 720 300" role="img" aria-label="{alt}">'
            '<style>.s-b{font-family:Satoshi,sans-serif;font-size:15px;font-weight:700;fill:rgb(18,10,11)}'
            '.s-s{font-family:Satoshi,sans-serif;font-size:12px;fill:rgb(69,65,64)}'
            '.s-n{font-family:Satoshi,sans-serif;font-size:13px;fill:rgba(248,244,241,.8)}</style>'
            '<rect x="0" y="0" width="720" height="300" rx="24" fill="rgb(248,244,241)"/>'
            f'{body}'
            '<rect x="500" y="60" width="176" height="180" rx="16" fill="rgb(18,10,11)"/>'
            f'<text x="524" y="100" font-family="Satoshi,sans-serif" font-size="12" letter-spacing="1.6" fill="rgba(248,244,241,.55)">{lbl}</text>'
            f'<text x="524" y="146" font-family="Satoshi,sans-serif" font-size="38" font-weight="900" fill="rgb(204,255,0)">{big}</text>'
            '<line x1="524" y1="166" x2="652" y2="166" stroke="rgba(248,244,241,.18)" stroke-width="1"/>'
            f'{ns}</svg>')


def wave(n=26, dark=True):
    """The lime waveform glyph used across the site as the voice signature."""
    hs = [10, 22, 34, 18, 40, 14, 28, 44, 20, 36, 12, 30, 42, 16, 26, 38, 22, 34, 12, 28, 40, 18, 24, 32, 14, 20]
    out = []
    for i in range(n):
        h = hs[i % len(hs)]
        out.append(f'<rect x="{i*13}" y="{(48-h)//2}" width="5" height="{h}" rx="2.5" '
                   f'fill="{"rgb(204,255,0)" if i % 3 else "rgba(204,255,0,.45)"}"/>')
    return f'<svg class="wave" viewBox="0 0 {n*13} 48" aria-hidden="true">{"".join(out)}</svg>'


def build(slug, d):
    url = f"{BASE}/industries/{slug}"
    q_rows = "".join(
        f'<div class="q-row"><p class="q-ask">{q}</p>'
        f'<div class="q-ans"><p>{a}</p><code>{f_}</code></div></div>'
        for q, a, f_ in d["questions"])

    wf = "".join(
        f'<a class="wf-card" href="{href}"><span class="wf-n">{i:02d}</span>'
        f'<span class="wf-arrow" aria-hidden="true">&rarr;</span>'
        f'<h3>{name}</h3><p>{desc}</p></a>'
        for i, (name, desc, href) in enumerate(d["workflows"], 1))

    rank = "".join(
        f'<li><span class="r-n">{i}</span><span class="r-t">{t}</span></li>'
        for i, t in enumerate(d["rank"], 1))

    tr = "".join(
        f'<div class="t-row"><span class="t-spk {who}">{wave(4)}<b>{who.upper()}</b></span><p>{txt}</p></div>'
        for who, txt in d["transcript"])

    data_rows = "".join(
        f'<div class="d-row"><h3>{k}</h3><p>{v}</p></div>' for k, v in d["data_rows"])

    faq = "".join(
        f'<div class="faq-item"><p class="faq-q">{q}</p><p class="faq-a">{a}</p></div>'
        for q, a in d["faq"])

    meta = "".join(f'<div class="cm-row"><span>{k}</span><b>{v}</b></div>'
                   for k, v in d["call_meta"])

    proof = (f'<p class="proof"><span class="proof-dot"></span>{d["proof"]}</p>'
             if d.get("proof") else "")

    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": re.sub("<[^>]+>", "", html.unescape(q)),
                        "acceptedAnswer": {"@type": "Answer",
                                           "text": re.sub("<[^>]+>", "", html.unescape(a))}}
                       for q, a in d["faq"]],
    }
    import json
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Industries", "item": f"{BASE}/industries"},
        {"@type": "ListItem", "position": 3, "name": re.sub("<[^>]+>", "", html.unescape(d["label"])), "item": url},
    ]}

    tpl = open(os.path.join(ROOT, "templates", "industry.html"), encoding="utf-8").read()
    page = (tpl
            .replace("{{TITLE}}", d["title"])
            .replace("{{DESCRIPTION}}", d["description"])
            .replace("{{URL}}", url)
            .replace("{{LABEL}}", d["label"])
            .replace("{{H1}}", d["h1"])
            .replace("{{SUB}}", d["sub"])
            .replace("{{HAND}}", d["hand"])
            .replace("{{CALL_Q}}", d["call_q"])
            .replace("{{CALL_META}}", meta)
            .replace("{{WAVE}}", wave(30))
            .replace("{{PROOF}}", proof)
            .replace("{{BAND_EYEBROW}}", d["band_eyebrow"])
            .replace("{{BAND_H2}}", d["band_h2"])
            .replace("{{BAND_COPY}}", "".join(f"<p>{p}</p>" for p in d["band_copy"]))
            .replace("{{RANK_HEAD}}", d["rank_head"])
            .replace("{{RANK}}", rank)
            .replace("{{QUESTIONS_H2}}", d["questions_h2"])
            .replace("{{QUESTIONS_INTRO}}", d["questions_intro"])
            .replace("{{QUESTIONS}}", q_rows)
            .replace("{{WORKFLOWS}}", wf)
            .replace("{{WF_COUNT}}", str(len(d["workflows"])))
            .replace("{{SCENE}}", scene(d["scene"]))
            .replace("{{ICON}}", ICONS[slug])
            .replace("{{TRANSCRIPT_META}}", d["transcript_meta"])
            .replace("{{TRANSCRIPT}}", tr)
            .replace("{{DATA_H2}}", d["data_h2"])
            .replace("{{DATA_COPY}}", d["data_copy"])
            .replace("{{DATA_ROWS}}", data_rows)
            .replace("{{FAQ}}", faq)
            .replace("{{CTA_H2}}", d["cta_h2"])
            .replace("{{CTA_SUB}}", d["cta_sub"])
            .replace("{{CTA_HAND}}", d["cta_hand"])
            .replace("{{CAL}}", CAL)
            .replace("{{FAQ_LD}}", json.dumps(faq_ld, ensure_ascii=False))
            .replace("{{BC_LD}}", json.dumps(bc_ld, ensure_ascii=False))
            )
    out = os.path.join(SITE, "industries", f"{slug}.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page)
    return out



def build_index():
    """Hub page at /industries. Gives the header nav item a real destination and
    a place for the nine to be crawled from, rather than nav pointing at one
    arbitrary category."""
    from industry_icons import ICONS
    cards = ""
    for slug in ORDER:
        d = INDUSTRIES[slug]
        when = {"before": "Calls before buying",
                "after": "Calls after buying",
                "mixed": "Calls before and after"}[d["when"]]
        lead = d["workflows"][0][0]
        cards += (
            f'<a class="ix-card" href="/industries/{slug}">'
            f'<span class="ix-icon">{ICONS[slug]}</span>'
            f'<h3>{d["label"]}</h3>'
            f'<p class="ix-when">{when}</p>'
            f'<p class="ix-lead">Leads with: {lead}</p></a>')

    tpl = open(os.path.join(ROOT, "templates", "industry-index.html"), encoding="utf-8").read()
    page = tpl.replace("{{CARDS}}", cards).replace("{{CAL}}", CAL)
    out = os.path.join(SITE, "industries", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page)
    return out


def link_footer_industries():
    """Footer industries ship as plain <span>. Make the built ones real links."""
    touched = 0
    for dirpath, _, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                t = open(fp, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            orig = t
            for label, href in FOOTER_INDUSTRIES:
                if not href:
                    continue
                t = t.replace(f"<li><span>{label}</span></li>",
                              f'<li><a href="{href}">{label}</a></li>')
            if t != orig:
                open(fp, "w", encoding="utf-8").write(t)
                touched += 1
    return touched


if __name__ == "__main__":
    for slug in ORDER:
        print("  wrote", os.path.relpath(build(slug, INDUSTRIES[slug]), ROOT))
    print("  wrote", os.path.relpath(build_index(), ROOT))
    n = link_footer_industries()
    print(f"  footer: linked built industries on {n} page(s)")
