#!/usr/bin/env python3
"""Customer story content.

DRAFT STATUS - read before touching anything here.

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
   one thing a reviewer skims past - and the person it is attributed to will not.
2. A number without a definition is not a number. `53.1% autonomy rate` means
   nothing to a buyer until the page says what was counted and over what period.
   Every metric therefore carries a `sub` explaining what it measures.
"""

CUSTOMERS = {
    # ------------------------------------------------------------------ 1
    "clima-convenienza": {
        "name": "ClimaConvenienza",
        "initials": "CC",
        "logo": "/customers/assets/climaconvenienza-logo.png",
        "person": "Alessio Perrucci",
        "person_initials": "AP",
        "role": "CEO",
        "photo": "/customers/assets/alessio-perrucci.jpg",
        # the graphic in the situation band. "coverage" wins over "storefront".
        "coverage": {
            "title": "One agent · every queue · every market",
            "languages": ["Italiano", "Français", "Deutsch"],
            "queues": ["General information", "Where is my order", "Product configurator"],
            "note": "Every queue answered in every market, from one Italian team - "
                    "no market waiting on a hire before it gets a phone line.",
        },
        "storefront": "/customers/assets/climaconvenienza-store.jpg",
        "storefront_url": "climaconvenienza.it",
        "platform": "Shopify",
        "platform_logo": "/customers/assets/shopify.png",
        "industry": "Home Improvement",
        "industry_href": "/industries/home-improvement",
        "chip": "Customer story",
        "approved": True,
        "title": "ClimaConvenienza - Voice AI Case Study | Sabato AI",
        "description": ("How ClimaConvenienza scaled phone support across Italy, France and Germany "
                        "without hiring - nine multilingual agents live, 53.1% of calls handled "
                        "autonomously in the first month."),
        "h1": "Growing across three markets faster than a phone team [nb]can be hired.[/nb]",
        "sub": ("ClimaConvenienza sells climate equipment into Italy, France and Germany. Demand "
                "was climbing in all three - and then a heatwave pushed it to a record eight days "
                "after go-live. The phone line scaled with the business instead of capping it."),

        "situation_eyebrow": "The situation",
        "situation_h2": "Expansion moves faster than hiring does",
        "situation_body": [
            "ClimaConvenienza sells heat pumps, boilers and air conditioning on Shopify, and the "
            "business has been growing well beyond Italy. New markets generate phone calls long "
            "before they generate the volume that justifies a native-speaking hire - a French line "
            "and a German line are a full salary each on the day they open, and a fraction of the "
            "traffic. Growth arrives first; the business case for headcount arrives later.",
            "Then the weather intervened. Climate equipment has one demand curve and it is the "
            "temperature. The agent went live on 22 June 2026 and days later was taking its "
            "busiest day on record - in its second week of operation, absorbed without a single "
            "additional hire.",
        ],
        "situation_points": [
            ("New markets ring before they pay for themselves",
             "France and Germany were producing calls from customers already far enough down the "
             "funnel to pick up the phone - well before the volume in either market justified "
             "dedicated headcount."),
            ("Demand is set by the weather, not the plan",
             "A heatwave does not give notice. The volume that matters most arrives in the days you "
             "could not have staffed for, and it arrives from people ready to buy today."),
            ("Half the phone traffic is one question",
             "Where is my order accounts for 48% of every call. Answering it well is not a support "
             "nicety - it is the single largest claim on the team's day."),
        ],

        "stack_h2": "What went live",
        "stack": [
            ("languages", "Multilingual pre-sales and support",
             "The agent takes calls in Italian, French and German across all three queues - general "
             "information, order tracking and the product configurator - on the same catalogue and "
             "the same rules."),
            ("wismo", "Where is my order",
             "The biggest queue by far. Order status read live from Shopify and confirmed back to "
             "the caller, with the detail sent as a text so nothing rests on the customer "
             "remembering it."),
            ("configurator", "Configuratore",
             "The configurator queue, on the phone. The agent takes a caller through sizing and "
             "compatibility to a specific unit for their space and system. It is the "
             "highest-autonomy queue on the line, at 57.8%."),
        ],
        "stack_note": ("Connected to Shopify, so the agent reads the same catalogue, pricing and order "
                       "data the storefront does. Live from 22 June 2026."),

        "call_h2": "What a ClimaConvenienza call sounds like",
        "calls": [
            {"label": "Product Configurator", "icon": "configurator",
             "caption": "Picking the right unit for the room",
             "duration": "01:24",
             "lines": [
                 ("caller", "I need air conditioning for a bedroom, about 30 square metres. "
                            "I've no idea which size to get."),
                 ("agent", "I can work that out with you. Is the room on a top floor, and does it "
                           "get much direct sun in the afternoon?"),
                 ("caller", "Top floor, and yes, sun all afternoon."),
                 ("agent", "Then 9000 BTU would be under-sized for that room - 12000 is the right "
                           "match. We have a dual-split Hisense at 12000 with built-in Wi-Fi in "
                           "stock, and a Mitsubishi in the same class if you'd prefer that brand."),
                 ("caller", "What's the difference in price?"),
                 ("agent", "The Hisense is €313.95 including VAT, the Mitsubishi starts at €525. "
                           "Both are A++ on cooling. Shall I text you both so you can compare?"),
                 ("caller", "Yes, send them over."),
             ]},
            {"label": "WISMO", "icon": "wismo",
             "caption": "Where is my order",
             "duration": "00:51",
             "lines": [
                 ("caller", "Hi, I ordered a heat pump last week and I've not heard anything."),
                 ("agent", "I can check that now. Do you have the order number, or the email "
                           "address you ordered with?"),
                 ("caller", "The email is fine."),
                 ("agent", "Thank you. Your order left the warehouse yesterday and it's due "
                           "Thursday. I'm sending you the tracking link by text now."),
                 ("caller", "And what if nobody's home when it arrives?"),
                 ("agent", "The courier leaves a card and tries again the next day. If you'd rather "
                           "fix a specific slot, I'll note that and the team will confirm it with "
                           "you."),
             ]},
        ],
        "call_note": ("Product and order details here are illustrative. On a live call the agent "
                      "reads ClimaConvenienza's real catalogue, stock and order data - and takes "
                      "the same two calls in French and German."),

        "results_eyebrow": "Results · 22 June - 23 July 2026",
        "results_h2": "The first month",
        "results": [
            ("53.1%", "Calls handled autonomously",
             "Resolved by the agent with no operator involved, in the first month live "
             "(22-30 June 2026)."),
            ("435", "Hours of support time returned",
             "Phone time the agent absorbed instead of an operator, redeployed into B2B sales."),
            ("1,535", "Calls on the busiest day",
             "Absorbed during a heatwave, without a single additional hire."),
        ],
        "results_foot": "Measured from go-live on 22 June 2026.",

        "quote": ("We faced a massive demand spike without hiring anyone - and we moved a large part "
                  "of the customer support team into B2B sales, so they are growing the business "
                  "instead of repeating the same thing on the phone all day."),
        
        "cta_h2": "Want the same for your e-commerce store?",
        "cta_sub": ("A pilot runs on your real calls and measures what changed against your own "
                    "baseline. No slideware."),
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
        "storefront": None,
        "storefront_url": "",
        "platform": "",
        "platform_logo": None,
        "industry": "Furniture & Home",
        "industry_href": "/industries/furniture-home",
        "chip": "Customer story",
        "title": "Creative Cables - Voice AI Case Study | Sabato AI",
        "description": ("How Creative Cables handles configuration and order questions across "
                        "multiple countries with a Sabato voice agent."),
        "h1": "[[Headline outcome for Creative Cables - to be set once the metric is approved.]]",
        "sub": ("Configurable lighting and cabling, sold across several countries and several "
                "languages. A catalogue you assemble rather than pick off a shelf - which means the "
                "phone rings with questions no filter can answer."),

        "situation_eyebrow": "The situation",
        "situation_h2": "A configurable catalogue multiplies the questions",
        "situation_body": [
            "When a product is assembled from components - a cable, a fitting, a shade, a length - the "
            "number of things a customer can be unsure about grows faster than the catalogue does. "
            "Compatibility between parts, what is included, whether a finish matches across two "
            "different items: these are the questions that stop a basket at the last step.",
            "Selling across borders multiplies it again. The same question arrives in several "
            "languages, at hours that do not overlap with one team's working day.",
        ],
        "situation_points": [
            ("Configuration questions block checkout",
             "The customer is not browsing. They have chosen, and they need one thing confirmed before "
             "they pay - which makes the answer worth more than the call costs."),
            ("Several languages, one team",
             "Cross-border demand does not queue politely inside one country's office hours."),
            ("The catalogue changes constantly",
             "Components, finishes and stock move. An answer that was right last month is a returned "
             "order this month."),
        ],

        "stack_h2": "What went live",
        "stack": [
            ("configurator", "Pre-sales consultation",
             "Component and compatibility questions answered against the live catalogue, in the "
             "caller's language."),
            ("wismo", "Checkout summary via text",
             "What was discussed - items, specs, a direct link - sent as a message after the call, so "
             "the customer can complete the order without reconstructing it from memory."),
            ("languages", "Escalation to the team",
             "Bespoke configurations and anything commercially unusual routed to a person with the "
             "full context."),
        ],
        "stack_note": "[[Platform, languages live, and go-live date to be confirmed.]]",

        "call_h2": "What a Creative Cables call sounds like",
        "call_caption": "Example call",
        "calls": [
            {"label": "Product Configurator", "icon": "configurator",
             "caption": "Example call · configuration",
             "duration": "01:05",
             "lines": [
            ("caller", "I've got a fabric cable in the basket and a brass fitting - will the two "
                       "actually go together?"),
            ("agent", "They will, as long as the cable is the 2-core and not the 3-core - the brass "
                      "fitting takes the 2-core. Can you tell me the colour code in your basket?"),
            ("caller", "It says RM09."),
            ("agent", "That's the 2-core, so you're fine. One thing worth knowing: that fitting doesn't "
                      "include the ceiling rose, which people often assume. Do you want me to add it "
                      "and text you the updated basket?"),
            ("caller", "Yes - and does it come in the same brass finish?"),
            ("agent", "It does. I'm sending you the link now with both in the matching finish."),
            ]},
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

        "quote": "[[Approved quote from Marco Logreco to be supplied - one or two sentences, in his "
                 "words, on what changed for the business.]]",

        "cta_h2": "Want the same for your e-commerce store?",
        "cta_sub": ("A pilot runs on your real calls for two weeks and measures what changed against "
                    "your own baseline."),
    },
}

# Order on the homepage band and any future hub page.
ORDER = ["clima-convenienza", "creative-cables"]
