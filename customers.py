#!/usr/bin/env python3
"""Build the customer story pages.

    python3 customers.py

Renders site/customers/<slug>.html from templates/customer.html using the
content in customer_data.py. Sections are composed from the classes the
use-case pages already define, so these pages inherit the design system rather
than restating it — the only new CSS lives in the template.

Draft handling: any [[bracketed]] string becomes a loud orange TBC chip, and
every page carries noindex + a DRAFT ribbon until Daniel has written sign-off on
the figures and the quotes. See customer_data.py for why that matters.
"""
import html
import os
import re

from customer_data import CUSTOMERS, ORDER

TPL = "templates/customer.html"
OUT = "site/customers"

PH_RX = re.compile(r"\[\[(.+?)\]\]", re.DOTALL)


NB_RX = re.compile(r"\b([eE]-[cC]ommerce)\b")


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
    return NB_RX.sub(r'<span class="nb">\1</span>', "".join(out))


def is_ph(text):
    return bool(PH_RX.search(text))



_IW = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="rgb(204,255,0)" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>')

ICONS = {
    # globe with a speech tail — multilingual
    "languages": _IW % ('<circle cx="11" cy="11" r="7.5"/><path d="M3.5 11h15"/>'
                        '<path d="M11 3.5c2 2.4 3 5 3 7.5s-1 5.1-3 7.5"/>'
                        '<path d="M11 3.5c-2 2.4-3 5-3 7.5s1 5.1 3 7.5"/>'),
    # parcel in transit — where is my order
    "wismo": _IW % ('<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/>'
                    '<path d="M3 7.5 12 12l9-4.5"/><path d="M12 12v9"/>'),
    # sliders — configurator
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


def hero_visual(d):
    """Monogram + name card. Swapped for the real logo when we have the asset."""
    if d["logo"]:
        mark = '<img class="cust-logo" src="%s" alt="%s" width="640" height="97">' % (
            d["logo"], html.escape(d["name"]))
    else:
        mark = ('<span class="cust-logo-fallback"><span class="mono">%s</span>%s</span>'
                % (html.escape(d["initials"]), html.escape(d["name"])))
    rows = "".join(
        '<div class="t-row %s"><span class="t-spk">%s%s</span><p>%s</p></div>'
        % (who, SPK[who], GLYPH, ph(txt)) for who, txt in d["calls"][0]["lines"][:3])
    return ('<div class="call-panel" style="max-width:none">'
            '<div class="panel-head"><span class="ph-left"><span class="dot"></span>'
            'Live call — Sabato Agent</span><span class="ph-time">· 01:12</span></div>'
            '%s</div>' % rows), mark


def section_situation(d):
    # The body colour on this band is scoped to `.queue-grid .qcopy .qbody` in
    # the use-case stylesheet. Reusing `.queue-band` without reproducing that
    # exact ancestor chain silently renders ink-on-black — which is how the
    # first draft of this page came out unreadable. Match their markup, don't
    # patch the colour.
    cards = "".join(
        '<div class="stack-card"><h3>%s</h3><p>%s</p></div>' % (ph(t), ph(b))
        for t, b in d["situation_points"])
    body = "".join('<p class="qbody">%s</p>' % ph(p) for p in d["situation_body"])
    shot = ""
    cls = "queue-grid"
    if d.get("storefront"):
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
        <div class="panel-head"><span class="ph-left"><span class="dot"></span>Live call — Sabato Agent</span>
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
    pending = ('<p class="pending">Draft wording — awaiting written sign-off from %s</p>'
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
      <a class="btn-pill" href="https://cal.com/sabatoai/intro" target="_blank" rel="noopener">Start Free Pilot</a>
    </section>""" % (ph(d["cta_h2"]), ph(d["cta_sub"]))


def jsonld(slug, d):
    """Only emit review/quote markup once the quote is real — marking up a
    placeholder as a genuine customer statement is exactly the kind of thing
    that gets a site penalised, and deserved."""
    if is_ph(d["quote"]) or d.get("quote_pending"):
        return "<!-- JSON-LD withheld: quote not approved -->"
    import json
    return '<script type="application/ld+json">%s</script>' % json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": d["h1"], "description": d["description"],
        "url": "https://www.sabato.ai/customers/%s" % slug,
        "publisher": {"@type": "Organization", "name": "Sabato AI"},
    }, ensure_ascii=False)


def build(slug, d):
    tpl = open(TPL, encoding="utf-8").read()
    visual, mark = hero_visual(d)
    sections = "".join([
        section_situation(d), section_stack(d), section_call(d),
        section_results(d), section_quote(d), section_cta(d),
    ])
    page = (tpl
            .replace("{{TITLE}}", html.escape(d["title"]))
            .replace("{{DESCRIPTION}}", html.escape(d["description"]))
            .replace("{{SLUG}}", slug)
            .replace("{{JSONLD}}", jsonld(slug, d))
            .replace("{{CHIP}}", ph(d["chip"]))
            .replace("{{MARK}}", mark)
            .replace("{{H1}}", ph(d["h1"]))
            .replace("{{SUB}}", ph(d["sub"]))
            .replace("{{HERO_VISUAL}}", visual)
            .replace("{{SECTIONS}}", sections))
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, slug + ".html")
    open(p, "w", encoding="utf-8").write(page)
    n_ph = page.count('class="ph"')
    print("  wrote %-34s %d placeholder(s)" % (p, n_ph))
    return p


def main():
    for slug in ORDER:
        build(slug, CUSTOMERS[slug])
    print("\n%d customer page(s). All noindex + DRAFT until sign-off." % len(ORDER))


if __name__ == "__main__":
    main()
