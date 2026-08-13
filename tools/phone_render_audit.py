#!/usr/bin/env python3
"""Phone render audit: the two defects that only exist below 810px.

   python3 tools/phone_render_audit.py [base-url]

Everything else in this gate reasons about the DOM, or renders at 1440px. Both
bugs below pass every one of those checks and are obvious the moment a human
picks up a phone. Supersedes tools/svg_type_audit.py, which only did the first.

1. SVG TEXT TOO SMALL TO READ
-----------------------------
An inline SVG scales to its container, so the font-size in the source is NOT the
size anybody reads - it is multiplied by (rendered width / viewBox width), and
that factor is ~0.61 on a 390px phone where the column is narrow but the viewBox
is still 560 units wide.

The international-expansion bar chart shipped its first draft at 15px labels:
~13px on desktop, 9.3px on a phone. The peak-season hero calendar had been live
for a week at 7.3px. Nothing saw either one - contrast_audit.py measures colour
and never descends into an <svg>, scene_audit.py checks the industry scenes by
name, and postdeploy_check.py reads the DECLARED font-size, which looks fine.

Floor is 11px. The smallest deliberate type on the site is the 12px `.fine`
source line, and that is already the floor for something nobody reads closely.

2. THE PAGE SCROLLS SIDEWAYS
----------------------------
`.nb { white-space: nowrap }` is global and has no phone override, so [nb] round
a phrase that cannot fit the narrowest column it will ever occupy forces the
document wider than the viewport. The international-expansion h1 did exactly
this: "Answer in five languages." at the 37px phone h1 size is 430px wide on a
390px screen, and the whole page scrolled horizontally.

scrollWidth vs clientWidth is the right signal rather than hunting for elements
past the right edge: the homepage logo marquee legitimately parks items at
x=-927 inside an overflow:hidden track, and an element-level test flags it every
time. The document-level test is clean on every page that is actually fine.
"""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8909"

# Our hand-written markup, both languages, one of each page type. Framer's own
# sections are covered incidentally - they appear on every page here.
PAGES = [
    "/", "/it",
    "/playbooks/peak-season", "/it/playbook/picchi-stagionali",
    "/playbooks/international-expansion", "/it/playbook/espansione-internazionale",
    "/playbooks/missed-calls", "/it/playbook/chiamate-perse",
    "/playbooks/support-costs", "/it/playbook/costi-assistenza",
    "/playbooks/high-value-work", "/it/playbook/attivita-di-valore",
    "/playbooks/multilingual-support", "/it/playbook/assistenza-multilingue",
    "/customers/creative-cables", "/it/clienti/creative-cables",
    "/blog/multilingual-phone-support-eu-expansion",
    "/it/blog/multilingual-phone-support-eu-expansion",
    "/pricing", "/it/prezzi",
]

# KNOWN DEBT, 12 Aug 2026 - reported every run, never fails the gate.
#
# The first run of this audit found the same bug already live on the use-case
# and industry scene illustrations: labels down to 5.8px on a phone, because
# those scenes are drawn in a ~1000-unit viewBox that renders into a ~486px
# column. Fixing them is a real piece of work - the scenes are dense, the labels
# are positioned against artwork, and scene_audit.py checks that geometry, so
# every label that grows has to be re-fitted and re-checked.
#
# Blocking the gate on debt this audit itself discovered would mean the tool
# that found the problem is the tool that stops the unrelated fix from shipping.
# So these are WARNED, loudly, with a count - not silently dropped and not
# fatal. When the scenes are redrawn, move the entries up into PAGES.
BACKLOG = [
    "/use-cases/where-is-my-order", "/it/casi-duso/dove-e-il-mio-ordine",
    "/industries/fashion-apparel", "/it/settori/moda-abbigliamento",
]

FLOOR = 11.0
WIDTH = 390

SVG_JS = r"""(floor) => {
  const out = [];
  document.querySelectorAll('svg').forEach(svg => {
    const r = svg.getBoundingClientRect();
    if (!r.width || !r.height) return;                 // not rendered at all
    svg.querySelectorAll('text, tspan').forEach(t => {
      const txt = (t.textContent || '').trim();
      if (!txt) return;
      if (t.closest('defs, clipPath, mask')) return;   // never painted
      const tr = t.getBoundingClientRect();
      if (!tr.width || !tr.height) return;             // hidden at this width
      const declared = parseFloat(getComputedStyle(t).fontSize) || 0;
      // The screen CTM already folds in the viewBox scale AND any transform,
      // so we do not reimplement SVG coordinate maths here.
      let scale = 1;
      try {
        const m = t.getScreenCTM();
        if (m) scale = Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)) || 1;
      } catch (e) { /* getScreenCTM throws on a detached node */ }
      const real = declared * scale;
      if (real < floor) out.push({
        text: txt.slice(0, 44), declared: +declared.toFixed(1),
        scale: +scale.toFixed(3), real: +real.toFixed(1),
      });
    });
  });
  return out;
}"""

# When the document IS too wide, name the widest offenders so the fix is one
# edit rather than a hunt. Only consulted after the document-level test fails.
OVERFLOW_JS = r"""() => {
  const cw = document.documentElement.clientWidth;
  const sw = document.documentElement.scrollWidth;
  const blame = [];
  if (sw > cw) {
    document.querySelectorAll('body *').forEach(e => {
      const r = e.getBoundingClientRect();
      if (r.width > 0 && r.right > cw + 1) {
        blame.push({ el: (e.tagName + '.' + (e.className || '')).slice(0, 52),
                     right: Math.round(r.right),
                     text: (e.textContent || '').trim().slice(0, 40) });
      }
    });
  }
  return { sw, cw, blame: blame.slice(0, 5) };
}"""

failures = []
warned = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                          args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": WIDTH, "height": 900})
    for path in PAGES + BACKLOG:
        known = path in BACKLOG
        pg = ctx.new_page()
        bad = []
        try:
            pg.goto(BASE + path, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(1800)
            # Settle lazy content and any deferred layout - a graphic measured
            # before its column has its final width reports a scale factor no
            # reader will ever experience.
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            pg.wait_for_timeout(900)
            pg.evaluate("window.scrollTo(0, 0)")
            pg.wait_for_timeout(400)

            for s in pg.evaluate(SVG_JS, FLOOR):
                bad.append("svg-type %5.1fpx (%.0f x %.3f) %r"
                           % (s["real"], s["declared"], s["scale"], s["text"]))
            o = pg.evaluate(OVERFLOW_JS)
            if o["sw"] > o["cw"]:
                bad.append("h-scroll scrollWidth=%d > clientWidth=%d"
                           % (o["sw"], o["cw"]))
                for x in o["blame"]:
                    bad.append("         %s  right=%d  %r"
                               % (x["el"], x["right"], x["text"]))
        except Exception as e:
            bad.append("ERROR " + str(e)[:70])
        if bad and known:
            warned.append((path, len(bad)))
            print("WARN %s  - %d known issue(s), see BACKLOG in this file" % (path, len(bad)))
        elif bad:
            failures.append(path)
            print("FAIL %s" % path)
            for line in bad[:8]:
                print("       " + line)
        else:
            print("ok   %s" % path)
        pg.close()
    b.close()

if warned:
    print("\nKNOWN DEBT (not fatal): %d page(s), %d issue(s) - the use-case and"
          % (len(warned), sum(n for _, n in warned)))
    print("industry scene illustrations have labels as small as 5.8px on a phone.")
    print("Not silently ignored: listed in BACKLOG at the top of this file.")

print("\n" + ("PHONE RENDER CLEAN" if not failures
              else "%d PAGE(S) BROKEN AT %dpx" % (len(failures), WIDTH)))
sys.exit(1 if failures else 0)
