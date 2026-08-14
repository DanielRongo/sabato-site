#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Product pages: /product/<slug> and /it/prodotto/<slug>.

    python3 product.py

WHY THIS FILE IS SO SHORT
Because it borrows almost everything. Daniel, 13 Aug: "can't you reuse existing
modules for similar pages and just change content and graphics?" - so this
imports the playbook generator's stylesheet, its section renderers, its proof
widget and its CTA band, and adds exactly three things a playbook does not have:

  1. `section_shot`  - the full-bleed platform screenshot under the hero
  2. `section_hands` - the "who actually touches this" band
  3. `TOOLS_VIZ`     - a live-HTML diagram of the agent's tools

LAYOUT: OPTION A, chosen 14 Aug
    hero (text only)  ->  screenshot  ->  3 blocks  ->  hands  ->  FAQ  ->  CTA

The hero deliberately carries NO screenshot. A UI in the hero says "here is the
tool you will operate", which is the opposite of what this business sells; a
screenshot placed AFTER a claim reads as evidence for that claim instead. Same
image, opposite promise.

WHY THE TOOLS DIAGRAM IS HTML AND THE PLATFORM SHOT IS AN IMAGE
An image of a UI scales with its column. On a 390px phone the content column is
about 346px, so a 1560px-wide screenshot renders at ~0.22x and its 12px labels
land at under 3px. tools/phone_render_audit.py exists precisely because that
bug shipped twice. The platform shot survives it by having a separate, much
tighter phone crop; the tools diagram survives it by not being a picture at all
- it is real text in real elements, so it reflows and stays readable.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from product_data import PRODUCTS, ORDER                      # noqa: E402
from product_data_it import PRODUCTS_IT, ORDER_IT             # noqa: E402
import playbooks as pb                                        # noqa: E402

SITE = os.path.join(ROOT, "site")
CAL = pb.CAL
esc = pb.esc
nb = pb.nb

LANGS = {
    "en": dict(out=os.path.join(SITE, "product"), base="/product/%s",
               locale="en_US", lang="en",
               cta_btn="Start Free Pilot", hand="live in two weeks"),
    "it": dict(out=os.path.join(SITE, "it", "prodotto"), base="/it/prodotto/%s",
               locale="it_IT", lang="it",
               cta_btn="Inizia il Pilota Gratuito", hand="online in due settimane"),
}

# ---------------------------------------------------------------------------
# CSS - only what the playbook stylesheet does not already provide.
# ---------------------------------------------------------------------------
PRODUCT_CSS = """
    /* ============ Product: the full-bleed platform shot ============ */
    .pr-shot { max-width: 1200px; margin: 0 auto; padding: 64px 40px 0; }
    .pr-shot figure { margin: 0; }
    /* The frame is what makes a flat PNG read as a screenshot rather than as
       an illustration that happens to have a sidebar in it. */
    .pr-shot img { display: block; width: 100%; height: auto; border-radius: 16px;
      border: 1px solid rgba(18,10,11,.10);
      box-shadow: 0 24px 60px rgba(18,10,11,.13), 0 2px 6px rgba(18,10,11,.06); }
    .pr-shot figcaption { color: rgb(120,118,117); font-size: 14.5px;
      line-height: 1.6; margin: 18px auto 0; max-width: 62ch; text-align: center; }

    /* ============ Product: the tools diagram ============ */
    .tv { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .tv-card { border: 1px solid rgba(18,10,11,.12); border-radius: 14px;
      background: #fff; padding: 18px 18px 16px; }
    .tv-card .tv-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 1.4px;
      color: rgb(120,118,117); margin: 0 0 14px; }
    .tv-tool { display: flex; align-items: flex-start; gap: 11px; padding: 9px 0;
      border-bottom: 1px solid rgba(18,10,11,.07); }
    .tv-tool:last-child { border-bottom: 0; padding-bottom: 0; }
    .tv-ic { width: 30px; height: 30px; flex: 0 0 30px; border-radius: 9px;
      display: flex; align-items: center; justify-content: center; }
    .tv-ic svg { width: 16px; height: 16px; fill: none; stroke-width: 1.8;
      stroke-linecap: round; stroke-linejoin: round; }
    .tv-tool code { display: block; font-family: ui-monospace, SFMono-Regular,
      Menlo, monospace; font-size: 13.5px; font-weight: 600; color: var(--ink); }
    .tv-tool em { display: block; font-style: normal; font-size: 13px;
      line-height: 1.4; color: rgb(120,118,117); margin-top: 2px; }
    .tv-rule { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 11px; }
    .tv-rule:last-of-type { margin-bottom: 0; }
    .tv-n { width: 21px; height: 21px; flex: 0 0 21px; border-radius: 999px;
      background: var(--ink); color: #fff; font-size: 11px; font-weight: 700;
      line-height: 21px; text-align: center; }
    .tv-rule p { font-size: 14.5px; line-height: 1.45; margin: 0; color: var(--ink); }
    .tv-say { margin-top: 16px; border-top: 1px solid rgba(18,10,11,.07); padding-top: 14px; }
    .tv-bubble { background: rgb(250,249,247); border: 1px solid rgba(18,10,11,.10);
      border-radius: 12px 12px 12px 4px; padding: 10px 13px; font-size: 14.5px;
      line-height: 1.45; font-style: italic; color: rgb(61,57,54); }
    .tv-foot { grid-column: 1 / -1; display: flex; align-items: center; gap: 10px;
      border: 1px solid rgba(18,10,11,.12); border-radius: 12px;
      background: rgb(250,249,247); padding: 12px 15px; font-size: 14.5px;
      line-height: 1.4; }
    .tv-foot b { color: var(--ink); }
    .tv-foot em { font-style: normal; color: rgb(120,118,117); }
    .tv-dot { width: 8px; height: 8px; flex: 0 0 8px; border-radius: 999px;
      background: rgb(200,240,74); box-shadow: 0 0 0 3px rgba(200,240,74,.3); }

    /* ============ Product: the release flow ============ */
    /* Block 3 had no visual, so section_blocks rendered it as a centred
       statement - correct for one short line, wrong for two paragraphs, and
       with block 1 already centred the page read as two walls of centred text
       in a row. This gives block 3 something to sit beside. */
    .rf { display: flex; flex-direction: column; gap: 10px; }
    .rf-step { display: flex; align-items: flex-start; gap: 13px;
      border: 1px solid rgba(248,244,241,.16); border-radius: 13px;
      padding: 15px 16px; background: rgba(248,244,241,.04); }
    .rf-k { width: 26px; height: 26px; flex: 0 0 26px; border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 12px; font-weight: 700; background: rgba(248,244,241,.11);
      color: rgb(248,244,241); }
    .rf-step.is-live .rf-k { background: rgb(200,240,74); color: rgb(18,10,11); }
    .rf-step b { display: block; color: rgb(248,244,241); font-size: 16px;
      letter-spacing: -.2px; }
    .rf-step em { display: block; font-style: normal; color: rgba(248,244,241,.66);
      font-size: 14.5px; line-height: 1.5; margin-top: 3px; }
    .rf-arrow { height: 14px; margin: -6px 0 -6px 25px;
      border-left: 1px dashed rgba(248,244,241,.28); }

    /* ============ Product: who touches this ============ */
    .pr-hands { max-width: 1200px; margin: 0 auto; padding: 104px 40px 0; }
    .pr-hands h2 { color: var(--ink); font-size: 38px; font-weight: 700;
      letter-spacing: -1.1px; line-height: 1.15; margin: 0 0 14px; }
    .pr-hands .pb-lede { color: var(--gray); font-size: 17.5px; line-height: 1.7;
      margin: 0 0 34px; max-width: 62ch; }
    .pr-hands-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr));
      gap: 20px; }
    .pr-hand { border: 1px solid rgba(18,10,11,.12); border-radius: 16px;
      padding: 24px 24px 26px; background: #fff; }
    .pr-hand h3 { color: var(--ink); font-size: 19px; font-weight: 700;
      letter-spacing: -.3px; margin: 0 0 10px; }
    .pr-hand p { color: var(--gray); font-size: 15.5px; line-height: 1.65; margin: 0; }

    @media (max-width: 900px) {
      .tv { grid-template-columns: 1fr; }
      .pr-hands-grid { grid-template-columns: 1fr; }
      .pr-hands { padding: 72px 22px 0; }
      .pr-hands h2 { font-size: 30px; }
      .pr-shot { padding: 44px 22px 0; }
      /* The two-column flex squeezes the bold half into a three-line column on
         a phone. Stack it instead. */
      .tv-foot { display: block; position: relative; padding-left: 32px; }
      .tv-foot .tv-dot { position: absolute; left: 15px; top: 19px; }
      .tv-foot b { display: block; margin-bottom: 2px; }
    }
"""

# ---------------------------------------------------------------------------
# The tools diagram. Abstract, drawn from the real "Assign tool" dialog and the
# transfer_call settings screen - the five conditions below are the same shape
# as the real rule, rewritten from 200 words of prompt into something a CEO
# reads in six seconds.
# ---------------------------------------------------------------------------
_TOOL_ICONS = {
    "search": ('#e9f1fa', '#3d81c9',
               '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>'),
    "order":  ('#e8f4ec', '#3f9a63',
               '<path d="M4 5h16v14H4z"/><path d="M8 10h8M8 14h5"/>'),
    "track":  ('#e8f4ec', '#3f9a63',
               '<path d="M3 8h13v9H3zM16 11h3.5L21 14v3h-5"/>'
               '<circle cx="7" cy="18.5" r="1.8"/><circle cx="18" cy="18.5" r="1.8"/>'),
    "person": ('#f7ebf1', '#b2557f',
               '<path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/>'
               '<circle cx="10" cy="7" r="3.6"/><path d="M20 8v6M23 11h-6"/>'),
    "hook":   ('#fdf1d9', '#e8981f',
               '<path d="M12 20V9M8 13l4-4 4 4"/><path d="M4 5h16"/>'),
}

TOOLS_VIZ_TEXT = {
    "en": dict(
        tools_h="TOOLS ON THIS AGENT",
        rule_h="WHEN <code>TRANSFER_CALL</code> FIRES",
        say_h="AND IT SAYS, BEFORE IT TRANSFERS",
        tools=[("search", "search_products", "Find an item in the catalogue"),
               ("order", "get_order", "Look an order up by number"),
               ("track", "where_is_my_order", "Live tracking status"),
               ("person", "transfer_call", "Hand the call to a person"),
               ("hook", "webhook", "Push the outcome to your systems")],
        rules=["The answer isn't in the knowledge base.",
               "They ask about a specific model, price or stock level.",
               "The product sits outside the categories we cover.",
               "An order needs changing, or something arrived damaged.",
               "They ask for a person - or they're clearly annoyed."],
        say="&ldquo;One moment &mdash; I&rsquo;m putting you through to a "
            "colleague now.&rdquo;",
        foot_b="You never write any of this.",
        foot_e="We do, and we keep it current as your catalogue changes.",
    ),
    "it": dict(
        tools_h="STRUMENTI DI QUESTO AGENTE",
        rule_h="QUANDO SCATTA <code>TRANSFER_CALL</code>",
        say_h="E PRIMA DI PASSARE, DICE",
        tools=[("search", "search_products", "Cerca un articolo a catalogo"),
               ("order", "get_order", "Trova un ordine dal numero"),
               ("track", "where_is_my_order", "Stato della spedizione, live"),
               ("person", "transfer_call", "Passa la chiamata a una persona"),
               ("hook", "webhook", "Scrive l'esito nei tuoi sistemi")],
        rules=["La risposta non e' nella knowledge base.",
               "Chiedono un modello, un prezzo o una disponibilita' precisa.",
               "Il prodotto e' fuori dalle categorie che copriamo.",
               "Un ordine va modificato, o e' arrivato qualcosa di rotto.",
               "Chiedono una persona - o si sono chiaramente innervositi."],
        say="&ldquo;Un attimo, le passo subito un collega.&rdquo;",
        foot_b="Tutto questo non lo scrivi tu.",
        foot_e="Lo scriviamo noi, e lo aggiorniamo quando cambia il catalogo.",
    ),
}


def tools_viz(lang):
    t = TOOLS_VIZ_TEXT[lang]
    tools = ""
    for key, name, line in t["tools"]:
        bg, stroke, path = _TOOL_ICONS[key]
        tools += ('<div class="tv-tool"><span class="tv-ic" style="background:%s">'
                  '<svg viewBox="0 0 24 24" stroke="%s" aria-hidden="true">%s</svg>'
                  '</span><span><code>%s</code><em>%s</em></span></div>'
                  % (bg, stroke, path, esc(name), esc(line)))
    rules = "".join('<div class="tv-rule"><span class="tv-n">%d</span><p>%s</p></div>'
                    % (i + 1, esc(r)) for i, r in enumerate(t["rules"]))
    return ('<div class="tv">'
            '<div class="tv-card"><p class="tv-eyebrow">%s</p>%s</div>'
            '<div class="tv-card"><p class="tv-eyebrow">%s</p>%s'
            '<div class="tv-say"><p class="tv-eyebrow">%s</p>'
            '<div class="tv-bubble">%s</div></div></div>'
            '<div class="tv-foot"><span class="tv-dot"></span>'
            '<span><b>%s</b> <em>%s</em></span></div>'
            '</div>'
            % (esc(t["tools_h"]), tools, t["rule_h"], rules,
               esc(t["say_h"]), t["say"], esc(t["foot_b"]), esc(t["foot_e"])))


RELEASE_FLOW_TEXT = {
    "en": [("Draft", "A change is written. Nothing about the live agent moves.", False),
           ("Test", "Call the draft yourself and hear it handle the awkward one.", False),
           ("Publish", "It goes live. The version before it is still kept.", True)],
    "it": [("Bozza", "La modifica e' scritta. Sull'agente vero non cambia niente.", False),
           ("Prova", "Chiami la bozza e te la senti gestire il caso scomodo.", False),
           ("Pubblica", "Va online. La versione precedente resta comunque li'.", True)],
}


def release_flow(lang):
    parts = []
    for i, (title, line, live) in enumerate(RELEASE_FLOW_TEXT[lang]):
        if i:
            parts.append('<div class="rf-arrow"></div>')
        parts.append('<div class="rf-step%s"><span class="rf-k">%d</span>'
                     '<span><b>%s</b><em>%s</em></span></div>'
                     % (" is-live" if live else "", i + 1, esc(title), esc(line)))
    return '<div class="rf">%s</div>' % "".join(parts)


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------
def section_shot(d):
    """The platform screenshot, full-bleed, directly under the hero.

    <picture> with a phone-specific crop, not one image scaled down. The wide
    shot at 390px renders its UI labels below 3px - see the module docstring.
    """
    s = d["shot"]
    return """
    <section class="pr-shot">
      <figure>
        <picture>
          <source media="(max-width: 810px)" srcset="%s-phone.webp">
          <img src="%s.webp" alt="%s" width="1560" height="796" loading="lazy" decoding="async">
        </picture>
        <figcaption>%s</figcaption>
      </figure>
    </section>""" % (s["src"], s["src"], esc(s["alt"]), esc(s["caption"]))


def section_hands(d):
    """"Who actually touches this" - mandatory on every Product page.

    The moment a page shows a builder, the reader asks whether the work lands
    on them. Answer it here rather than on the sales call.
    """
    h = d["hands"]
    cards = "".join('<div class="pr-hand"><h3>%s</h3><p>%s</p></div>'
                    % (esc(t), esc(p)) for t, p in h["cards"])
    return """
    <section class="pr-hands">
      <h2>%s</h2>
      <p class="pb-lede">%s</p>
      <div class="pr-hands-grid">%s</div>
    </section>""" % (nb(esc(h["h2"])), esc(h["lede"]), cards)


def template(lang):
    t = pb.template(lang)                       # playbook CSS + hero furniture
    base = LANGS[lang]["base"] % "{{SLUG}}"
    t = t.replace("https://www.sabato.ai" + (pb.LANGS[lang]["base"] % "{{SLUG}}"),
                  "https://www.sabato.ai" + base)
    t = t.replace(">%s<" % esc(pb.LANGS[lang]["hand"]),
                  ">%s<" % esc(LANGS[lang]["hand"]))
    t = t.replace("  </style>", PRODUCT_CSS + "  </style>", 1)
    return t


def jsonld(slug, d, lang):
    url = "https://www.sabato.ai" + (LANGS[lang]["base"] % slug)
    out = [{
        "@context": "https://schema.org", "@type": "WebPage",
        "name": re.sub(r"\[/?nb\]", "", d["h1"].replace("[br]", " ")).strip(),
        "description": d["description"],
        "url": url,
        "inLanguage": lang,
        "isPartOf": {"@type": "WebSite", "name": "Sabato AI",
                     "url": "https://www.sabato.ai"},
        "publisher": {"@type": "Organization", "name": "Sabato AI"},
    }]
    if d.get("faq"):
        out.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in d["faq"]],
        })
    return "".join('<script type="application/ld+json">%s</script>'
                   % json.dumps(o, ensure_ascii=False) for o in out)


def hreflang(slug, lang):
    """Both directions or neither - a one-sided hreflang is worse than none."""
    en = slug if lang == "en" else PRODUCTS_IT[slug]["en"]
    it = slug if lang == "it" else PRODUCTS[slug].get("it")
    if not it:
        return ""
    return ('<link rel="alternate" hreflang="en" href="https://www.sabato.ai/product/%s">'
            '<link rel="alternate" hreflang="it" href="https://www.sabato.ai/it/prodotto/%s">'
            '<link rel="alternate" hreflang="x-default" href="https://www.sabato.ai/product/%s">'
            % (en, it, en))


def build(lang, slug, d):
    cfg = LANGS[lang]
    # The viz token is swapped for real markup here rather than in the data
    # file, so the copy file never has to hold a line of HTML.
    d = dict(d)
    d["blocks"] = [dict(b) for b in d["blocks"]]
    for b in d["blocks"]:
        if b.get("viz") == "TOOLS_VIZ":
            b["viz"] = tools_viz(lang)
        elif b.get("viz") == "RELEASE_FLOW":
            b["viz"] = release_flow(lang)

    sections = "".join([
        section_shot(d),
        pb.section_blocks(d),
        section_hands(d),
        pb.section_proof(d, lang),
        pb.section_faq(d),
        pb.section_cta(d, lang),
    ])
    page = (template(lang)
            .replace("{{TITLE}}", html.escape(d["title"]))
            .replace("{{DESCRIPTION}}", html.escape(d["description"]))
            .replace("{{SLUG}}", slug)
            .replace("{{JSONLD}}", jsonld(slug, d, lang) + hreflang(slug, lang))
            .replace("{{CHIP}}", esc(d["chip"]))
            .replace("{{H1}}", nb(esc(d["h1"])))
            .replace("{{SUB}}", esc(d["sub"]))
            .replace("{{HERO_VISUAL}}", d.get("hero_visual", ""))
            .replace("{{SECTIONS}}", sections))
    os.makedirs(cfg["out"], exist_ok=True)
    p = os.path.join(cfg["out"], slug + ".html")
    open(p, "w", encoding="utf-8").write(page)
    print("  wrote %s" % p)
    return "https://www.sabato.ai" + (cfg["base"] % slug)


def main():
    urls = []
    for slug in ORDER:
        urls.append(build("en", slug, PRODUCTS[slug]))
    for slug in ORDER_IT:
        urls.append(build("it", slug, PRODUCTS_IT[slug]))
    print("  sitemap: %d new URL(s) added" % pb.sitemap_add(urls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
