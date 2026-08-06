---
title: "Your Customers Aren't Calling Because Your Site Is Confusing. They're Calling Because It's Wrong."
seo_title: "Why Customers Call Instead of Ordering Online | Sabato AI"
slug: why-customers-call-instead-of-ordering-online
description: "Why customers call instead of ordering online: it's a data-accuracy problem, not a navigation one. How to measure your data-integrity tax from your own call log."
category: Data
date: 2026-07-30
cover_style: offwhite
---

33% of B2B buyers say they've had an order go wrong because the information on a supplier's web store was inaccurate. That's from [Sana Commerce's vendor-commissioned B2B Buyer Report 2025](https://www.globenewswire.com/news-release/2025/01/29/3017144/0/en/New-Survey-Reveals-Real-Time-Data-Is-the-Secret-Weapon-for-Winning-Over-Frustrated-B2B-Buyers) (fieldwork by SAPIO Research, n=750 professional buyers, six countries including the UK, Germany and the Netherlands). In the same vendor-commissioned survey, 40% named a lack of transparency on stock and delivery dates as their single biggest frustration.

Neither of those is a navigation problem. You cannot fix either with a new mega-menu.

Neither of them shows up in your analytics, either. A bounce tells you somebody left. It cannot tell you which claim on the page they stopped believing. A call can: the buyer names the product and reads the number back to you, asking you to confirm it. That makes the call log the only instrument you own that tells you which of your records is wrong.

:::quote
The phone rings because the site isn't trusted, and the site isn't trusted because it has been wrong before.
:::

A **data-integrity tax** is the salaried time you spend confirming by phone what your own website already claims. Every call that only verifies a claim your site already makes is that tax - and the call log is the itemised bill.

## What buyers actually say goes wrong

The stated failure modes are mostly accuracy, and they're not close.

:::chart bar
What B2B buyers say goes wrong, by share naming it
Lack of transparency on stock and delivery dates | 40% | top frustration
Struggle to find products online | 36% | the one findability problem
Order error caused by inaccurate web store info | 33%
Inaccurate delivery times stop them ordering | 29%
Inaccurate stock levels stop them ordering | 28%
Say their online buying experience meets expectations | 19% | the number to put on the wall
Source: Sana Commerce B2B Buyer Report 2025 - vendor-commissioned, SAPIO Research, n=750, September 2024 fieldwork
:::

40% of B2B buyers name lack of transparency on stock and delivery dates as their top frustration. 29% say inaccurate delivery times actively stop them ordering online - again, the software vendor's own commissioned study, not an independent one. 28% say the same about inaccurate stock levels.

The consequence: 33% have had an order error caused by inaccurate web store information, per the same vendor-commissioned research. 85% report frustrations that led them to abandon a purchase. And only 19% say their online buying experience meets expectations.

**The concession.** 36% struggle to find products online, in the same dataset. That one is a findability problem, and a redesign can fix it. So the argument isn't "UX doesn't matter". It's that one of the top failure modes is UX, the rest are accuracy, and your budget is allocated the other way round.

None of those percentages are yours, though. A survey of 750 buyers across six countries tells you the category. It cannot tell you whether it's your stock field or your lead-time field that's lying, or on which SKUs. One system in your business records that, and it's the phone.

And the stakes: 75% would switch supplier for a better online experience, which Sana reports as up from [74% the year before](https://www.globenewswire.com/en/news-release/2024/03/07/2842219/0/en/B2B-Web-Stores-Are-Driving-Buyers-Away-According-to-New-Survey.html). Don't read that as a trend. The one-point move sits inside anyone's margin of error, and the two waves aren't the same sample - the 74% came from n=1,000 fielded in summer 2023, the 75% from n=750 fielded in September 2024. Read 75% as a level. Three quarters of your buyers are open to leaving, and they have been for at least two surveys.

## Can you trust a software vendor's survey about how badly software is needed?

Conditionally, yes, and only if it passes a test most vendor reports fail.

Sana Commerce sells B2B ecommerce software and paid for this research, which is reason enough for scepticism. It is also the best-disclosed dataset available on the question: named independent fieldwork partner (SAPIO Research), stated sample (n=750 professional buyers), stated fieldwork window (September 2024), stated countries - US, UK, Germany, Netherlands, Mexico, Australia. Three of the six are European markets, which is rarer than it should be in this literature.

That's the whole test: named fieldwork partner, disclosed n, disclosed window, disclosed countries, and questions about the buyer's experience rather than the vendor's product category. Sana clears all five. Most vendor "reports" clear none, which is why "a recent industry study found" is usually a sentence with nothing behind it.

One thing that doesn't count as a check: a trade title repeating the press release. Half a dozen outlets carried these numbers in January 2025. That's circulation, not corroboration. You need a different house asking a different question.

Then the independent check. Gartner sells research subscriptions, not ecommerce platforms, and found that [69% of B2B buyers report inconsistencies](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-sales-survey-finds-61-percent-of-b2b-buyers-prefer-a-rep-free-buying-experience) between information on the sales organisation's website and what sellers tell them (n=632, fieldwork August - September 2024). The two studies corroborate the failure category, not each other's percentages.

One limit worth stating, because it cuts against my own argument: Gartner does not disclose which countries these waves cover. Neither the 2024 nor the 2025 wave names a geography anywhere I can find. So treat 69% as evidence that the failure category is real and widespread, not as a European percentage. I'm using it for the category, not the number.

Gartner doesn't validate Sana's percentages. It validates that the information layer contradicts itself and buyers notice.

If the site and the rep disagree roughly seven times out of ten, calling isn't irrational. It's an accurate risk assessment. The call is the buyer's audit of your data - and your call log is the only copy of that audit you get to keep.

## The three questions that generate the calls

Almost all pre-purchase call volume reduces to three database lookups, each owned by a different system nobody has reconciled.

**Is it in stock?** This is a WMS or ERP stock record. It fails on multi-warehouse setups where the site shows one pool, on cycle counts nobody reconciles, on allocated-versus-available confusion, on marketplace channels drawing down the same inventory, and on drop-ship lines where you hold no stock and have no live feed from the supplier. Whether the ERP is SAP, Business Central, NetSuite, Sage or Odoo changes the field names, not the failure.

**When will it ship?** This is available-to-promise, and ATP needs purchasing data, not warehouse data. It fails on supplier lead times typed into a field once in 2022, on no distinction between an in-stock ship date and a backorder date, on order cut-off times that were never modelled, and on carrier transit assumed rather than measured. Safety stock hides some of this until it doesn't.

**Will it fit?** This is PIM and manufacturer fitment data. In HVAC, electrical, building materials and spare parts that data arrives as ETIM classifications, BMEcat files, GS1 identifiers or a supplier spreadsheet, and it is frequently stale on arrival. It fails on attributes missing from older SKUs, on manufacturer revisions never re-imported, and on compatibility expressed as prose inside a PDF instead of as structured attributes against a GTIN. Bad attribute data also drives the wrong-product order that comes back as a return.

These aren't conversations. They're queries. A human is being paid to run a database lookup by voice because the database isn't trusted to display the answer. A query asked in Dutch is still a query - a separate staffing problem, covered in [the multilingual phone support post](/blog/multilingual-phone-support-eu-expansion).

One distinction most call-deflection content collapses: this is pre-purchase doubt about whether you'll actually deliver. [WISMO](/use-cases/where-is-my-order) is post-purchase, after the money moved, with different owners and different fixes. Don't put them in the same bucket.

## How to measure what share of your calls are just data questions

Your analytics package can tell you where people left. It cannot tell you which claim they stopped believing. The call line can, once you instrument it: one week of setup, two weeks of tagging. Not a project.

**Five buckets, no more.** (a) stock availability, (b) lead time or delivery date, (c) fitment or compatibility, (d) pricing or account, (e) everything else. Post-purchase order-status calls go in "everything else". You are measuring pre-purchase only.

**Tag at the point of the call, not from recordings.** One click by whoever answered. Retrospective coding of call recordings is a project, and projects don't happen.

**Sample.** Two full weeks, every call on the sales line. Two weeks is a small, seasonal sample and you should say so out loud. In HVAC, code one week in season and one week out, or the number will lie to you.

**Compute the share.** (calls in buckets a+b+c) ÷ (all pre-purchase calls).

**Convert to money.** Multiply by your fully loaded cost per contact - salary plus employer costs, systems, supervision and the share of overhead the function actually consumes, not the hourly wage.

**Then the part nobody does.** Take 20 stock and lead-time calls and go check what the site was showing at the time of the call. Sort each into wrong, missing, or right-but-not-believed. Three diagnoses, three completely different fixes, and only the third one is a UX problem. This step is the whole instrument: the call gives you the timestamp and the SKU, and the site record at that timestamp gives you the verdict.

:::takeaway The paragraph to steal
Tag every call on your sales line for two weeks into five buckets: stock availability, lead time, fitment, pricing or account, everything else.
Divide the first three by total pre-purchase calls. That percentage is your data-integrity tax in contact terms.
No published benchmark exists for the share of ecommerce calls that are stock and lead-time questions, so two weeks of your own tagging beats every number on the internet for this decision.
:::

Worth stating plainly, because vendors will fill the gap. If a deflection vendor quotes you a share, ask for the primary study, the sample and the fieldwork date. The most-recycled statistic in this genre - a widely quoted figure for the share of business calls that supposedly go unanswered - has no primary study, no named research body and no methodology anywhere in its citation chain, and this is exactly the topic where that kind of number gets laundered into a board deck.

## Now price the data fix against the redesign

Put the two next to each other before anything gets signed - with your tagged fortnight in hand, because that's the only thing in the room that knows which column your money belongs in.

| Site redesign | Data fix |
| --- | --- |
| Agency fees, discovery, design, build | Cycle-count discipline on top SKUs |
| Internal time from ops, merch, IT | One owned supplier lead-time field |
| Migration and re-platform risk | ATP rule instead of a static promise |
| Timeline measured in quarters | Stock shown as a band, not a fake integer |
| Addresses the findability failure | Fitment backfill, top 200 SKUs by call volume |
| ~36% of stated frustrations | The accuracy failures, which are most of the rest |

The last row is survey data, so read it as the shape of the market's frustrations, not yours. Your split comes off the call log - which is the point of tagging before you sign.

The data fix is usually cheaper, usually unglamorous, and has no vendor pushing it. That's exactly why it doesn't get funded. Nobody's quarterly target depends on your supplier lead-time field being right.

Display honesty beats display precision. "In stock, 4 available, counted this morning" and "ships in 2-3 weeks, supplier-confirmed" both outperform a confident integer that turns out to be wrong. The second time a buyer gets burned, they start phoning permanently, and you've bought yourself a recurring cost to save a UI decision.

## Why quietly removing the phone number backfires

Because deflection without the data fix trades call cost for regret.

[67% of B2B buyers](https://www.gartner.com/en/newsroom/press-releases/2026-03-09-gartner-sales-survey-finds-67-percent-of-b2b-buyers-prefer-a-rep-free-experience) say they'd prefer to complete a purchase with no sales rep interaction at all (Gartner, n=646, fieldwork August - September 2025, countries not disclosed). Read alone, that says hide the number.

But Gartner has also reported that buyers who prefer a rep-free experience show [purchase regret 23% higher](https://www.gartner.com/en/newsroom/press-releases/gartner-says-b2b-sales-organizations-need-to-give-customers-a-se) than buyers who do interact with a rep. Flag that one twice. First, it's old: those surveys were fielded November - December 2020 (n≈1,000), which pre-dates most of the self-serve tooling now in use, and it comes from the same research house as the 67%. One house, two waves, no independent replication. Second, read what it actually compares - buyer preference groups, not buying methods. It does not show that taking your phone number down causes regret. It's a caution, not a law, and I'm not going to dress it up as more.

For directional corroboration from a different house: [McKinsey's B2B Pulse](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/five-fundamental-truths-how-b2b-winners-keep-growing) describes a "rule of thirds" - roughly one-third of buyers hoping for in-person interaction, one-third wanting remote, one-third preferring digital self-serve, stable across geography, industry and deal size (n≈4,000, 13 countries). That corroborates the shape. It does not corroborate the 23%.

Gartner's 2024 wave (n=632) settles the practical question: the largest single preference group wasn't rep-only or digital-only. It was buyers wanting an average of 3.0 activities both online and with a rep, versus 2.3 with reps only and 1.8 via digital self-service only. Buyers don't want no rep. They want no unnecessary rep.

Removing the phone number while your data is wrong doesn't remove the doubt. It removes your chance to resolve it. And deflection-by-neglect, where the number stays up but nobody answers, is the expensive version, because abandoned calls skew high-intent. Deflection is legitimate after the answer on the page is correct. Only then.

## The part that argues against my own product

We sell voice AI. Here's the case against deploying it.

A voice agent answering "is it in stock" is a natural-language wrapper on the same ERP field a human would have read. If the field is wrong, the voice agent is wrong: faster, at higher volume, and with more apparent authority than the person it replaced. Fix the field, then automate reading it. That order is not optional.

Humans hedge, and the hedge is the quality control. Someone who half-trusts the screen says "let me check with the warehouse and call you back". That instinct is unwritten process, it catches errors, and it is the first thing automation removes. A confident wrong answer costs more than a slow right one, because it converts into an order that then fails. That's the 33% arriving by a new route.

:::quote
If your stock record is unreliable and you put voice AI on top of it, you've bought a machine for scaling misinformation at 3am.
:::

Where a voice layer does earn its place on imperfect data is when it's allowed to express uncertainty and take an action. "The system shows four, last counted Tuesday. I'll have the warehouse confirm and text you within the hour" is honest, and it's a real answer at 9pm when nobody's in. That's a different product from "we have four", and it's the only version worth deploying on data you don't fully trust. It's the version we build at Sabato, and it's still second in the sequence, not first.

:::action What to do this week
Add five call-reason buttons to the sales line. Start tagging tomorrow.
Pull 20 stock and lead-time calls and check what the site displayed at the time. Sort into wrong, missing, right-but-not-believed.
Find out who owns the supplier lead-time field. If the answer is "nobody", that's the finding.
Put the measured data-question share next to the redesign quote before it gets signed.
Switch stock display from a precise number you can't defend to a band you can.
:::

The site isn't confusing. It's wrong, and your customers found out before you did.

## FAQ

**Why do customers call instead of ordering online?** Mostly to verify information they don't trust. In Sana Commerce's vendor-commissioned B2B Buyer Report 2025 (fieldwork by SAPIO Research, n=750), 40% of buyers named a lack of transparency on stock and delivery dates as their top frustration, and 33% had experienced an order error caused by inaccurate web store information. The call is a verification step, not a navigation failure.

**What share of ecommerce support calls are about stock and delivery dates?** No credible published benchmark exists, and any vendor quoting one is likely citing an untraceable figure. Measure it yourself: tag every call on your sales line for two weeks into five buckets - stock, lead time, fitment, pricing, other - then divide the first three by total pre-purchase calls. Two weeks of your own tagging beats every number online.

**Is it better to fix product data or redesign the website?** Measure first, then fund. Buyers' stated failure modes split into one findability problem - 36% struggle to find products online - and several accuracy problems, per Sana Commerce's vendor-commissioned 2025 survey. A redesign addresses the first. Only accurate stock, lead-time and fitment data addresses the rest, and it is usually the cheaper fix.

**Should we remove the phone number to reduce call volume?** Not before the on-page answer is correct. Gartner found 67% of B2B buyers prefer a rep-free experience (n=646, August - September 2025, countries not disclosed), and has separately reported that buyers who prefer rep-free show 23% higher purchase regret than buyers who interact with a rep. Treat that second figure carefully: it was fielded November - December 2020, and it compares preference groups, not buying methods. Removing the phone number removes your chance to resolve doubt, not the doubt.

**Can voice AI answer stock and lead-time questions?** Only as accurately as the ERP record behind it. A voice agent is a natural-language wrapper on the same stock field, so a wrong field produces wrong answers faster and with more authority than a human who would have hedged. Fix the data first. Automate reading it second. That order is not optional.
