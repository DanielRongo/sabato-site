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

## TASK (12 Aug, Daniel): rework the homepage messaging around the TEAM

Daniel, verbatim: "rework the messaging in the homepage making it about powering
up customer service staff with the use of AI, or add an AI powered super
customer service agent to your team. I mean something that is not too technical
and that E-Commerce CEOs can understand and relate to."

WHERE IT IS TODAY

  EN h1     "The voice layer your e-commerce is missing."
  IT h1     "Il tuo e-commerce ha tutto. Tranne la voce."
  band h1   "We handle the AI. You handle your store."
  title     "Voice AI Agent Platform for E-Commerce | Sabato AI"
  desc      "Managed voice AI that guides buyers through complex product
             decisions - sizing, compatibility, specs. We build it, we run it."

All of it is infrastructure framing. "Voice layer", "platform", "agent" describe
the thing we built, not what changes for the person buying it. A CEO does not
have a voice-layer problem; they have a team that is drowning in repetitive
calls and a headcount they cannot grow.

THE SHIFT

  FROM  a voice layer / platform you install
  TO    a customer service teammate you add, who takes the repetitive volume so
        your people move onto the work that needs a human

The proof already says this - Marco's quote is literally "our team now focuses
on the cases that actually need a person." The homepage is the only surface
still talking like a product spec.

FOUR THINGS TO GET RIGHT, and they are the traps

  1. AUGMENTATION MUST NOT KILL THE ROI STORY. "Powers up your team" is warmer
     and it defuses the layoff objection, which is real - no CEO wants to
     announce they replaced support with a robot. But if it implies you still
     need the same headcount, the business case evaporates. The honest
     resolution is the one the case study already makes: the agent absorbs the
     repetitive volume, so the same team covers more without growing. That IS
     the cost story, told from the team's side instead of the P&L's.

  2. DO NOT LOSE THE SEARCH TERM IN THE REWRITE. The <title> and description
     carry "voice AI" / "e-commerce", which is what the page is actually found
     for, and Search Console work is mid-flight. Human language belongs in the
     H1 and the subhead; the keyword stays in the title tag and the meta. These
     are two different audiences reading two different surfaces - do not
     sacrifice the crawler's copy to fix the human's.

  3. "SUPER AGENT" IS CROWDED. The phrase is becoming generic across the AI
     tooling market in 2026. Check it does not put us in a category we do not
     want before it goes in an H1. "Teammate", "the person who never misses a
     call", or naming the agent (Elena, as in the Creative Cables story) are
     warmer and more ownable than a category noun.

  4. THREE <h1> TAGS. site/index.html renders the same H1 three times (Framer's
     responsive variants). Whatever the new copy is, this is the moment to fix
     that rather than triplicate the new one.

SCOPE: EN and IT together - a homepage rewritten in one language only is a
half-rewrite, same rule as the blog. IT is not a translation of EN here; "Il tuo
e-commerce ha tutto. Tranne la voce." is its own line and the Italian will need
its own idea, not a rendering of the English one.

NOT STARTED. Needs Daniel's copy direction first, or a draft to react to -
the last two landing-page rewrites were rejected for reading like blog posts,
so bring three short options, not one long page.

---

## TRIGGERS / PLAYBOOKS - state of the set (13 Aug)

LIVE (six):
  Handle Peak Season          /playbooks/peak-season
  Expand Into New Countries   /playbooks/international-expansion
  Answer Every Call           /playbooks/missed-calls
  Cut Support Costs           /playbooks/support-costs
  Free Up Your Team           /playbooks/high-value-work      <- SEE NAMING BELOW
  Support Every Language      /playbooks/multilingual-support

TWO NEW ONES DANIEL ADDED, 13 Aug:

  1. OFFER MULTILINGUAL SUPPORT - BUILT (multilingual-support).
     The line against international-expansion is the buyer's STATE, and it must
     be held or the two become one page twice:
       Expand    - you do NOT sell there yet. Trigger is a launch decision.
       Multiling - you ALREADY sell there. Trigger is customers you are
                   underserving today; the orders already exist.

  2. UPSCALE YOUR CS REPS - NOT BUILT, and it needs a naming decision first.
     Daniel, 13 Aug, verbatim: "I mean that if you re-allocate them to do
     something higher value (e.g. launch a new initiative) they'll be better.
     Free up your team I see it more as alleviating workload from stressed out
     customer service reps."

     So these are TWO different pages, and the one already built is the wrong
     one for its label:

       /playbooks/high-value-work  - currently labelled "Free Up Your Team", but
           its content is B2B channel + VIP concierge + "the phone is eating
           your best people". That is the RE-ALLOCATION page, i.e. UPSCALE.
           It should probably be relabelled.

       STILL TO BUILD - the actual "Free Up Your Team": workload relief for
           reps who are stressed and buried. Distinct from Cut Support Costs,
           which is the same team seen from the CFO's side. Three angles on one
           team, and they are genuinely different buyers:
             Cut Support Costs  - it costs too much            (CFO)
             Free Up Your Team  - they are drowning, burning out (people/ops)
             Upscale the reps   - redeploy them to grow something (growth)

     DO NOT collapse these again. I merged upskill into costs on 13 Aug on the
     argument that they were one buyer conversation; Daniel corrected it, and he
     was right. Cost is defensive, relief is human, upscale is offensive.

STILL UNBUILT from the earlier list: replacing an outsourced BPO (sharpest
commercially - a renewal date is a real deadline with an incumbent to displace),
out-of-hours coverage, and call intelligence.

CAUTION THAT STILL APPLIES: these pages get almost no organic traffic. Nobody
googles "replace my BPO". They are sales and positioning assets, and framing an
LLM can quote - do not judge them on sessions.

---

## TASK (13 Aug, Daniel): split the Product section into four

Daniel, verbatim: "add to the things to do the product section split into:
Voice Agent Builder, Visual Agentic Workflow Builder (to be renamed), Called
Data Intelligence, Calls Evaluation Tool (to be renamed)".

  1. Voice Agent Builder
  2. Visual Agentic Workflow Builder      <- NAME NOT FINAL
  3. Call Data Intelligence               <- Daniel typed "Called"; confirm
  4. Calls Evaluation Tool                <- NAME NOT FINAL
  5. Integrations & Webhooks              (added 13 Aug)

Note on 5: it is a different KIND of item from 1-4. Those are things the
customer uses; integrations are how the thing connects to what they already
run. On most sites that argues for it sitting slightly apart - last in the
section, or as a page the other four link into - rather than as a peer tile.
Worth deciding when the section is laid out, not after.

TWO NAMES ARE EXPLICITLY PROVISIONAL. Do not build nav labels, slugs or a hub
around 2 and 4 until Daniel has settled them - a slug is the one thing on this
site that is expensive to change once indexed, which is exactly why the
/use-cases URL space was never renamed when the menu was reorganised.

THIS IS A THIRD TAXONOMY. The header already carries Use Cases (what the agent
does), Industries (who it is for) and now Playbooks (why you are looking).
Product (what you actually buy) is a fourth axis and the menu is already at its
limit - Daniel's own words on 13 Aug were that it is "overcrowding". Decide
where Product lives BEFORE building the pages: most likely its own top-level
nav item rather than a fourth column in an existing dropdown.

NOT STARTED. Needs the two names first, then a nav decision, then pages.

---

## 14 Aug: SITE-INVENTORY.md, and the three bugs writing it exposed

`tools/site_inventory.py` generates `SITE-INVENTORY.md` from the **built** site -
every page, its H1, lede, title, meta, section headlines, plus one table of every
cited figure on the site. Written so the homepage and pricing rewrites cannot
contradict the ninety-odd pages already live. Re-run it after any build; never
hand-edit the output, edit the tool.

Reading its first output found three things nobody had seen:

1. **`/it` homepage: the WISMO card was still in English on phones.** Framer's
   phone breakpoint carries its own copy of the text, and that copy was never
   translated. Now reads the Italian line the desktop variant uses.
2. **`/it/contatti`: the subtitle was still in English on phones.** Same cause.
3. **`/it` homepage: an English `<h1>`** ("We handle the AI. You handle your
   store.") in the static HTML. React replaces it at hydration so no human ever
   saw it - but a crawler reading raw HTML does.

**Where these actually live, and why this will happen again.** Fixing the HTML
was not enough: Framer re-renders from a content-hashed `.mjs` bundle under
`site/fuc/`, so the English text came straight back. The real fix was patching
the two IT-only chunks and running `tools/rehash_edited_assets.py origin/main`.
Check `site/fuc/*.mjs`, not just the HTML, for any Framer-page copy change - and
confirm the chunk is IT-only first (`grep` the basename against `index.html` and
`it.html`); the shared chunks carry both languages.

**No automated check covers this class of bug.** It was found by rendering the
seven Framer Italian pages at 1440/810/390 and flagging visible text that scored
English-heavy. Worth turning into a gate step if a fourth one turns up.

### Also fixed: the injectors were leaking a blank line per run

`inject_ga.py` inserted its Consent Mode block as `"\n" + BLOCK` but stripped it
with a pattern that did not eat the leading newline. Every gate run therefore
added one blank line to all 108 files, forever, and produced a 108-file diff even
when nothing had changed - which is exactly the noise that hides a real change.
The strip pattern now eats it. Verified: running the three injectors twice in a
row now yields an identical site digest, i.e. a stable fixed point.

### Delivering a batch over the bridge - the two commands that do NOT work

Both of these were learned the hard way on 14 Aug, and both fail in ways that
look like something else.

1. **`tar --overwrite` does not exist on macOS.** BSD tar rejects the flag
   outright and extracts nothing - but the shell keeps going, so the next
   command in the block runs against an untouched repo and its error is the one
   you end up debugging.
2. **`tar` cannot replace an existing file on the bridge mount at all.** The
   mount refuses `unlink`, and tar's overwrite path is unlink-then-create, so
   every existing file fails with `Cannot open: File exists` while every NEW
   file extracts fine. That half-applied state is the dangerous one: the repo
   ends up holding new asset hashes with old HTML referencing the old ones.

**What does work:** truncate-and-write in place. Extract to a scratch dir, then
copy byte-for-byte over the destinations:

```python
with open(dst, "wb") as f:      # truncate: permitted
    f.write(open(src, "rb").read())
```

`os.remove` / `shutil.move` onto an existing path still fail. `_to_delete/` is
gitignored for exactly this reason - the bridge cannot delete, so scratch lands
there and Daniel removes the folder by hand.

**Also:** `.git/index.lock` has to be moved aside after most bridge git calls,
and `.deploy-receipt.json` is gitignored, so it only reaches the Mac if it is in
the delivery payload. If it is missing, `ship.sh` refuses with "site/ does not
match" even though the site is fine.

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
