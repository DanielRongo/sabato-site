# Session handoff - 6 Aug 2026

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
| Distinct metadata on 11 pages; Italian titles localised; thank-you pages noindexed | `cc68f52` |
| **All 42 over-length titles fixed; blog SEO titles decoupled from headlines** | `b555a35` |
| Page titles owned at their generators, not post-build patches | `fbe8578` |

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

### DONE 6 Aug: items 1, 2 and the titles half of item 3

- Six pages wearing the homepage's title and description: fixed. **Zero duplicate
  titles and zero duplicate descriptions** across all 66 pages, from 14 and 12.
- Italian pages carrying English titles: all localised, including the two blog
  indexes (`blog-index-it.html` had a hardcoded English `<title>`).
- Thank-you pages `noindex` + out of the sitemap, so they cannot fire phantom
  GA4 conversions. `/thank-you-page` also gained the canonical it never had.
- **42 titles over 60 characters -> 0.** The real fix was not length: 36 use-case
  and industry pages all began "Voice AI for" / "Voice AI per", and Google
  truncates from the end, cutting the only part that identified each page. All
  now front-load the distinguisher.
- Blog posts gained an optional `seo_title` frontmatter field, so the `<title>`
  is short while the `<h1>` keeps the full editorial headline. Permanent for
  every future post.
- Verified on production: 66 pages, 0 over-length, 0 duplicates.

### 3b. STILL OPEN: 33 meta descriptions over 160 characters

Deliberately not done. Automated trimming produced 18 fragments ending
mid-thought ("e 57% delle", "quasi nessun brand") and four collapsed under 63
characters, because their first sentence was already over the limit.

Worth knowing before spending time here: **meta descriptions are not a ranking
factor** and Google rewrites most of them. The existing ones already front-load
the strong material, which is exactly what shows when Google truncates. This
needs hand-written copy or nothing - do not ship machine-trimmed fragments.

### 4. Build a `/use-cases` hub page

Nine use-case pages exist with **no index page**. Industries has `/industries`;
use-cases has nothing. They are reachable only through footer links, which is why
Google has to be told about each one individually rather than discovering them as
a group. A hub is the single biggest structural gap left, and it is a page real
visitors want too.

**Build this hub with the TRIGGER band already in mind** - Daniel approved the
idea on 11 Aug and it is specified in full further down this file ("IDEA (11
Aug): split the Use Cases menu into TASKS and TRIGGERS"). The cheapest first
version of the triggers is a band on this hub, so doing the hub first and
retrofitting the band later is wasted work. Read that section before starting.

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

## IDEA (11 Aug, APPROVED - belongs with backlog item 4): TASKS vs TRIGGERS

Daniel's observation: the use-case menu shows only what the agent DOES on a
call. It says nothing about why an ecommerce operator starts looking in the
first place. Two different readers at two different moments.

  TASK  (what happens on the call)      TRIGGER (why they came looking)
  -----------------------------------   -----------------------------------
  Where is my order                     Peak season is coming
  Cart abandonment recovery             We are opening a new market
  Pre-sales consultation                Our team is stuck on repetitive work
  Managing returns                      We are launching a new store
  ...9 of these, all live                Care costs are out of control

Daniel's five triggers, verbatim from customer conversations:
  1. Peak season handling
  2. Expand into foreign markets, in their languages
  3. Upskill the CS team onto high-value activities
  4. Start new pilot stores
  5. Optimise customer care costs

MISSING, in rough order of how much they are worth:

  a. REVENUE LEAKING OFF THE PHONE. All five above are cost, capacity or
     coverage. Not one of them says "you are losing orders today." In
     high-consideration categories a missed call is a missed cart, and this is
     the only framing that gets a yes without waiting for a budget cycle. It
     also prices higher than any cost-saving story.
  b. Out-of-hours coverage. Distinct from peak season: one is a spike, the
     other is a permanent hole in the week.
  c. Cannot hire / churn in the team. Distinct from cost: "we would happily
     pay, we cannot staff it" is a different conversation.
  d. Replacing an outsourced BPO. A renewal date is a real trigger with a real
     incumbent to displace, and the buyer already has a number to compare to.
  e. Nobody knows what is actually said on the phone. Call intelligence is the
     part customers do not churn from once they have it.

TWO CAUTIONS BEFORE BUILDING ANY OF IT:

  * Consolidate first. 3 and 5 are one conversation to a buyer (team economics);
     2 and 4 are one conversation (launching something new). Five near-duplicate
     pages dilute; three sharp ones convert.
  * These pages will get almost no organic search traffic. Nobody googles
     "upskill my CS team". Task pages match search intent, trigger pages match
     a state of mind. Build them as sales and positioning assets - and as
     framing an LLM can quote - not as an SEO play, and do not judge them on
     sessions or the conclusion will be that they failed.

Nav risk: this would make three taxonomies - Use Cases (what), Industries
(who), Triggers (why). That is a lot for one header. Cheapest first version is
a band on the /use-cases hub, promoted into the nav only if it earns it.

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
