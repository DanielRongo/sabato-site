#!/usr/bin/env python3
"""Build the customer story pages.

    python3 customers.py

Renders site/customers/<slug>.html from templates/customer.html using the
content in customer_data.py. Sections are composed from the classes the
use-case pages already define, so these pages inherit the design system rather
than restating it - the only new CSS lives in the template.

Draft handling: any [[bracketed]] string becomes a loud orange TBC chip, and
every page carries noindex + a DRAFT ribbon until Daniel has written sign-off on
the figures and the quotes. See customer_data.py for why that matters.
"""
import html
import os
import re

from customer_data import CUSTOMERS, ORDER
from customer_data_it import CUSTOMERS_IT, ORDER_IT

LANGS = {
    "en": {"tpl": "templates/customer.html",    "out": "site/customers",
           "base": "/customers/%s",     "data": None, "order": None,
           "cta": "Start Free Pilot"},
    "it": {"tpl": "templates/customer-it.html", "out": "site/it/clienti",
           "base": "/it/clienti/%s",    "data": None, "order": None,
           "cta": "Inizia Pilot Gratuito"},
}

PH_RX = re.compile(r"\[\[(.+?)\]\]", re.DOTALL)


NB_RX = re.compile(r"\b([eE]-[cC]ommerce)\b")
NBM_RX = re.compile(r"\[nb\](.+?)\[/nb\]", re.DOTALL)


def ph(text):
    """Escape, turn [[...]] into a visible TBC chip, and keep 'e-commerce' whole.

    Browsers treat the hyphen as a break opportunity, so a headline can split as
    'e-' / 'commerce'. Site convention is the .nb nowrap span."""
    out, last = [], 0
    for m in PH_RX.finditer(text):
        out.append(html.escape(text[last:m.start()]))
        out.append('<span class="ph">%s</span>' % html.escape(m.group(1)))
        last = m.end()
    out.append(html.escape(text[last:]))
    out = NB_RX.sub(r'<span class="nb">\1</span>', "".join(out))
    # [nb]...[/nb] in the content keeps a phrase on one line
    return NBM_RX.sub(r'<span class="nb">\1</span>', out)


def is_ph(text):
    return bool(PH_RX.search(text))


def plain(text):
    """Marker-free text for anywhere the string is not rendered as HTML -
    JSON-LD, meta tags, alt text. Without this the [nb] markers leak into
    structured data, which is both wrong and visible to Google."""
    return NBM_RX.sub(r"\1", PH_RX.sub(r"\1", text))



_IW = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="rgb(204,255,0)" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>')

ICONS = {
    # globe with a speech tail - multilingual
    "languages": _IW % ('<circle cx="11" cy="11" r="7.5"/><path d="M3.5 11h15"/>'
                        '<path d="M11 3.5c2 2.4 3 5 3 7.5s-1 5.1-3 7.5"/>'
                        '<path d="M11 3.5c-2 2.4-3 5-3 7.5s1 5.1 3 7.5"/>'),
    # parcel in transit - where is my order
    "wismo": _IW % ('<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/>'
                    '<path d="M3 7.5 12 12l9-4.5"/><path d="M12 12v9"/>'),
    # sliders - configurator
    "configurator": _IW % ('<line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/>'
                           '<line x1="4" y1="17" x2="20" y2="17"/><circle cx="9" cy="7" r="2.2"/>'
                           '<circle cx="15" cy="12" r="2.2"/><circle cx="8" cy="17" r="2.2"/>'),
}

GLYPH = ('<svg viewBox="0 0 16 12" aria-hidden="true"><g fill="currentColor">'
         '<rect x="0" y="3.5" width="2.5" height="5" rx="1.25"/>'
         '<rect x="4.5" y="1.5" width="2.5" height="9" rx="1.25"/>'
         '<rect x="9" y="0" width="2.5" height="12" rx="1.25"/>'
         '<rect x="13.5" y="3.5" width="2.5" height="5" rx="1.25"/></g></svg>')
SPK = {"caller": "CALLER", "agent": "AGENT"}


def _block(s, a, b):
    i = s.index(a); return s[i:s.index(b, i) + len(b)]


def italian_template():
    """Derive the Italian template from the English one at build time.

    It used to be a checked-in copy, and that copy went stale the moment new CSS
    was added to the English template: the knowledge-base panel rendered
    ink-on-black on the Italian page because those rules only existed in the
    English file. A snapshot of a stylesheet is a bug with a delay on it.

    Only the chrome and the locale differ, and the chrome is taken verbatim from
    the shipped Italian industry template so the two page families cannot drift.
    """
    en = open("templates/customer.html", encoding="utf-8").read()
    it_ind = open("templates/industry-it.html", encoding="utf-8").read()
    HDR = ('<header class="site-header">', '</header>')
    out = en.replace(_block(en, *HDR), _block(it_ind, *HDR))
    # The footer used to be swapped here too. It is no longer in any template -
    # tools/apply_footer.py renders it last, and picks the language from the
    # page's own path, so an Italian customer page gets the Italian footer
    # without this file knowing anything about footers.
    out = out.replace('<html lang="en">', '<html lang="it">')
    out = out.replace("https://www.sabato.ai/customers/{{SLUG}}",
                      "https://www.sabato.ai/it/clienti/{{SLUG}}")
    out = out.replace('<meta property="og:locale" content="en_US">',
                      '<meta property="og:locale" content="it_IT">')
    out = out.replace("DRAFT - NOT APPROVED", "BOZZA - NON APPROVATA")
    return out


def hero_mark(d):
    """The customer's logo above the headline, monogram if we have no asset."""
    if d["logo"]:
        mark = '<img class="cust-logo" src="%s" alt="%s" width="640" height="97">' % (
            d["logo"], html.escape(d["name"]))
    else:
        mark = ('<span class="cust-logo-fallback"><span class="mono">%s</span>%s</span>'
                % (html.escape(d["initials"]), html.escape(d["name"])))
    return mark


TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="rgb(204,255,0)" stroke-width="3.2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M4 12.5 9.5 18 20 6.5"/></svg>')


def coverage_block(d):
    """A queue x language matrix. Reads as breadth of deployment at a glance and,
    unlike any volume graphic, discloses nothing about the customer's traffic."""
    c = d["coverage"]
    head = "".join('<span class="lang">%s</span>' % html.escape(l) for l in c["languages"])
    rows = ""
    for q in c["queues"]:
        rows += '<span class="queue">%s</span>' % html.escape(q)
        rows += '<span class="cov-cell">%s</span>' % TICK * len(c["languages"])
    return ('<div class="cov"><p class="cov-h">%s</p>'
            '<div class="cov-grid"><span></span>%s%s</div>'
            '<p class="cov-note">%s</p></div>'
            % (html.escape(c["title"]), head, rows, ph(c["note"])))


def kb_block(d):
    """What the agent knows, as chips. Shown where a coverage matrix would be a
    2x1 stub."""
    k = d["kb"]
    chips = "".join("<span>%s</span>" % html.escape(t) for t in k["topics"])
    return ('<div class="kb"><p class="kb-h">%s</p><p class="kb-n">%s</p>'
            '<div class="kb-list">%s</div><p class="kb-note">%s</p></div>'
            % (html.escape(k["title"]), html.escape(k["number"]), chips, ph(k["note"])))


def section_forward(d):
    if not d.get("forward_h2"):
        return ""
    return """
    <section class="fwd">
      <p class="eyebrow">%s</p>
      <h2>%s</h2>
      <p>%s</p>
    </section>""" % (ph(d["forward_eyebrow"]), ph(d["forward_h2"]), ph(d["forward_body"]))


def section_situation(d):
    # The body colour on this band is scoped to `.queue-grid .qcopy .qbody` in
    # the use-case stylesheet. Reusing `.queue-band` without reproducing that
    # exact ancestor chain silently renders ink-on-black - which is how the
    # first draft of this page came out unreadable. Match their markup, don't
    # patch the colour.
    cards = "".join(
        '<div class="stack-card"><h3>%s</h3><p>%s</p></div>' % (ph(t), ph(b))
        for t, b in d["situation_points"])
    body = "".join('<p class="qbody">%s</p>' % ph(p) for p in d["situation_body"])
    shot = ""
    cls = "queue-grid"
    if d.get("coverage"):
        cls = "queue-grid with-shot"
        shot = coverage_block(d)
    elif d.get("kb"):
        cls = "queue-grid with-shot"
        shot = kb_block(d)
    elif d.get("storefront"):
        cls = "queue-grid with-shot"
        shot = ("""<div class="browser"><div class="bar"><i></i><i></i><i></i>"""
                """<span class="url">%s</span></div><img src="%s" alt="%s storefront" """
                """loading="lazy"></div>""" % (html.escape(d["storefront_url"]),
                                               d["storefront"], html.escape(d["name"])))
    return """
    <section class="queue-band">
      <div class="%s">
        <div class="qcopy">
          <p class="eyebrow">%s</p>
          <h2>%s</h2>
          %s
        </div>
        %s
      </div>
    </section>
    <section class="stack"><div class="stack-grid">%s</div></section>""" % (
        cls, ph(d["situation_eyebrow"]), ph(d["situation_h2"]), body, shot, cards)


def section_stack(d):
    cards = "".join(
        '<div class="stack-card"><span class="ic-chip">%s</span><h3>%s</h3><p>%s</p></div>'
        % (ICONS.get(icon, ""), ph(t), ph(b))
        for icon, t, b in d["stack"])
    logo = ('<img src="%s" alt="%s" loading="lazy">' % (d["platform_logo"], d["platform"])
            if d.get("platform_logo") else "")
    return """
    <section class="stack">
      <h2>%s</h2>
      <div class="stack-grid">%s</div>
      <div class="stack-note-row">%s<p>%s</p></div>
    </section>""" % (ph(d["stack_h2"]), cards, logo, ph(d["stack_note"]))


def section_call(d):
    """One panel per call. Two short, specific calls beat one long generic one:
    a buyer recognises their own situation faster in the one that matches it."""
    panels = ""
    for c in d["calls"]:
        rows = "".join(
            '<div class="t-row %s"><span class="t-spk">%s%s</span><p>%s</p></div>'
            % (who, SPK[who], GLYPH, ph(txt)) for who, txt in c["lines"])
        panels += """
      <p class="call-sub">%s<span>%s</span></p>
      <p class="call-caption">%s</p>
      <div class="call-panel">
        <div class="panel-head"><span class="ph-left"><span class="dot"></span>Live call - Sabato Agent</span>
          <span class="ph-time">· %s</span></div>
        %s
      </div>""" % (ICONS.get(c.get("icon"), ""), ph(c["label"]), ph(c["caption"]),
             ph(c["duration"]), rows)
    return """
    <section class="call-band">
      <h2>%s</h2>
      %s
      <p class="phone-note">%s</p>
    </section>""" % (ph(d["call_h2"]), panels, ph(d["call_note"]))


def section_results(d):
    cards = "".join(
        '<div class="res-card"><p class="res-num">%s</p><p class="res-lab">%s</p>'
        '<p class="res-sub">%s</p></div>' % (ph(n), ph(l), ph(s))
        for n, l, s in d["results"])
    return """
    <section class="results">
      <p class="eyebrow">%s</p>
      <h2>%s</h2>
      <div class="res-grid">%s</div>
      <p class="res-foot">%s</p>
    </section>""" % (ph(d["results_eyebrow"]), ph(d["results_h2"]), cards, ph(d["results_foot"]))


def section_quote(d):
    if d["photo"]:
        face = ('<img class="portrait" src="%s" alt="%s, %s at %s" width="720" height="720">'
                % (d["photo"], html.escape(d["person"]), html.escape(d["role"]),
                   html.escape(d["name"])))
    else:
        face = '<span class="mono-lg">%s</span>' % html.escape(d["person_initials"])
    pending = ('<p class="pending">Draft wording - awaiting written sign-off from %s</p>'
               % html.escape(d["person"])) if d.get("quote_pending") else ""
    return """
    <section class="pq">
      %s
      <div>
        <blockquote>%s</blockquote>
        <div class="who"><strong>%s</strong><span>%s, %s</span></div>
        %s
      </div>
    </section>""" % (face, ph(d["quote"]), html.escape(d["person"]),
                     html.escape(d["role"]), html.escape(d["name"]), pending)


def section_honest(d):
    items = "".join("<li>%s</li>" % ph(p) for p in d["honest_points"])
    return """
    <section class="honest">
      <h2>%s</h2>
      <p>%s</p>
      <ul>%s</ul>
    </section>""" % (ph(d["honest_h2"]), ph(d["honest_body"]), items)


def section_cta(d):
    return """
    <section class="cta-band">
      <h2>%s</h2>
      <p>%s</p>
      <a class="btn-pill" href="https://cal.com/sabatoai/intro" target="_blank" rel="noopener">%s</a>
    </section>""" % (ph(d["cta_h2"]), ph(d["cta_sub"]), LANGS[d["_lang"]]["cta"])


def jsonld(slug, d):
    """Only emit review/quote markup once the quote is real - marking up a
    placeholder as a genuine customer statement is exactly the kind of thing
    that gets a site penalised, and deserved."""
    if is_ph(d["quote"]) or d.get("quote_pending"):
        return "<!-- JSON-LD withheld: quote not approved -->"
    import json
    return '<script type="application/ld+json">%s</script>' % json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": plain(d["h1"]), "description": plain(d["description"]),
        "url": "https://www.sabato.ai%s" % (LANGS[d["_lang"]]["base"] % slug),
        "publisher": {"@type": "Organization", "name": "Sabato AI"},
    }, ensure_ascii=False)


def build(lang, slug, d):
    cfg = LANGS[lang]
    d["_lang"] = lang
    tpl = italian_template() if lang == "it" else open(cfg["tpl"], encoding="utf-8").read()
    mark = hero_mark(d)
    sections = "".join([
        section_situation(d), section_stack(d), section_call(d),
        section_results(d), section_quote(d), section_forward(d), section_cta(d),
    ])

    # An approved story drops the draft ribbon. Everything else on the page is
    # unchanged: the pages are still unlinked and still carry noindex until
    # Daniel decides how they should be reached.
    if d.get("approved"):
        tpl = re.sub(r'\s*<div class="draft-ribbon">[^<]*</div>', "", tpl)

    page = (tpl
            .replace("{{TITLE}}", html.escape(d["title"]))
            .replace("{{DESCRIPTION}}", html.escape(d["description"]))
            .replace("{{SLUG}}", slug)
            .replace("{{JSONLD}}", jsonld(slug, d) + hreflang(lang, slug, d))
            .replace("{{CHIP}}", ph(d["chip"]))
            .replace("{{MARK}}", mark)
            .replace("{{H1}}", ph(d["h1"]))
            .replace("{{SUB}}", ph(d["sub"]))
            .replace("{{SECTIONS}}", sections))
    os.makedirs(cfg["out"], exist_ok=True)
    p = os.path.join(cfg["out"], slug + ".html")
    open(p, "w", encoding="utf-8").write(page)
    n_ph = page.count('class="ph"')
    state = "approved" if d.get("approved") else "DRAFT"
    print("  wrote %-40s %-8s %d placeholder(s)" % (p, state, n_ph))
    return p


def hreflang(lang, slug, d):
    """Bidirectional alternates. A one-sided hreflang is worse than none: Google
    ignores the pair and may treat the two pages as duplicates."""
    en_slug = d["en"] if lang == "it" else slug
    it_slug = slug if lang == "it" else _IT_FOR_EN.get(slug)
    if not it_slug:
        return ""
    return ('<link rel="alternate" hreflang="en" href="https://www.sabato.ai/customers/%s">'
            '<link rel="alternate" hreflang="it" href="https://www.sabato.ai/it/clienti/%s">'
            '<link rel="alternate" hreflang="x-default" href="https://www.sabato.ai/customers/%s">'
            % (en_slug, it_slug, en_slug))


_IT_FOR_EN = {v["en"]: k for k, v in CUSTOMERS_IT.items()}


def main():
    for slug in ORDER:
        build("en", slug, CUSTOMERS[slug])
    for slug in ORDER_IT:
        build("it", slug, CUSTOMERS_IT[slug])
    print("\n%d page(s). Approved stories drop the ribbon; all stay noindex and\n"
          "unlinked until Daniel decides how they should be reached."
          % (len(ORDER) + len(ORDER_IT)))


if __name__ == "__main__":
    main()
