---
title: "What a Conversation Actually Costs, and Why It Never Prices Like a Ticket"
seo_title: "What a Customer Conversation Actually Costs | Sabato AI"
slug: what-a-conversation-actually-costs
description: "Cost per contact for voice, built bottom-up from Eurostat labour cost data across eight European countries - plus the occupancy divisor, the employer load and the break-even test that says when automating doesn't pay."
category: Economics
date: 2026-08-05
cover_style: offwhite
---

Eurostat's 2025 reference-year release, published 31 March 2026, puts hourly labour cost across the whole economy at €12.0 in Bulgaria and €56.8 in Luxembourg - a 4.7x spread inside one single market. That is the price of an hour, and it is the only input in this post you can look up. Everything else that decides what a customer conversation costs comes from the fact that it is a conversation: a live exchange that has to be answered when it arrives, written down after it ends, and started over from the beginning if it changes hands.

Three properties, three multipliers on the hourly rate. Run them at the illustrative inputs I use below and six minutes on the call plus two writing it up bills for about eleven and a half minutes of paid time, before anyone escalates anything. That gap is the channel.

What follows is the model, resolved to euros for three countries, plus the cases where it says don't automate.

:::keystat
4.7x
spread in hourly labour cost between Bulgaria and Luxembourg
Source: Eurostat, 2025 reference year, published 31 March 2026

24.8%
of total EU labour cost is employer-side non-wage cost
Source: Eurostat, same release
:::

## The three things that make a conversation cost what it costs

Nobody argues about the hourly rate. Payroll knows it. The argument is about what multiplies it, and every multiplier in a voice model comes from the same place: the channel is synchronous and human on both ends.

### 1. You pay for the gaps, because calls arrive when they arrive

Occupancy is the share of paid hours actually spent on contacts - the price of being answerable in real time. Efficiency has nothing to do with it.

Calls arrive stochastically and you don't get to schedule them, batch them or push them to the end of the day. A ticket queue absorbs a bad hour - it gets longer and nobody notices until the SLA clock does. A phone queue absorbs nothing: the customer is standing in it, and at ninety seconds they are gone. So somebody has to be sitting there before the call arrives, and a person cannot be half-staffed. You buy them in whole hours whether or not the phone rings.

That is what the divisor is. At 70% occupancy you pay for ten hours to get seven hours of contacts. Worth about 43% on the per-contact number, and in my experience it's the step most vendor formula pages skip - because on a channel where work queues politely, it barely exists.

You cannot fix it by pushing people harder; it is set by your arrival curve. Pull the real figure out of your telephony platform, per site and per shift - if you assumed it, every number downstream is wrong by whatever the gap is.

### 2. You pay for writing it down, because speech doesn't record itself into anything

After-call work exists for one reason: the conversation carried information and nothing captured it while it was happening. The part number the customer read off the unit. The promise your agent just made about a delivery date. All of it was said out loud and none of it landed in a system.

So you buy the minutes twice. Once for the exchange, once for transcribing the exchange into the ERP, the CRM and the notes field. On a written channel that step is close to free - the customer typed the record for you. On voice it is a fixed tax per conversation, and it does not shrink when the call gets shorter.

It is also the block of minutes you can attack without touching the conversation. Shaving handle time means rushing a customer; shaving after-call work means fixing a form or a field somebody has to alt-tab to reach. In the placeholder split below it is a quarter of the billed minutes, and most operators have never measured it separately from talk time.

### 3. You pay twice for anything that escalates, because the customer starts again

A ticket that changes hands arrives at the second person with everything the first person wrote. A call that changes hands arrives with a human being who has to re-explain from the top - the order number, the model, the fault, what they already tried, what they were told. The customer is the storage medium, and the handoff makes them replay it.

So an escalated contact is first handling plus a second handling that runs longer than the first, because it opens with a recap and an annoyed person. Half-cost and shared-cost treatments both understate it. Handle time on escalations goes up.

That term decides whether automating a contact pays, and it moves against you exactly when you were wrong about it. The arithmetic is further down.

## You cannot buy this shape off a shelf

A cost-per-contact benchmark cannot know your arrival curve, your after-call-work discipline or your escalation rate, and those are the three terms doing the work. Which makes it useless to you even when it's honest.

The published ones fail before they get that far. They are single-currency - one figure in dollars or pounds, which is arithmetic on the wrong operands if your agents sit in Sofia, Budapest and Rotterdam. They resolve to no country: total operational expenditure divided by contacts handled won't tell you whether to open a desk in Bucharest. And they omit the employer load, because in-house models get built off gross wages from the payroll export - employer social contributions are not in that number, and they are roughly a quarter of the total.

Then there's provenance. The most-cited live-contact cost figure in this category sits behind a paywall and can't be verified from any free primary source, so I'm not repeating it and neither should your finance team. Eurostat publishes for free, names its method, dates its releases.

## The input: what an hour of labour actually costs in Europe

Eurostat's estimate for the 2025 reference year, published 31 March 2026, puts average hourly labour cost across the whole economy at €34.9 in the EU and €38.2 in the euro area, ranging from €12.0 in Bulgaria to €56.8 in Luxembourg - a 4.7x spread. Eurostat publishes no contact-centre-specific series in this release. Anyone quoting €38.2 as "what an agent costs" is wrong, including anyone quoting this post.

The middle of the range matters more than the extremes, because that's where the nearshore decision sits: Romania €13.6, Hungary €15.2, the Netherlands €47.9, Denmark €51.7, all Eurostat whole-economy for 2025.

Growth isn't uniform either. Whole-economy hourly labour costs rose 4.1% year on year in the EU and 3.8% in the euro area in 2025, per the same Eurostat release - but France came in at +2.0%, Italy at +3.2% and Spain at +3.5%. None of them the EU average.

Treat €12.0 to €56.8 as the base rate any per-contact model has to be built on, never as the answer. Eurostat's "whole economy" here means enterprises with ten or more employees across NACE sections B-N and P-S - agriculture, public administration and household employers are outside it - and there is no line item anywhere in it for a customer service desk.

## The 24.8% everyone leaves out

Non-wage labour costs - employer social contributions and the rest of the employer-side load - were 24.8% of total labour cost in the EU and 25.6% in the euro area, in the same whole-economy Eurostat release.

Read that carefully, because the error here is worth about eight percentage points on your own number.

24.8% is a share of the total, not a markup on wages. The €34.9 EU whole-economy figure already contains it. Of €34.9, roughly €8.66 is non-wage and €26.24 is wages and salaries (€34.9 × 0.248 = €8.66; €34.9 − €8.66 = €26.24).

So the conversion you need runs the other way - payroll shows gross, you need fully-loaded:

```
fully-loaded hourly cost ≈ gross hourly wage ÷ (1 − 0.248)
                         = gross × 1.33
```

That step is my arithmetic on the Eurostat share, not a figure Eurostat publishes. Use 24.8% for EU-framed maths, 25.6% (gross × 1.34) for euro-area-framed maths, and say which one you used.

:::takeaway
Plus 33%, not plus 25%.
If your internal cost model applies a 25% uplift to gross, it reads low, and it reads low on every single line.
:::

| Country / aggregate | Hourly labour cost, whole economy (€) | Contact time cost @ 8 min | Fully loaded per contact @ 70% occupancy |
| --- | --- | --- | --- |
| Bulgaria | 12.0 | €1.60 | €2.29 |
| Romania | 13.6 | €1.81 | €2.59 |
| Hungary | 15.2 | €2.03 | €2.90 |
| EU average | 34.9 | €4.65 | €6.64 |
| Euro area | 38.2 | €5.09 | €7.27 |
| Netherlands | 47.9 | €6.39 | €9.13 |
| Denmark | 51.7 | €6.89 | €9.84 |
| Luxembourg | 56.8 | €7.57 | €10.81 |

Hourly labour cost figures are Eurostat, 2025 reference year, published 31 March 2026, and are whole-economy averages - enterprises with ten or more employees, NACE sections B-N and P-S, agriculture and public administration excluded. Eurostat publishes no contact-centre-specific or customer-service-specific hourly cost series. **These are not agent costs.** Columns three and four are the author's arithmetic on illustrative inputs (8 minutes handle time plus after-call work, 70% occupancy) that readers should replace with their own; no benchmark for those inputs exists in the source data. Each column is rounded to the cent before the next one is calculated, so the table reproduces exactly as printed. Carry full precision through instead and four cells land a cent higher - EU €6.65, euro area €7.28, Denmark €9.85, Luxembourg €10.82 - and the Netherlands lands a cent lower, at €9.12.

## The worked calculation: what one conversation costs in Bulgaria, Hungary and the Netherlands

The formula, once. The rate is Eurostat's; the rest is the three properties above, in order:

```
cost per contact = fully-loaded hourly cost
                   × ((handle time + after-call work) in hours)
                   ÷ occupancy
```

The inputs are placeholders. 6 minutes handle time (talk plus hold), 2 minutes after-call work, 70% occupancy - round numbers, to keep the arithmetic legible. Eurostat publishes no handle time, no after-call work and no occupancy figures, and there is no European contact-centre benchmark for them in any source I'd put my name to. Pull your own three out of your telephony platform before you run this.

6 + 2 = 8 minutes = 0.1333 hours. Multiply the hourly rate by that, then divide by 0.70 - the second step is what pays for breaks, briefings, outages and the Tuesday morning where nothing rings.

* **Bulgaria:** €12.0 → €1.60 → €2.29
* **Hungary:** €15.2 → €2.03 → €2.90
* **Netherlands:** €47.9 → €6.39 → €9.13

Every row of the table runs the same two lines.

> **How to compute cost per contact in the Netherlands.** Take Eurostat's whole-economy hourly labour cost for the Netherlands in 2025, €47.9, published 31 March 2026. Multiply by handle time plus after-call work in hours: €47.9 × 0.1333 (8 minutes) = €6.39. Divide by occupancy: €6.39 ÷ 0.70 = €9.13 per contact. Swap all three inputs for your own. The base rate is whole-economy, not contact-centre-specific.

**Sensitivity.** Push handle time plus after-call work from 8 minutes to 10 (0.1667 hours) and hold occupancy at 70%:

* **Bulgaria:** €12.0 × 0.1667 ÷ 0.70 = €2.86 (was €2.29, +€0.57)
* **Netherlands:** €47.9 × 0.1667 ÷ 0.70 = €11.41 (was €9.13, +€2.28)

Two minutes of extra handle time costs 57 cents a contact in Bulgaria and €2.28 in the Netherlands. Four times the money for the identical operational failure - an agent who can't find the fitment table, a hold while somebody walks to the warehouse.

That's the strategic point. In a low-cost location a slow conversation is a rounding error and your effort belongs elsewhere. In a high-cost location the conversation is the cost structure, and every minute you shave is margin.

## Germany's wage floor rises 13.9% by January 2027, and that is a German fact, not a European one

Germany's statutory minimum wage goes from €12.82 in 2025 to €13.90 on 1 January 2026 and €14.60 on 1 January 2027. That's 13.9% across two steps, decided by the Mindestlohnkommission on 27 June 2025 and described by the BMAS - the Bundesministerium für Arbeit und Soziales - as the largest social-partner-agreed increase since the minimum wage was introduced.

I'm not carrying a German hourly labour cost figure here, so the bridge from wage floor to per-contact number has to be built by hand and labelled at every step. The following is my arithmetic, not Eurostat's:

```
€14.60/hr gross from 1 January 2027
÷ (1 − 0.256), applying the Eurostat euro-area
  non-wage share to the statutory minimum   = €19.62/hr fully loaded
× 0.1333 ÷ 0.70                             = €3.74 per contact
```

Eurostat does not publish that €19.62. I derived it, using a euro-area average non-wage share that is not a German employer contribution rate - an order of magnitude, not a payroll figure and not the German market rate for a support agent. It only bites where you're actually paying at or near minimum. Above the floor it is direction of travel, nothing more.

Now the part that gets misused. This does not generalise. In Q1 2026, Eurostat's 16 June 2026 release put hourly labour cost growth at +3.2% in the euro area, +3.6% in the EU and +3.1% in euro-area services. On the wage component, the country range ran from Hungary at +16.4% and Bulgaria at +13.2% down to France at +1.8% and Malta at +1.3%.

There is no single "European wage inflation" number. Anyone who hands you one is selling something. Model each location separately or don't model at all.

## The occupancy you assumed is a hiring assumption

The model assumes the headcount exists at the price. In some markets it doesn't, and on a live channel that shortfall never becomes a backlog you clear on Saturday. It rings out.

Eurostat's 16 June 2026 release puts the Q1 2026 euro-area job vacancy rate in administrative and support service activities - the NACE category that contains call centres, though it is dominated by temporary employment agencies rather than contact centres - at 3.2%, tied with accommodation and food service as the highest of any sector. Euro-area overall was 2.3%, the EU 2.1%, services 2.4% in the euro area. Another sector aggregate, not a read on your hiring market.

Build in a vacancy allowance or your effective occupancy drops and your real per-contact cost rises above the number you just computed. And treat "hire two more" as a plan with a probability attached, not a budget line - especially in the peak, which for HVAC, spare parts and building materials is the same short window every year.

Language coverage and where to recruit native speakers is [its own post](/blog/multilingual-phone-support-eu-expansion).

## The break-even: when does automating a conversation actually pay?

```
contacts/month to break even
  = monthly automation cost
  ÷ (per-contact cost × containment rate)
```

Containment rate is the share of conversations the automation finishes without a human touching them. Not the share it answers. The share it finishes. The difference is property three: anything it doesn't finish gets re-explained to a person from the beginning.

Resolve it. €1,000/month as the automation cost - a round placeholder, put your actual quote in - and 60% containment. Volumes rounded up to whole contacts:

* **Netherlands, at €9.13 per contact:** €1,000 ÷ (€9.13 × 0.60) = €1,000 ÷ €5.478 = **183 contacts/month** to break even.
* **Bulgaria, at €2.29 per contact:** €1,000 ÷ (€2.29 × 0.60) = €1,000 ÷ €1.374 = **728 contacts/month**.

Same project. Four times the volume requirement.

> **The break-even test for automating customer contacts.** Break-even volume = monthly automation cost ÷ (per-contact labour cost × containment rate). At €9.13 per contact and 60% containment, a €1,000/month tool - a round placeholder; use your own quote - needs 183 contacts a month to pay for itself. Then the second test: the saving is only real if paid hours fall. If hours or headcount don't change, the labour saving is zero.

That second gate is where most automation business cases quietly become fiction. Removing conversations from a team whose payroll doesn't change creates capacity, not savings. Capacity is worth having on a channel where an unanswered call is gone for good - an abandoned call has a cost too, off the same fully-loaded rate. It is still not cost out, and it should never go to a board as one.

## The cases where automating does not pay

I sell voice AI. Here is the arithmetic that says don't buy it.

**1. Low volume.** At the Bulgarian per-contact figure of €2.29, 300 contacts a month is €687 of labour in scope. Automate 60% of it and you're chasing €412 a month. Almost nothing with a setup fee and an integration project clears that, and the internal time to run the project costs more than the saving.

**2. You're already in a low-cost location.** The 4.7x spread in Eurostat's whole-economy figures between Bulgaria at €12.0 and Luxembourg at €56.8 means the identical automation project has a 4.7x different payback depending only on where the desk sits. A tool that pays back in four months against a Dutch cost base may never pay back against a Bulgarian one. Nothing about the tool changed.

**3. Containment lands below break-even.** Escalated contacts are paid for twice - the automation fee plus the full human cost - and it's worse than double, because the customer re-explains everything from the start. Handle time on escalations goes up. Halve containment from 60% to 30% and the break-even volume doubles: the Netherlands goes to 366 contacts a month (365.1 before rounding up) and Bulgaria to 1,456. Model your containment pessimistically and then halve it.

**4. The headcount doesn't come out.** Three people who also process returns, chase suppliers and handle the odd complaint. Remove 30% of their calls and payroll falls by exactly zero. This is the most common shape of business in the €5-100M band and the most common place automation ROI gets overstated.

**5. High-consideration categories where the cost driver is being right, not being fast.** Fitment, spare-part identification, cross-compatibility, whether that compressor fits that unit. Handle time is not the expensive part of those calls. The wrong answer is - it comes back as a return, a re-ship and a lost customer. Optimising the cheap variable while risking the expensive one is a bad trade.

**6. Some conversations shouldn't be automated, they should be eliminated.** If people are calling because the site says something the ERP doesn't, fixing the data is cheaper than automating the conversation about the bad data.

**7. Conversion sensitivity on a sales line.** If automation touches a line that closes revenue, a labour saving of a few euros per contact can be swamped by a conversion movement of a few points. Don't net it out to zero by ignoring it.

Sabato sells into exactly the arithmetic above, and on cases 1, 2 and 4 it usually says no. That's why the arithmetic is in the post rather than in a footnote.

:::action
What to do this week
Rebuild cost per contact bottom-up, per location. Pull handle time, after-call work and occupancy from your own telephony data - three separate numbers, not one blended figure - take the fully-loaded hourly cost for each location, run the lines above. An afternoon.
Time one escalation properly. Sit with a transfer from the moment the customer starts over, and log the recap separately from the resolution. That single number sets your containment threshold, and almost nobody has it.
Ask your BPO for their 2027 rate card now, not at renewal. If any volume sits in Germany at or near the wage floor, the 1 January 2027 step is already decided and they're already pricing it.
Run the break-even in both directions. Compute the volume at which automation pays and the volume at which it doesn't, and be willing to write down the answer where it loses.
:::

If your current number came from a vendor page you'll find it's low, and the gap is mostly the employer load and the occupancy divisor. Same discipline as instrumenting your own [per-return cost](/blog/reduce-bracketing-returns) before buying returns software: don't buy against a number you can't reproduce.

Every multiplier here - the divisor, the wrap-up minutes, the double charge on escalation - exists because the contact is a live conversation between two people. None of them apply where the customer types the record and the queue waits patiently. So a per-contact figure borrowed from anywhere else isn't a benchmark you're missing. It's a different cost shape wearing the same units.

All labour cost figures are Eurostat whole-economy averages - enterprises with ten or more employees, NACE B-N and P-S - from the 2025 reference year published 31 March 2026 and Q1 2026 published 16 June 2026. Eurostat publishes no contact-centre-specific series. The non-wage uplift and the German minimum wage bridge are the author's arithmetic on Eurostat inputs. This is a cost model, not a benchmark.

## FAQ

**Why does a phone contact cost more than a contact on a written channel?** Three multipliers that only exist on a live channel. You pay for idle time between calls, because calls arrive when they arrive and a person cannot be half-staffed - that is the occupancy divisor. You pay after-call work, because the conversation carried information that nothing captured while it happened. And you pay escalated conversations twice, because the customer re-explains from the beginning to the second person.

**What is occupancy and why does it belong in a cost-per-contact model?** Occupancy is the share of paid hours actually spent on contacts. It belongs in the model because calls have to be answered in real time, so you buy whole hours of a person's time to cover contacts that fill only part of them. At 70% occupancy you pay for ten hours to get seven hours of contacts, which raises the per-contact cost by about 43%. Measure it from your telephony platform rather than assuming it.

**How much does a customer service contact cost in Europe?** There is no single figure. Eurostat's whole-economy hourly labour cost for 2025 ranged from €12.0 in Bulgaria to €56.8 in Luxembourg, an EU average of €34.9 and euro area €38.2. Eurostat publishes no contact-centre-specific series, so cost per contact must be built bottom-up per location from your own handle time, after-call work and occupancy.

**What is a fully-loaded hourly cost, and how do I calculate it?** Fully-loaded cost is gross wages plus employer non-wage costs such as social contributions. Eurostat puts non-wage costs at 24.8% of total labour cost in the EU and 25.6% in the euro area. Because that is a share of the total, not a markup, converting a gross wage gives roughly gross ÷ 0.752 - about a 33% uplift, not 25%.

**Is the German minimum wage increase happening across Europe?** No. Germany's statutory minimum wage rises from €12.82 in 2025 to €13.90 in January 2026 and €14.60 in January 2027, 13.9% across two steps, decided by the Mindestlohnkommission in June 2025. That is Germany-specific. Q1 2026 hourly wage cost growth ranged from Hungary at +16.4% to Malta at +1.3%. There is no single European rate.

**When does automating customer conversations not pay off?** When volume is too low to amortise setup, when your cost base is already low, when containment falls below break-even so escalated conversations are paid for twice, or when the headcount does not actually come out. If a small team also handles returns, removing 30% of calls removes no payroll at all.

**Why can't I use a US cost-per-contact benchmark?** Because it is denominated in a single currency, resolved to no country, and typically excludes employer non-wage costs. It also cannot know your arrival curve, your after-call-work discipline or your escalation rate, which are the three terms doing the work. European hourly labour cost varies 4.7x between member states, and hourly wage costs grew at rates ranging from +1.3% in Malta to +16.4% in Hungary year on year in Q1 2026.

## Sources

* Eurostat, *Hourly labour costs ranged from €12.0 to €56.8 in 2025*, published 31 March 2026 - [ec.europa.eu](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260331-2)
* Eurostat, *Hourly labour costs* (Statistics Explained) - [ec.europa.eu](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Hourly_labour_costs)
* Eurostat, *Labour cost index, Q1 2026*, published 16 June 2026 - [ec.europa.eu](https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/3-16062026-bp)
* Eurostat, *Job vacancy rate, Q1 2026*, published 16 June 2026 - [ec.europa.eu](https://ec.europa.eu/eurostat/web/products-euro-indicators/w/3-16062026-ap)
* BMAS, *Mindestlohn steigt zum 1. Januar 2026* - [bmas.de](https://www.bmas.de/DE/Service/Presse/Pressemitteilungen/2025/mindestlohn-steigt-zum-ersten-januar-2026.html)
* Mindestlohnkommission, *Evolution of the minimum wage* - [mindestlohn-kommission.de](https://www.mindestlohn-kommission.de/en/Information-on-the-minimum-wage/Evolution-of-the-minimum-wage)
