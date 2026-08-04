# Session handoff — 3 Aug 2026

Read this **after** `SABATO-SITE-HANDBOOK.md`. The handbook is the permanent
playbook; this file is the volatile part — what just shipped, what is half-done,
and what is waiting on a decision. Delete sections as they are resolved.

## How to bootstrap a new chat

Cowork sessions run in a throwaway cloud container: no files, installs or shell
state survive. Persistent Claude memory is **disabled** on this account, so the
repo is the only thing that carries over. Skills and the personal-preferences
block are account-level and follow you automatically.

Opening prompt for a fresh session:

```
Clone github.com/danielrongo/sabato-site, read SABATO-SITE-HANDBOOK.md
and HANDOFF.md, then <the task>.
```

Everything below is written so a session that has never seen this work can pick
it up without re-deriving anything.

---

## Shipped this session (live on main)

| What | Commit |
|---|---|
| Every band constrained to the homepage 1200px grid, desktop + mobile gutters | `05126f3` |
| GA4 `G-BSK4KH9JJF` on all 73 pages, exactly once | `bf30113` |
| ROI calculator hosted **unlisted** at `/roi-calculator` | `0d3e807` |
| Crisp live chat removed; `Becked by` → `Backed by` | `16976fe` |
| CTA card no longer covers the footer logo below 1200px | `b8db75f` |

Notes that are easy to lose:

- **GA4** — Framer pages shipped with Framer's placeholder property
  `G-499419803`, malformed for GA4 (nine digits, GA4 wants ten alphanumerics), so
  the homepage reported to nothing for months. `tools/inject_ga.py` rewrites it in
  place rather than adding a second tag; run it **last** in every build.
- **ROI calculator** — hosted but unlisted: `noindex,nofollow`, absent from the
  sitemap, and nothing links to it. `robots.txt` is deliberately untouched (a
  `Disallow` line would publish the path and would also stop crawlers seeing the
  `noindex`). Daniel's reasoning: "cost of a human vs our robot" is fine to walk a
  CFO through on a call, dangerous unattended on a public page.
  It weighs 4.4MB raw / ~900KB gzipped — React *development* build plus in-browser
  Babel. Swapping to React production and pre-compiling the JSX would take it to
  ~60KB gzipped without touching a line of the calculator's code.
- **Crisp** was a Framer `bodyEnd` snippet (`BWQzQLg24`), website ID
  `27aa4aad-…`, on all 16 exported pages.

---

## Fixed — CTA panel covering the footer logo (`b8db75f`)

Shipped as a per-page, per-breakpoint `<style id="cta-footer-clearance">` block
lifting the CTA card at 768–1199px and ≤767px. Desktop untouched. Applied to
index, pricing, contact, it, it/prezzi, it/contatti, it/chi-siamo; about.html was
already clear.

**Two cases still covered — decide whether they are worth another pass:**

- `/it` at 600–767px: lifted 118px, measurement says it needs ~150. Still 32px of
  overlap.
- `/404` at 900px: same CTA structure but not included in the fix at all.
- Everywhere else the gap lands between −5 and +7px rather than the intended
  ~48px, so the logo is visible but its top edge touches the card. Looks tight
  rather than deliberate. Desktop keeps its original +39px.

Background below is kept because it explains why the obvious fixes do not work.

On Framer pages at mobile widths the final lime CTA panel is painted on top of
the footer's Sabato logo, so the footer reads as an unlabelled block of links.
Reproduced at 390px, 600px and 767px on `/` (107–119px of overlap) and on
`/pricing`. Clean at 1440px. Authored pages (use-cases, industries, blog) are
clean at every width.

Root cause, from `site/index.html`:

```css
/* base */
.framer-12u8b35 { position: relative; z-index: 1; }
/* @media (max-width: 767.98px) */
.framer-12u8b35 { position: absolute; height: 547px; padding: 50px 20px;
                  top: calc(-119.585% - 273.5px); left: 0; right: 0 }
.framer-qg4q0x  { top: 92%; transform: translate(-50%,-50%); bottom: unset }
```

At the mobile breakpoint Framer takes the CTA out of flow, so the footer does not
reserve space for it, and `z-index: 1` puts it over the footer.

**Dead end already tested:** adding `padding-top` to the footer moves the overlap
by only 6px (107 → 101). The CTA is positioned as a *percentage* of a container
that includes the footer, so growing the footer pushes the CTA down by almost the
same amount. Any fix that grows the footer is circular — do not retry it.

**Live lever:** shift the panel itself. Either put it back in flow at mobile
(`position: relative; top: auto; transform: none`) or shift it by a fixed pixel
amount (`transform: translate(-50%, calc(-50% - 130px))`), which is independent of
page height. Check it does not then collide with the section above.

**Complication:** the footer class `framer-PFscP` is shared by all 8 Framer pages,
but the CTA section classes (`framer-qg4q0x`, `framer-12u8b35`) are generated
per page and exist only on `/`. A CSS-only fix needs the equivalent class from
each page; a JS fix in `enhance.js` can find "the absolutely-positioned element
overlapping the footer logo" generically.

**Verification harness that works** (page-agnostic, survives Framer's generated
class names): scroll the footer logo to the middle of the viewport, then
`document.elementFromPoint` at its centre. If the hit is not the logo, something
is painted over it. Two probes were written before this one and both gave false
results — one matched `QRoxyaGHHfHSyA4`, which is the *header* logo, so it kept
"finding" the header covering itself; the other anchored on the last image on the
page, which is the LinkedIn icon sitting below the logo. The footer logo's asset
is `KY1UqOX7…` (white/inverted); the header's is `UTATYXc6…`.

---

## Open decisions for Daniel

1. **Pricing page rewrite.** Reviewed this session; findings in order of damage:
   "One predictable monthly price" sits directly above three "Starting from"
   tiers with no overage rate stated; **"Human escalation workflows" is gated to
   the Merchant tier**, which reads as "the cheap plan cannot reach a human";
   live typo **"2 languags"**; no proof anywhere (no logos, testimonial or real
   deployment number) on either page; CTA drift between "Start Free Pilot",
   "Start a Pilot" and "Book a Demo"; minutes are the wrong unit for a CEO
   (calls are); homepage claims "9 voice workflows" while three are marked
   Coming Soon. Recommendation: keep three tiers, cut ambiguity — who each tier
   is for, calls not minutes, stated overage, escalation everywhere, one pilot
   promise. Mechanical fixes were approved but **not yet applied**.
2. **Cookie consent.** GA4 sets `_ga` before any consent and there is no banner
   anywhere on the site. Standard ePrivacy exposure for an Italy-based, EU-facing
   business. Fix is Consent Mode v2 with defaults denied plus a light banner.
3. **Sources blocks** still on `reduce-bracketing-returns` and
   `multilingual-phone-support-eu-expansion`; the later "skip the sources"
   instruction post-dates them.
4. **This repo is public.** The reverted ROI-calculator commits are still in
   history, so the calculator is readable by anyone who looks at the git log.
   Squashing it out is possible if that matters.
5. **Footer layout differs between the two page families on mobile** — Framer
   pages centre the footer, authored pages left-align it. Not yet raised as a fix.
