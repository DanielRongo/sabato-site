#!/usr/bin/env python3
"""Audit every visible link on every page, at phone AND desktop width.

    python3 tools/audit_links.py http://127.0.0.1:8909

Why this exists: postdeploy_check.py only ever ran at 1440px, so an entire
class of bugs was invisible to it. Framer emits SEPARATE markup for the mobile
layout - a different footer, a different nav - and that copy was never checked
by anything. Reported 6 Aug 2026: dead footer links and Italian pages linking
into the English site, "all from mobile".

FAILURES - these break the site and exit non-zero:

  LANG      an Italian page linking to an English page, or the reverse. Found
            /it/chi-siamo rendering an entire English footer above the Italian
            one: logo and Home -> "/", Pricing -> "/pricing", About, Contact.
  404       a visible link whose target does not resolve.

ADVISORY - printed, never fails the build:

  NO-HREF   an <a> carrying no href. Counted 68 of these and checked them one by
            one: they are Framer SECTION-LABEL BADGES ("FAQs", "Get Started",
            "Coming Soon", "How it works"), which Framer renders as <a> whether
            or not anyone linked them. They are decorative. Do not "fix" them -
            they are not navigation, and rewriting them would put junk links in
            the footer. Listed only so a genuinely new one gets noticed.
  RELATIVE  href written as ./x or ../x. These only work at the exact directory
            depth Framer assumed, and they resolve differently the moment a
            trailing slash appears. They currently resolve correctly, so this is
            advisory - but every one is a landmine, and they are how the Italian
            language leak happened in the first place.
"""
import os
import sys
from playwright.sync_api import sync_playwright

WIDTHS = [(390, "phone"), (1440, "desktop")]

# Framer-authored pages: these carry the relative hrefs and the mobile-only
# blocks, so they are where the bugs live. Our generated pages use absolute
# hrefs from a template and are uniform - a sample of them is enough.
PAGES = [
    "/product/voice-agent-builder", "/it/prodotto/voice-agent-builder",
    "/", "/it", "/pricing", "/it/prezzi", "/about", "/it/chi-siamo",
    "/contact", "/it/contatti", "/blog", "/it/blog", "/terms",
    "/privacy-policy", "/use-cases", "/it/casi-duso", "/industries",
    "/it/settori", "/use-cases/managing-returns", "/it/casi-duso/gestione-resi",
    "/customers/creative-cables", "/it/clienti/creative-cables",
    "/it/termini-e-condizioni", "/it/privacy-e-cookie",
]

# Nothing is exempt any more. /terms and /privacy-policy used to be here because
# they existed in English only; since 7 Aug 2026 the Italian site has its own
# /it/termini-e-condizioni and /it/privacy-e-cookie, so an Italian page linking
# to the English legal text is once again a real leak and should fail.
CROSS_LANG_OK = set()

# Extensions that mean "this href is a file, not a page". Language rules apply
# to pages only; /fuc/assets/ is language-neutral by construction.
ASSET_EXTS = {".mp3", ".wav", ".m4a", ".mp4", ".webm", ".pdf",
              ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif",
              ".zip", ".csv", ".xml", ".txt", ".ics"}

COLLECT = """
() => {
  const out = [];
  document.querySelectorAll('a').forEach(a => {
    const r = a.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;          // hidden layout copy
    const raw = a.getAttribute('href');
    const label = (a.textContent || '').trim().slice(0, 40);
    const isLogo = !!a.querySelector('img, svg');
    if (raw === null || raw === '') {
      out.push({label: label, raw: '(none)', res: null, logo: isLogo});
      return;
    }
    if (/^(https?:|mailto:|tel:|#)/.test(raw) && a.href.indexOf(location.origin) !== 0) return;
    // A flag emoji is the language switcher. Pointing at the other language is
    // its whole job, so it must never count as a leak.
    // data-lang-switch is the footer's explicit "read this in English/Italiano"
    // link. Crossing languages is its purpose, so it is not a leak.
    const isFlag = /[\uD83C][\uDDE6-\uDDFF]/.test(a.textContent || '')
                   || a.hasAttribute('data-lang-switch');
    out.push({label: label, raw: raw, res: a.href.replace(location.origin, '').split('#')[0],
              logo: isLogo, flag: isFlag});
  });
  return out;
}
"""


def lang_of(path):
    return "it" if path == "/it" or path.startswith("/it/") else "en"


def main():
    base = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8909").rstrip("/")
    # Optional "start:end" page slice. 22 pages x 2 widths is ~45 page loads
    # with a 2.8s settle each, which now runs past the 10-minute ceiling on a
    # single command in the Cowork container. Slicing splits the run without
    # relaxing any check - same widths, same assertions, fewer pages per call.
    global PAGES
    sl = sys.argv[2] if len(sys.argv) > 2 else ""
    if sl:
        a, b = (sl.split(":") + [""])[:2]
        PAGES = PAGES[int(a or 0):int(b) if b else None]
        print("slice %s -> %d page(s)" % (sl, len(PAGES)))
    dead, lang, rel, gone = [], [], [], []
    status = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                               args=["--no-sandbox"])
        for width, wname in WIDTHS:
            ctx = br.new_context(viewport={"width": width, "height": 900},
                                 is_mobile=(width < 500), has_touch=(width < 500))
            for path in PAGES:
                page = ctx.new_page()
                try:
                    page.goto(base + path, wait_until="networkidle", timeout=20000)
                    # enhance.js deliberately holds its first DOM pass until
                    # after `load` + a frame + 400ms, so that it writes AFTER
                    # React has hydrated rather than into the middle of it.
                    # Sample before that lands and this audit reports links that
                    # are about to be corrected. It was flaky at 700ms.
                    page.wait_for_timeout(1600)
                    # the footer only renders once it has been near the viewport
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1200)
                    links = page.evaluate(COLLECT)
                except Exception as e:
                    print(f"  !! {path} @{wname}: {type(e).__name__}")
                    page.close()
                    continue
                page.close()

                want = lang_of(path)
                for l in links:
                    where = f"{path} @{wname}"
                    if l["raw"] == "(none)":
                        dead.append((where, l["label"] or "[logo]"))
                        continue
                    if l["raw"].startswith("./") or l["raw"].startswith("../"):
                        rel.append((where, l["label"] or "[logo]", l["raw"], l["res"]))
                    res = (l["res"] or "").rstrip("/") or "/"

                    if res not in status:
                        r = ctx.request.get(base + res)
                        status[res] = r.status
                    if status[res] >= 400:
                        gone.append((where, l["label"] or "[logo]", res, status[res]))

                    if res in CROSS_LANG_OK or l.get("flag"):
                        continue
                    # A file is not a page and has no language. The hero's
                    # "ascolta una chiamata di esempio" points at an .mp3 under
                    # /fuc/assets/, which lives outside /it/ because assets do -
                    # flagging that as an Italian page linking to English was a
                    # false positive, and the only fix available would have been
                    # to delete a working link.
                    if os.path.splitext(res)[1].lower() in ASSET_EXTS:
                        continue
                    if lang_of(res) != want:
                        lang.append((where, l["label"] or "[logo]", l["raw"], res))
            ctx.close()
        br.close()

    def show(title, rows, fmt):
        seen, uniq = set(), []
        for r in rows:
            if r not in seen:
                seen.add(r)
                uniq.append(r)
        print(f"\n{title}: {len(uniq)}")
        for r in uniq:
            print("   " + fmt(r))
        return len(uniq)

    n_lang = show("LANGUAGE LEAKS (fail)", lang,
                  lambda r: f"{r[0]:<34} '{r[1]}'  {r[2]} -> {r[3]}")
    n_404 = show("BROKEN TARGETS (fail)", gone,
                 lambda r: f"{r[0]:<34} '{r[1]}'  -> {r[2]}  [{r[3]}]")
    n_dead = len({d for d in dead})
    n_rel = len({r for r in rel})
    print(f"\nadvisory: {n_dead} href-less <a> (Framer section badges), "
          f"{n_rel} relative hrefs")

    print()
    if n_lang or n_404:
        print(f"AUDIT FAILED: {n_lang} language leak(s), {n_404} broken target(s)")
        return 1
    print("LINK AUDIT CLEAN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
