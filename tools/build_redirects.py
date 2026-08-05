#!/usr/bin/env python3
"""Generate site/_redirects from the dead-URL map.

Context: sabato.ai migrated off a multi-vertical positioning (banking, saas,
insurance, real estate, hospitality, education, telco, property management) and
off a WordPress-era blog, and shipped the new e-commerce site with NO redirects
at all - the Netlify deploy log said "No redirect rules processed". Google
Search Console (5 Aug 2026) reported 48 URLs as "Not found (404)" plus more in
"Crawled - currently not indexed", all of them old-site paths.

Those dead URLs are the only pages on this domain Google has actually crawled,
some for over a year. They are where whatever link equity exists lives, and
right now every one of them dead-ends. Redirecting them does two jobs: it passes
that equity, and it hands Google live doorways into a site it currently cannot
find its way into.

    python3 tools/build_redirects.py           # write site/_redirects
    python3 tools/build_redirects.py --check   # validate only, write nothing

Every target is validated against the real files under site/. A redirect that
lands on a 404 is worse than the 404 it replaced, so an unknown target is a hard
error, not a warning.

DELIBERATELY NO WILDCARDS that could shadow a live page. Netlify only applies
non-forced rules when no file matches, which would make `/blog/* -> /blog` safe
in theory - but the Playwright gate runs against a local server that does not
process _redirects, so redirect behaviour cannot be tested before it ships.
Untestable cleverness is not worth it: every rule here is explicit.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(SITE, "_redirects")

# (old path, new path, why)
MAP = [
    # --- old vertical pages: the pre-pivot positioning -----------------------
    # No equivalent page exists for these verticals any more. The industries hub
    # is the honest destination: the visitor asked "do you serve my sector?" and
    # lands on the page that answers exactly that. Sending them to the homepage
    # instead is what Google treats as a soft 404.
    ("/banking",                "/industries",                    "vertical dropped in pivot"),
    ("/saas",                   "/industries",                    "vertical dropped in pivot"),
    ("/insurance",              "/industries",                    "vertical dropped in pivot"),
    ("/hospitality",            "/industries",                    "vertical dropped in pivot"),
    ("/education",              "/industries",                    "vertical dropped in pivot"),
    ("/real-estate",            "/industries",                    "vertical dropped in pivot"),
    ("/telco",                  "/industries",                    "vertical dropped in pivot"),
    ("/property-management",    "/industries",                    "vertical dropped in pivot"),
    ("/it/banking",             "/it/settori",                    "vertical dropped in pivot"),
    ("/it/saas",                "/it/settori",                    "vertical dropped in pivot"),
    ("/it/insurance",           "/it/settori",                    "vertical dropped in pivot"),
    ("/it/hospitality",         "/it/settori",                    "vertical dropped in pivot"),
    ("/it/education",           "/it/settori",                    "vertical dropped in pivot"),
    ("/it/real-estate",         "/it/settori",                    "vertical dropped in pivot"),
    ("/it/telco",               "/it/settori",                    "vertical dropped in pivot"),
    ("/it/property-management", "/it/settori",                    "vertical dropped in pivot"),

    # --- verticals that DID survive, under a new name -----------------------
    ("/automotive",             "/industries/automotive-parts",   "direct successor"),
    ("/it/automotive",          "/it/settori/ricambi-auto",       "direct successor"),

    # --- ecommerce-retail was the old name for what the whole site now is ----
    ("/ecommerce-retail",       "/",                              "now the entire positioning"),
    ("/it/ecommerce-retail",    "/it",                            "now the entire positioning"),

    # --- old product/marketing pages ----------------------------------------
    ("/product",                "/",                              "product story moved to homepage"),
    ("/product-old",            "/",                              "product story moved to homepage"),
    ("/old-home",               "/",                              "superseded homepage"),
    ("/pricing-old",            "/pricing",                       "direct successor"),
    ("/it/product",             "/it",                            "product story moved to homepage"),
    ("/it/product-old",         "/it",                            "product story moved to homepage"),
    ("/it/old-home",            "/it",                            "superseded homepage"),
    ("/it/pricing",             "/it/prezzi",                     "localised slug"),
    ("/it/contact-us",          "/it/contatti",                   "localised slug"),
    ("/contact-us",             "/contact",                       "direct successor"),
    ("/it/thank-you-page",      "/it/grazie",                     "localised slug"),
    # NB: /thank-you-page (EN) is a LIVE page - deliberately no rule for it.

    # --- old use-case style pages -------------------------------------------
    ("/ai-voice-for-sales",     "/use-cases/pre-sales-consultation", "closest live use case"),
    ("/ai-voice-for-support",   "/use-cases/open-a-complaint",       "closest live use case"),
    ("/it/ai-voice-for-sales",  "/it/casi-duso/consulenza-pre-vendita", "closest live use case"),
    ("/it/ai-voice-for-support","/it/casi-duso/apertura-reclamo",      "closest live use case"),

    # --- old English prefix --------------------------------------------------
    ("/en",                     "/",                              "old locale prefix"),
    ("/en/",                    "/",                              "old locale prefix"),

    # --- WordPress-era blog: pagination and theme junk -----------------------
    ("/blog/page/1",            "/blog",                          "old pagination"),
    ("/blog/page/2",            "/blog",                          "old pagination"),
    ("/blog/page/3",            "/blog",                          "old pagination"),
    ("/blog/page/4",            "/blog",                          "old pagination"),
    ("/blog/page/5",            "/blog",                          "old pagination"),
    ("/blog/page/6",            "/blog",                          "old pagination"),
    ("/blog/page/7",            "/blog",                          "old pagination"),
    ("/blog/page/8",            "/blog",                          "old pagination"),
    ("/blog/page/9",            "/blog",                          "old pagination"),
    ("/real-estate-ai/page/3",  "/",                              "old vertical archive"),
    ("/blog/lexend-footer/footer-style-one", "/blog",             "old theme demo page"),

    # --- WordPress-era blog posts -------------------------------------------
    # Two have a genuinely close successor and are mapped to it; the rest are
    # off-positioning (cold calls, franchises, brokers) with no equivalent, so
    # they go to the blog index rather than being force-fit to a post.
    ("/blog/voice-ai-or-call-center-guess-which-keeps-more-cash-in-your-pocket",
     "/blog/what-a-conversation-actually-costs",   "same subject: cost per conversation"),
    ("/blog/missed-call-recovery-and-lead-qualification-workflow-for-solo-brokers",
     "/blog/why-customers-call-instead-of-ordering-online", "same subject: inbound calls"),
    ("/blog/the-ceos-rescue-plan-for-turning-dead-calls-into-live-deals", "/blog", "off-positioning"),
    ("/blog/voice-ai-follow-ups-ensure-no-office-drops-a-hot-prospect",   "/blog", "off-positioning"),
    ("/blog/ai-marketing-engine-auto-creates-localized-ads-for-every-franchise", "/blog", "off-positioning"),
    ("/blog/ai-voice-assistant-for-real-estate-agents",                  "/blog", "off-positioning"),
    ("/blog/predict-next-months-revenue-with-ai-driven-lead-scoring",    "/blog", "off-positioning"),
    ("/blog/network-metrics-in-one-dashboard-ai-pulls-data-from-every-office", "/blog", "off-positioning"),
    ("/blog/ai-scripts-for-cold-calls-that-actually-get-call-backs",     "/blog", "off-positioning"),
    ("/blog/from-prospect-to-paycheck-automate-the-entire-sales-cycle-with-ai", "/blog", "off-positioning"),
    ("/blog/one-click-call-to-crm-sync-for-all-tenant-conversations",    "/blog", "off-positioning"),
    ("/blog/training-feedback-loops-ai-analyzes-calls-to-coach-agents-daily", "/blog", "off-positioning"),
    ("/blog/ai-qualifies-leads-then-routes-them-to-the-right-branch",    "/blog", "off-positioning"),
    ("/blog/roll-out-ai-crm-sync-to-hundreds-of-agents-without-it-pain", "/blog", "off-positioning"),
    ("/blog/see-every-lead-in-one-dashboard-ditch-the-spreadsheets",     "/blog", "off-positioning"),
]

# DELIBERATELY EMPTY. Google still holds WordPress query URLs like
# /?page_id=1789, and the obvious rule is `/  page_id=1789  /  301`. It should
# not loop, because the target carries no query string and so cannot re-match.
# "Should not" is doing too much work: redirects cannot be tested before they
# ship (the local gate does not process _redirects), and the failure mode is an
# infinite redirect on the homepage - the entire site down - to recover a single
# junk URL that is not even indexed. Asymmetric. Left undone on purpose.
QUERY_RULES = []


def live_paths():
    """Every path the deployed site actually answers on."""
    paths = set()
    for dirpath, _, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), SITE)
            p = "/" + rel[:-len(".html")]
            if p.endswith("/index"):
                p = p[: -len("index")]
            paths.add(p)
            paths.add(p.rstrip("/") or "/")
    return paths


def main():
    check_only = "--check" in sys.argv
    live = live_paths()

    bad, seen, dupes = [], set(), []
    for old, new, _why in MAP:
        if new.rstrip("/") not in live and new not in live:
            bad.append((old, new))
        if old in seen:
            dupes.append(old)
        seen.add(old)
        if old.rstrip("/") in live or old in live:
            bad.append((old, f"SOURCE IS A LIVE PAGE - rule would hijack it"))

    if dupes:
        print("DUPLICATE SOURCE PATHS:", dupes, file=sys.stderr)
    if bad:
        print("INVALID RULES - refusing to write:", file=sys.stderr)
        for o, n in bad:
            print(f"   {o:60s} -> {n}", file=sys.stderr)
        return 1
    print(f"validated {len(MAP)} rules; every target resolves to a real page")

    if check_only:
        return 0

    # Both columns sized from the real data. A fixed target width silently glued
    # "301" onto the end of any URL longer than it, producing a redirect to a
    # page that does not exist - which is exactly the failure this file is meant
    # to eliminate.
    width = max(len(o) for o, _, _ in MAP) + 2
    twidth = max(len(n) for _, n, _ in MAP) + 3
    lines = [
        "# Generated by tools/build_redirects.py - do not hand-edit.",
        "#",
        "# Recovers the pre-pivot URL space (multi-vertical positioning + the",
        "# WordPress-era blog) that shipped with no redirects at all. Every",
        "# target is validated against real files before this file is written.",
        "",
    ]
    for old, new, why in MAP:
        lines.append(f"{old:<{width}}{new:<{twidth}}301   # {why}")
    lines.append("")
    if QUERY_RULES:
        lines.append("# Query-string survivors from the WordPress install")
        for path, query, new, why in QUERY_RULES:
            lines.append(f"{path}  {query}  {new}  301   # {why}")
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"wrote {OUT} ({len(MAP)} path rules + {len(QUERY_RULES)} query rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
