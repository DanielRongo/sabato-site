#!/usr/bin/env python3
"""Contrast audit: WCAG AA on every text-bearing element of a page.

   python3 tools/contrast_audit.py /blog/some-post [/another/page ...]
   python3 tools/contrast_audit.py --base https://example.com /page

Why this exists: a style diff proves two pages *declare* the same colours. Only
a contrast audit proves a human can read them. Two invisible-text bugs shipped
here before this was a script - ink-on-black in a band whose body colour was
scoped to a selector chain the markup didn't have, and a 1.07:1 panel on a page
built from a stale copy of a stylesheet.

Climbs to the first opaque ancestor for the background, so it survives nested
transparent wrappers. Large text (>=24px, or >=18.66px bold) needs 3:1;
everything else needs 4.5:1.
"""
import sys
from playwright.sync_api import sync_playwright

JS = r"""() => {
  const lum = c => { const s = c.map(v => { v /= 255;
    return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
    return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2]; };
  const parse = s => { const m = (s||'').match(/[\d.]+/g);
    return m ? m.slice(0,4).map(Number) : null; };
  const bgOf = el => {
    let n = el;
    while (n && n !== document.documentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && (c.length < 4 || c[3] > 0.95)) return c.slice(0,3);
      n = n.parentElement;
    }
    return [255,255,255];
  };
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    // Skip SVG. Two reasons, and both produce false alarms if ignored: SVG text
    // paints with `fill`, not CSS `color`, and its background is a sibling
    // <rect> rather than an ancestor, so climbing the tree finds the band behind
    // the whole chart instead of the bar behind the label. This tool cannot
    // judge charts - check those on a screenshot. A checker that cries wolf on
    // every chart gets ignored on the one page where it was right.
    if (el.namespaceURI === 'http://www.w3.org/2000/svg') return;
    let txt = '';
    el.childNodes.forEach(n => { if (n.nodeType === 3) txt += n.textContent; });
    txt = txt.trim();
    if (txt.length < 2) return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return;
    const fg = parse(cs.color).slice(0,3), bg = bgOf(el);
    const L1 = lum(fg), L2 = lum(bg);
    const ratio = (Math.max(L1,L2)+0.05) / (Math.min(L1,L2)+0.05);
    const size = parseFloat(cs.fontSize);
    const large = size >= 24 || (size >= 18.66 && (+cs.fontWeight) >= 700);
    const need = large ? 3 : 4.5;
    if (ratio < need) out.push({t: txt.slice(0,50), ratio: +ratio.toFixed(2),
      need, size, fg, bg});
  });
  return out;
}"""

args = sys.argv[1:]
base = "http://127.0.0.1:8909"
if args and args[0] == "--base":
    base = args[1].rstrip("/")
    args = args[2:]
if not args:
    sys.exit("usage: contrast_audit.py [--base URL] /path [/path ...]")

fails = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                          args=["--no-sandbox"])
    for width in (1440, 390):
        ctx = b.new_context(viewport={"width": width, "height": 900})
        for path in args:
            pg = ctx.new_page()
            pg.goto(base + path, wait_until="networkidle", timeout=60000)
            pg.wait_for_timeout(1200)
            bad = pg.evaluate(JS)
            tag = f"{path} @{width}"
            if bad:
                fails += len(bad)
                print(f"FAIL {tag}: {len(bad)}")
                for x in bad[:10]:
                    print(f"     {x['ratio']}:1 (needs {x['need']}) "
                          f"{x['size']}px fg={x['fg']} bg={x['bg']}  {x['t']!r}")
            else:
                print(f"ok   {tag}")
            pg.close()
        ctx.close()
    b.close()
print("\n" + ("CONTRAST CLEAN" if not fails else f"{fails} FAILING ELEMENT(S)"))
sys.exit(1 if fails else 0)
