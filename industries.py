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
INDUSTRIES = {
    "home-improvement": {
        "label": "Home Improvement / HVAC",
        "nav_label": "Home Improvement",
        "when": "before",
        "title": "Voice AI for HVAC &amp; Home Improvement E-Commerce | Sabato AI",
        "description": "A managed voice agent that sizes the unit, checks the climate zone and books the site visit — from your own kW tables and ERP. Live in two weeks.",
        "h1": "Heating and cooling buyers phone before they buy.",
        "sub": "Sabato's managed voice agent sizes the unit, checks the climate zone, says what the installation actually includes — and books the site visit while the caller is still interested.",
        "hand": "in this category the call is the configurator",
        "call_q": "&ldquo;I&rsquo;ve got 120 m&sup2; on one floor just outside Milan — is the 9 kW split the right one?&rdquo;",
        "call_meta": [("Detected intent", "Sizing + installation"),
                      ("Data pulled", "kW table &middot; climate zone E"),
                      ("Outcome", "Site visit booked")],
        "band_eyebrow": "Why this category phones",
        "band_h2": "A heat pump is a specification decision made by someone who doesn&rsquo;t have the specification.",
        "band_copy": [
            "Nobody buys 12 kW. They buy a house: 120 m&sup2;, built in 1978, single floor, radiators they&rsquo;d rather keep, a postcode with a specific winter design temperature. The product page cannot answer that, so the buyer either phones or leaves.",
            "That call is not support. It is the last step of the sale, and it lands during working hours on a line that is usually already busy with an installer asking about a delivery.",
        ],
        "rank_head": "What the inbound calls are about",
        "rank": ["Which unit for my space (sizing)",
                 "Installation: included, who, when",
                 "Price, discount, quote for a full system",
                 "Incentives and certification documents",
                 "Delivery timing and where the order is"],
        "questions_h2": "Six questions an HVAC line hears every day — and what has to be true in your systems to answer them",
        "questions_intro": "An agent is only as good as what it can read. These are the pairings that matter in heating and cooling: each question resolves against a specific field, not against a general knowledge of HVAC.",
        "questions": [
            ("&ldquo;Which unit do I need for 120 m&sup2; on one floor?&rdquo;",
             "kW/BTU sizing table crossed with the climate zone for the caller&rsquo;s postcode and the declared ceiling height.",
             "product.heating_capacity_kw &middot; zone.design_temp"),
            ("&ldquo;Is installation included, and who does it?&rdquo;",
             "Installer coverage by postcode plus the installation service SKU and its current lead time.",
             "installers.by_cap &middot; sku.INSTALL_STD"),
            ("&ldquo;Will it work with the radiators I already have?&rdquo;",
             "Maximum flow temperature on the unit against the emitter type the caller describes; hands over to a human when the answer is borderline.",
             "product.max_flow_temp_c"),
            ("&ldquo;Does this model qualify for the incentive scheme?&rdquo;",
             "ErP energy class and SCOP value from the certification documents held in the DAM, sent by email as the PDF itself.",
             "docs.erp_class &middot; docs.scop"),
            ("&ldquo;If I order today, when does it arrive?&rdquo;",
             "Available-to-promise in the ERP, plus the supplier lead time when the item is not in the warehouse.",
             "erp.atp &middot; supplier.lead_days"),
            ("&ldquo;Where is the rest of my installation kit?&rdquo;",
             "Carrier tracking events on the parent order, split shipments reconciled into one answer.",
             "carrier.events &middot; order.shipments[]"),
        ],
        "workflows": [
            ("Pre-sales consultation", "Sizing, compatibility, what&rsquo;s in the box. The call that decides the sale.", "/use-cases/pre-sales-consultation"),
            ("Qualify &amp; collect for quote", "Full-system enquiries captured with the fields an installer quote actually needs.", "/use-cases/qualify-and-collect-for-quote"),
            ("Where is my order", "Split shipments and installation kits, reconciled into one spoken answer.", "/use-cases/where-is-my-order"),
            ("Checkout summary via text", "Confirming a four-line order with an install slot before the card is charged.", "/use-cases/checkout-summary-via-text"),
        ],
        "transcript_meta": "Inbound &middot; 2 min 41 s &middot; language: Italian, translated here &middot; outcome: site check booked",
        "transcript": [
            ("caller", "Hi — I&rsquo;m looking at the 9 kW split on your site. I&rsquo;ve got about 120 square metres, all on one floor, just outside Milan. Is that the right one?"),
            ("agent", "Let me check the sizing table. 120 square metres on one floor, climate zone E — for cooling you&rsquo;re at roughly eleven to twelve kilowatts, so the 9 kW would be running flat out in August. The 12 kW is the safer fit. Is the ceiling height standard, around 2.7 metres?"),
            ("caller", "Yes, standard. Nothing unusual."),
            ("agent", "Then the 12 kW. One thing to know before you order: it needs a dedicated sixteen-amp line. If you&rsquo;re not sure you have one, the installer checks that on the site visit."),
            ("caller", "That&rsquo;s the other thing — is the installation you, or do I find someone myself?"),
            ("agent", "Three certified installers cover your postcode. Installation is quoted separately after the site check, and the site check is free and takes about twenty minutes."),
            ("caller", "And does it qualify for the incentive?"),
            ("agent", "This one is ErP class A+++ with an SCOP of 4.6, so yes. I&rsquo;ll email you the certification PDF and the two nearest installers. Shall I book the site check now?"),
            ("caller", "Yes, go ahead."),
        ],
        "data_h2": "The data reality behind an HVAC answer",
        "data_copy": "Every answer on this page depends on a field somebody has to maintain. Where a field is missing we say so on the call and hand over — we do not let the agent reason its way to a kilowatt figure.",
        "data_rows": [
            ("kW / BTU sizing tables", "Per model, with the assumptions stated: floor area, ceiling height, insulation class."),
            ("Climate zone by postcode", "Zones A–F or the local equivalent, mapped to winter design temperature."),
            ("ErP class, SCOP, SEER", "As documents, not as marketing copy — the agent emails the PDF the incentive scheme asks for."),
            ("Installer coverage", "Which certified installers serve which postcodes, and their current booking horizon."),
            ("ERP available-to-promise", "Stock plus inbound purchase orders, so lead times spoken on the phone are the ones the ERP will honour."),
        ],
        "proof": "Sabato answers the phone for ClimaConvenienza — heat pumps, boilers and air conditioning, on Shopify.",
        "faq": [
            ("Can an AI voice agent really size a heat pump on the phone?",
             "It reads your sizing table against the caller&rsquo;s floor area, ceiling height and climate zone, and it flags the cases that need a human — borderline emitter compatibility, three-phase supply, anything unmapped. It does not invent a kilowatt figure. Sizing that ends in an order should still be confirmed on the site visit, and the agent books that visit."),
            ("Does it work in Italian and English on the same line?",
             "Yes. The agent detects the caller&rsquo;s language on the first turn and stays in it for the whole call, including the email it sends afterwards. Sabato is built for European merchants, so multilingual is the default, not an add-on."),
            ("What happens outside opening hours?",
             "The agent answers, handles what it can from your systems — order status, availability, documents — and books a callback with the installer team for anything that needs a human. Evening and weekend calls are the ones HVAC merchants lose most often."),
            ("How does this differ from a chatbot on the product page?",
             "Sabato answers the phone. In high-consideration categories the buyer has already decided that typing is not enough — they want to describe their house to someone. A chat widget cannot take that call, and a voicemail box loses it."),
            ("What does it need from our Shopify store to go live?",
             "Read access to orders and products, your sizing and certification documents, and the installer coverage list. Most HVAC merchants have the first two and keep the third in a spreadsheet; that is fine, we map it."),
        ],
        "cta_h2": "Hear the agent take an HVAC sizing call",
        "cta_sub": "We&rsquo;ll run a live call against your own catalogue on the intro call — your sizing table, your postcodes, your questions.",
        "cta_hand": "twenty minutes, no deck",
        "scene": "hvac",
    },
    "fashion-apparel": {
        "label": "Fashion &amp; Apparel",
        "nav_label": "Fashion &amp; Apparel",
        "when": "after",
        "title": "Voice AI for Fashion &amp; Apparel E-Commerce | Sabato AI",
        "description": "Fashion buyers rarely phone before buying — they phone after. A managed voice agent that handles WISMO, exchanges and restock calls from live order data.",
        "h1": "Fashion buyers don&rsquo;t phone before they buy. They phone after.",
        "sub": "Nobody calls to ask about a t-shirt. They call because the parcel is late, the size was wrong, or the piece they wanted came back into stock. That queue is post-purchase, it is seasonal, and it is the one that breaks.",
        "hand": "here the call is the aftermath, not the sale",
        "call_q": "&ldquo;My order was supposed to arrive Tuesday and the tracking hasn&rsquo;t moved since Friday.&rdquo;",
        "call_meta": [("Detected intent", "Order status &middot; late parcel"),
                      ("Data pulled", "Carrier events &middot; order 48213"),
                      ("Outcome", "Answered, exchange offered")],
        "band_eyebrow": "Why this category phones",
        "band_h2": "The call arrives after the money moved, which is why it costs more than it looks.",
        "band_copy": [
            "A fashion buyer will happily choose a jacket without speaking to anyone. The product page does its job. Then the parcel is late, or the 12 fitted like a 10, and the same buyer wants a human — quickly, and usually during a peak week when the queue is already at its worst.",
            "This is deflection and retention work, not conversion work. We are honest about that: on a &euro;40 t-shirt there is no call to win. On the returns and delivery queue behind it, there is a real cost to remove.",
        ],
        "rank_head": "What the inbound calls are about",
        "rank": ["Where is my order / late delivery",
                 "Size exchange or return",
                 "Refund status and when the money lands",
                 "Back in stock: when, and reserve it",
                 "Promo code, discount and payment issues"],
        "questions_h2": "Five questions a fashion line hears every day — and what has to be true in your systems to answer them",
        "questions_intro": "None of these need product expertise. All of them need a live, correct record. That is the whole job in this category: read the right field, out loud, at eleven at night in the caller&rsquo;s language.",
        "questions": [
            ("&ldquo;Where is my order, it was supposed to be here Tuesday?&rdquo;",
             "Carrier tracking events on the order, with the exception reason spoken plainly rather than as a status code.",
             "carrier.events &middot; order.promised_date"),
            ("&ldquo;Can I exchange this for the next size up?&rdquo;",
             "Return eligibility window, plus whether that size is in stock right now — so the answer is an exchange, not a refund.",
             "returns.window &middot; variant.available"),
            ("&ldquo;I sent it back two weeks ago, where is my refund?&rdquo;",
             "Return receipt scan at the warehouse and the refund state on the payment provider.",
             "rma.received_at &middot; payment.refund_state"),
            ("&ldquo;When is this coming back in stock?&rdquo;",
             "Inbound purchase order date for the variant, and a callback booked for the day it lands.",
             "po.expected_at &middot; variant.id"),
            ("&ldquo;Does this run small? I&rsquo;m usually a 12.&rdquo;",
             "Garment measurements per size where you hold them, and an explicit hand-off when you don&rsquo;t — the one question in this category the agent should refuse to guess.",
             "variant.measurements &middot; fallback: human"),
        ],
        "workflows": [
            ("Where is my order", "The volume workflow in fashion. Carrier events read out loud, exceptions explained.", "/use-cases/where-is-my-order"),
            ("Managing returns", "Eligibility checked against policy, exchange offered before refund.", "/use-cases/managing-returns"),
            ("Back-in-stock notification", "Calls the customers who wanted it, instead of an email in a spam folder.", "/use-cases/back-in-stock-notification"),
            ("Post-delivery feedback", "Catches the problem while it is still fixable, and earns the review.", "/use-cases/post-delivery-feedback"),
        ],
        "transcript_meta": "Inbound &middot; 1 min 52 s &middot; language: English &middot; outcome: exchange booked, no refund",
        "transcript": [
            ("caller", "Hi, I ordered a coat last week, it was meant to arrive Tuesday and the tracking hasn&rsquo;t moved since Friday."),
            ("agent", "Let me look. Order ending 8213, the coat in navy — it&rsquo;s at the Milan depot and it was held there on Saturday because of a failed delivery attempt at the address. It&rsquo;s scheduled to go out again tomorrow morning."),
            ("caller", "Nobody came on Saturday."),
            ("agent", "That happens more than it should. I can either leave it on tomorrow&rsquo;s round, or reroute it to a pickup point near you — there&rsquo;s one about four hundred metres from the delivery address."),
            ("caller", "The pickup point. And actually — if the size is wrong when it turns up, how does that work?"),
            ("agent", "Thirty days from delivery. If it&rsquo;s the size rather than the coat, I&rsquo;d do an exchange instead of a return: the navy is in stock in both the size above and below, so it ships the day we scan yours back."),
            ("caller", "Good. Do the pickup point then."),
            ("agent", "Rerouted, and I&rsquo;ll text you the pickup code when it arrives. Anything else on this one?"),
        ],
        "data_h2": "The data reality behind a fashion answer",
        "data_copy": "This category asks less of your product data and more of your operational data. The failure mode is not a wrong recommendation — it is a confident wrong delivery date, which turns one annoyed customer into two calls.",
        "data_rows": [
            ("Carrier tracking events", "Raw events, not a status label, so an exception can be explained rather than recited."),
            ("Order promise date", "What the customer was actually told at checkout, which is often not what the carrier thinks."),
            ("Returns window and policy", "Per channel and per promotion, so the answer on the phone matches the portal."),
            ("Variant availability", "Live, so an exchange can be offered instead of a refund while the buyer is on the line."),
            ("Inbound purchase orders", "Expected dates by variant, for back-in-stock calls that are worth making."),
        ],
        "proof": None,
        "faq": [
            ("Do fashion customers actually call?",
             "Not usually before buying — that is the honest answer, and it is why this page leads with post-purchase. They call when a parcel is late, when a size is wrong, or when a refund has not landed. In peak weeks that queue is the one that overflows."),
            ("Is voice AI worth it if our average order value is low?",
             "It depends on your call volume, not your order value. If the post-purchase queue is large and seasonal, the case is deflection and retention. If it is small and steady, self-service is probably enough and we will say so on the intro call."),
            ("Can the agent handle a size or fit question?",
             "Only where you hold garment measurements per size. Where you do not, it hands over rather than guessing — fit is the one question in this category where a confident wrong answer converts directly into a return."),
            ("What happens during a sale week when volume triples?",
             "Concurrency is the point. The agent takes every call at once rather than queueing them, which is when abandoned calls in fashion usually spike — and abandoned calls skew towards the customers with a problem."),
            ("Does it work in more than one language?",
             "Yes, and in fashion that matters more than in most categories, because cross-border share is high. The agent detects the caller&rsquo;s language on the first turn and stays in it, including the follow-up message."),
        ],
        "cta_h2": "Hear the agent take a late-parcel call",
        "cta_sub": "We&rsquo;ll run it against your own order data on the intro call — your carrier, your returns policy, your peak-week volume.",
        "cta_hand": "twenty minutes, no deck",
        "scene": "fashion",
    },
}

ORDER = ["home-improvement", "fashion-apparel"]

FOOTER_INDUSTRIES = [
    ("Home Improvement", "/industries/home-improvement"),
    ("Automotive &amp; Parts", None),
    ("Electronics &amp; Tech", None),
    ("Furniture &amp; Home", None),
    ("Outdoor &amp; Garden", None),
    ("Fashion &amp; Apparel", "/industries/fashion-apparel"),
    ("Health &amp; Wellness", None),
    ("Sports &amp; Fitness", None),
    ("Industrial &amp; B2B", None),
]


# --------------------------------------------------------------------------
# SVG category scenes — flat, geometric, palette only. Written as code so they
# scale, restyle from tokens and weigh a few KB. No raster, no photography.
# --------------------------------------------------------------------------
def scene(kind):
    if kind == "hvac":
        return '''<svg class="scene" viewBox="0 0 720 300" role="img" aria-label="A wall-mounted unit sized against a floor plan and a climate zone">
  <rect x="0" y="0" width="720" height="300" rx="24" fill="rgb(248,244,241)"/>
  <!-- floor plan -->
  <rect x="44" y="60" width="200" height="180" rx="8" fill="none" stroke="rgb(18,10,11)" stroke-width="3"/>
  <line x1="44" y1="150" x2="150" y2="150" stroke="rgb(18,10,11)" stroke-width="3"/>
  <line x1="150" y1="150" x2="150" y2="240" stroke="rgb(18,10,11)" stroke-width="3"/>
  <text x="60" y="98" font-family="Satoshi,sans-serif" font-size="15" font-weight="700" fill="rgb(18,10,11)">120 m&#178;</text>
  <text x="60" y="120" font-family="Satoshi,sans-serif" font-size="12" fill="rgb(69,65,64)">single floor</text>
  <!-- the unit -->
  <rect x="300" y="76" width="150" height="46" rx="10" fill="rgb(18,10,11)"/>
  <rect x="316" y="92" width="118" height="4" rx="2" fill="rgb(204,255,0)"/>
  <rect x="316" y="102" width="86" height="4" rx="2" fill="rgba(248,244,241,.35)"/>
  <!-- airflow -->
  <path d="M310 140 q40 26 80 0" fill="none" stroke="rgb(204,255,0)" stroke-width="4" stroke-linecap="round"/>
  <path d="M330 170 q40 26 80 0" fill="none" stroke="rgb(204,255,0)" stroke-width="4" stroke-linecap="round" opacity=".65"/>
  <path d="M350 200 q40 26 80 0" fill="none" stroke="rgb(204,255,0)" stroke-width="4" stroke-linecap="round" opacity=".35"/>
  <!-- capacity readout -->
  <rect x="500" y="60" width="176" height="180" rx="16" fill="rgb(18,10,11)"/>
  <text x="524" y="100" font-family="Satoshi,sans-serif" font-size="12" letter-spacing="1.6" fill="rgba(248,244,241,.55)">SIZED AT</text>
  <text x="524" y="146" font-family="Satoshi,sans-serif" font-size="42" font-weight="900" fill="rgb(204,255,0)">12 kW</text>
  <line x1="524" y1="166" x2="652" y2="166" stroke="rgba(248,244,241,.18)" stroke-width="1"/>
  <text x="524" y="192" font-family="Satoshi,sans-serif" font-size="13" fill="rgba(248,244,241,.8)">climate zone E</text>
  <text x="524" y="214" font-family="Satoshi,sans-serif" font-size="13" fill="rgba(248,244,241,.8)">ceiling 2.7 m</text>
</svg>'''
    return '''<svg class="scene" viewBox="0 0 720 300" role="img" aria-label="A parcel tracked through carrier events to a pickup point">
  <rect x="0" y="0" width="720" height="300" rx="24" fill="rgb(248,244,241)"/>
  <!-- parcel -->
  <rect x="48" y="96" width="120" height="100" rx="10" fill="rgb(18,10,11)"/>
  <line x1="108" y1="96" x2="108" y2="196" stroke="rgb(204,255,0)" stroke-width="5"/>
  <rect x="66" y="120" width="42" height="5" rx="2.5" fill="rgba(248,244,241,.4)"/>
  <!-- route -->
  <line x1="188" y1="146" x2="520" y2="146" stroke="rgb(227,226,226)" stroke-width="4"/>
  <line x1="188" y1="146" x2="386" y2="146" stroke="rgb(204,255,0)" stroke-width="4"/>
  <circle cx="188" cy="146" r="11" fill="rgb(204,255,0)"/>
  <circle cx="287" cy="146" r="11" fill="rgb(204,255,0)"/>
  <circle cx="386" cy="146" r="11" fill="rgb(204,255,0)"/>
  <circle cx="470" cy="146" r="11" fill="none" stroke="rgb(18,10,11)" stroke-width="3" stroke-dasharray="4 4"/>
  <text x="176" y="186" font-family="Satoshi,sans-serif" font-size="11" fill="rgb(69,65,64)">picked</text>
  <text x="268" y="186" font-family="Satoshi,sans-serif" font-size="11" fill="rgb(69,65,64)">in transit</text>
  <text x="356" y="186" font-family="Satoshi,sans-serif" font-size="11" font-weight="700" fill="rgb(18,10,11)">held at depot</text>
  <text x="446" y="186" font-family="Satoshi,sans-serif" font-size="11" fill="rgb(69,65,64)">pickup</text>
  <!-- rerouted destination -->
  <rect x="536" y="86" width="140" height="120" rx="16" fill="rgb(18,10,11)"/>
  <text x="558" y="122" font-family="Satoshi,sans-serif" font-size="11" letter-spacing="1.6" fill="rgba(248,244,241,.55)">REROUTED</text>
  <path d="M560 146 l14 14 l28 -30" fill="none" stroke="rgb(204,255,0)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="558" y="190" font-family="Satoshi,sans-serif" font-size="13" fill="rgba(248,244,241,.8)">400 m away</text>
</svg>'''


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
    hdr = open("/tmp/_header.html").read() if os.path.exists("/tmp/_header.html") else ""

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
            .replace("{{HEADER}}", hdr))
    out = os.path.join(SITE, "industries", f"{slug}.html")
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
    n = link_footer_industries()
    print(f"  footer: linked built industries on {n} page(s)")
