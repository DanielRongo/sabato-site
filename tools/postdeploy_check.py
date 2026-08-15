#!/usr/bin/env python3
"""Post-deploy sanity sweep. Run after EVERY deploy:
   python3 tools/postdeploy_check.py https://delicate-valkyrie-20e427.netlify.app
Checks every page type for: duplicated nav items, missing logo, local 4xx,
console errors, and (where applicable) blog link / dropdown / footer wiring.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from customer_data import CUSTOMERS  # noqa: E402

# Names that must NOT appear on any page other than their own case study.
# Read from the data, not typed here - see the check that uses it.
UNAPPROVED = sorted(d["name"] for d in CUSTOMERS.values() if not d.get("promotable"))
# The pages the proof widget lives on, plus the two homepages. Anywhere a
# customer could plausibly be named by us rather than by their own page.
PROOF_PATHS = ("/", "/it", "/pricing", "/about", "/it/prezzi", "/it/chi-siamo")
# Slugs whose case study is allowed in the index. Same flag, same source.
PROMOTABLE_SLUGS = {s for s, d in CUSTOMERS.items() if d.get("promotable")}

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8909"
# Optional "start:end" slice. The full sweep is ~50 page loads with a 2.5s
# settle each, which now runs past the 10-minute ceiling on a single command in
# the Cowork container. Slicing lets the gate be run in two halves without
# weakening any individual check - it is a harness accommodation, not a shortcut.
SLICE = sys.argv[2] if len(sys.argv) > 2 else ""
PAGES = [
    "/product/voice-agent-builder", "/it/prodotto/voice-agent-builder",
    "/product/workflow-builder", "/it/prodotto/workflow-builder",
    "/product/call-data-intelligence", "/it/prodotto/call-data-intelligence",
    "/product/agent-evaluation", "/it/prodotto/agent-evaluation",
    "/product/integrations-webhooks", "/it/prodotto/integrations-webhooks","/", "/it", "/pricing", "/about", "/contact", "/blog", "/it/blog",
         # The Italian pricing and about pages were never swept until the proof
         # widget landed on them. Two more page loads, one more blind spot gone.
         "/it/prezzi", "/it/chi-siamo",
         "/use-cases", "/it/casi-duso",
         "/playbooks", "/it/playbook",
         "/blog/reduce-bracketing-returns", "/it/blog/reduce-bracketing-returns",
         "/blog/multilingual-phone-support-eu-expansion",
         "/it/blog/multilingual-phone-support-eu-expansion",
         "/blog/why-customers-call-instead-of-ordering-online",
         "/it/blog/why-customers-call-instead-of-ordering-online",
         "/blog/should-you-remove-the-phone-number",
         "/it/blog/should-you-remove-the-phone-number",
         "/blog/what-a-conversation-actually-costs",
         "/it/blog/what-a-conversation-actually-costs",
         "/blog/voice-agent-acceptance-test",
         "/it/blog/voice-agent-acceptance-test",
         "/blog/voice-ai-prototype-to-production",
         "/it/blog/voice-ai-prototype-to-production",
         "/use-cases/where-is-my-order", "/it/casi-duso/dove-e-il-mio-ordine",
         "/playbooks/peak-season", "/it/playbook/picchi-stagionali",
         "/playbooks/international-expansion",
         "/it/playbook/espansione-internazionale",
         "/playbooks/missed-calls", "/it/playbook/chiamate-perse",
         "/playbooks/support-costs", "/it/playbook/costi-assistenza",
         "/playbooks/high-value-work", "/it/playbook/attivita-di-valore",
         "/playbooks/multilingual-support", "/it/playbook/assistenza-multilingue",
         "/industries", "/industries/home-improvement", "/industries/fashion-apparel",
         "/it/settori", "/it/settori/clima-e-riscaldamento", "/it/settori/moda-abbigliamento",
         "/industries/automotive-parts", "/industries/electronics-tech",
         "/industries/furniture-home", "/industries/industrial-b2b",
         "/industries/outdoor-garden", "/industries/health-wellness",
         "/industries/sports-fitness",
         "/privacy-policy", "/roi-calculator",
         "/customers/clima-convenienza", "/it/clienti/clima-convenienza",
         "/customers/creative-cables", "/it/clienti/creative-cables"]

if SLICE.startswith("only:"):
    # only:/a,/b - check exactly these pages. Added so a single page can be
    # checked in two minutes instead of forty; it never writes a receipt, so
    # it cannot be mistaken for the full sweep.
    want = [x.strip() for x in SLICE[5:].split(",") if x.strip()]
    unknown = [w for w in want if w not in PAGES]
    if unknown:
        print("only: unknown page(s) %s - add them to PAGES first" % unknown)
        sys.exit(1)
    PAGES = want
    print("only -> %d page(s): %s" % (len(PAGES), ", ".join(PAGES)))
elif SLICE:
    _a, _b = (SLICE.split(":") + [""])[:2]
    PAGES = PAGES[int(_a or 0):int(_b) if _b else None]
    print("slice %s -> %d page(s)" % (SLICE, len(PAGES)))

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
                    "reb2b_gated": pg.evaluate("""(key) => {
                  // THE COMPLIANCE ASSERTION. A fresh visitor has given no
                  // consent, so the loader must be DEFINED and NOT CALLED.
                  // window.reb2b being set on a first load means the tag fired
                  // before anyone agreed to it - which is the exact failure a
                  // consent banner exists to prevent, and it is invisible to
                  // every other check here.
                  const inline = [...document.querySelectorAll('script')]
                    .filter(s => !s.src && (s.textContent || '').includes(key)).length;
                  return inline === 1 && typeof window.sbReb2b === 'function'
                         && !window.reb2b;
                }""", "5NRP9H3Q9YO1"),
                "no_cookies_before_consent": pg.evaluate("""() => {
                  // Same idea, measured at the browser rather than the tag:
                  // nothing in the _ga family may exist before a choice.
                  return !/(^|;\s*)_ga/.test(document.cookie);
                }"""),
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
                # The banner itself: present, visible on a first visit (no
                # stored choice), in the page's own language, and offering
                # reject at the same layer as accept. A banner that only shows
                # accept at the first layer is the violation regulators
                # actually fine people for.
                "consent_banner": pg.evaluate("""(want) => {
                  const b = document.getElementById('sb-consent');
                  if (!b || b.hidden) return false;
                  if (b.getAttribute('data-lang') !== want) return false;
                  const has = a => !!b.querySelector('[data-sb-c="' + a + '"]:not([hidden])');
                  return has('accept') && has('reject');
                }""", "it" if it else "en"),
                # Withdrawal must be reachable from every page, forever.
                "consent_reopen_link": pg.evaluate(
                    "!!document.querySelector('[data-sb-consent-open]')"),
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
                "reb2b_gated": pg.evaluate("""(key) => {
                  // THE COMPLIANCE ASSERTION. A fresh visitor has given no
                  // consent, so the loader must be DEFINED and NOT CALLED.
                  // window.reb2b being set on a first load means the tag fired
                  // before anyone agreed to it - which is the exact failure a
                  // consent banner exists to prevent, and it is invisible to
                  // every other check here.
                  const inline = [...document.querySelectorAll('script')]
                    .filter(s => !s.src && (s.textContent || '').includes(key)).length;
                  return inline === 1 && typeof window.sbReb2b === 'function'
                         && !window.reb2b;
                }""", "5NRP9H3Q9YO1"),
                "no_cookies_before_consent": pg.evaluate("""() => {
                  // Same idea, measured at the browser rather than the tag:
                  // nothing in the _ga family may exist before a choice.
                  return !/(^|;\s*)_ga/.test(document.cookie);
                }"""),
            }
            if not it and path in ("/", "/pricing", "/about", "/contact"):
                checks["dropdown_present"] = pg.evaluate("!!document.querySelector('[data-uc-dropdown]')")
            # A customer's name and metrics may appear off their own case study
            # ONLY once they have signed off on that specific use. The list is
            # not hand-maintained here: it is derived from `promotable` in
            # customer_data.py, so the day a flag flips the gate follows without
            # anyone remembering to edit this file. Creative Cables gave the
            # green light on 10 Aug 2026; ClimaConvenienza has not, and this is
            # the thing that keeps it off the homepage.
            # Also asserts enhance.js's old auto-injected band stays dead.
            # A case study is indexable if and only if the customer is
            # promotable. Both directions are asserted, because both directions
            # are expensive: an unapproved customer indexed is a trust problem
            # with a named company, and an approved one left noindex is the
            # thing that just cost eight days of a live case study earning
            # nothing. Read from the data, so flipping the flag moves the
            # assertion with it.
            if path.startswith("/customers/") or path.startswith("/it/clienti/"):
                slug = path.rsplit("/", 1)[1]
                want_index = slug in PROMOTABLE_SLUGS
                has_noindex = pg.evaluate(
                    """!!document.querySelector('meta[name="robots"][content*="noindex"]')""")
                checks["index_matches_permission"] = (has_noindex != want_index)
                if want_index:
                    checks["canonical_self"] = pg.evaluate("""(p) => {
                      const c = document.querySelector('link[rel=canonical]');
                      return !!c && c.href.replace('https://www.sabato.ai','') === p;
                    }""", path)
                    checks["jsonld_present"] = pg.evaluate(
                        """!!document.querySelector('script[type="application/ld+json"]')""")

            if path in PROOF_PATHS:
                # THE PHONE INVARIANT (regression, 11 Aug). At phone widths
                # Framer positions #main's children with CSS `order`, so a node
                # can be DOM-before the FAQ and still RENDER after the hero -
                # which is precisely what shipped. Every check here ran at
                # 1440px, where all orders are 0 and the bug cannot show. So
                # this one check drops to 390px and asserts the widget's
                # VISUAL position: below 40% of page height and above the FAQ.
                pg.set_viewport_size({"width": 390, "height": 900})
                pg.wait_for_timeout(1200)
                checks["proof_visual_mobile"] = pg.evaluate("""() => {
                  const w = document.querySelector('section.sb-proof');
                  if (!w) return false;
                  const top = w.getBoundingClientRect().top + scrollY;
                  let faq = null;
                  document.querySelectorAll('#main [data-framer-name]').forEach(e => {
                    if (!faq && (e.getAttribute('data-framer-name') || '')
                        .toLowerCase().trim().startsWith('faq section')) faq = e; });
                  const ftop = faq ? faq.getBoundingClientRect().top + scrollY : -1;
                  const b = w.getBoundingClientRect().bottom + scrollY;
                  // ADJACENCY, not a page fraction: a 40%-of-page floor failed
                  // /pricing, where the FAQ legitimately sits at 37%. What is
                  // actually required is that the widget ENDS just above where
                  // the FAQ begins - when flex `order` missorts it, that gap
                  // becomes thousands of pixels and this fails loudly.
                  return ftop > 0 && top < ftop
                      && (ftop - b) > -60 && (ftop - b) < 400;
                }""")
                pg.set_viewport_size({"width": 1440, "height": 900})
                pg.wait_for_timeout(600)

                checks["no_unapproved_customer"] = pg.evaluate(
                    """(names) => !document.querySelector('[data-sb-cust]')
                       && !names.some(n => document.body.innerText.includes(n))""",
                    UNAPPROVED)
            # A blog post that has a sibling in the other language must declare
            # it both ways. The visible language-switch link is for humans and
            # proves nothing to a crawler; blog posts shipped without these tags
            # for months while use-case pages had them.
            if "/blog/" in path:
                # A post WITH a sibling must declare it both ways. A post
                # WITHOUT one must declare nothing - a lone hreflang pointing at
                # a page that does not exist is worse than silence, and the
                # English-only Build File series made that case real rather than
                # hypothetical. publish.py already gets this right; this asserts
                # it stays right.
                checks["hreflang_pair"] = pg.evaluate("""(slug) => {
                  const a = {};
                  document.querySelectorAll('link[rel=alternate]').forEach(l => {
                    a[l.getAttribute('hreflang')] = (l.getAttribute('href')||'')
                      .replace('https://www.sabato.ai', ''); });
                  const en = '/blog/' + slug, it = '/it/blog/' + slug;
                  const solo = !document.querySelector('a[href="' + it + '"]')
                            && !document.querySelector('a[href="' + en + '"][data-lang-switch]');
                  if (Object.keys(a).length === 0) return solo;
                  return a.en === en && a.it === it && a['x-default'] === en;
                }""", path.rsplit("/", 1)[1])
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
# Skipped on a leading slice so it runs exactly once per full gate, not twice.
CLICKS = not SLICE or (not SLICE.startswith("only:")
          and (SLICE.split(":")[1:] == [""] or SLICE.endswith(":")))
print("\nclick-through checks:" if CLICKS else "\nclick-through: deferred to final slice")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    for src, label, expect in ([] if not CLICKS else [("/", "Managing Returns", "/use-cases/managing-returns"),
                               ("/", "Industrial & B2B", "/industries/industrial-b2b"),
                               ("/pricing", "Industries", "/industries"),
                               ("/it", "Automotive e Ricambi", "/it/settori/ricambi-auto"),
                               ("/it/blog", "Settori", "/it/settori"),
                               ("/blog", "Open a Complaint", "/use-cases/open-a-complaint"),
                               ("/use-cases/where-is-my-order", "Pre-Sales Consultation",
                                "/use-cases/pre-sales-consultation")]):
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
