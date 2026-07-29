#!/usr/bin/env python3
"""Post-deploy sanity sweep. Run after EVERY deploy:
   python3 tools/postdeploy_check.py https://delicate-valkyrie-20e427.netlify.app
Checks every page type for: duplicated nav items, missing logo, local 4xx,
console errors, and (where applicable) blog link / dropdown / footer wiring.
"""
import sys, json
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8909"
PAGES = ["/", "/it", "/pricing", "/about", "/contact", "/blog", "/it/blog",
         "/blog/what-wismo-calls-cost", "/it/blog/what-wismo-calls-cost",
         "/use-cases/where-is-my-order", "/privacy-policy"]

NAV_COUNT_JS = """(label) => {
  let c = 0;
  document.querySelectorAll('a').forEach(a => {
    const r = a.getBoundingClientRect();
    if ((a.textContent||'').trim() === label && r.top >= 0 && r.top < 200 && r.height > 0) c++;
  });
  return c; }"""

failures = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    for path in PAGES:
        pg = ctx.new_page()
        errs, bad = [], []
        pg.on("console", lambda m: errs.append(m.text[:100]) if m.type == "error"
              and "ERR_" not in m.text and "framer.com/edit" not in m.text else None)
        pg.on("response", lambda r: bad.append(f"{r.status} {r.url[-60:]}")
              if r.status >= 400 and BASE.split("//")[1].split("/")[0] in r.url else None)
        try:
            pg.goto(BASE + path, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(2500)
            it = path == "/it" or path.startswith("/it/")
            checks = {
                "blog_link_x1": pg.evaluate(NAV_COUNT_JS, "Blog") == 1,
                "no_dup_nav": pg.evaluate(NAV_COUNT_JS, "Prezzi" if it else "Pricing") == 1,
                "logo_present": pg.evaluate(
                    "!!document.querySelector('img[src*=\"UTATYXc6\"], a[href=\"/\"] img, a[href=\"./\"] img')"),
                "no_local_4xx": not bad,
                "no_console_err": not errs,
            }
            if not it and path in ("/", "/pricing", "/about", "/contact"):
                checks["dropdown_present"] = pg.evaluate("!!document.querySelector('[data-uc-dropdown]')")
            if not it:
                # every footer use-case link must point at its real page, not the old anchor
                checks["footer_uc_links"] = pg.evaluate("""(() => {
                  const labels = ['Pre-Sales Consultation','Cart Abandonment Recovery','Where Is My Order',
                    'Qualify & Collect for Quote','Open a Complaint','Checkout Summary via Text',
                    'Managing Returns','Post-Delivery Feedback','Back-in-Stock Notification'];
                  let found = 0, bad = 0;
                  document.querySelectorAll('a').forEach(a => {
                    const t = (a.textContent||'').trim();
                    if (!labels.includes(t)) return;
                    found++;
                    const h = a.getAttribute('href') || '';
                    if (!h.startsWith('/use-cases/')) bad++;
                  });
                  return found > 0 && bad === 0; })()""")
            failed = {k: v for k, v in checks.items() if not v}
            if failed:
                failures.append((path, failed, bad[:3], errs[:3]))
                print(f"FAIL {path}: {list(failed)} {bad[:2]} {errs[:2]}")
            else:
                print(f"ok   {path}")
        except Exception as e:
            failures.append((path, str(e)[:100], [], []))
            print(f"FAIL {path}: {e}")
        pg.close()
    b.close()

print("\n" + ("ALL PAGES CLEAN" if not failures else f"{len(failures)} PAGE(S) FAILED"))
sys.exit(1 if failures else 0)
