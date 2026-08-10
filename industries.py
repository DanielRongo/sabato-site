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
from industry_data_it import INDUSTRIES_IT
from industry_icons import ICONS

# EN slug -> IT slug, for hreflang and the language switch
IT_BY_EN = {d["en"]: slug for slug, d in INDUSTRIES_IT.items()}
EN_BY_IT = {slug: d["en"] for slug, d in INDUSTRIES_IT.items()}

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
# SVG category scenes - flat, geometric, palette only. Written as code so they
# scale, restyle from tokens and weigh a few KB. No raster, no photography.
# --------------------------------------------------------------------------
# One layout law across all nine: the situation on the left, the resolved answer
# in a dark card on the right, so the family reads as one system. Each scene is
# a format string plus a per-language string table - the Italian pages used to
# render "single floor" and "climate zone E" in English because scene() had no
# idea what language it was drawing for.
BG   = "rgb(249,250,253)"     # matches --off on these pages; was cream
INK  = "rgb(18,10,11)"
LIME = "rgb(204,255,0)"
LINE = "rgb(227,226,226)"

SCENES = {

# A real floorplan, not a rectangle: walls drawn with thickness, a window
# opening, a door with its swing, dimensions with ticks. Sizing is in BTU
# because that is how split units are sold - a "9 kW split" is not a thing on a
# price list, a 9,000 BTU one is.
"hvac": {
  "alt": {"en": "A room measured and matched to a split unit in BTU",
          "it": "Una stanza misurata e abbinata a uno split in BTU"},
  "label": {"en": "SIZED AT", "it": "DIMENSIONATO"},
  "big": "12 000 BTU",
  "notes": {"en": ["climate zone E", "one exterior wall"],
            "it": ["zona climatica E", "una parete esterna"]},
  "t": {"en": {"area": "35 m&#178;", "ceil": "ceiling 2.7 m", "w": "7.0 m", "h": "5.0 m"},
        "it": {"area": "35 m&#178;", "ceil": "altezza 2,7 m", "w": "7,0 m", "h": "5,0 m"}},
  "svg": '''
  <path d="M56 78 h190 v148 h-190 z" fill="none" stroke="{ink}" stroke-width="9"/>
  <path d="M56 78 h190 v148 h-190 z" fill="none" stroke="{bg}" stroke-width="3"/>
  <line x1="132" y1="78" x2="182" y2="78" stroke="{bg}" stroke-width="11"/>
  <line x1="132" y1="78" x2="182" y2="78" stroke="{ink}" stroke-width="2"/>
  <line x1="56" y1="186" x2="56" y2="226" stroke="{bg}" stroke-width="11"/>
  <path d="M60 186 a40 40 0 0 1 40 40" fill="none" stroke="{ink}" stroke-width="2" opacity=".5"/>
  <line x1="60" y1="186" x2="60" y2="226" stroke="{ink}" stroke-width="3"/>
  <text x="104" y="140" class="s-b">{area}</text>
  <text x="104" y="160" class="s-s">{ceil}</text>
  <line x1="56" y1="248" x2="246" y2="248" stroke="{ink}" stroke-width="1.5"/>
  <line x1="56" y1="243" x2="56" y2="253" stroke="{ink}" stroke-width="1.5"/>
  <line x1="246" y1="243" x2="246" y2="253" stroke="{ink}" stroke-width="1.5"/>
  <text x="151" y="268" class="s-s" text-anchor="middle">{w}</text>
  <rect x="300" y="88" width="150" height="42" rx="10" fill="{ink}"/>
  <rect x="316" y="102" width="118" height="4" rx="2" fill="{lime}"/>
  <rect x="316" y="114" width="70" height="3" rx="1.5" fill="rgba(248,244,241,.35)"/>
  <path d="M310 150 q40 26 80 0" fill="none" stroke="{lime}" stroke-width="4" stroke-linecap="round"/>
  <path d="M330 180 q40 26 80 0" fill="none" stroke="{lime}" stroke-width="4" stroke-linecap="round" opacity=".6"/>
  <path d="M350 210 q40 26 80 0" fill="none" stroke="{lime}" stroke-width="4" stroke-linecap="round" opacity=".3"/>''',
},

# A plate that reads as a plate: UK rear proportions, black on yellow, the blue
# band, real character spacing. The old one was a rounded rectangle with a tab.
"auto": {
  "alt": {"en": "A registration plate decoded to the correct brake disc",
          "it": "Una targa decodificata nel disco freno corretto"},
  "label": {"en": "FITS", "it": "CORRISPONDE"},
  "big": "312 mm",
  "notes": {"en": ["vented front disc", "not the 288"],
            "it": ["anteriore ventilato", "non il 288"]},
  "t": {"en": {"veh": "2016 Golf 2.0 TDI &#183; built 03/2016", "note": "post-facelift"},
        "it": {"veh": "Golf 2.0 TDI 2016 &#183; imm. 03/2016", "note": "post-restyling"}},
  "svg": '''
  <rect x="46" y="92" width="252" height="58" rx="7" fill="rgb(252,209,22)" stroke="{ink}" stroke-width="2.5"/>
  <path d="M53 92 h23 v58 h-23 a7 7 0 0 1 -7 -7 v-44 a7 7 0 0 1 7 -7z" fill="rgb(0,51,153)"/>
  <text x="61" y="128" text-anchor="middle" font-family="Satoshi,sans-serif" font-size="12" font-weight="700" fill="#fff">UK</text>
  <text x="92" y="136" font-family="Satoshi,sans-serif" font-size="30" font-weight="900" letter-spacing="2.5" fill="rgb(12,12,12)">BD16 ZKP</text>
  <text x="46" y="178" class="s-s">{veh}</text>
  <text x="46" y="200" class="s-s">{note}</text>
  <circle cx="372" cy="150" r="64" fill="none" stroke="{ink}" stroke-width="4"/>
  <circle cx="372" cy="150" r="47" fill="none" stroke="{ink}" stroke-width="1.5" opacity=".4"/>
  <circle cx="372" cy="150" r="22" fill="{ink}"/>
  <circle cx="372" cy="104" r="5" fill="{lime}"/><circle cx="372" cy="196" r="5" fill="{lime}"/>
  <circle cx="326" cy="150" r="5" fill="{lime}"/><circle cx="418" cy="150" r="5" fill="{lime}"/>
  <line x1="372" y1="88" x2="372" y2="100" stroke="{ink}" stroke-width="1.5" opacity=".45"/>
  <line x1="406" y1="116" x2="414" y2="108" stroke="{ink}" stroke-width="1.5" opacity=".45"/>
  <line x1="338" y1="116" x2="330" y2="108" stroke="{ink}" stroke-width="1.5" opacity=".45"/>''',
},

# The old version answered a question nobody had asked. The question is now
# written into the drawing.
"electronics": {
  "alt": {"en": "A monitor checked against a laptop port, with the answer",
          "it": "Un monitor verificato con la porta del portatile, con la risposta"},
  "label": {"en": "WORKS AT", "it": "FUNZIONA A"},
  "big": "4K 60Hz",
  "notes": {"en": ["Thunderbolt cable", "charges at 96 W"],
            "it": ["cavo Thunderbolt", "ricarica a 96 W"]},
  "t": {"en": {"q": "&ldquo;will this monitor work with my laptop?&rdquo;",
               "port": "USB-C / TB4", "mon": "32&#8243; 4K"},
        "it": {"q": "&ldquo;questo monitor funziona col mio portatile?&rdquo;",
               "port": "USB-C / TB4", "mon": "32&#8243; 4K"}},
  "svg": '''
  <text x="44" y="66" class="s-q">{q}</text>
  <rect x="56" y="108" width="150" height="86" rx="6" fill="{ink}"/>
  <rect x="44" y="194" width="174" height="10" rx="5" fill="{ink}" opacity=".55"/>
  <rect x="72" y="126" width="90" height="5" rx="2.5" fill="{lime}"/>
  <rect x="72" y="140" width="58" height="5" rx="2.5" fill="rgba(248,244,241,.3)"/>
  <circle cx="206" cy="151" r="7" fill="{lime}"/>
  <text x="131" y="228" class="s-s" text-anchor="middle">{port}</text>
  <path d="M213 151 q42 0 42 -26 0 -26 42 -26" fill="none" stroke="{lime}" stroke-width="4"/>
  <rect x="300" y="76" width="152" height="98" rx="8" fill="none" stroke="{ink}" stroke-width="4"/>
  <rect x="314" y="90" width="124" height="70" rx="4" fill="{ink}" opacity=".08"/>
  <path d="M362 174 v20 h28 v-20" fill="none" stroke="{ink}" stroke-width="4"/>
  <line x1="336" y1="196" x2="416" y2="196" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>
  <text x="376" y="228" class="s-s" text-anchor="middle">{mon}</text>''',
},

# Not the staircase. The question people actually ask is whether it fits the
# room they are standing in.
"furniture": {
  "alt": {"en": "A sofa footprint placed in a living room plan",
          "it": "L&rsquo;ingombro di un divano in una pianta di soggiorno"},
  "label": {"en": "FITS", "it": "CI STA"},
  "big": "38 cm",
  "notes": {"en": ["walkway left", "delivered in two boxes"],
            "it": ["di passaggio", "consegnato in due colli"]},
  "t": {"en": {"room": "4.20 &#215; 3.60 m", "sofa": "sofa 205 &#215; 95",
               "gap": "38 cm", "tbl": "table"},
        "it": {"room": "4,20 &#215; 3,60 m", "sofa": "divano 205 &#215; 95",
               "gap": "38 cm", "tbl": "tavolino"}},
  "svg": '''
  <path d="M52 84 h230 v150 h-230 z" fill="none" stroke="{ink}" stroke-width="9"/>
  <path d="M52 84 h230 v150 h-230 z" fill="none" stroke="{bg}" stroke-width="3"/>
  <rect x="66" y="98" width="150" height="40" rx="6" fill="{ink}"/>
  <rect x="72" y="104" width="26" height="28" rx="4" fill="rgba(248,244,241,.22)"/>
  <rect x="184" y="104" width="26" height="28" rx="4" fill="rgba(248,244,241,.22)"/>
  <rect x="104" y="178" width="74" height="32" rx="5" fill="none" stroke="{ink}" stroke-width="2.5" opacity=".45"/>
  <text x="141" y="199" class="s-s" text-anchor="middle" font-size="11">{tbl}</text>
  <line x1="66" y1="148" x2="216" y2="148" stroke="{lime}" stroke-width="3"/>
  <text x="141" y="168" class="s-b" text-anchor="middle" font-size="12.5">{sofa}</text>
  <line x1="216" y1="130" x2="268" y2="130" stroke="{lime}" stroke-width="3"/>
  <line x1="216" y1="124" x2="216" y2="136" stroke="{lime}" stroke-width="3"/>
  <line x1="268" y1="124" x2="268" y2="136" stroke="{lime}" stroke-width="3"/>
  <text x="242" y="118" class="s-b" text-anchor="middle" font-size="12">{gap}</text>
  <text x="52" y="262" class="s-s">{room}</text>
  <rect x="330" y="104" width="122" height="72" rx="8" fill="{ink}"/>
  <line x1="391" y1="104" x2="391" y2="176" stroke="{lime}" stroke-width="4"/>
  <text x="330" y="198" class="s-s" font-size="11.5">2 &#215; box</text>''',
},

# Was a restock date, which answers nothing. Now the plot picks the machine.
"outdoor": {
  "alt": {"en": "A lawn measured and matched to a robot mower model",
          "it": "Un prato misurato e abbinato al modello di robot rasaerba"},
  "label": {"en": "MODEL", "it": "MODELLO"},
  "big": "1000 m&#178;",
  "notes": {"en": ["handles a 22% slope", "fits a 60 cm gate"],
            "it": ["pendenza fino al 22%", "cancello da 60 cm"]},
  "t": {"en": {"area": "800 m&#178;", "slope": "slope at rear 22%", "gate": "gate 60 cm"},
        "it": {"area": "800 m&#178;", "slope": "pendenza sul retro 22%", "gate": "cancello 60 cm"}},
  "svg": '''
  <path d="M52 96 h132 v54 h68 v84 h-200z" fill="{lime}" opacity=".14"/>
  <path d="M52 96 h132 v54 h68 v84 h-200z" fill="none" stroke="{ink}" stroke-width="3"/>
  <line x1="190" y1="112" x2="248" y2="112" stroke="{ink}" stroke-width="1.5" opacity=".4"/>
  <line x1="198" y1="126" x2="248" y2="126" stroke="{ink}" stroke-width="1.5" opacity=".4"/>
  <line x1="206" y1="140" x2="248" y2="140" stroke="{ink}" stroke-width="1.5" opacity=".4"/>
  <text x="66" y="178" class="s-b">{area}</text>
  <text x="66" y="198" class="s-s" font-size="11.5">{slope}</text>
  <line x1="112" y1="234" x2="152" y2="234" stroke="{bg}" stroke-width="7"/>
  <text x="132" y="256" class="s-s" text-anchor="middle" font-size="11.5">{gate}</text>
  <rect x="296" y="132" width="136" height="46" rx="14" fill="{ink}"/>
  <rect x="316" y="148" width="60" height="5" rx="2.5" fill="{lime}"/>
  <circle cx="322" cy="188" r="15" fill="none" stroke="{ink}" stroke-width="4"/>
  <circle cx="406" cy="188" r="15" fill="none" stroke="{ink}" stroke-width="4"/>
  <line x1="296" y1="118" x2="432" y2="118" stroke="{lime}" stroke-width="3"/>
  <line x1="296" y1="112" x2="296" y2="124" stroke="{lime}" stroke-width="3"/>
  <line x1="432" y1="112" x2="432" y2="124" stroke="{lime}" stroke-width="3"/>
  <text x="364" y="106" class="s-b" text-anchor="middle" font-size="12.5">22 cm</text>''',
},

# Composition, not parcel tracking - the thing that decides whether it comes
# back.
"fashion": {
  "alt": {"en": "Two fabric compositions compared on the properties that drive returns",
          "it": "Due composizioni a confronto sulle proprieta&#768; che generano i resi"},
  "label": {"en": "PICK", "it": "SCEGLI"},
  "big": "100% CO",
  "notes": {"en": ["pre-shrunk, true to size", "the blend runs small"],
            "it": ["pre-ristretto", "il misto veste stretto"]},
  "t": {"en": {"a": "100% cotton", "b": "65% PES / 35% CO",
               "r1": "shrinkage", "r2": "stretch", "r3": "breathable"},
        "it": {"a": "100% cotone", "b": "65% PES / 35% CO",
               "r1": "ritiro", "r2": "elasticita&#768;", "r3": "traspirante"}},
  "svg": '''
  <rect x="48" y="84" width="150" height="94" rx="10" fill="{ink}"/>
  <line x1="48" y1="108" x2="198" y2="108" stroke="rgba(248,244,241,.13)" stroke-width="1"/>
  <line x1="48" y1="131" x2="198" y2="131" stroke="rgba(248,244,241,.13)" stroke-width="1"/>
  <line x1="48" y1="154" x2="198" y2="154" stroke="rgba(248,244,241,.13)" stroke-width="1"/>
  <line x1="86" y1="84" x2="86" y2="178" stroke="rgba(248,244,241,.13)" stroke-width="1"/>
  <line x1="124" y1="84" x2="124" y2="178" stroke="rgba(248,244,241,.13)" stroke-width="1"/>
  <line x1="162" y1="84" x2="162" y2="178" stroke="rgba(248,244,241,.13)" stroke-width="1"/>
  <rect x="48" y="84" width="150" height="94" rx="10" fill="none" stroke="{lime}" stroke-width="3"/>
  <text x="48" y="200" class="s-b" font-size="12.5">{a}</text>
  <rect x="230" y="84" width="150" height="94" rx="10" fill="none" stroke="{line}" stroke-width="3"/>
  <line x1="230" y1="113" x2="380" y2="113" stroke="{line}" stroke-width="1"/>
  <line x1="230" y1="142" x2="380" y2="142" stroke="{line}" stroke-width="1"/>
  <line x1="280" y1="84" x2="280" y2="178" stroke="{line}" stroke-width="1"/>
  <line x1="330" y1="84" x2="330" y2="178" stroke="{line}" stroke-width="1"/>
  <text x="230" y="200" class="s-s" font-size="12.5">{b}</text>
  <circle cx="54" cy="228" r="5" fill="{lime}"/><text x="68" y="233" class="s-s" font-size="11.5">{r1}</text>
  <circle cx="170" cy="228" r="5" fill="{line}"/><text x="184" y="233" class="s-s" font-size="11.5">{r2}</text>
  <circle cx="286" cy="228" r="5" fill="{lime}"/><text x="300" y="233" class="s-s" font-size="11.5">{r3}</text>''',
},

# Choosing the wrong size is the expensive mistake here, not the delivery.
"sports": {
  "alt": {"en": "A rider height and inseam matched to a frame size",
          "it": "Altezza e cavallo del ciclista abbinati alla taglia del telaio"},
  "label": {"en": "FRAME", "it": "TAGLIA"},
  "big": "M &#183; 54",
  "notes": {"en": ["rider 178 cm", "inseam 81 cm"],
            "it": ["ciclista 178 cm", "cavallo 81 cm"]},
  "t": {"en": {"h": "178 cm", "ins": "inseam 81 cm", "reach": "reach 389"},
        "it": {"h": "178 cm", "ins": "cavallo 81 cm", "reach": "reach 389"}},
  "svg": '''
  <line x1="72" y1="76" x2="72" y2="242" stroke="{ink}" stroke-width="3"/>
  <line x1="64" y1="76" x2="80" y2="76" stroke="{ink}" stroke-width="3"/>
  <line x1="64" y1="242" x2="80" y2="242" stroke="{ink}" stroke-width="3"/>
  <line x1="66" y1="118" x2="78" y2="118" stroke="{ink}" stroke-width="1.5" opacity=".45"/>
  <line x1="66" y1="160" x2="78" y2="160" stroke="{ink}" stroke-width="1.5" opacity=".45"/>
  <line x1="66" y1="202" x2="78" y2="202" stroke="{ink}" stroke-width="1.5" opacity=".45"/>
  <text x="92" y="118" class="s-b">{h}</text>
  <line x1="94" y1="176" x2="94" y2="242" stroke="{lime}" stroke-width="4"/>
  <text x="108" y="214" class="s-s" font-size="11.5">{ins}</text>
  <circle cx="262" cy="204" r="34" fill="none" stroke="{ink}" stroke-width="3"/>
  <circle cx="398" cy="204" r="34" fill="none" stroke="{ink}" stroke-width="3"/>
  <path d="M262 204 L316 204 L344 138 L296 138 Z" fill="none" stroke="{ink}" stroke-width="4" stroke-linejoin="round"/>
  <path d="M316 204 L398 204" stroke="{ink}" stroke-width="4"/>
  <path d="M344 138 L398 204" stroke="{ink}" stroke-width="4"/>
  <path d="M296 138 L262 204" stroke="{ink}" stroke-width="4"/>
  <path d="M344 138 L352 122" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>
  <path d="M338 120 h26" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>
  <path d="M296 138 L288 118" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>
  <path d="M276 114 h26" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>
  <circle cx="316" cy="204" r="6" fill="{lime}"/>
  <circle cx="344" cy="138" r="5" fill="{lime}"/>''',
},

# A quote request, start to finish.
"industrial": {
  "alt": {"en": "A quote request read back with contract pricing applied",
          "it": "Una richiesta di preventivo con prezzo contrattuale applicato"},
  "label": {"en": "QUOTE IN", "it": "PREVENTIVO IN"},
  "big": "2 h",
  "notes": {"en": ["contract price applied", "PDF to purchasing"],
            "it": ["prezzo contrattuale", "PDF all&rsquo;ufficio acquisti"]},
  "t": {"en": {"head": "RFQ &#183; Harlow Engineering", "l1": "M10 &#215; 40 A4-316",
               "q1": "2 000", "l2": "Washer A4 M10", "q2": "4 000",
               "foot": "delivery to site &#183; week 34"},
        "it": {"head": "RdO &#183; Harlow Engineering", "l1": "M10 &#215; 40 A4-316",
               "q1": "2 000", "l2": "Rondella A4 M10", "q2": "4 000",
               "foot": "consegna in cantiere &#183; settimana 34"}},
  "svg": '''
  <rect x="48" y="70" width="230" height="168" rx="10" fill="#fff" stroke="{ink}" stroke-width="3"/>
  <path d="M58 70 h210 a10 10 0 0 1 10 10 v24 h-230 v-24 a10 10 0 0 1 10 -10z" fill="{ink}"/>
  <text x="64" y="94" font-family="Satoshi,sans-serif" font-size="12" font-weight="700" fill="rgba(248,244,241,.9)">{head}</text>
  <text x="64" y="136" class="s-s" font-size="12">{l1}</text>
  <text x="262" y="136" class="s-b" font-size="12" text-anchor="end">{q1}</text>
  <line x1="64" y1="148" x2="262" y2="148" stroke="{line}" stroke-width="1"/>
  <text x="64" y="172" class="s-s" font-size="12">{l2}</text>
  <text x="262" y="172" class="s-b" font-size="12" text-anchor="end">{q2}</text>
  <line x1="64" y1="184" x2="262" y2="184" stroke="{line}" stroke-width="1"/>
  <text x="64" y="208" class="s-s" font-size="11">{foot}</text>
  <rect x="64" y="216" width="88" height="8" rx="4" fill="{lime}"/>
  <path d="M300 154 h50" stroke="{ink}" stroke-width="3"/>
  <path d="M342 144 l12 10 -12 10" fill="none" stroke="{ink}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="372" y="104" width="96" height="100" rx="8" fill="{ink}"/>
  <rect x="388" y="126" width="64" height="5" rx="2.5" fill="{lime}"/>
  <rect x="388" y="142" width="44" height="4" rx="2" fill="rgba(248,244,241,.32)"/>
  <rect x="388" y="156" width="54" height="4" rx="2" fill="rgba(248,244,241,.32)"/>
  <rect x="388" y="174" width="30" height="8" rx="4" fill="{lime}"/>''',
},

# Unchanged drawing - not flagged - but now bilingual and on grey.
"health": {
  "alt": {"en": "A subscription schedule with one delivery skipped",
          "it": "Un abbonamento con una consegna saltata"},
  "label": {"en": "NEXT CHARGE", "it": "PROSSIMO"},
  "big": "3rd",
  "notes": {"en": ["one skipped", "new address saved"],
            "it": ["una saltata", "nuovo indirizzo salvato"]},
  "t": {"en": {"a": "sent", "b": "skipped", "c": "next"},
        "it": {"a": "inviata", "b": "saltata", "c": "prossima"}},
  "svg": '''
  <rect x="44" y="76" width="196" height="164" rx="12" fill="none" stroke="{ink}" stroke-width="3"/>
  <line x1="44" y1="116" x2="240" y2="116" stroke="{ink}" stroke-width="3"/>
  <circle cx="88" cy="152" r="14" fill="{line}"/>
  <circle cx="142" cy="152" r="14" fill="none" stroke="{ink}" stroke-width="3" stroke-dasharray="4 4"/>
  <circle cx="196" cy="152" r="14" fill="{lime}"/>
  <text x="88" y="196" class="s-s" font-size="12" text-anchor="middle">{a}</text>
  <text x="142" y="196" class="s-s" font-size="12" text-anchor="middle">{b}</text>
  <text x="196" y="196" class="s-s" font-size="12" text-anchor="middle">{c}</text>
  <rect x="286" y="96" width="160" height="124" rx="12" fill="{ink}"/>
  <rect x="308" y="126" width="116" height="6" rx="3" fill="{lime}"/>
  <rect x="308" y="146" width="86" height="6" rx="3" fill="rgba(248,244,241,.32)"/>
  <rect x="308" y="166" width="100" height="6" rx="3" fill="rgba(248,244,241,.32)"/>''',
},
}


def scene(kind, lang="en"):
    """Flat geometric SVG per category, in the language of the page.

    scene() used to take no language at all, so every Italian industry page
    rendered "single floor", "SIZED AT" and "climate zone E" in English inside
    the graphic. The string table lives with the drawing rather than in
    industry_data*.py because the two have to line up pixel by pixel - a longer
    Italian word is a layout problem, not a content one.
    """
    s = SCENES[kind]
    t = dict(s["t"][lang], ink=INK, lime=LIME, line=LINE, bg=BG)
    body = s["svg"].format(**t)
    ns = "".join(f'<text x="524" y="{192 + i*22}" class="s-n">{n}</text>'
                 for i, n in enumerate(s["notes"][lang]))
    # The answer card is 176px wide with a 24px gutter, so 152px of room. At a
    # fixed 34px, "12 000 BTU" and "100% CO" ran straight off the edge. Sized
    # from the visible glyph count - an entity is one character, not six.
    plain = re.sub(r"&[#a-zA-Z0-9]+;", "x", s["big"])
    big_size = 34 if len(plain) <= 6 else 28 if len(plain) <= 8 else 23 if len(plain) <= 11 else 19
    return (f'<svg class="scene" viewBox="0 0 720 300" role="img" '
            f'aria-label="{s["alt"][lang]}">'
            '<style>.s-b{font-family:Satoshi,sans-serif;font-size:15px;font-weight:700;fill:'
            + INK + '}'
            '.s-s{font-family:Satoshi,sans-serif;font-size:12px;fill:rgb(69,65,64)}'
            '.s-q{font-family:Satoshi,sans-serif;font-size:13.5px;font-style:italic;fill:rgb(69,65,64)}'
            '.s-n{font-family:Satoshi,sans-serif;font-size:13px;fill:rgba(248,244,241,.8)}</style>'
            f'<rect x="0" y="0" width="720" height="300" rx="24" fill="{BG}"/>'
            f'{body}'
            f'<rect x="500" y="60" width="176" height="180" rx="16" fill="{INK}"/>'
            f'<text x="524" y="100" font-family="Satoshi,sans-serif" font-size="12" '
            f'letter-spacing="1.6" fill="rgba(248,244,241,.55)">{s["label"][lang]}</text>'
            f'<text x="524" y="146" font-family="Satoshi,sans-serif" font-size="{big_size}" '
            f'font-weight="900" fill="{LIME}">{s["big"]}</text>'
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


def build(slug, d, lang="en"):
    d = dict(d, lang=lang)
    prefix = "/industries" if lang == "en" else "/it/settori"
    url = f"{BASE}{prefix}/{slug}"
    alt = (f"{BASE}/it/settori/{IT_BY_EN[slug]}" if lang == "en"
           else f"{BASE}/industries/{EN_BY_IT[slug]}")
    tpl_name = "industry.html" if lang == "en" else "industry-it.html"
    icon_key = slug if lang == "en" else d["en"]
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

    GLYPH = ('<svg viewBox="0 0 16 12" aria-hidden="true"><g fill="currentColor">'
             '<rect x="0" y="3.5" width="2.5" height="5" rx="1.25"/>'
             '<rect x="4.5" y="1" width="2.5" height="10" rx="1.25"/>'
             '<rect x="9" y="2.5" width="2.5" height="7" rx="1.25"/>'
             '<rect x="13.5" y="4.5" width="2.5" height="3" rx="1.25"/></g></svg>')
    SPK = {"caller": "CALLER", "agent": "AGENT"}
    if d.get("lang") == "it":
        SPK = {"caller": "CLIENTE", "agent": "AGENTE"}
    # Same markup as the use-case pages: the speaker class sits on .t-row, and
    # .t-spk holds the label plus the waveform glyph. Colour comes from their
    # CSS (.t-row.caller .t-spk / .t-row.agent .t-spk) rather than from ours.
    tr = "".join(
        f'<div class="t-row {who}"><span class="t-spk">{SPK[who]}{GLYPH}</span><p>{txt}</p></div>'
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

    tpl = open(os.path.join(ROOT, "templates", tpl_name), encoding="utf-8").read()
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
            .replace("{{BAND_COPY}}", "".join(f'<p class="qbody">{p}</p>' for p in d["band_copy"]))
            .replace("{{RANK_HEAD}}", d["rank_head"])
            .replace("{{RANK}}", rank)
            .replace("{{QUESTIONS_H2}}", d["questions_h2"])
            .replace("{{QUESTIONS_INTRO}}", d["questions_intro"])
            .replace("{{QUESTIONS}}", q_rows)
            .replace("{{WORKFLOWS}}", wf)
            .replace("{{WF_COUNT}}", str(len(d["workflows"])))
            .replace("{{SCENE}}", scene(d["scene"], lang))
            .replace("{{ICON}}", ICONS[icon_key])
            .replace("{{ALT}}", alt)
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
    out = (os.path.join(SITE, "industries", f"{slug}.html") if lang == "en"
           else os.path.join(SITE, "it", "settori", f"{slug}.html"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page)
    return out



def build_index(lang="en"):
    """Hub page at /industries. Gives the header nav item a real destination and
    a place for the nine to be crawled from, rather than nav pointing at one
    arbitrary category."""
    from industry_icons import ICONS
    src = INDUSTRIES if lang == "en" else INDUSTRIES_IT
    prefix = "/industries" if lang == "en" else "/it/settori"
    WHEN = {"en": {"before": "Calls before buying", "after": "Calls after buying",
                   "mixed": "Calls before and after"},
            "it": {"before": "Chiama prima di comprare", "after": "Chiama dopo l'acquisto",
                   "mixed": "Chiama prima e dopo"}}[lang]
    LEAD = "Leads with: " if lang == "en" else "Parte da: "
    cards = ""
    for slug in src:
        d = src[slug]
        when = WHEN[d["when"]]
        lead = d["workflows"][0][0]
        icon_key = slug if lang == "en" else d["en"]
        cards += (
            f'<a class="ix-card" href="{prefix}/{slug}">'
            f'<span class="ix-icon">{ICONS[icon_key]}</span>'
            f'<h3>{d["label"]}</h3>'
            f'<p class="ix-when">{when}</p>'
            f'<p class="ix-lead">{LEAD}{lead}</p></a>')

    tpl_name = "industry-index.html" if lang == "en" else "industry-index-it.html"
    tpl = open(os.path.join(ROOT, "templates", tpl_name), encoding="utf-8").read()
    page = tpl.replace("{{CARDS}}", cards).replace("{{CAL}}", CAL)
    out = (os.path.join(SITE, "industries", "index.html") if lang == "en"
           else os.path.join(SITE, "it", "settori", "index.html"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page)
    return out


def link_footer_industries():
    """Footer industries ship as plain <span>. Make them real links - and point
    Italian pages at Italian pages. An earlier version keyed only on the English
    label and put /industries/ hrefs onto nine Italian pages, which is a worse
    bug than leaving them unlinked."""
    it_by_label = {}
    for slug, d in INDUSTRIES_IT.items():
        for lab in [d["label"]] + d.get("alias", []):
            it_by_label[lab] = f"/it/settori/{slug}"
    en_by_label = {lab: href for lab, href in FOOTER_INDUSTRIES if href}

    touched = 0
    for dirpath, _, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, SITE).replace(os.sep, "/")
            is_it = rel == "it.html" or rel.startswith("it/")
            table = it_by_label if is_it else en_by_label
            try:
                t = open(fp, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            orig = t
            for label, href in table.items():
                t = t.replace(f"<li><span>{label}</span></li>",
                              f'<li><a href="{href}">{label}</a></li>')
            # repair any cross-language href a previous run wrote
            if is_it:
                for label, href in table.items():
                    t = re.sub(r'<li><a href="/industries/[a-z-]+">' + re.escape(label) + r'</a></li>',
                               f'<li><a href="{href}">{label}</a></li>', t)
            if t != orig:
                open(fp, "w", encoding="utf-8").write(t)
                touched += 1
    return touched


if __name__ == "__main__":
    for slug in ORDER:
        print("  wrote", os.path.relpath(build(slug, INDUSTRIES[slug], "en"), ROOT))
    for slug, d in INDUSTRIES_IT.items():
        print("  wrote", os.path.relpath(build(slug, d, "it"), ROOT))
    print("  wrote", os.path.relpath(build_index("en"), ROOT))
    print("  wrote", os.path.relpath(build_index("it"), ROOT))
    n = link_footer_industries()
    print(f"  footer: linked built industries on {n} page(s)")
