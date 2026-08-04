#!/usr/bin/env python3
"""Customer story content.

DRAFT STATUS — read before touching anything here.

Every page built from this file carries `noindex, nofollow` and a DRAFT ribbon,
and nothing links to them from production. That is deliberate: these pages put
numbers and words next to a real, named company and a real, named executive.
Until Daniel has each customer's written sign-off on the exact figures and the
exact quote, the pages stay unindexed and staging-only.

Anything wrapped in [[double brackets]] renders as a loud orange TBC chip. Use it
for every figure and every first-person statement that is not yet approved.

Two rules that matter more than they look:

1. NEVER write a quote for a named person and leave it unmarked. A plausible
   invented quote is far more dangerous than an obvious blank, because it is the
   one thing a reviewer skims past — and the person it is attributed to will not.
2. A number without a definition is not a number. `53.1% autonomy rate` means
   nothing to a buyer until the page says what was counted and over what period.
   Every metric therefore carries a `sub` explaining what it measures.
"""

CUSTOMERS = {
    # ------------------------------------------------------------------ 1
    "clima-convenienza": {
        "name": "ClimaConvenienza",
        "initials": "CC",
        "logo": None,                       # no asset yet -> monogram fallback
        "person": "Alessio Perrucci",
        "person_initials": "AP",
        "role": "CEO",
        "photo": None,                      # no headshot yet -> monogram fallback
        "industry": "Home Improvement",
        "industry_href": "/industries/home-improvement",
        "chip": "Customer story",
        "title": "ClimaConvenienza — Voice AI Case Study | Sabato AI",
        "description": ("How ClimaConvenienza handles pre-sales and order calls on heat pumps, "
                        "boilers and air conditioning with a Sabato voice agent — 53.1% of calls "
                        "resolved without a human."),
        "h1": "ClimaConvenienza resolves half its phone calls without a human.",
        "sub": ("Heat pumps, boilers and air conditioning sold on Shopify. Every one of those is a "
                "sizing question before it is a sale — and every sizing question used to be a person "
                "on the phone."),

        # ---- the situation
        "situation_eyebrow": "The situation",
        "situation_h2": "A catalogue where nobody buys without asking first",
        "situation_body": [
            "Climate equipment does not sell itself off a product page. Before a customer commits to "
            "a heat pump they want to know whether it fits the room, whether it works with the "
            "existing system, what the installation involves, and what happens if it arrives and the "
            "plumber says no. Those questions arrive by phone, in bursts, and they arrive from people "
            "who are ready to spend.",
            "The calls were being answered by the same small team running the shop. Which meant they "
            "were answered well when someone was free, and not at all when nobody was — evenings, "
            "weekends, and the hours around a promotion when volume spikes and the questions are at "
            "their most valuable.",
        ],
        "situation_points": [
            ("The expensive questions come by phone",
             "Sizing, compatibility and installation — the questions that decide a four-figure order — "
             "are the ones customers will not resolve from a spec sheet."),
            ("Volume is spiky, staffing is not",
             "A promotion or a cold snap doubles the calls in a day. Headcount cannot follow that curve, "
             "so the peak is exactly when calls go unanswered."),
            ("A missed call is not a missed ticket",
             "In this category the caller is mid-decision. An unanswered phone is a customer who buys "
             "the equivalent product from whoever picks up."),
        ],

        # ---- what went live
        "stack_h2": "What went live",
        "stack": [
            ("Pre-sales consultation",
             "The agent answers product questions against the live catalogue — models, specs, stock — "
             "and points the caller to the right configuration for their situation."),
            ("Where is my order",
             "Order status pulled in real time and confirmed back to the customer, with the details "
             "sent as a text so nothing depends on the caller remembering it."),
            ("Escalation to the team",
             "Anything outside the agent's rules — a disputed order, an unusual install, a case that "
             "needs judgement — goes to a person with the full call context attached."),
        ],
        "stack_note": ("Connected to Shopify, so the agent reads the same catalogue, pricing and order "
                       "data the storefront does. Live in two weeks."),

        # ---- transcript: illustrative, and the page says so
        "call_h2": "What a ClimaConvenienza call sounds like",
        "call_caption": "Example call",
        "call": [
            ("caller", "Hi, I'm looking at a heat pump for a room of about 30 square metres. "
                       "Do you know if the 9000 BTU is enough?"),
            ("agent", "For 30 square metres with standard insulation, 9000 BTU is usually under-sized — "
                      "12000 is the safer match. Is the room on a top floor, or does it get a lot of "
                      "direct sun?"),
            ("caller", "Top floor, and yes, sun most of the afternoon."),
            ("agent", "Then I'd go 12000. The model you're looking at comes in that size and it's in "
                      "stock. Do you want me to text you the link to the exact configuration?"),
            ("caller", "Yes please. And how long is delivery?"),
            ("agent", "Three to five working days to your area. One thing I can't confirm is whether "
                      "your existing wiring supports it — that's a question for the installer, and I "
                      "can have someone from the team call you about it tomorrow if you'd like."),
            ("caller", "That would help, thanks."),
        ],
        "call_note": ("Product details here are illustrative. On a live call the agent reads "
                      "ClimaConvenienza's real catalogue and stock, and anything outside its rules "
                      "goes to the team."),

        # ---- results
        "results_eyebrow": "Results",
        "results_h2": "What changed",
        "results": [
            ("53.1%", "Autonomy rate",
             "Share of calls the agent resolved end to end, with no human involved."),
            ("[[+00%]]", "[[Metric two]]",
             "[[Second approved figure — e.g. calls answered outside business hours, "
             "or average time to answer.]]"),
            ("[[+00%]]", "[[Metric three]]",
             "[[Third approved figure — e.g. conversion on calls handled, or orders "
             "attributed to phone.]]"),
        ],
        "results_foot": ("[[Measurement window and method to be confirmed with ClimaConvenienza "
                         "before publication — over what period, against what baseline.]]"),

        # ---- quote: NOT invented. Placeholder until approved in writing.
        "quote": "[[Approved quote from Alessio Perrucci to be supplied — one or two sentences, "
                 "in his words, on what changed for the business.]]",

        # ---- honest limits
        "honest_h2": "What it does not do",
        "honest_body": ("Every case study is more believable with this section in it, so here it is. "
                        "The agent is not a replacement for the people who know this category."),
        "honest_points": [
            "It does not give installation advice. Anything that depends on the customer's existing "
            "system, wiring or plumbing goes to a human — as it does in the call above.",
            "It does not approve exceptions. Discounts, out-of-policy returns and disputed orders are "
            "captured with full context and routed, never decided.",
            "It does not pretend to be a person. Callers are told they are speaking to Sabato, and can "
            "ask for the team at any point.",
        ],

        "cta_h2": "Want the same for your catalogue?",
        "cta_sub": ("A pilot runs on your real calls for two weeks and measures what changed against "
                    "your own baseline. No slideware."),
    },

    # ------------------------------------------------------------------ 2
    "creative-cables": {
        "name": "Creative Cables",
        "initials": "CC",
        "logo": None,
        "person": "Marco Logreco",
        "person_initials": "ML",
        "role": "Head of E-Commerce",
        "photo": None,
        "industry": "Furniture & Home",
        "industry_href": "/industries/furniture-home",
        "chip": "Customer story",
        "title": "Creative Cables — Voice AI Case Study | Sabato AI",
        "description": ("How Creative Cables handles configuration and order questions across "
                        "multiple countries with a Sabato voice agent."),
        "h1": "[[Headline outcome for Creative Cables — to be set once the metric is approved.]]",
        "sub": ("Configurable lighting and cabling, sold across several countries and several "
                "languages. A catalogue you assemble rather than pick off a shelf — which means the "
                "phone rings with questions no filter can answer."),

        "situation_eyebrow": "The situation",
        "situation_h2": "A configurable catalogue multiplies the questions",
        "situation_body": [
            "When a product is assembled from components — a cable, a fitting, a shade, a length — the "
            "number of things a customer can be unsure about grows faster than the catalogue does. "
            "Compatibility between parts, what is included, whether a finish matches across two "
            "different items: these are the questions that stop a basket at the last step.",
            "Selling across borders multiplies it again. The same question arrives in several "
            "languages, at hours that do not overlap with one team's working day.",
        ],
        "situation_points": [
            ("Configuration questions block checkout",
             "The customer is not browsing. They have chosen, and they need one thing confirmed before "
             "they pay — which makes the answer worth more than the call costs."),
            ("Several languages, one team",
             "Cross-border demand does not queue politely inside one country's office hours."),
            ("The catalogue changes constantly",
             "Components, finishes and stock move. An answer that was right last month is a returned "
             "order this month."),
        ],

        "stack_h2": "What went live",
        "stack": [
            ("Pre-sales consultation",
             "Component and compatibility questions answered against the live catalogue, in the "
             "caller's language."),
            ("Checkout summary via text",
             "What was discussed — items, specs, a direct link — sent as a message after the call, so "
             "the customer can complete the order without reconstructing it from memory."),
            ("Escalation to the team",
             "Bespoke configurations and anything commercially unusual routed to a person with the "
             "full context."),
        ],
        "stack_note": "[[Platform, languages live, and go-live date to be confirmed.]]",

        "call_h2": "What a Creative Cables call sounds like",
        "call_caption": "Example call",
        "call": [
            ("caller", "I've got a fabric cable in the basket and a brass fitting — will the two "
                       "actually go together?"),
            ("agent", "They will, as long as the cable is the 2-core and not the 3-core — the brass "
                      "fitting takes the 2-core. Can you tell me the colour code in your basket?"),
            ("caller", "It says RM09."),
            ("agent", "That's the 2-core, so you're fine. One thing worth knowing: that fitting doesn't "
                      "include the ceiling rose, which people often assume. Do you want me to add it "
                      "and text you the updated basket?"),
            ("caller", "Yes — and does it come in the same brass finish?"),
            ("agent", "It does. I'm sending you the link now with both in the matching finish."),
        ],
        "call_note": ("Product details here are illustrative. On a live call the agent reads Creative "
                      "Cables' real catalogue and stock."),

        "results_eyebrow": "Results",
        "results_h2": "What changed",
        "results": [
            ("[[00%]]", "[[Headline metric]]",
             "[[The one number Creative Cables has approved for publication, and what it measures.]]"),
            ("[[+00%]]", "[[Metric two]]", "[[Second approved figure.]]"),
            ("[[+00%]]", "[[Metric three]]", "[[Third approved figure.]]"),
        ],
        "results_foot": ("[[Measurement window and method to be confirmed with Creative Cables before "
                         "publication.]]"),

        "quote": "[[Approved quote from Marco Logreco to be supplied — one or two sentences, in his "
                 "words, on what changed for the business.]]",

        "honest_h2": "What it does not do",
        "honest_body": ("The limits are part of the reason this works. The agent handles the questions "
                        "that repeat; it does not handle the ones that need a specialist."),
        "honest_points": [
            "It does not design bespoke configurations. Anything genuinely custom is captured and "
            "handed to the team.",
            "It does not approve exceptions. Pricing, out-of-policy returns and disputes are routed, "
            "never decided.",
            "It does not pretend to be a person. Callers are told they are speaking to Sabato.",
        ],

        "cta_h2": "Want the same for your catalogue?",
        "cta_sub": ("A pilot runs on your real calls for two weeks and measures what changed against "
                    "your own baseline."),
    },
}

# Order on the homepage band and any future hub page.
ORDER = ["clima-convenienza", "creative-cables"]
