# mocks/

Design mocks and their generators. Not part of the site.

Netlify publishes `site/` only, and `tools/site_digest.py` hashes `site/` only,
so nothing here can affect a deploy or the receipt. It lives in the repo for one
reason: the cloud container that generates these mocks gets reset without
warning, and an ungenerated mock is a rebuild from scratch.

Each generator writes a self-contained HTML file (fonts inlined as base64) that
opens anywhere with no server. Regenerate the font bundle first:

    python3 mocks/make_font_css.py     # writes /tmp/satoshi.css from site/index.html
    python3 mocks/pricing/build_dial.py

## pricing/

The 2026 pricing page redesign. Decisions locked with Daniel, 19 Aug 2026:

- one all-inclusive per-minute rate, no tiers, no feature gating
- $0.65 on the English site, 0,55 EUR on the Italian site
- volume bands 0.65 / 0.60 / 0.55 (EN), 0.55 / 0.50 / 0.45 (IT)
- no setup fee, and the page says so loudly
- no per-call price is ever quoted: a 40 second WISMO call and a 5 minute
  pre-sales call are not the same product
- comparisons name categories, never brands
- the "where we lose" break-even section was cut
- the dial row reuses hero.py's masked card component (variant D2)
