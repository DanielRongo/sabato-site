# Sabato Site — Build Handbook

Everything needed to design, write and ship anything on sabato.ai without
re-deriving it. Written to be dropped into a Claude Project as knowledge, so any
new session can produce work that matches what's already live.

**Repo:** `github.com/danielrongo/sabato-site` (public)
**Production:** Netlify, auto-deploys from `main`
**Staging:** auto-deploys from `staging` → `staging--delicate-valkyrie-20e427.netlify.app`

---

## 1. The one rule

**Nothing reaches production without Daniel's review.**

```
build on `staging`  →  push  →  Daniel reviews on the staging URL  →  "ship"  →  merge to `main`
```

Never push straight to `main`. Never drag-and-drop to Netlify (it desynchronises
the repo — the next push silently wipes it). After every production deploy, run
the post-deploy sweep (§9).

---

## 2. What the site is

A static, self-hosted clone of what used to be a Framer site. Framer is no longer
in the loop: every asset is local, forms post to Netlify, nothing depends on a
Framer subscription. Two page families coexist and **they have different DOM
structures** — this matters constantly (§10):

| Family | Origin | Examples |
|---|---|---|
| **Framer pages** | mirrored from the original Framer build, React hydrates them | `/`, `/it`, `/pricing`, `/about`, `/contact`, legal pages |
| **Authored pages** | written by us, plain HTML, no framework | all `/use-cases/*`, all `/it/casi-duso/*`, all blog pages |

---

## 3. Repo map

```
site/                     ← the deploy directory (Netlify publish dir)
  index.html, it.html …   ← Framer pages (do not hand-edit lightly)
  use-cases/*.html        ← 9 English use-case pages
  it/casi-duso/*.html     ← 9 Italian use-case pages
  blog.html, it/blog.html ← blog indexes (generated)
  blog/*.html             ← blog posts (generated — never hand-edit)
  it/blog/*.html          ← Italian posts (generated)
  js/enhance.js           ← all site-wide nav/link behaviour
  fuc/                    ← mirrored Framer assets (fonts, images, JS bundles)
  gf/                     ← Google fonts
  _headers, netlify.toml  ← caching + build config
  sitemap.xml, robots.txt
posts/en/*.md             ← blog source (English)
posts/it/*.md             ← blog source (Italian)
posts/_BLOCKS.md          ← block authoring cheat-sheet
templates/                ← blog-post-{en,it}, blog-index-{en,it}, use-case.html
publish.py                ← markdown → blog HTML + indexes + sitemap
tools/postdeploy_check.py ← run after every deploy
tools/rehash_edited_assets.py ← run after editing anything in site/fuc/
```

---

## 4. Design system

Declared as CSS custom properties at the top of every authored page:

```css
--lime:  rgb(204, 255, 0);   /* accent: CTAs, numbers, highlights */
--black: rgb(0, 0, 0);       /* hero bands, CTA bands, cards */
--ink:   rgb(18, 10, 11);    /* headings, body on light */
--gray:  rgb(69, 65, 64);    /* body copy */
--off:   rgb(248, 244, 241); /* soft cards / bands */
--line:  rgb(227, 226, 226); /* hairlines */
--blue:  rgb(0, 153, 255);   /* links */
--radius: 24px;
--font: "Satoshi", "Inter", -apple-system, "Helvetica Neue", sans-serif;
--hand: "Kalam", cursive;    /* handwriting accent, ~19px, sparing */
```

Rules of thumb:
- **Lime is the accent, never the background of long text.** Big numbers, CTA
  pills, one highlighted column, bar fills.
- **Pill CTAs:** border-radius 100px, padding 12px 30px, Satoshi 700 16px,
  black on lime. Primary CTA is always → `https://cal.com/sabatoai/intro`.
- **Cards / bands:** 24px radius. Alternate white → black → off-white down a page
  so it never reads as one long column.
- **Mobile breakpoint: 809px.** Test at 390px width.
- **Fonts are local.** Satoshi from `/fuc/third-party-assets/fontshare/…`, Kalam
  and Inter from `/fuc/assets/…`. Never add a webfont CDN.
- **Graphics are inline SVG**, flat and geometric, only palette colours, no
  gradients or drop shadows. Icons must be *mathematically* centred in their
  circles (compute the bbox — do not eyeball).
- **Italian runs 15–20% longer than English.** Shorten SVG labels rather than
  letting them clip, and re-check every label against its shape.

Shared assets:
- nav logo `/fuc/images/UTATYXc6NipXQRoxyaGHHfHSyA4-f2557e25.png`
- footer logo `/fuc/images/KY1UqOX7zKeKJdbxTotIopeeZIU-f2557e25.png`
- default `og:image` `https://www.sabato.ai/fuc/assets/8Q4ofjOgRTqsr8FpanTJF9nzLwU.png`

---

## 5. Page anatomy — use-case pages

The nine English and nine Italian use-case pages share one structure. Copy an
existing page (`site/use-cases/open-a-complaint.html` is the best-built
reference) rather than starting from scratch; `templates/use-case.html` has the
same shell with placeholders.

Section order that works:

1. **Split hero** — white. Left: lime `USE CASE` chip, H1, subline, lime pill CTA,
   Kalam line ("live in two weeks"). Right: a **live-call card** SVG (black, lime
   waveform, timer, a context block that differs per page, three call controls).
   The call card is the family signature — every page has one, none identical.
2. **Dark band** — the argument with the data. Eyebrow + H2 + copy on the left,
   a chart/diagram on the right, sources in 12px grey small print underneath.
3. **Flow diagram** — black node → lime node → the path *splits*: thick lime =
   handled, thin black = escalated to a human. Separate desktop and mobile SVGs.
4. **Call transcript panel** — dark panel, `CALLER` / `AGENT` rows with
   mini-waveform glyphs. Reads as a transcribed phone call, never chat bubbles
   (we sell voice, not chat). Always labelled as an example.
5. **Two-up value cards** — off-white, one small SVG each.
6. **Pilot band** — off-white. Always the same promise: we measure, we don't
   quote invented numbers, you can walk away.
7. **CTA band** — black, Kalam line, H2, lime pill.
8. **Footer** — identical to the rest of the site.

Head: title, meta description, canonical, `og:image`, **BreadcrumbList JSON-LD**,
hreflang trio (§8). No FAQ schema on use-case pages. Never `noindex`.

---

## 6. Blog

### Source format

One markdown file per post per language: `posts/en/<slug>.md`, `posts/it/<slug>.md`
(**same slug both languages** — that's how the language-switch link is found).

```yaml
---
title: Post title
slug: url-slug
description: Meta description, also used as the index-card excerpt
category: Voice AI | Operations | Benchmarks
date: 2026-07-29
cover_style: black | lime | offwhite
read_time: 7 min read      # optional — computed from word count if absent
---
```

`cover_style` sets the index card's cover block: `black` (lime text), `lime`
(black text), `offwhite` (black text + hairline). Rotate them so the grid reads well.

Special sections, by heading name:
- `## FAQ` → renders as FAQ cards **and** emits FAQPage JSON-LD.
- `## Sources` / `## Fonti` → renders as the sources block.

### Block kit

Full syntax with examples: `posts/_BLOCKS.md`. Summary:

| Block | Use it for |
|---|---|
| `:::keystat` | one or two big numbers on black cards (blank line = second card) |
| `:::takeaway` | the save-worthy summary box — *The takeaway* / *In sintesi* |
| `:::action` | numbered "do this" checklist; first line is the heading |
| `:::compare` | two-column comparison, right column highlighted |
| `:::quote` | pull quote; last line starting `—` becomes attribution |
| `:::chart bar` | horizontal bar chart as inline SVG, `label \| number \| note` |
| markdown tables | no fence needed — auto-styled |

Every block renders exactly what it's given: no invented numbers, no source line
unless supplied. A malformed block degrades to plain paragraphs and logs a warning
rather than breaking the page. Fixed labels follow the post's language.

**Use blocks where they earn their place.** A chart with nothing to show is worse
than a sentence. The two that most reliably make a post worth saving are
`:::action` and `:::takeaway`.

### Publishing

```bash
pip install markdown --break-system-packages
python3 publish.py        # renders posts, rebuilds both indexes, updates sitemap
```

Author is the **Organization "Sabato AI"** in byline and Article schema. Do not
reintroduce a named person without Daniel asking for it.

---

## 7. Site wiring — `site/js/enhance.js`

One file, loaded on every page, responsible for all cross-page link behaviour.
**Adding a use-case page = adding one line here.**

```js
var USECASES_EN = [
  { label: "Managing Returns", href: "/use-cases/managing-returns" },
  …
];
var USECASES_IT = [
  { label: "Riepilogo Checkout via Messaggio",
    href: "/it/casi-duso/riepilogo-checkout-via-messaggio",
    aliases: ["Riepilogo Acquisto via SMS"] },   // ← tile and footer names differ
  …
];
```

What it does:
1. **Blog link in the footer**, immediately after "Book a Demo" / "Prenota una
   Demo" — deliberately *not* in the header. Picks the *lowest* matching demo
   link on the page (there are several) and strips the inherited `target="_blank"`.
2. **"Use Cases" dropdown**, positioned against the link's own bounding box
   (fixed, viewport-clamped) and bound by event delegation.
3. **Retargets footer links and homepage tiles** from `#usecases` to the real
   pages, matching on label **or alias**, apostrophe-insensitive.
4. **Click interceptor** (window, capture phase) that navigates our URLs itself —
   see §10, this is not optional on Framer pages.

---

## 8. Bilingual conventions

| | English | Italian |
|---|---|---|
| Use-case URLs | `/use-cases/<en-slug>` | `/it/casi-duso/<it-slug>` (translated) |
| Blog | `/blog`, `/blog/<slug>` | `/it/blog`, `/it/blog/<slug>` (same slug) |
| Nav labels | Use Cases · Pricing · About · Contact | Casi d'uso · Prezzi · Chi Siamo · Contatti |
| CTA | Start Free Pilot | Inizia Pilot Gratuito |
| Footer demo link | Book a Demo | Prenota una Demo |

Italian rules:
- **Write natively, never translate.** Keep each section's argument and structure,
  but find the Italian line that lands — don't calque an English pun.
- Site copy uses **"tu"**; phone-call transcripts use **"lei"**, as a real agent would.
- Transcripts get Italian names, products, places, couriers (BRT, GLS, Poste
  Italiane), euro prices — same dramatic beats as the English.
- **Statistics carry over identically** — same numbers, same source names, same
  caveats. Translate the sentence around a number, never the number or source.
- **Straight apostrophes** in nav/footer labels (`Casi d'uso`, not `d’uso`) — a
  typographic apostrophe used to break label matching. The JS normalises now, but
  keep the site consistent.

**hreflang is bidirectional** — every page carries all three tags, and its twin
must point back:

```html
<link rel="alternate" hreflang="en" href="https://www.sabato.ai/use-cases/managing-returns">
<link rel="alternate" hreflang="it" href="https://www.sabato.ai/it/casi-duso/gestione-resi">
<link rel="alternate" hreflang="x-default" href="https://www.sabato.ai/use-cases/managing-returns">
```

---

## 9. Tooling

```bash
python3 publish.py                                   # blog build
python3 tools/rehash_edited_assets.py                # after ANY edit under site/fuc/
python3 tools/postdeploy_check.py <base-url>         # after EVERY deploy
```

`postdeploy_check.py` sweeps every page type for: duplicated nav items, missing
logo, local 4xx, console errors, dropdown presence, footer link targets, and
**real click-through navigation**. It exists because each of those was a live bug
at some point.

---

## 10. Traps that have already bitten

Every one of these cost a debugging cycle. They are the reason the checks exist.

1. **Framer's router intercepts clicks.** On Framer pages it calls
   `preventDefault()` and navigates via its own route table, so *rewriting an
   `href` is not enough* — the link looks right and goes somewhere else. We
   intercept on `window` in the capture phase and navigate ourselves. Our handler
   deliberately does **not** skip already-cancelled events, because Framer
   registers first. → **An href is not proof. Always click-test.**

2. **`site/fuc/*` is cached `immutable, max-age=1y`.** Correct for Framer's
   content-hashed files, wrong the moment you edit one in place: returning
   visitors keep the stale copy for a year. Run `rehash_edited_assets.py`, which
   renames edited files with a fresh hash **and cascades** — renaming a file
   changes its importers, which are cached too.

3. **Two DOM structures.** Framer pages wrap each nav item individually; our
   pages share one `<nav>`. Code written against one silently misbehaves on the
   other — it produced a duplicated header, a 220px-misaligned dropdown, and nine
   dead footer links, each found only after shipping. **Verify on both families.**

4. **Label drift inside the site.** The Italian homepage tile says "Riepilogo
   Acquisto via SMS"; the footer says "Riepilogo Checkout via Messaggio". Same
   workflow, two names. Hence `aliases`.

5. **Apostrophes.** `Casi d'uso` vs `Casi d’uso` broke label matching silently.

6. **Cloned links inherit attributes.** The footer Blog link cloned "Book a Demo"
   and inherited `target="_blank"`, so it opened in a new tab.

7. **My own verification lies if coordinates are stale.** Measuring an element in
   page coordinates then clicking in viewport coordinates produced two phantom
   "reproductions" of bugs that didn't exist. **Screenshot first, then click what
   you can see.**

8. **A test can rot into the opposite of its intent.** `postdeploy_check.py`
   asserted "Blog appears once in the top 200px" — correct until Blog moved to
   the footer, after which it failed on every page *and* would have passed if
   Blog were accidentally restored to the header. When a design decision
   inverts, go fix the assertion that encoded the old one. **When a check fails
   everywhere at once, suspect the check before the site** — and prove which it
   is by mutation-testing: break the thing on purpose and confirm the assertion
   catches it.

---

## 11. Content rules (non-negotiable)

These protect the brand's whole positioning — the site's credibility *is* the product.

- **No invented statistics, ever.** A number appears only with a real source and
  date, inline. If nothing honest fits, argue from process — two live pages carry
  zero statistics by design and are no weaker for it.
- **No invented Sabato performance claims.** There is no published case study yet,
  so no deflection rates, no conversion uplifts. Every page sells the *pilot*:
  we measure your baseline, we show you the delta, you can walk away.
- **Flag data age and boundaries.** Bamberg's return figures are 2020–21 and say
  so on the page. Never merge sources with different methodologies into one number.
- **Complaints page guardrail:** the agent does *not* resolve complaints, calm
  angry customers, or offer compensation. It answers instantly, captures, routes,
  and tells the customer what happens next. Humans resolve. The page says so.
- **Post-delivery page guardrail:** no review gating. Selectively soliciting only
  happy customers is prohibited by the FTC's 2024 reviews rule, Google's review
  policies and Trustpilot's terms. The agent calls *everyone*; the page states
  this openly, naming Google and Trustpilot.
- **Voice, not chat.** Sabato is voice AI. Transcript panels, waveforms, call
  controls — never chat bubbles.

---

## 12. Current inventory

- 9 English use-case pages + 9 Italian, fully cross-linked with hreflang
- Bilingual blog with block kit; author = Sabato AI. Live posts (EN+IT):
  `multilingual-phone-support-eu-expansion`, `reduce-bracketing-returns`
- Tables with 4+ columns automatically get a `dense` class (`publish.py`):
  smaller cells and wrapping headers, so wide tables fit the prose column
  instead of clipping behind a horizontal scroll
- `tools/serve_like_netlify.py` serves the built site the way Netlify does
  (extensionless URLs, plus the `_headers` Content-Type rule for the
  hash-suffixed feather-icon modules) so the post-deploy sweep runs offline:
  `python3 tools/serve_like_netlify.py 8913 &` then
  `python3 tools/postdeploy_check.py http://127.0.0.1:8913`
- Contact forms → Netlify Forms (form name `sabato-contact`, field `page` records
  the source page). Enable notifications under Netlify → Forms.
- A scheduled "Sabato blog publisher" task (daily 09:00 CET) that publishes at
  most one approved post per run and pushes to GitHub
- `sitemap.xml` covering all pages; dummy/demo posts get `noindex` and stay out of it

**Open items:** the publisher currently has no queue feeding it (the Trello board
was dropped in favour of a Google Doc/Sheet source, not yet wired). Comparison
pages ("voice AI vs chatbots", "managed vs DIY") and a glossary hub are the
highest-value pages not yet built.

---

## 13. How to ask for new work

A prompt that produces the right result first time looks like this:

> Build a new use-case page for X. Read `site/use-cases/open-a-complaint.html`
> as the structural reference and `SABATO-SITE-HANDBOOK.md` for the rules. Work on
> the `staging` branch, don't commit. Give it its own hero call card and its own
> data visual — don't reuse another page's. Only verified statistics with inline
> sources; if none fit, argue from process. Add it to `USECASES_EN` in
> `site/js/enhance.js` and to the sitemap. Verify at 1440 and 390 with zero
> console errors, exactly one Blog and one Pricing link in the nav, and a real
> click-through test from the footer. Screenshot both widths.

Then: push to `staging`, send Daniel the staging URL plus screenshots, wait for
"ship", merge to `main`, run `postdeploy_check.py`.
