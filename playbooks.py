#!/usr/bin/env python3
"""Playbook pages - the TRIGGER half of the Use Cases menu.

    python3 playbooks.py

TWO TAXONOMIES, ONE MENU
------------------------
The nine pages under /use-cases/ answer "what does the agent do on a call":
Where is my order, Managing returns, Cart abandonment. They are WORKFLOWS.

A playbook answers a different question - "why am I looking at this at all".
Peak season is coming. We are opening a market. Care costs are out of control.
Same buyer, earlier moment, completely different page.

Both live under the Use Cases menu in two columns. Deliberately NOT a rename of
the /use-cases/ URL space: those nine pages are a week into being indexed and
moving them now would reset that for a label change nobody outside the company
would ever notice.

DERIVED FROM templates/use-case.html AT BUILD TIME, not copied. A snapshot of a
stylesheet is a bug with a delay on it - the Italian customer template was
already learned that way, where new CSS added to the English file left the
Italian page rendering ink-on-black. Playbooks get every token, breakpoint and
component the use-case pages get, forever, because they read the same file.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from playbook_data import PLAYBOOKS, ORDER                     # noqa: E402
from playbook_data_it import PLAYBOOKS_IT, ORDER_IT            # noqa: E402

SITE = os.path.join(ROOT, "site")
CAL = "https://cal.com/sabatoai/intro"

LANGS = {
    "en": dict(out=os.path.join(SITE, "playbooks"), base="/playbooks/%s",
               locale="en_US", lang="en",
               cta_btn="Start Free Pilot", hand="live in two weeks"),
    "it": dict(out=os.path.join(SITE, "it", "playbook"), base="/it/playbook/%s",
               locale="it_IT", lang="it",
               cta_btn="Inizia il Pilota Gratuito", hand="online in due settimane"),
}

# Playbook-only components. Everything else - tokens, hero, dark band, CTA band,
# every breakpoint - comes from the use-case stylesheet unchanged.
EXTRA_CSS = """
    /* ============ Playbook: light problem block ============ */
    /* Same geometry as the dark band so the two alternate without the page
       stepping. Only the colours change. */
    .pb-light { max-width: 1200px; margin: 0 auto; padding: 96px 40px 0; }
    .pb-light .eyebrow { color: rgb(120,118,117); font-size: 13px; font-weight: 700;
      letter-spacing: 2.5px; margin: 0 0 18px; }
    .pb-light h2 { color: var(--ink); font-size: 38px; font-weight: 700;
      letter-spacing: -1.1px; line-height: 1.15; margin: 0 0 26px; }
    /* .queue-grid .qcopy .qbody in the use-case stylesheet is specificity 0,3,0
       and paints near-white for the dark band. Reusing .queue-grid inside a light
       block therefore inherited white-on-white and the copy vanished - obvious in
       a screenshot, invisible to every automated check in this repo. Match the
       specificity rather than reaching for !important. */
    .pb-light .queue-grid .qcopy .qbody,
    .pb-light .qcopy .qbody {
      color: var(--gray); font-size: 17.5px; line-height: 1.75; margin: 0;
    }
    .pb-light .qcopy .qbody b { color: var(--ink); }
    .pb-light .qbody + .qbody { margin-top: 16px; }
    .pb-light .queue-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 64px;
      align-items: center; }
    /* Source lines are small print, not decoration - if a reader cannot read the
       citation the number might as well be unsourced. rgb(110,108,107) clears
       4.5:1 on white; the 140-grey it replaced sat at 3.4:1 and failed AA. */
    .pb-light .fine, .pb-light .queue-viz .fine {
      color: rgb(110,108,107); font-size: 12px; line-height: 1.6; margin: 18px 0 0;
    }
    /* Same reasoning on the dark bands: .45 alpha over black is 4.1:1. */
    .queue-band .queue-viz .fine, .queue-band .fine { color: rgba(248,244,241,.66); }
    /* The use-case stylesheet only paints .qbody near-white INSIDE .queue-grid
       (.queue-grid .qcopy .qbody). A wide block has no grid, so its text fell
       back to body ink - black on black, contrast 1.07, found by the AA audit.
       Scope by band, not by grid, so the colour follows the background. */
    .queue-band .qcopy .qbody { color: rgba(248, 244, 241, .82); font-size: 17.5px;
      line-height: 1.75; margin: 0; }
    .queue-band .qbody + .qbody { margin-top: 16px; }
    /* A block with no picture gets a reading measure instead of the full 1060px. */
    .pb-wide { max-width: 760px; }
    .queue-viz .fine a, .pb-light .fine a { color: inherit; text-decoration: underline;
      text-underline-offset: 2px; }
    @media (max-width: 809px) {
      .pb-light { padding: 64px 22px 0; }
      .pb-light h2 { font-size: 29px; letter-spacing: -.9px; }
      .pb-light .queue-grid { grid-template-columns: 1fr; gap: 34px; }
      .pb-light .qbody { font-size: 16.5px; }
    }

    /* ============ Playbook: slim mid-page CTA ============ */
    .pb-mid { max-width: 1200px; margin: 0 auto; padding: 76px 40px 0; text-align: center; }
    .pb-mid p { font-size: 21px; font-weight: 700; letter-spacing: -.4px; color: var(--ink);
      margin: 0 0 18px; }

    /* ============ Playbook: visible FAQ ============ */
    .pb-faqs { max-width: 1200px; margin: 0 auto; padding: 96px 40px 0; }
    .pb-faqs h2 { font-size: 38px; font-weight: 700; letter-spacing: -1.1px;
      color: var(--ink); margin: 0 0 34px; text-align: center; }
    .pb-faq-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .pb-qa { background: var(--off); border-radius: var(--radius); padding: 28px 30px; }
    .pb-qa h3 { font-size: 18px; font-weight: 700; letter-spacing: -.3px;
      color: var(--ink); margin: 0 0 10px; }
    .pb-qa p { font-size: 15.5px; line-height: 1.65; color: var(--gray); margin: 0; }
    @media (max-width: 809px) {
      .pb-mid { padding: 56px 22px 0; }
      .pb-mid p { font-size: 18px; }
      .pb-faqs { padding: 64px 22px 0; }
      .pb-faqs h2 { font-size: 29px; margin-bottom: 24px; }
      .pb-faq-grid { grid-template-columns: 1fr; }
    }

    /* ============ Playbook: the countdown ============ */
    .pb-steps { max-width: 1200px; margin: 0 auto; padding: 104px 40px 0; }
    .pb-steps h2 { font-size: 38px; font-weight: 700; letter-spacing: -1.1px; line-height: 1.2;
      color: var(--ink); margin: 0 0 12px; text-align: center; }
    .pb-steps .pb-lede { font-size: 16.5px; line-height: 1.7; color: var(--gray);
      max-width: 680px; margin: 0 auto 46px; text-align: center; }
    .pb-step { display: grid; grid-template-columns: 190px 1fr; gap: 40px;
      padding: 30px 0; border-top: 1px solid var(--line); align-items: start; }
    .pb-step:last-child { border-bottom: 1px solid var(--line); }
    .pb-when { font-size: 14px; font-weight: 700; letter-spacing: 1.6px;
      text-transform: uppercase; color: var(--ink); padding-top: 4px; }
    .pb-when span { display: block; font-weight: 500; letter-spacing: 0;
      text-transform: none; font-size: 14.5px; color: var(--gray); margin-top: 6px; }
    .pb-step h3 { font-size: 23px; font-weight: 700; letter-spacing: -.5px;
      line-height: 1.3; color: var(--ink); margin: 0 0 10px; }
    .pb-step p { font-size: 16.5px; line-height: 1.7; color: var(--gray); margin: 0; }
    .pb-step p + p { margin-top: 10px; }
    .pb-step a { color: var(--blue); text-decoration: underline; text-underline-offset: 2px; }

    /* ============ Playbook: the workflow row ============ */
    .pb-wf { max-width: 1200px; margin: 0 auto; padding: 96px 40px 0; }
    .pb-wf h2 { font-size: 38px; font-weight: 700; letter-spacing: -1.1px; line-height: 1.2;
      color: var(--ink); margin: 0 0 12px; text-align: center; }
    .pb-wf .pb-lede { font-size: 16.5px; line-height: 1.7; color: var(--gray);
      max-width: 700px; margin: 0 auto 40px; text-align: center; }
    .pb-wf-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
    .pb-card { display: block; background: var(--off); border-radius: var(--radius);
      padding: 30px 32px; transition: transform .15s ease; }
    .pb-card:hover { transform: translateY(-2px); }
    .pb-card h3 { font-size: 20px; font-weight: 700; letter-spacing: -.4px;
      color: var(--ink); margin: 0 0 8px; }
    .pb-card p { font-size: 16px; line-height: 1.65; color: var(--gray); margin: 0; }
    .pb-card .pb-go { display: inline-block; margin-top: 14px; font-size: 15px;
      font-weight: 700; color: var(--blue); }

    /* ============ Playbook: the proof strip ============ */
    .pb-proofline { max-width: 1200px; margin: 96px auto 0; padding: 0 40px; }
    .pb-proofline .pb-inner { background: var(--black); border-radius: var(--radius);
      padding: 56px 56px 52px; color: #fff; }
    .pb-proofline .eyebrow { color: var(--lime); font-size: 13px; font-weight: 700;
      letter-spacing: 2.5px; margin: 0 0 18px; }
    .pb-proofline blockquote { font-size: 24px; line-height: 1.45; font-weight: 500;
      letter-spacing: -.4px; margin: 0 0 20px; max-width: 900px; }
    .pb-proofline .pb-who { font-size: 15px; line-height: 1.5;
      color: rgba(248, 244, 241, .6); }
    .pb-proofline .pb-who b { color: #fff; display: block; font-weight: 700; }
    .pb-proofline .pb-nums { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 28px; margin-top: 34px; padding-top: 30px;
      border-top: 1px solid rgba(248, 244, 241, .16); }
    .pb-proofline .pb-n { display: block; font-size: 40px; font-weight: 900;
      letter-spacing: -1.2px; color: var(--lime); font-variant-numeric: tabular-nums; }
    .pb-proofline .pb-l { display: block; margin-top: 8px; font-size: 14px;
      line-height: 1.45; color: rgba(248, 244, 241, .66); }
    .pb-proofline .pb-read { display: inline-block; margin-top: 28px; font-size: 15px;
      font-weight: 700; color: var(--lime); }

    @media (max-width: 809px) {
      .pb-steps { padding: 72px 22px 0; }
      .pb-steps h2, .pb-wf h2 { font-size: 29px; }
      .pb-step { grid-template-columns: 1fr; gap: 10px; padding: 24px 0; }
      .pb-when span { display: inline; margin: 0 0 0 8px; }
      .pb-step h3 { font-size: 20px; }
      .pb-wf { padding: 72px 22px 0; }
      .pb-wf-grid { grid-template-columns: 1fr; }
      .pb-proofline { padding: 0 16px; margin-top: 72px; }
      .pb-proofline .pb-inner { padding: 34px 24px 32px; }
      .pb-proofline blockquote { font-size: 19px; }
      .pb-proofline .pb-nums { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
      .pb-proofline .pb-n { font-size: 26px; letter-spacing: -.8px; }
      .pb-proofline .pb-l { font-size: 11.5px; }
    }
"""


def esc(s):
    return html.escape(s, quote=False)


def nb(s):
    """[nb]...[/nb] keeps a phrase on one line, same convention as every other
    template here."""
    return s.replace("[nb]", '<span class="nb">').replace("[/nb]", "</span>")


def template(lang):
    """The use-case template, re-pointed at /playbooks/ and given its own CSS."""
    t = open(os.path.join(ROOT, "templates", "use-case.html"), encoding="utf-8").read()
    base = LANGS[lang]["base"] % "{{SLUG}}"
    t = t.replace("https://www.sabato.ai/use-cases/{{SLUG}}",
                  "https://www.sabato.ai" + base)
    if lang == "it":
        t = t.replace('<html lang="en">', '<html lang="it">')
        t = t.replace('<meta property="og:locale" content="en_US">',
                      '<meta property="og:locale" content="it_IT">')
    # The hero's hand-written note and button live in the template, not the data.
    t = t.replace(">live in two weeks<", ">%s<" % esc(LANGS[lang]["hand"]))
    if lang == "it":
        t = t.replace(">Start Free Pilot<", ">%s<" % esc(LANGS[lang]["cta_btn"]))
    t = t.replace("  </style>", EXTRA_CSS + "  </style>", 1)
    return t


def section_blocks(d):
    """The problem, in as many blocks as it takes.

    A playbook has to earn the reader before it sells anything, and the problem
    is the part they recognise. Dark and light blocks alternate so a long
    argument still reads as a page rather than an essay.

    `fine` is not decoration either: every figure on these pages carries its
    source and its date underneath it, because a claim about somebody's payroll
    that cannot be checked is worth less than no claim at all.
    """
    out = []
    for b in d["blocks"]:
        body = "".join('<p class="qbody">%s</p>' % b_p for b_p in b["body"])
        fine = '<p class="fine">%s</p>' % b["fine"] if b.get("fine") else ""
        if b.get("viz"):
            grid = ('<div class="queue-grid"><div class="qcopy">%s</div>'
                    '<div class="queue-viz">%s%s</div></div>' % (body, b["viz"], fine))
        else:
            # A block with no picture still has to carry its source. The first
            # version attached `fine` to the visual, so the one block without one
            # - the block with the 48.9% figure on it - published an unsourced
            # number. Every figure on these pages cites itself or it does not ship.
            grid = '<div class="qcopy pb-wide">%s%s</div>' % (body, fine)
        cls = "queue-band" if b.get("tone", "dark") == "dark" else "pb-light"
        out.append("""
    <section class="%s">
      <div class="queue-inner">
        <p class="eyebrow">%s</p>
        <h2>%s</h2>
        %s
      </div>
    </section>""" % (cls, esc(b["eyebrow"]), nb(esc(b["h2"])), grid))
    return "".join(out)


def section_steps(d):
    s = d["steps"]
    rows = "".join(
        '<div class="pb-step"><div class="pb-when">%s<span>%s</span></div>'
        '<div><h3>%s</h3>%s</div></div>'
        % (esc(w), esc(sub), esc(t), "".join("<p>%s</p>" % p for p in body))
        for w, sub, t, body in s["rows"])
    return """
    <section class="pb-steps">
      <h2>%s</h2>
      <p class="pb-lede">%s</p>
      %s
    </section>""" % (nb(esc(s["h2"])), esc(s["lede"]), rows)


def section_mid(d, lang):
    """A slim CTA between the problem and the mechanics. On a landing page the
    reader who is already convinced must never have to scroll to convert - the
    black band at the bottom stays the finale, this is the exit for the
    impatient."""
    m = d.get("midcta")
    if not m:
        return ""
    return """
    <section class="pb-mid">
      <p>%s</p>
      <a class="btn-pill" href="%s" target="_blank" rel="noopener">%s</a>
    </section>""" % (esc(m), CAL, esc(LANGS[lang]["cta_btn"]))


def section_faq(d):
    """The FAQ, VISIBLE. The FAQPage schema in <head> must describe content
    that is actually on the page - schema for invisible answers is what rich-
    result penalties are made of, and it was the one dishonest inch in the
    first version of this page. Rendered from the same list the JSON-LD reads,
    so the two cannot drift."""
    if not d.get("faq"):
        return ""
    items = "".join(
        '<div class="pb-qa"><h3>%s</h3><p>%s</p></div>' % (esc(q), esc(a))
        for q, a in d["faq"])
    return """
    <section class="pb-faqs">
      <h2>%s</h2>
      <div class="pb-faq-grid">%s</div>
    </section>""" % (esc(d.get("faq_h2", "FAQ")), items)


def section_workflows(d):
    w = d["workflows"]
    cards = "".join(
        '<a class="pb-card" href="%s"><h3>%s</h3><p>%s</p>'
        '<span class="pb-go">%s &rarr;</span></a>' % (href, esc(label), esc(line), esc(w["go"]))
        for label, href, line in w["items"])
    return """
    <section class="pb-wf">
      <h2>%s</h2>
      <p class="pb-lede">%s</p>
      <div class="pb-wf-grid">%s</div>
    </section>""" % (nb(esc(w["h2"])), esc(w["lede"]), cards)


def section_proof(d):
    p = d.get("proof")
    if not p:
        return ""
    nums = "".join('<div><span class="pb-n">%s</span><span class="pb-l">%s</span></div>'
                   % (esc(v), esc(l)) for v, l in p["nums"])
    return """
    <section class="pb-proofline">
      <div class="pb-inner">
        <p class="eyebrow">%s</p>
        <blockquote>&ldquo;%s&rdquo;</blockquote>
        <p class="pb-who"><b>%s</b>%s</p>
        <div class="pb-nums">%s</div>
        <a class="pb-read" href="%s">%s &rarr;</a>
      </div>
    </section>""" % (esc(p["eyebrow"]), esc(p["quote"]), esc(p["who"]),
                     esc(p["role"]), nums, p["href"], esc(p["link"]))


def section_cta(d, lang):
    c = d["cta"]
    return """
    <section class="cta-band">
      <p class="hand">%s</p>
      <h2>%s</h2>
      <p>%s</p>
      <a class="btn-pill" href="%s" target="_blank" rel="noopener">%s</a>
    </section>""" % (esc(c["hand"]), nb(esc(c["h2"])), esc(c["sub"]),
                     CAL, esc(LANGS[lang]["cta_btn"]))


def jsonld(slug, d, lang):
    """Article + a FAQPage when the playbook carries questions.

    No datePublished and no aggregateRating: we hold neither, and decorating a
    rich result with a number we invented is the one SEO shortcut that is
    actually punished rather than merely useless.
    """
    import json
    url = "https://www.sabato.ai" + (LANGS[lang]["base"] % slug)
    out = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": re.sub(r"\[/?nb\]", "", d["h1"]),
        "description": d["description"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "inLanguage": lang,
        "image": "https://www.sabato.ai/fuc/assets/8Q4ofjOgRTqsr8FpanTJF9nzLwU.png",
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
    """Both directions or neither. A one-sided hreflang is worse than none."""
    en = slug if lang == "en" else PLAYBOOKS_IT[slug]["en"]
    it = slug if lang == "it" else PLAYBOOKS[slug].get("it")
    if not it:
        return ""
    return ('<link rel="alternate" hreflang="en" href="https://www.sabato.ai/playbooks/%s">'
            '<link rel="alternate" hreflang="it" href="https://www.sabato.ai/it/playbook/%s">'
            '<link rel="alternate" hreflang="x-default" href="https://www.sabato.ai/playbooks/%s">'
            % (en, it, en))


def build(lang, slug, d):
    cfg = LANGS[lang]
    tpl = template(lang)
    sections = "".join([section_blocks(d), section_mid(d, lang),
                        section_steps(d), section_workflows(d),
                        section_proof(d), section_faq(d),
                        section_cta(d, lang)])
    page = (tpl
            .replace("{{TITLE}}", html.escape(d["title"]))
            .replace("{{DESCRIPTION}}", html.escape(d["description"]))
            .replace("{{SLUG}}", slug)
            .replace("{{JSONLD}}", jsonld(slug, d, lang) + hreflang(slug, lang))
            .replace("{{CHIP}}", esc(d["chip"]))
            .replace("{{H1}}", nb(esc(d["h1"])))
            .replace("{{SUB}}", esc(d["sub"]))
            .replace("{{HERO_VISUAL}}", d["hero_visual"])
            .replace("{{SECTIONS}}", sections))
    os.makedirs(cfg["out"], exist_ok=True)
    p = os.path.join(cfg["out"], slug + ".html")
    open(p, "w", encoding="utf-8").write(page)
    print("  wrote %s" % p)
    return "https://www.sabato.ai" + (cfg["base"] % slug)


def sitemap_add(urls):
    path = os.path.join(SITE, "sitemap.xml")
    if not os.path.exists(path):
        return 0
    xml = open(path, encoding="utf-8").read()
    have = set(re.findall(r"<loc>(.*?)</loc>", xml))
    add = [u for u in urls if u not in have]
    if add:
        xml = xml.replace("</urlset>",
                          "".join("<url><loc>%s</loc></url>" % u for u in add) + "</urlset>")
        open(path, "w", encoding="utf-8").write(xml)
    return len(add)


def main():
    urls = []
    for slug in ORDER:
        urls.append(build("en", slug, PLAYBOOKS[slug]))
    for slug in ORDER_IT:
        urls.append(build("it", slug, PLAYBOOKS_IT[slug]))
    print("  sitemap: %d new URL(s) added" % sitemap_add(urls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
