#!/usr/bin/env python3
"""Regression test for the cold-load footer bug (reported 6 Aug 2026).

    python3 tools/test_footer_clicks.py http://127.0.0.1:8912

The bug: on a first, cold visit the footer use-case links did nothing; after a
reload they worked. Cause: those links ship as the "/#usecases" hook and only
become real destinations once enhance.js has run wireUseCaseTargets() AND that
rewrite has survived Framer's hydration. On a warm load enhance.js is in cache
and wins the race; on a cold load it does not.

A plain click test cannot catch that - locally enhance.js loads with zero
latency, so it always wins. This test instead RECREATES the losing state: it
puts every footer hook back to its pre-wiring href ("/#usecases", target and rel
stripped exactly as Framer would leave them) and only then clicks. If the click
still lands on the right page, the destination is being resolved at click time
and the fix does not depend on timing.

Run it against the same local server verify.sh uses.
"""
import sys
from playwright.sync_api import sync_playwright

# (page to load, visible label of a footer entry, where it must end up)
CASES = [
    ("/",       "Managing Returns",  "/use-cases/managing-returns"),
    ("/",       "Where Is My Order", "/use-cases/where-is-my-order"),
    ("/pricing", "Open a Complaint", "/use-cases/open-a-complaint"),
    ("/it",     "Gestione Resi",     "/it/casi-duso/gestione-resi"),
    # Alias case: the Italian footer says "Riepilogo Acquisto via SMS" while the
    # nav array's label is "Riepilogo Checkout via Messaggio".
    ("/it",     "Riepilogo Acquisto via SMS", "/it/casi-duso/riepilogo-checkout-via-messaggio"),
]

# Undo everything enhance.js does to the use-case links, so the click happens in
# exactly the state a cold visitor sees.
UNWIRE = """
(() => {
  let n = 0;
  document.querySelectorAll('a').forEach(a => {
    const h = a.getAttribute('href') || '';
    if (h.startsWith('/use-cases/') || h.startsWith('/it/casi-duso/')) {
      a.setAttribute('href', '/#usecases');
      a.removeAttribute('target'); a.removeAttribute('rel');
      n++;
    }
  });
  return n;
})()
"""


def main():
    base = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8912").rstrip("/")
    bad = 0
    with sync_playwright() as p:
        # Same launch as postdeploy_check.py - the container's Chromium lives at
        # a fixed path and needs --no-sandbox.
        browser = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                                    args=["--no-sandbox"])
        for path, label, expect in CASES:
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            page.goto(base + path, wait_until="networkidle")
            unwired = page.evaluate(UNWIRE)
            if not unwired:
                print(f"SKIP {path:9} '{label}' - nothing to unwire (page has no wired use-case links)")
                ctx.close()
                continue

            # Several nodes carry the same label: a hero paragraph, the footer
            # entry, and a zero-size copy inside the collapsed mobile nav. Only
            # the visible ones are clickable, and the footer is the last of them.
            all_hits = page.get_by_text(label, exact=True)
            visible = [all_hits.nth(i) for i in range(all_hits.count())
                       if all_hits.nth(i).is_visible()]
            if not visible:
                print(f"FAIL {path:9} '{label}' - no visible element with that label")
                bad += 1
                ctx.close()
                continue
            loc = visible[-1]
            try:
                loc.scroll_into_view_if_needed(timeout=3000)
                loc.click(timeout=3000)
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(400)
            except Exception as e:
                print(f"FAIL {path:9} '{label}' - could not click: {type(e).__name__}")
                bad += 1
                ctx.close()
                continue

            got = page.url[len(base):].split("?")[0].rstrip("/") or "/"
            if got == expect.rstrip("/"):
                print(f"ok   {path:9} '{label}' -> {got}   (after unwiring {unwired} link(s))")
            else:
                print(f"FAIL {path:9} '{label}' -> {got}   expected {expect}")
                bad += 1
            ctx.close()
        browser.close()

    print("\n" + ("COLD-LOAD FOOTER CLICKS OK" if not bad else f"{bad} failure(s)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
