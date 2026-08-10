#!/usr/bin/env python3
"""Check every industry scene, in both languages, for unreadable text.

    python3 tools/scene_audit.py            # all nine, en + it
    python3 tools/scene_audit.py sports     # one

WHY THIS EXISTS
---------------
The bike scene shipped with "reach 389" drawn straight across the frame's top
tube - dark text on dark strokes, unreadable. It passed every check we had,
because the checks asked "does the text fit on the canvas" and the answer was
yes. Fitting is not the same as being readable.

It also only ever looked at English. Italian strings are longer - "PREVENTIVO
IN" against "QUOTE IN", "pendenza sul retro 22%" against "slope at rear 22%" -
so the language that was never checked is the one most likely to collide.

WHAT IT FLAGS
-------------
  OFF-CANVAS   a glyph box crossing the 720x300 edge
  TEXT/TEXT    two text boxes overlapping each other
  TEXT/INK     a dark text box sitting on a dark shape - the bike case

Rendered geometry, not guesses: it measures getBBox() in a real browser with
the real font, so a word that only collides once Satoshi loads is still caught.
"""
import subprocess
import sys
import time

PORT = 8937
DARK = ("rgb(18, 10, 11)", "rgb(69, 65, 64)", "rgb(12, 12, 12)")

JS = r"""() => {
  const sv = document.querySelector('.scene');
  if (!sv) return {err: 'no .scene'};
  const vb = sv.viewBox.baseVal;
  const box = e => { const b = e.getBBox(); return {x:b.x, y:b.y, w:b.width, h:b.height}; };
  const hit = (a, b) => !(a.x + a.w <= b.x || b.x + b.w <= a.x ||
                          a.y + a.h <= b.y || b.y + b.h <= a.y);
  const shrink = (b, p) => ({x:b.x+p, y:b.y+p, w:Math.max(0,b.w-2*p), h:Math.max(0,b.h-2*p)});

  const texts = [...sv.querySelectorAll('text')].map(t => ({
      s: t.textContent.trim(), b: box(t), fill: getComputedStyle(t).fill}));
  // Shapes that paint dark. A stroked path counts: the bike frame is strokes.
  // A dark FILL under the text is unreadable. A dark STROKE is just an outline -
  // the room plan, the RFQ card and the subscription box are all outlines with
  // perfectly readable text inside them, and treating their bounding box as
  // solid flagged 36 false positives on the first run.
  const isDark = c => c && c !== 'none' &&
      (c.startsWith('rgb(18') || c.startsWith('rgb(12') || c.startsWith('rgb(0,'));
  const inks = [...sv.querySelectorAll('path,rect,circle,line,polygon')].map(e => {
      const cs = getComputedStyle(e);
      return {t: e.tagName, b: box(e), filled: isDark(cs.fill),
              stroked: isDark(cs.stroke), sw: parseFloat(cs.strokeWidth) || 0};
  }).filter(e => e.filled || e.stroked);

  // The answer card is x=500..676. Anything drawn inside it has 152px before it
  // runs under the rounded corner - and the Italian notes are longer than the
  // English ones, which is how "prezzo contrattuale applicato" ended up clipped
  // while its English twin fitted.
  const CARD = {x: 500, r: 676};
  const clipped = [];
  const off = [], tt = [], ti = [];
  texts.forEach((t, i) => {
    if (t.b.x < -0.5 || t.b.y < -0.5 ||
        t.b.x + t.b.w > vb.width + 0.5 || t.b.y + t.b.h > vb.height + 0.5)
      off.push(t.s);
    if (t.b.x >= CARD.x && t.b.x + t.b.w > CARD.r - 12)
      clipped.push(t.s + '  (' + Math.round(t.b.x + t.b.w - (CARD.r - 12)) + 'px over)');
    for (let j = i + 1; j < texts.length; j++)
      if (hit(shrink(t.b,1), shrink(texts[j].b,1))) tt.push(t.s + '  ><  ' + texts[j].s);
    // Only dark text on dark shapes is a readability problem; the lime and the
    // white-on-black card are deliberate.
    const darkText = ['rgb(18, 10, 11)','rgb(69, 65, 64)','rgb(12, 12, 12)'].includes(t.fill);
    if (!darkText) return;
    const inside = (a, b, pad) => a.x >= b.x + pad && a.y >= b.y + pad &&
                                  a.x + a.w <= b.x + b.w - pad && a.y + a.h <= b.y + b.h - pad;
    inks.forEach(s => {
      if (s.b.w > 400 && s.b.h > 200) return;          // the canvas backdrop
      if (s.b.w < 1 && s.b.h < 1) return;
      if (!hit(shrink(t.b,1.5), shrink(s.b,1.5))) return;
      // Outline only: fine as long as the text clears the stroke band.
      if (!s.filled && inside(t.b, s.b, s.sw + 2)) return;
      ti.push(t.s + '  on  <' + s.t + (s.filled ? ' filled>' : ' stroke>'));
    });
  });
  return {off, tt, clipped, ti: [...new Set(ti)]};
}"""


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    sys.path.insert(0, __file__.rsplit("/tools/", 1)[0])
    import industry_data as en
    import industry_data_it as it
    pages = []
    for slug, d in en.INDUSTRIES.items():
        if only and d["scene"] != only:
            continue
        pages.append(("en", d["scene"], f"/industries/{slug}"))
    for slug, d in it.INDUSTRIES_IT.items():
        if only and d["scene"] != only:
            continue
        pages.append(("it", d["scene"], f"/it/settori/{slug}"))

    srv = subprocess.Popen([sys.executable, "tools/serve_like_netlify.py", str(PORT)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
    bad = 0
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                                   args=["--no-sandbox"])
            pg = br.new_page(viewport={"width": 1440, "height": 900})
            for lang, kind, path in pages:
                pg.goto(f"http://127.0.0.1:{PORT}{path}", wait_until="load", timeout=40000)
                pg.evaluate("() => document.fonts.ready")
                pg.wait_for_timeout(900)
                r = pg.evaluate(JS)
                probs = []
                for x in r.get("off", []):
                    probs.append(f"OFF-CANVAS  {x}")
                for x in r.get("clipped", []):
                    probs.append(f"CARD-CLIP   {x}")
                for x in r.get("tt", []):
                    probs.append(f"TEXT/TEXT   {x}")
                for x in r.get("ti", []):
                    probs.append(f"TEXT/INK    {x}")
                if probs:
                    bad += len(probs)
                    print(f"\n  {kind} [{lang}]")
                    for x in probs:
                        print(f"     {x}")
            br.close()
    finally:
        srv.terminate()

    print(f"\n{'SCENE AUDIT CLEAN' if not bad else str(bad) + ' problem(s)'}"
          f"  -  {len(pages)} scene renders checked")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
