---
title: "What a voice agent costs to run, not to build"
seo_title: "Voice Agent Running Costs: The Seven Lines | Sabato AI"
slug: voice-agent-cost-to-run
description: "The per-minute price is the smallest line on the sheet. The seven costs that actually recur, and why running cost scales with variety, not volume."
category: Voice AI DIY
date: 2026-08-18
cover_style: black
---

*The Build File, issue 03. A season on running a voice build without being an engineer.*

Everybody quotes the per-minute cost.

It's the number on the pricing page, it's the one your technical lead brings to the meeting, and
it is the smallest line on the sheet. Not one of the smaller ones. The smallest.

This matters because almost every in-house business case for a voice agent is built on the cost
to *build* it. A one-off, quoted in weeks of developer time, which everyone will have forgotten
about within a year. The cost to *run* it is forever, and it usually isn't in the document at all.

The running cost breaks into seven lines. You won't find your own numbers here; you'll find
which questions to send to your finance director, and what happens if one of the lines is missing.

---

## The seven lines

**1. Processing, per minute of conversation.** Speech in, a model deciding what to say, speech
back out, metered by the minute. This is the famous one, it's genuinely metered, and it has been
falling steadily for two years. It is the line people quote because it's the only one with a
published price, which is a bad reason.

**2. The line itself.** A phone number in each country you sell in, rented monthly, plus inbound
minutes at carrier rates. Modest per market. The thing to notice is *per market*. Four countries
is four arrangements, four invoices and four sets of paperwork, not one line item with a bigger
number.

**3. Somebody who listens.** Every week, a person pulls a sample of calls, listens to them, and
fixes what went wrong. Not during the project. Forever.

This is the largest recurring line in most voice operations and it is missing from most business
cases, because it doesn't look like infrastructure. It looks like somebody's afternoon. It is
still the difference between an agent that improves and an agent that decays.

**4. Somebody who answers at 8pm.** When the thing breaks outside office hours, either a person
is paid to be reachable, or the line is degraded until Monday. Both are legitimate choices. Only
one of them is usually costed, and it's rarely the one that got chosen.

**5. The testing that keeps happening.** Maintaining a test set, running it monthly, re-running it
after every change to the instructions or the catalogue. This is small, unglamorous, and always
the first line cut. It is why so many agents that worked in March don't in September.
[The twenty calls](/blog/voice-agent-acceptance-test) is the cheap version of this line.

**6. Each additional language.** Not a multiplier of line 1. A repeat of lines 2 through 5: another
set of numbers, another test set, another weekly listening session. And the part that
surprises people: another person who can actually judge whether those calls were any good. You cannot
review Dutch calls with an Italian team.

**7. The rebuild.** Every eighteen months or so the ground moves underneath: models change,
a supplier's data format shifts, the thing you built around gets deprecated. Treat it as a
recurring capital line rather than an annual surprise, because it is one.

---

## The line that inverts everything

This is the part worth taking to your CFO, because it contradicts the instinct that everyone
brings to software spending.

In normal software, you build once and each additional user costs you close to nothing. That's
the whole shape of the industry and it's why software companies are valuable.

Voice doesn't behave like that, because most of the recurring cost is **human attention**, which is
lines 3, 4, 5 and half of 6. Human attention does not scale with volume. It scales with **variety**.

Ten thousand calls a month about three things is cheap to run. Two thousand calls a month about
forty things is expensive, and can easily cost more in total despite being a fifth of the volume.
Every distinct kind of call needs its own instructions, its own test cases, its own review, and
its own failure modes that somebody has to notice.

So the question your business case is built on is probably the wrong one. It's almost
always *how many calls do we get?* The question that actually drives the running cost is **how
many different kinds of call do we get**. The answer decides whether this is cheap or
ruinous. That's not a budgeting detail; it's the entire argument for scoping the first agent
narrowly.
<!-- FORWARD LINK - issue 05. On the day /blog/scoping-a-voice-agent publishes, restore:
     [scoping the first agent narrowly](/blog/scoping-a-voice-agent) -->

---

## The European multiplier

Every one of those human lines is priced in local labour, which is why this business case does
not transfer across the continent.

In 2025, hourly labour costs across the EU ranged from &euro;12.0 in Bulgaria to &euro;56.8 in
Luxembourg, against an EU average of &euro;34.9 and a euro area average of &euro;38.2, according
to Eurostat. The Netherlands sat at &euro;47.9, Denmark at &euro;51.7, Romania at &euro;13.6.

A caveat, because it matters: those are whole-economy figures for enterprises with ten or more
employees, covering wages plus employer social contributions. They are a sound proxy for how
relative labour cost varies between markets. They are not a quote for what a customer service
agent costs you, and anyone using them that way is being sloppy.

Used properly, though, they say something blunt. The identical agent, handling identical volume,
has a business case that differs by roughly four times depending on which side of Europe your
support team sits on.

And there's an awkward consequence. The operators with the strongest financial case for
automating are in the highest-cost markets. The operators most likely to attempt building it
in-house, because capable developers nearby are affordable, are in the lowest. The build
instinct is strongest precisely where the payoff is weakest, and it's worth knowing which of
those two you are before anyone writes a line of code.
<!-- FORWARD LINK - issue 07. On the day /blog/voice-ai-europe-markets publishes, restore:
     More of this in [why a Dutch playbook doesn't transfer to Italy](/blog/voice-ai-europe-markets). -->

---

## The one-page model

Take this to whoever owns the numbers. The right-hand column is the work.

| Line | Recurs | How to get a real number |
|---|---|---|
| Processing per minute | Monthly, with volume | Ask for a quote at your actual monthly minutes, not list price |
| Numbers and carrier minutes | Monthly, per country | One quote per market you sell in |
| Weekly listening and fixes | Forever | Hours per week x your loaded hourly cost. Name the person |
| Out-of-hours cover | Forever, or never | Decide explicitly. "We'll see" costs the same as the expensive option |
| Monthly testing | Forever | Half a day a month. Put it in someone's calendar or it won't happen |
| Each extra language | Per market | Re-run rows 2 to 5 for that market, including a reviewer who speaks it |
| Rebuild | Every 18 to 24 months | A fraction of the original build, annualised |

If a build proposal covers the first row and none of the others, it isn't a costing. It is a
quote for the cheapest component, and it will be wrong by a multiple rather than a percentage.

None of this means building in-house is the wrong answer. For some businesses it plainly is the
right one. It means the decision should be made against the running cost, not the build cost,
because the build cost is the part that ends.
<!-- FORWARD LINK - issue 04. On the day /blog/build-vs-buy-voice-ai publishes, restore:
     ...the right one, and the honest criteria are in
     [when you should build it yourself](/blog/build-vs-buy-voice-ai). It means... -->

---

*The Build File is a season for people approving voice builds rather than writing them.*

<!--
NOT FOR PUBLICATION. Verification note. publish.py strips HTML comments, so this
never reaches the page - it stays here as the provenance record.

Every euro figure in this post is 2025 hourly labour cost data, cross-checked in two independent
sources before drafting:
  1. Eurostat, "EU hourly labour costs ranged from EUR 12 to EUR 57 in 2025" (31 Mar 2026)
     https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260331-2
  2. Plataforma Media, reporting the same Eurostat release independently
     https://www.plataformamedia.com/en/2026/03/31/eu-labour-costs-2025-portugal-19-4-euro/
  Corroborated by Eurostat Statistics Explained, "Hourly labour costs"
     https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Hourly_labour_costs

Figures used: EU 34.9 - euro area 38.2 - Bulgaria 12.0 - Romania 13.6 - Netherlands 47.9 -
Denmark 51.7 - Luxembourg 56.8.

Deliberately NOT used: Italy, Germany, Spain, France, Poland. The release does not state 2025
absolute values for these, only year-on-year changes. Do not add them without going to the
source dataset.

Scope caveat is stated in the body and must stay: whole-economy, enterprises with 10+ employees,
wages plus employer social contributions. Not contact-centre specific.

No per-minute, telephony or vendor prices are quoted anywhere in this post. That is deliberate.
They are single-source, they move quarterly, and quoting them dates the page. The post gives the
model and tells the reader to get his own quotes.
-->
