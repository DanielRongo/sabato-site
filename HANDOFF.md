# Session handoff - 5 Aug 2026

Read this **after** `SABATO-SITE-HANDBOOK.md` (permanent playbook) and
`DEPLOY.md` (how to ship). This file is the volatile part: what just shipped,
what is next, and what is waiting on a decision. Delete sections as they resolve.

## How to bootstrap a new chat

Cowork sessions run in a throwaway cloud container: no files, installs or shell
state survive. Persistent Claude memory is **disabled** on this account, so the
repo is the only thing that carries over. Skills and the personal-preferences
block are account-level and follow you automatically.

Opening prompt for a fresh session:

```
Read DEPLOY.md, SABATO-SITE-HANDBOOK.md and HANDOFF.md in
~/Documents/sabato-site, then <the task>. Verify with tools/verify.sh
before handing anything back.
```

If the folder is not connected, Claude can `git clone
https://github.com/DanielRongo/sabato-site.git` - public, no credentials - but
then it can only hand files back, not write into the working copy.

**Deploying is a defined procedure now.** See `DEPLOY.md`. Claude verifies in its
container (`bash tools/verify.sh`), which writes `.deploy-receipt.json`; Daniel
pushes from his own Terminal (`./tools/ship.sh staging "msg"`, then `./tools/ship.sh
live`); Claude confirms the deployed result in Daniel's browser with Claude in
Chrome. Claude never pushes and never holds a credential.

---

## Shipped this session (live on main)

| What | Commit |
|---|---|
| Deploy bridge: `verify.sh`, `ship.sh`, `site_digest.py`, receipt gate | `b6c7a99` |
| Staging branch deploy noindexed via `netlify.toml` contexts | `b6c7a99` |
| Corrected: cloud container cannot reach deployed URLs | `7ff5ad8` |
| **63 redirects recovering the pre-pivot URL space** | `009062f` |
| Browser-verification leg documented | `613925c` |

Verified on production: 44/44 redirects land correctly, 18/18 live pages still
serve themselves, `x-robots-tag` null on prod and `noindex, nofollow` on staging.

**Why the redirects mattered.** Search Console showed 78 URLs not indexed, 48 of
them 404s - the entire pre-pivot URL space (`/banking`, `/saas`, `/insurance`,
`/real-estate`, a WordPress-era blog) shipped with no redirects at all. Those
were the only URLs on the domain Google had actually crawled. They now point at
live pages.

**What was NOT the problem:** the sitemap. It was submitted 30 Jul, re-read by
Google 4 Aug unprompted, 60 pages discovered, status Success. Do not build
sitemap-submission automation; Google re-fetches on its own.

---

## NEXT: the backlog, in priority order

### 1. Fix the six pages wearing the homepage's clothes  ← do this first

`/`, `/it`, `/privacy-policy`, `/terms`, `/thank-you-page` and `/it/grazie` all
carry the **identical** title *"Voice AI Agent Platform for E-Commerce | Sabato
AI"*. Four of them also share the homepage's meta description verbatim.

This is not cosmetic. `/terms` is one of only **five** pages Google has indexed -
so a legal page is currently competing with the homepage in search results
wearing its title and description. Cheapest, highest-value fix on this list.

### 2. The Italian site is wearing English titles

Every Framer-exported Italian page carries an English `<title>`:

| Page | Current title |
|---|---|
| `/it` | Voice AI Agent Platform for E-Commerce \| Sabato AI |
| `/it/prezzi` | Pricing for Managed Voice AI \| Sabato AI |
| `/it/contatti` | Get in Touch with Sabato AI \| Book a Demo |
| `/it/chi-siamo` | Meet the Team Behind Sabato \| AI Voice Agents… |
| `/it/blog` | Blog \| Sabato AI |
| `/it/grazie` | Voice AI Agent Platform for E-Commerce \| Sabato AI |
| `/it/clienti/clima-convenienza` | ClimaConvenienza - Case Study Voice AI \| Sabato AI |
| `/it/clienti/creative-cables` | Creative Cables - Case Study Voice AI \| Sabato AI |

Italian searchers see English in Google.it. For an Italy-based company selling to
Italian merchants that is a direct commercial cost. Note the **Italian blog posts
already have Italian titles** - `publish.py` does this correctly. It is only the
Framer-exported pages that were never localised.

### 3. Rest of the SEO metadata pass

Audited 5 Aug across 66 indexable pages. Nothing is missing - every page has a
title and a description - but:

- **43 titles exceed 60 characters** and get truncated in results
- **29 descriptions exceed 160 characters** and get truncated
- 4 descriptions are under 70 characters, wasting the space
- 2 titles are under 25 characters

Reproduce the audit before starting; the numbers will have moved.

### 4. Build a `/use-cases` hub page

Nine use-case pages exist with **no index page**. Industries has `/industries`;
use-cases has nothing. They are reachable only through footer links, which is why
Google has to be told about each one individually rather than discovering them as
a group. A hub is the single biggest structural gap left, and it is a page real
visitors want too.

### 5. Pricing page rewrite - approved 3 Aug, still not applied

Findings in order of damage:

- live typo **"2 languags"**
- **"Human escalation workflows" is gated to the Merchant tier**, which reads as
  "the cheap plan cannot reach a human"
- "One predictable monthly price" sits directly above three "Starting from"
  tiers with **no overage rate stated**
- no proof anywhere - no logos, testimonial or real deployment number
- CTA drift between "Start Free Pilot", "Start a Pilot" and "Book a Demo"
- minutes are the wrong unit for a CEO; calls are
- homepage claims "9 voice workflows" while three are marked Coming Soon

Recommendation: keep three tiers, cut ambiguity - who each tier is for, calls not
minutes, stated overage, escalation everywhere, one pilot promise.

### 6. Live test numbers - US, UK, IT

Publish phone numbers so a prospect can call the agent and hear it work. Strongest
possible demo for a voice product: no form, no calendar, just call it.

**Decide these before building anything:**

- **Cost is unmetered by default.** A public number pointing at a voice agent
  bills per minute with no natural ceiling. One bored crawler, one bot, or one
  competitor on a loop is a real bill against a 70%-net-margin target. Needs a
  hard cap: per-number daily spend limit, max call duration, per-caller-ID rate
  limit, and an out-of-hours message rather than a live agent.
- **Provisioning is not uniform.** Italian and UK numbers generally require
  local address or ID documentation and take days, not minutes. US is immediate.
  Do not promise all three at once.
- **Which agent answers?** A generic demo agent is unimpressive. A catalogue-
  connected one is the actual product - but that means exposing a real or
  seeded catalogue to anonymous callers.
- **Where do the numbers live on the site?** Homepage hero is highest intent;
  pricing page converts better; a dedicated `/try` page is measurable. Pick one,
  do not scatter them.

Open question for Daniel: is this a **marketing asset** (always-on, hardened,
capped) or a **sales tool** (a number handed out on calls, unlisted)? The answer
changes the whole build.

---

## Still open from earlier sessions

1. **Cookie consent.** GA4 sets `_ga` before any consent and there is no banner.
   Standard ePrivacy exposure for an Italy-based, EU-facing business. Fix is
   Consent Mode v2 with defaults denied plus a light banner.
2. **CTA panel over the footer logo** - two cases remain: `/it` at 600-767px
   (lifted 118px, needs ~150, so 32px still overlaps) and `/404` at 900px, which
   was never included. Elsewhere the gap is -5 to +7px rather than the intended
   ~48px: visible but tight. Full root-cause analysis and the dead ends already
   tested are in git history at `b8db75f`.
3. **Sources blocks** still on `reduce-bracketing-returns` and
   `multilingual-phone-support-eu-expansion`; the "skip the sources" instruction
   post-dates them.
4. **This repo is public.** Reverted ROI-calculator commits remain in history.
5. **Footer layout differs between page families on mobile** - Framer pages
   centre it, authored pages left-align it.
6. **ROI calculator** is 4.4MB raw / ~900KB gzipped - React *development* build
   plus in-browser Babel. Production React + pre-compiled JSX takes it to ~60KB
   gzipped without touching the calculator's code.

---

## Search Console - check back 12 Aug

Requested indexing 5 Aug on six hub pages: `/industries`, `/blog`, `/it/settori`,
`/it/blog`, `/it/prezzi`, `/use-cases/cart-abandonment-recovery`.

**Do not re-request them.** Google's own message: submitting a page repeatedly
does not change its queue position.

Expect the 48 "Not found (404)" to collapse as the redirects are crawled. The
Page Indexing report lags roughly two weeks, so read dates before drawing
conclusions - on 5 Aug it was still showing a snapshot from 24 Jul, which is what
made the site look far worse than it was.
