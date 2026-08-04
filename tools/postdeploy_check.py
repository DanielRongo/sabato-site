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
         "/blog/reduce-bracketing-returns", "/it/blog/reduce-bracketing-returns",
         "/blog/multilingual-phone-support-eu-expansion",
         "/it/blog/multilingual-phone-support-eu-expansion",
         "/blog/why-customers-call-instead-of-ordering-online",
         "/it/blog/why-customers-call-instead-of-ordering-online",
         "/blog/should-you-remove-the-phone-number",
         "/it/blog/should-you-remove-the-phone-number",
         "/use-cases/where-is-my-order", "/it/casi-duso/dove-e-il-mio-ordine",
         "/industries", "/industries/home-improvement", "/industries/fashion-apparel",
         "/it/settori", "/it/settori/clima-e-riscaldamento", "/it/settori/moda-abbigliamento",
         "/industries/automotive-parts", "/industries/electronics-tech",
         "/industries/furniture-home", "/industries/industrial-b2b",
         "/industries/outdoor-garden", "/industries/health-wellness",
         "/industries/sports-fitness",
         "/privacy-policy", "/roi-calculator",
         "/customers/clima-convenienza", "/it/clienti/clima-convenienza",
         "/customers/creative-cables", "/it/clienti/creative-cables"]

NAV_COUNT_JS = """(label) => {
  let c = 0;
  document.querySelectorAll('a').forEach(a => {
    const r = a.getBoundingClientRect();
    if ((a.textContent||'').trim() === label && r.top >= 0 && r.top < 200 && r.height > 0) c++;
  });
  return c; }"""

# Blog lives in the FOOTER, not the header (right after Book a Demo / Prenota una
# Demo). Assert both halves: absent from the header, present exactly once in the
# footer, pointing at the right language and NOT opening in a new tab - the
# footer link is cloned from the cal.com demo button, which carries target=_blank.
BLOG_PLACEMENT_JS = """(expectedHref) => {
  const pageH = document.body.scrollHeight;
  let header = 0; const footer = [];
  document.querySelectorAll('a').forEach(a => {
    if ((a.textContent||'').trim() !== 'Blog') return;
    const r = a.getBoundingClientRect();
    if (r.height <= 0) return;
    const absTop = r.top + window.scrollY;
    if (r.top >= 0 && r.top < 200) header++;
    if (absTop > pageH * 0.6) footer.push({
      href: a.getAttribute('href'), target: a.getAttribute('target') });
  });
  return { header, footer };
}"""

failures = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    for path in PAGES:
        pg = ctx.new_page()
        errs, bad, ext = [], [], []
        # "Failed to load resource" carries no URL in its text, so it cannot be
        # attributed on its own. Collect those separately: if no local response
        # 4xx'd, the failure was third-party (a font CDN, an analytics beacon)
        # and is environmental, not a site defect. Re-running until green would
        # have hidden a real local 404 the same way.
        pg.on("console", lambda m: errs.append(m.text[:100]) if m.type == "error"
              and "ERR_" not in m.text and "framer.com/edit" not in m.text
              and "Failed to load resource" not in m.text else None)
        pg.on("console", lambda m: ext.append(m.text[:100]) if m.type == "error"
              and "Failed to load resource" in m.text else None)
        pg.on("response", lambda r: bad.append(f"{r.status} {r.url[-60:]}")
              if r.status >= 400 and BASE.split("//")[1].split("/")[0] in r.url else None)
        try:
            pg.goto(BASE + path, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(2500)

            # The ROI calculator is a standalone React tool page - no site
            # header, footer or nav by design, so the shared checks below do not
            # apply. What matters is that it actually mounts: a blank #root is
            # exactly how a broken asset path or a Babel failure presents.
            # It is UNLISTED: nothing on the site links to it and it carries
            # noindex, so the check also guards that it stays that way.
            if path == "/roi-calculator":
                checks = {
                    "noindex_present": pg.evaluate(
                        """!!document.querySelector('meta[name="robots"][content*="noindex"]')"""),
                    "app_mounted": pg.evaluate(
                        "!!document.querySelector('#root') && document.querySelector('#root').children.length > 0"),
                    "inputs_render": pg.evaluate("document.querySelectorAll('input').length >= 3"),
                    "logo_loads": pg.evaluate("""(() => {
                        const i = document.querySelector('img.brand-logo');
                        return !!i && i.naturalWidth > 0; })()"""),
                    "no_local_4xx": not bad,
                    "no_console_err": not errs,
                    "ga_tag_once": pg.evaluate("""(id) => {
                      const loaders = document.querySelectorAll(
                        'script[src*="googletagmanager.com/gtag/js?id=' + id + '"]').length;
                      const cfg = (window.dataLayer || []).filter(
                        a => Array.from(a || [])[0] === 'config').map(a => a[1]);
                      return loaders === 1 && cfg.length === 1 && cfg[0] === id;
                    }""", "G-BSK4KH9JJF"),
                }
                failed = {k: v for k, v in checks.items() if not v}
                if failed:
                    failures.append((path, failed, bad[:3], errs[:3]))
                    print(f"FAIL {path}: {list(failed)} {bad[:2]} {errs[:2]}")
                else:
                    print(f"ok   {path}")
                pg.close()
                continue

            it = path == "/it" or path.startswith("/it/")
            blog = pg.evaluate(BLOG_PLACEMENT_JS, "/it/blog" if it else "/blog")
            checks = {
                "blog_not_in_header": blog["header"] == 0,
                "blog_in_footer_x1": len(blog["footer"]) == 1,
                "blog_footer_href": bool(blog["footer"]) and
                    blog["footer"][0]["href"] == ("/it/blog" if it else "/blog"),
                "blog_footer_same_tab": bool(blog["footer"]) and
                    blog["footer"][0]["target"] != "_blank",
                "no_dup_nav": pg.evaluate(NAV_COUNT_JS, "Prezzi" if it else "Pricing") == 1,
                "logo_present": pg.evaluate(
                    "!!document.querySelector('img[src*=\"UTATYXc6\"], a[href=\"/\"] img, a[href=\"./\"] img')"),
                # unlisted means unlisted: no page may link to the calculator
                "roi_unlinked": pg.evaluate(
                    """!document.querySelector('a[href*="roi-calculator"]')"""),
                "no_local_4xx": not bad,
                "no_console_err": not errs,
                # GA4 must be present exactly once. Two loaders double-counts
                # every pageview; zero silently reports nothing at all.
                "ga_tag_once": pg.evaluate("""(id) => {
                  const loaders = document.querySelectorAll(
                    'script[src*="googletagmanager.com/gtag/js?id=' + id + '"]').length;
                  const cfg = (window.dataLayer || []).filter(
                    a => Array.from(a || [])[0] === 'config').map(a => a[1]);
                  return loaders === 1 && cfg.length === 1 && cfg[0] === id;
                }""", "G-BSK4KH9JJF"),
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

# click-through test: an href alone is not proof - Framer's router can intercept
print("\nclick-through checks:")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    for src, label, expect in [("/", "Managing Returns", "/use-cases/managing-returns"),
                               ("/", "Industrial & B2B", "/industries/industrial-b2b"),
                               ("/pricing", "Industries", "/industries"),
                               ("/it", "Automotive e Ricambi", "/it/settori/ricambi-auto"),
                               ("/it/blog", "Settori", "/it/settori"),
                               ("/blog", "Open a Complaint", "/use-cases/open-a-complaint"),
                               ("/use-cases/where-is-my-order", "Pre-Sales Consultation",
                                "/use-cases/pre-sales-consultation")]:
        pg = ctx.new_page()
        try:
            pg.goto(BASE + src, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(2800)
            loc = pg.locator(f'a:has-text("{label}")').filter(visible=True).last
            loc.scroll_into_view_if_needed()
            pg.wait_for_timeout(400)
            loc.click(timeout=8000)
            pg.wait_for_timeout(1800)
            landed = pg.url.replace(BASE, "")
        except Exception as e:
            landed = "ERR " + str(e)[:40]
        if landed != expect:
            failures.append((f"{src} click {label}", {"landed": landed, "expected": expect}, [], []))
            print(f"FAIL {src} click '{label}' -> {landed}")
        else:
            print(f"ok   {src} click '{label}' -> {landed}")
        pg.close()
    b.close()

print("\n" + ("ALL PAGES CLEAN" if not failures else f"{len(failures)} PAGE(S) FAILED"))
sys.exit(1 if failures else 0)
