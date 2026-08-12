#!/usr/bin/env python3
"""SVG type audit: is the text inside our graphics actually readable on a phone?

   python3 tools/svg_type_audit.py [base-url]

WHY THIS EXISTS
---------------
An inline SVG scales to its container. The font-size written in the source is
therefore NOT the size a human reads - it is multiplied by (rendered width /
viewBox width), and that factor is well under 1 on a phone, where the column is
narrow but the viewBox is still 560 units wide.

The international-expansion bar chart shipped its first draft with 15px labels.
On desktop that renders at ~13px and looks fine. On a 390px phone the same
labels render at 9.3px - too small to read, and the whole point of that block is
that the reader takes in two numbers.

Nothing else in this gate could see it:
  * contrast_audit.py measures colour, and never looks inside an <svg>;
  * scene_audit.py checks the industry scene geometry only, by name;
  * postdeploy_check.py reads the DOM, where the declared font-size is 15 and
    looks perfectly reasonable.

So this is the missing measurement: compute the real rendered pixel size of
every <text> node in every inline SVG, at phone width, and fail on anything a
person cannot read.

THE FLOOR
---------
11px. The smallest deliberate type on the site is the 12px `.fine` source line,
and that is already the floor for something nobody has to read closely. Chart
labels carry the argument, so they get no discount; 11px is set as the hard fail
so a decorative tick label does not block a deploy, while body-carrying labels
(which are never that small once fixed) stay well clear.

Decorative and structural text is exempt by intent, not by accident: a node
inside <defs>, or one that is invisible at this width, is not something a reader
is being asked to read.
"""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8909"

# Every page that carries a hand-drawn SVG with words in it.
PAGES = [
    "/playbooks/peak-season", "/it/playbook/picchi-stagionali",
    "/playbooks/international-expansion", "/it/playbook/espansione-internazionale",
]

FLOOR = 11.0
WIDTH = 390

# Walk every inline <svg>, work out its scale factor from the rendered width
# against the viewBox width, and report the true size of each <text>. Nested
# <svg> and transform= are handled by asking the browser for the actual screen
# CTM rather than trying to reimplement SVG's coordinate maths here.
JS = r"""(floor) => {
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
      // The screen CTM already folds in the viewBox scale AND any transform.
      let scale = 1;
      try {
        const m = t.getScreenCTM();
        if (m) scale = Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)) || 1;
      } catch (e) { /* getScreenCTM throws on a detached node */ }
      const real = declared * scale;
      if (real < floor) out.push({
        text: txt.slice(0, 48), declared: +declared.toFixed(1),
        scale: +scale.toFixed(3), real: +real.toFixed(1),
        label: svg.getAttribute('aria-label') ? 'labelled' : 'unlabelled',
      });
    });
  });
  return out;
}"""

failures = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                          args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": WIDTH, "height": 900})
    for path in PAGES:
        pg = ctx.new_page()
        try:
            pg.goto(BASE + path, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(1800)
            # Scroll the page so lazy content and any deferred layout settles -
            # a graphic measured before its column has its final width reports
            # a scale factor that no reader will ever experience.
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            pg.wait_for_timeout(900)
            pg.evaluate("window.scrollTo(0, 0)")
            pg.wait_for_timeout(400)
            small = pg.evaluate(JS, FLOOR)
        except Exception as e:
            small = [{"text": "ERROR " + str(e)[:60], "declared": 0,
                      "scale": 0, "real": 0, "label": "-"}]
        if small:
            failures.append((path, small))
            print("FAIL %s  - %d label(s) under %.0fpx at %dpx wide"
                  % (path, len(small), FLOOR, WIDTH))
            for s in small[:6]:
                print("       %5.1fpx  (%.0fpx x %.3f)  %r"
                      % (s["real"], s["declared"], s["scale"], s["text"]))
        else:
            print("ok   %s" % path)
        pg.close()
    b.close()

print("\n" + ("SVG TYPE CLEAN" if not failures
              else "%d PAGE(S) WITH UNREADABLE SVG TEXT" % len(failures)))
sys.exit(1 if failures else 0)
