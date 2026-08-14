# assets-src

Sources for the raster assets under `site/**/assets/`. **Outside `site/` on
purpose**: `tools/inject_ga.py`, `inject_reb2b.py` and `inject_consent.py` all
glob `site/**/*.html`, so a source file left in there would be injected with
analytics tags, a consent banner and a marketing pixel, and then re-rendered
into the screenshot. It would also be publicly served.

## voice-agent-builder.html

The Sabato agent designer, rebuilt rather than screenshotted. Anonymised: no
customer name, no real user, no vendor names, and the system message is written
for the fictional "Northaven Home" rather than copied from a live account.

Re-render after any platform UI change:

    python3 - <<'PY'
    from playwright.sync_api import sync_playwright
    from PIL import Image
    OUT = "site/product/assets"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                              args=["--no-sandbox"])
        pg = b.new_page(viewport={"width":1560,"height":796}, device_scale_factor=2)
        pg.goto("file://" + __import__("os").path.abspath("assets-src/voice-agent-builder.html"))
        pg.wait_for_timeout(800)
        pg.screenshot(path="/tmp/wide.png")
        box = pg.locator(".stage").bounding_box(); pad = 34
        pg.screenshot(path="/tmp/phone.png", clip={"x":box["x"]-pad,"y":box["y"]-pad,
            "width":box["width"]+pad*2,"height":box["height"]+pad*2})
        b.close()
    Image.open("/tmp/wide.png").save(OUT+"/voice-agent-builder.webp","WEBP",quality=90,method=6)
    Image.open("/tmp/phone.png").save(OUT+"/voice-agent-builder-phone.webp","WEBP",quality=90,method=6)
    PY

The phone crop is a DIFFERENT PICTURE, not the wide shot scaled. At 390px the
content column is ~346px, so the wide shot renders at 0.22x and its 12px UI
labels land under 3px. `tools/phone_render_audit.py` exists because that class
of bug shipped twice.

Fonts: Inter and JetBrains Mono. A fresh container has neither - install into
`~/.fonts` and run `fc-cache -f` before re-rendering, or the shot falls back to
DejaVu and stops looking like the product.
