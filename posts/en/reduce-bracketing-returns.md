---
title: "How to Reduce Bracketing Returns Without Losing the Sale"
slug: reduce-bracketing-returns
description: "How to reduce bracketing returns without losing the sale: the SQL to measure it, the true cost per order, and the break-even most brands never calculate."
category: Returns
date: 2026-07-30
cover_style: lime
---

A customer wants the 12. She isn't sure your 12 is really a 12, so she buys the 12 and the 14, keeps one, ships the other back. ZigZag and Retail Economics' *Annual Returns Benchmark 2024* has 27.4% of UK clothing and footwear shoppers doing this on purpose. Every one of them paid for a second unit because your product page would not answer a question.

## Why is bracketing an information problem and not a logistics one?

Bracketing is when a shopper deliberately orders the same item in two or more sizes, intending to return all but one. It lands in your reverse-logistics report, so it gets treated as a reverse-logistics problem. It isn't.

Sahoo, Dellarocas and Srinivasan documented the mechanism in *Information Systems Research* in 2018, across two years of transaction-level data from a North American specialty retailer. Where reviews were thin, shoppers bought substitutes alongside the primary purchase to hedge, and returns rose with them. More reviews meant fewer returns. Reviews other shoppers voted helpful meant fewer still.

:::quote
The second size is not a behaviour you can police. It is a purchase the customer makes instead of an answer you didn't give her.
:::

Withhold the answer and she buys the hedge. That puts the problem upstream, out of the warehouse and into merchandising.

## Step 1: Count it. The three-level detection rule for your own data

Nobody can tell you your bracket rate. Compute it.

**Level 1 - same order.** One order contains two or more variants of the same parent product differing only in size.

```
WITH size_groups AS (
  SELECT
    ol.order_id,
    o.customer_id,
    v.product_id,
    v.option_colour,
    COUNT(DISTINCT v.option_size)   AS distinct_sizes,
    SUM(ol.qty)                     AS units,
    SUM(ol.qty * ol.unit_price)     AS gross_value
  FROM order_lines ol
  JOIN variants v ON v.variant_id = ol.variant_id
  JOIN orders   o ON o.order_id   = ol.order_id
  GROUP BY 1,2,3,4
)
SELECT * FROM size_groups
WHERE distinct_sizes >= 2;         -- the bracket flag
```

Group by product_id **and colour**. Two colours of the same style is a *style* hedge, a different question with a different answer. Merge them and you will misdiagnose the fix.

**Level 2 - the short window.** Some customers order, get nervous, and buy the next size up ten minutes later. Self-join the same customer, same product_id and colour, different size, within a window:

```
SELECT a.customer_id, a.product_id, a.option_colour,
       a.order_id AS order_a, b.order_id AS order_b,
       ABS(EXTRACT(EPOCH FROM (b.created_at - a.created_at)))/3600 AS hours_apart
FROM order_variant_flat a
JOIN order_variant_flat b
  ON  a.customer_id   = b.customer_id
  AND a.product_id    = b.product_id
  AND a.option_colour = b.option_colour
  AND a.option_size  <> b.option_size
  AND a.order_id      < b.order_id
WHERE ABS(EXTRACT(EPOCH FROM (b.created_at - a.created_at))) <= 48*3600;
```

Do not inherit 48 hours from me. Plot hours-between-same-product-different-size orders. You'll see a spike in the first few hours (the hedge) and a long flat tail (genuine repurchase after trying). Cut at the elbow, document the cut, never change it mid-experiment.

**Level 3 - confirmed bracket.** This is the only level with P&L in it: bracket flag AND partial return of the size group.

```
bracket_confirmed = (distinct_sizes >= 2)
                AND (returned_units_in_group >= 1)
                AND (returned_units_in_group <  units_in_group)
```

| Outcome | Rule | What it means | What to do |
| --- | --- | --- | --- |
| Confirmed bracket | partial return of the size group | The hedge worked. You paid for it. | Target with a pre-purchase answer |
| Full-group return | every unit returned | The product failed, not the size | Route to merchandising / QA |
| Full-group keep | nothing returned | Gift, household, genuine multi-buy | Exclude - this is your false-positive rate |

:::takeaway How to measure bracketing
Flag orders containing two or more variants of the same parent product and colour that differ only in size (Level 1).
Add same-customer, same-product orders placed inside a short window (Level 2).
Confirm the bracket where part, but not all, of that size group comes back (Level 3).
Group by parent product plus colour, never product alone. There is no published benchmark; you are your own baseline.
:::

Two things will bite you before the analysis does.

**The week-one blocker is data, not SQL.** If option_size isn't a structured variant option, common on migrated Shopify and Magento catalogues, you have a cleaning job before you have a query. Then set your exclusions: gifts (size gap over two steps, or crossing department), promo-bundle SKUs, guest-checkout identity gaps (report your stitch rate honestly, or your Level 2 number is a floor), exchanges booked as returns, marketplace channel, and non-ordinal size systems that need a size_rank lookup first.

**There is no public benchmark for bracketed orders as a share of orders. None.** Every figure in circulation is share-of-*returns* and vendor-published. Compute monthly for 24 months and segment by style, category, new versus returning, channel and discount depth. The signal isn't the average. It's the variance between styles. Any style running above 1.5× the category median on 200+ orders in 90 days has an unanswered question sitting on its PDP. That list is your fix queue.

## Step 2: Price it. What one bracketed order actually costs

Most operators count two lines: return carriage and a bit of warehouse labour. Here is the full model on a mid-market UK fashion rate card. Every [ASSUMPTION] is a placeholder you replace with your own numbers.

| Line | Value | Source |
| --- | --- | --- |
| ASP per unit | £40.00 | [ASSUMPTION] |
| Gross margin 60% → gross profit | £24.00 | [ASSUMPTION] |
| Incremental outbound shipping (second size, same parcel) | £0.50 | [ASSUMPTION] |
| Incremental pick & pack | £0.35 | [ASSUMPTION] |
| Inbound return carriage | £3.50 | [ASSUMPTION] |
| Goods-in, inspect, steam, re-tag, re-bag, restock | £2.50 | [ASSUMPTION], anchored to bevh fashion processing |
| Payment fee not returned on refund | £0.80 | Stripe published UK rate + Stripe refund policy |
| Depreciation / markdown, 13.1% of goods value | £5.24 | bevh-Retourenkompendium, citing University of Bamberg |
| CS contact: 20% of returns × £4.00 handle cost | £0.80 | [ASSUMPTION] |

Two of those lines are silent, and almost nobody books them. Stripe's support documentation states that processing fees from the original transaction aren't returned when you refund; at the published UK standard card rate of 1.5% + 20p, a refunded £40 item permanently costs you £0.80, buried in payment fees where nobody attributes it to returns. Depreciation is the other, and it's the biggest line here.

:::chart bar
Where the £13.69 cost of one returned unit goes
Depreciation / markdown | £5.24 | 38% - the line nobody books
Inbound return carriage | £3.50 | the only line the industry optimises
Goods-in, refurb, restock | £2.50
Payment fee not refunded | £0.80
CS contact (allocated) | £0.80
Incremental outbound | £0.50
Incremental pick & pack | £0.35
Source: worked model above - bevh-Retourenkompendium; Stripe UK pricing and refund policy
:::

Now the bracketed order. Two units at £40. Keeps one, returns one.

:::compare One order, two outcomes
Bracketed order | Right size, first time
Units bought | 2 | 1
Gross profit on the kept unit | £24.00 | £24.00
Cost of the returned unit | −£13.69 | £0.00
Net contribution | £10.31 | £24.00
:::

The fit question you didn't answer costs 57% of the gross profit on that order.

£13.69 sits inside the £10 - £20 per-return range ZigZag and Retail Economics published for UK non-food in 2024, though their range also carries lost-sale opportunity cost and mine doesn't. Treat it as a sanity check on the order of magnitude, not a match.

Look at which line dominates. Return carriage, the thing the entire industry optimises, is £3.50 of £13.69 - 26%. Depreciation is 38%. Renegotiate reverse logistics down to literally zero and you still carry £10.19 of cost on every bracketed order.

One warning, because it is the most common error in returns content: £10 - £20 (ZigZag 2024, includes lost-sale opportunity cost) and €2.85 (Bamberg/EUROM, 2020-21, transport and handling only) are not two estimates of the same thing. They are two different cost boundaries. Pick one, state it, stick to it.

## Step 3: Do the break-even before you deter anyone

You can always drive return rate down by making it harder to buy. The question is how much deterrence you can afford.

Let G = gross profit per kept unit, C = net cost of a returned unit, s = the share of would-be bracketers who still buy after your intervention, k = their keep rate afterwards.

```
Break-even survival rate:  s* = (G − C) / ( k·G − (1−k)·C )
```

**Case A - perfect information, k = 1.**

```
s* = (24.00 − 13.69) / 24.00 = 10.31 / 24.00 = 43%
```

An intervention that eliminates bracketing pays only if at least 43 of every 100 would-be bracketers still buy. If more than 57 walk, you made yourself poorer while the returns dashboard turned green.

**Case B - a £3.95 returns fee, the ASOS rate.** The fee recovers £3.95, so net C = £9.74. Assume k = 0.9:

```
s* = 10.31 / (0.9 × 24.00 − 0.1 × 9.74) = 10.31 / 20.626 = 50%
```

:::keystat
43%
of would-be bracketers must still buy for a perfect-information fix to break even
Source: worked example - £40 ASP, 60% margin, £13.69 cost per return

50%
must still buy if you charge a £3.95 returns fee instead
Source: same model, fee recovered against the return cost
:::

A returns fee needs half your would-be bracketers to keep buying. The one deterrence survey available (Trustpilot/OnePoll, 2023, US, stated intent rather than observed behaviour) has 49% of shoppers claiming they won't buy from retailers who charge for returns. You are being asked to bet the P&L on a coin flip.

**Case C - answer the question instead of deterring it.** Take 100 bracketers. Say 70 now buy a single size (keeping 90% of them), 25 still bracket, 5 buy nothing.

```
70 buy →  63 kept × £24.00     = £1,512.00
       →   7 returned × £13.69 =  − £95.83
25 still bracket × £10.31      =  + £257.75
 5 buy nothing                 =       £0.00
                        Total  =  £1,673.92

Baseline: 100 × £10.31         =  £1,031.00
Uplift                         =  + £642.92  (+62.4%)
```

Answering the question is worth +62% contribution on that cohort. Suppressing the behaviour is worth, at best, break-even.

I charge the full £13.69 to those 7 single-size returns even though £0.85 of it - the outbound shipping and pick-and-pack on a second unit - was never incurred. That understates the uplift. I'd rather round against my own argument.

And note the counterweight: Balaram, Perdikaki and Galbreth showed in *Naval Research Logistics* in 2022 that bracketing cuts both ways, raising reverse-logistics cost while reducing fit hesitation and driving volume. Which is why you compute your own threshold instead of borrowing mine.

## Step 4: Sort your reason codes into what you can answer and what you can't

Before you spend a penny on tooling, re-map your existing reason codes into these six buckets.

| Bucket | Example codes | Answerable pre-purchase? | Owner |
| --- | --- | --- | --- |
| **A. Dimensional fit** | too small, sleeves short, waist gapes | Fully, given garment measurements | Product data |
| **B. Fit character / drape** | "boxy", "runs small", "not true to size" | Yes - but only by someone who has worn it | UGC, clienteling, conversation |
| **C. Spec / material** | weight, opacity, stretch, warmth | Yes. Pure information gap | PDP copy and Q&A |
| **D. Expectation mismatch** | colour differs from photo, looked cheaper | Partly, and more media can make it worse | Merchandising |
| **E. Taste / occasion** | "didn't like it", changed my mind | No. Stop trying | Nobody |
| **F. Product or ops failure** | faulty, wrong item sent | No. Different problem entirely | QA / warehouse |

On bucket D, resist the reflex to add content. De, Hu and Rahman's 2013 econometric study of a women's clothing retailer found that zoom usage reduced returns while *alternative photos increased them*. More media is not monotonically better.

Two rules.

**Only A, B and C are in scope for a pre-purchase intervention.** If your taxonomy has a single bucket called "size/fit", you cannot separate A from B, and a size chart structurally cannot fix B. If free-text "other" is more than 15% of volume, that's job one; B and C are usually hiding in there.

**Almost no returns portal offers a code that says "I ordered two sizes on purpose."** So bracketed returns get logged as "too small", pollute your fit-failure signal, and aim your PDP fixes at the wrong styles. Add the code. ZigZag's 27.4% exists because somebody asked the question directly. Your portal never does.

## Step 5: Rank the interventions by evidence and speed to ship

| Intervention | Cost | Time to ship | Bucket | Evidence (grade) |
| --- | --- | --- | --- | --- |
| Model measurements + "model wears size X" | ~£0 | days | A | Baymard #10 (independent UX) |
| Garment measurements + size guide next to the selector | labour | 2-6 wks | A | Baymard #3 - #7; NN/g 2022 (independent UX) |
| Aggregate fit subscore + structured "runs small" reviews | low SaaS | 2-6 wks | **B** | Sahoo et al. 2018 (**peer-reviewed - strongest**) |
| Bracketing checkout nudge | one sprint | 1-3 wks | A/B | SAIZ, True Fit (vendor only, unquantified) |
| Fit finder / size recommender | SaaS | 4-12 wks | A | Zalando −10%; Fit Analytics A/B (first-party + vendor) |
| Lengthen your returns window | £0 + WC drag | days | endowment | Janakiraman et al. 2016 (peer-reviewed meta) |
| Returns fee | £0 | days | suppression | Contradictory; 50% break-even (weak) |
| Virtual try-on | high SaaS | 8-16 wks | A/D | None credible (poor) |
| Shift payment mix away from BNPL | revenue risk | quarters | structural | 30.15% returns prepaid vs 55.65% invoice - Bamberg (correlational) |
| [Pre-purchase conversation (Sabato)](/use-cases/pre-sales-consultation) | SaaS | weeks | A/B/C | Baymard #9; EHI 48% (**hypothesis - no third-party evidence**) |

Time-to-ship ranges are my estimate from implementation experience, not vendor-published numbers.

Rows 1 and 2 are free or nearly free, and everything downstream depends on them: fit tools, chatbots and agents are all garbage-in, garbage-out on garment measurements. Baymard's 2022 testing found 83% of desktop apparel sites give shoppers insufficient sizing information, so assume you are one of them until you've checked. Row 3 is the best-evidenced item here, and it carries a warning from the same paper. Showing average ratings *higher* than the true rating increased returns. Suppressing negative fit reviews is actively harmful.

The checkout nudge is the Level 1 rule from Step 1, run against the cart object: roughly twenty lines of JS plus a variant-to-parent lookup, shippable in a sprint. **Design rule: the nudge must answer the question, never block or shame.** Removing the second size removes the hedge. Answering removes the *need* for the hedge. Vendors ship this; none of them publish numbers.

Be honest about the evidence on fit finders. The credible figure is Zalando's own July 2023 claim of a 10% reduction in size-related returns where its size advice is available. The credible *methodology* is Fit Analytics' A/B with THE ICONIC: 250,000 shoppers, three months, measured as revenue after returns. The "+150% conversion" and "−50% bracketing" numbers circulating elsewhere are unaudited vendor marketing.

Two rows deserve a second look. Lengthening your returns window is free and counter-intuitive: Janakiraman, Syrdal and Freling's 2016 meta-analysis of 21 papers found *time* leniency reduces returns via the endowment effect, while scope leniency increases them. Operators under returns pressure shorten the window. That's backwards.

And if you are going to charge, steal ASOS's mechanism rather than the headline. ASOS computes a personal return rate per customer on a rolling 12 months and charges £3.95 above 70% with three or more orders - **unless you keep more than £40 of the order.** That threshold means ASOS isn't punishing returns, it's punishing low basket retention. Bracketing a £60 dress and keeping it is free. Then go back and run your own s*.

Virtual try-on is the biggest gap between hype and evidence on the list, and not a first move. The only sourced datapoint is negative: in EHI's German retailer survey (~2019), virtual fitting tools were rated effective by 34%, below personal consultation at 48%.

On the payment row: before you touch your PDP, segment your bracket rate by payment method. If BNPL is 40% of your fashion orders, that's a bigger structural driver than your size chart. German data, correlational, and the self-selection is obvious - people who plan to return choose invoice. Don't read it as causal.

**On the Sabato row.** Our thesis: a pre-purchase conversation removes the need for the hedge. Vanity sizing gives a deterministic algorithm a ceiling. The residual question is a judgement call: does this brand's 12 run like your usual 12? Nobody has published evidence that a conversation reduces bracketing, us included. The honest supports are Baymard listing a customer-service link inside the size guide as a *sizing* best practice, and retailers ranking personal consultation above virtual try-on. Treat it as a hypothesis. Falsify it with the design below: power on confirmed-bracket rate, guardrail on new-customer order rate.

## Step 6: Test it properly, or you'll ship the wrong thing

**Never ship on return rate alone.** You can drive return rate to zero by shipping nothing. Return rate cannot tell a demand-suppression path from a demand-neutral one, which is the entire question.

**Pick the OEC.** Kohavi, Tang and Xu's *Trustworthy Online Controlled Experiments* (2020): one Overall Evaluation Criterion, plus guardrails that must not degrade. Use net contribution per session - (kept units × gross profit − returned units × C) ÷ sessions. Primary: kept units per session. Diagnostic: confirmed-bracket rate. Guardrails: order rate, **new-customer order rate** (new customers bracket most and are the ones a fee scares off), AOV, CS contact rate. Units per order may legitimately fall. That's the point.

**Randomise by user, sticky, never by session.** The same shopper must see one experience across browse, cart and return, or your bracket detection straddles both arms. Never test at product level either; shoppers cross styles in a single session and contaminate both.

**The power problem, stated honestly.** Detecting a 1pp drop in confirmed-bracket rate from an assumed 8% base - plug in your own - needs about 11,800 orders per arm, reachable in a quarter for most mid-market brands. Detecting a 3% lift in revenue per session, on a mean of £2.00 with a standard deviation of £12.00, needs 640,000 sessions per arm. You cannot power the money metric. So run a two-tier readout: power the test on the diagnostic, treat revenue as a directional guardrail with a wide interval, and never let an underpowered "revenue up 4%" become the business case.

**The lag trap.** You cannot read returns metrics until the window has closed. Freeze the exposure cohort, then wait return_window + 21 days. Report interim results on order-side metrics only, and label them interim.

**Pre-register the confounds.** Seasonality (never straddle a sale boundary), promo depth, new-versus-returning mix, catalogue turnover (fashion assortment turns in six to eight weeks), novelty decay (discard week one), and multiple comparisons - five metrics across eight segments is forty tests and you will find "significance."

## Does this apply outside fashion?

The mechanism generalises: when a decisive pre-purchase question goes unanswered, the shopper buys a hedge or doesn't buy at all. In fashion the hedge is a second size. At higher ASPs the hedge becomes too expensive to buy, so the failure mode shifts from *return* to *non-purchase* - invisible in returns data, visible only in PDP exit rate and pre-purchase contact volume.

| Category | The unanswered question | The hedge | How to detect it |
| --- | --- | --- | --- |
| Furniture | Will it fit through the door, up the stairs, in the alcove? | Swatch first, two finishes, or abandon | Multi-variant same-parent in one order |
| Appliances | Aperture, door reversal, plumbing fit | Rarely brackets - calls or abandons | Pre-purchase contact rate per SKU |
| Bikes | Frame size, and I'm between two | Two frame sizes where returns are free | Same model, two sizes, ≤7 days |
| Auto parts | Does it fit *my* vehicle? | Two variants, or buys from whoever guarantees fit | Two variants of one part family, one order |
| B2B spec-driven | Tolerance, certification, interoperability | Samples of two or three specs | Sample orders, multi-spec carts |

The proof point is in parts. In February 2023 eBay Motors launched Guaranteed Fit: enter your vehicle, get a green "Fits" checkmark, and if the part doesn't fit, eBay covers return shipping and refunds you. eBay then bought the myFitment group to keep the compatibility data right. A business eBay describes as $10bn+ in annual GMV underwrote the fitment answer with its own balance sheet. Nobody does that for a logistics problem. They do it for a conversion problem.

No credible bracket-rate benchmark exists in any of these categories. The argument here is structural, not statistical.

:::action Your next 30 days
Days 1-3: check whether option_size is a structured variant option. If it isn't, that's your whole first week.
Days 3-7: run the Level 1 query across 24 months. Segment by style. Build the >1.5×-median fix queue.
Days 3-7, in parallel, zero cost: pull the last 500 pre-purchase CS contacts, tag each with the question it asked, sort by frequency. Every top-10 question answered nowhere on the PDP is a hedge or an abandonment you're paying for.
Week 2: rebuild the cost model on your own rate card. Compute your s*.
Week 2: re-map reason codes to A - F. Add the "ordered two sizes on purpose" code.
Weeks 3-4: ship the free stuff - model measurements, size worn, size guide beside the selector, CS link inside the size guide.
Week 4: pre-register one test on the top style in the queue. Pick the OEC before you build anything.
:::

Bracketing isn't a returns problem you process. It's a question you didn't answer, and you can find out exactly which question by Friday.

## FAQ

**What is bracketing in ecommerce?** Bracketing is when a shopper deliberately orders the same item in two or more sizes or variants, intending to keep one and return the rest. They do it as a hedge against a question the product page didn't answer. ZigZag and Retail Economics' *Annual Returns Benchmark 2024* found 27.4% of UK clothing and footwear shoppers admit to it.

**How do you calculate your bracketing rate?** Three levels. Level 1: orders containing two or more variants of the same parent product and colour differing only in size - group by parent product *and* colour, never product alone. Level 2: the same pair across two orders inside a short window. Level 3, the only level with P&L: bracket flag plus a partial return of that size group.

**Does charging for returns stop bracketing?** It reduces the behaviour. Whether it makes you money is a different question. On a £40 item at 60% margin, a £3.95 fee needs roughly half your would-be bracketers to keep buying just to break even, and the one available survey has 49% saying fees stop them shopping with a retailer. Do the arithmetic first.

**What is the average cost of a returned item?** On the worked model here (carriage, pick and pack, goods-in, refurb, unrecovered payment fees, depreciation and a CS contact) one returned unit costs £13.69. That sits inside ZigZag's £10 - £20 UK range, which uses an even broader boundary - it also includes lost-sale opportunity cost. Published per-return costs use incompatible boundaries, so never compare them without checking what's inside.

**Should you shorten your returns window to reduce returns?** No. Janakiraman, Syrdal and Freling's 2016 meta-analysis of 21 papers found that *time* leniency reduces return rates, attributed to the endowment effect: the longer someone keeps an item, the more attached they get. Scope leniency increases returns; time leniency doesn't. Lengthening the window is the free, evidence-backed lever almost nobody pulls.

## Sources

- Sahoo, Dellarocas & Srinivasan (2018), *The Impact of Online Product Reviews on Product Returns*, Information Systems Research - [ideas.repec.org](https://ideas.repec.org/a/inm/orisre/v29y2018i3p723-738.html)
- De, Hu & Rahman (2013), *Product-Oriented Web Technologies and Product Returns*, Information Systems Research - [econpapers.repec.org](https://econpapers.repec.org/article/inmorisre/v_3a24_3ay_3a2013_3ai_3a4_3ap_3a998-1010.htm)
- Balaram, Perdikaki & Galbreth (2022), *Bracketing of purchases to manage size uncertainty*, Naval Research Logistics - [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3823892)
- Janakiraman, Syrdal & Freling (2016), *The Effect of Return Policy Leniency on Consumer Purchase and Return Decisions*, Journal of Retailing - [UT Dallas](https://news.utdallas.edu/business-management/researchers-examine-effect-of-return-policies-on-c)
- ZigZag / Retail Economics, *Annual Returns Benchmark 2024* - [PDF](https://info.zigzag.global/hubfs/Annual-Returns-Benchmark-Report-2024-ZigZag.pdf)
- bevh-Retourenkompendium, 2. Auflage (citing University of Bamberg returns research and EHI Retail Institute retailer survey, ~2019) - [PDF](https://bevh.org/fileadmin/user_upload/Studien/Retourenkompendium/Final_2._Auflage_Retourenkompendium_41_.pdf)
- University of Bamberg, EUROM project (n=411 European retailers, 2020-21) - [retourenforschung.de](https://www.retourenforschung.de/forschungsprojekt-eurom-2122.html)
- Baymard Institute (2022), *Apparel: 10 Best Practices on Sizing* - [baymard.com](https://baymard.com/blog/apparel-size-information)
- Baymard Institute (2024), *Always Provide an Aggregate Fit Subscore* - [baymard.com](https://baymard.com/blog/apparel-provide-aggregate-fit-subscore-in-reviews)
- Nielsen Norman Group (2022), *Size Guides and Product Measurements for International Shoppers* - [nngroup.com](https://www.nngroup.com/articles/sizes-measurements-ecommerce/)
- Zalando (2023), *Size recommendations based on customers' own body measurements* - [corporate.zalando.com](https://corporate.zalando.com/en/technology/zalando-launches-size-recommendations-based-customers-own-body-measurements)
- Fit Analytics, THE ICONIC case study (vendor) - [fitanalytics.com](https://fitanalytics.com/case-studies/the-iconic)
- True Fit, ASICS case study (vendor) - [truefit.com](https://info.truefit.com/asics-case-study)
- SAIZ, *Automated checkout nudges to stop bracketing* (vendor) - [saiz.io](https://www.saiz.io/checkout-nudges)
- ASOS, *What is your Fair Use Policy* - [asos.com](https://www.asos.com/customer-care/returns-refunds/what-is-your-fair-use-policy)
- Trustpilot / OnePoll (2023), US online shopper survey - [trustpilot.com](https://corporate.trustpilot.com/press/news/a-quarter-of-americans-admit-to-buying-more-to-save)
- Stripe, *Understanding fees for refunded payments* - [support.stripe.com](https://support.stripe.com/questions/understanding-fees-for-refunded-payments)
- Stripe UK pricing - [stripe.com](https://stripe.com/gb/pricing)
- eBay Motors (2023), *eBay Guaranteed Fit launch* - [stocktitan.net](https://www.stocktitan.net/news/EBAY/e-bay-motors-launches-new-purchase-protections-for-auto-parts-y44cw5yq6mdz.html)
- eBay acquires the myFitment group - [stocktitan.net](https://www.stocktitan.net/news/EBAY/e-bay-acquires-the-my-fitment-group-of-companies-to-enhance-part-and-fj5wzm5b5dan.html)
- Kohavi, Tang & Xu (2020), *Trustworthy Online Controlled Experiments* - [experimentguide.com](https://experimentguide.com/wp-content/uploads/TrustworthyOnlineControlledExperiments_PracticalGuideToABTesting_Chapter1.pdf)
