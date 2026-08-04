#!/usr/bin/env python3
"""Render every blog chart to a branded, shareable PNG.

Each `:::chart bar` figure already carries the Sabato mark and the
"© 2026 Sabato LTD · sabato.ai" credit inside the figure, so the credit
survives a screenshot or a right-click-save - not just a link. This tool
screenshots those figures at 2x into site/blog/charts/ (and site/it/blog/charts/)
so the "↓ PNG" button on each chart resolves to a real file.

Run after publish.py, before deploying:

    python3 tools/serve_like_netlify.py 8913 &
    python3 tools/render_chart_images.py http://127.0.0.1:8913
"""
import os
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8913"

# (url path, output dir, slug) for every post that contains a chart
def posts_with_charts():
    out = []
    for prefix, sub in (("/blog", "blog"), ("/it/blog", os.path.join("it", "blog"))):
        d = os.path.join(SITE, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".html"):
                continue
            p = os.path.join(d, fn)
            if 'class="chart-card"' not in open(p, encoding="utf-8").read():
                continue
            out.append((f"{prefix}/{fn[:-5]}", os.path.join(d, "charts"), fn[:-5]))
    return out


def main():
    targets = posts_with_charts()
    if not targets:
        print("no charts found")
        return 0

    written = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                              args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 1200, "height": 1400},
                            device_scale_factor=2)
        for url_path, out_dir, slug in targets:
            pg = ctx.new_page()
            pg.goto(BASE + url_path, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(1200)
            # hide the share row itself - it is UI, not part of the graphic
            pg.add_style_tag(content=".chart-share{display:none !important}"
                                     ".chart-card{background:#F8F4F1 !important}")
            figs = pg.query_selector_all("figure.chart-card")
            os.makedirs(out_dir, exist_ok=True)
            for i, fig in enumerate(figs, 1):
                dest = os.path.join(out_dir, f"{slug}-{i}.png")
                fig.scroll_into_view_if_needed()
                pg.wait_for_timeout(250)
                fig.screenshot(path=dest)
                written += 1
                print(f"  {os.path.relpath(dest, ROOT)}")
            pg.close()
        b.close()
    print(f"\n{written} chart image(s) written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
