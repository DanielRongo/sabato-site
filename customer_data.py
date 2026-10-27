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

TWO FLAGS, NOT ONE
------------------
`approved`   - the figures and the quote on THIS customer's own case study page
               are signed off, so the page drops its TBC chips and DRAFT ribbon.
`promotable` - we may name this customer, and show their numbers, on pages that
               are NOT their own: the homepage, /pricing, /about. This is a
               strictly stronger permission and it is a separate question. A
               customer can be perfectly happy with a page that nothing links to
               and much less happy about being the face of the homepage.

Overloading one flag for both is how a pending customer ends up on the homepage.
Creative Cables gave the green light on 10 Aug 2026; ClimaConvenienza has not,
so it is approved but not promotable. tools/postdeploy_check.py reads this field
and fails the gate if a non-promotable name appears off its own page.
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
            "note": "Every queue answered in every market by the same agent, live in "
                    "every language from day one.",
        },
        "storefront": "/customers/assets/climaconvenienza-store.jpg",
        "storefront_url": "climaconvenienza.it",
        "platform": "Shopify",
        "platform_logo": "/customers/assets/shopify.png",
        "industry": "Home Improvement",
        "industry_href": "/industries/home-improvement",
        "chip": "Customer story",
        "approved": True,
        "promotable": False,
        "title": "ClimaConvenienza - Voice AI Case Study | Sabato AI",
        "description": "How ClimaConvenienza runs phone support across Italy, France and Germany: 12,127 calls in month one, 44.7% closed without an operator.",
        "h1": "Three markets, three languages, one phone line that grows with [nb]the business.[/nb]",
        "sub": ("ClimaConvenienza offers home comfort solutions in Italy, France and Germany. "
                "Demand was climbing in all three markets, and six days after go-live a heatwave "
                "pushed it to a record. The phone line held the peak and kept pace with growth."),

        "situation_eyebrow": "The situation",
        "situation_h2": "Multilingual support behind international growth",
        "situation_body": [
            "ClimaConvenienza brings home comfort to three countries and has been growing beyond "
            "Italy for years. Every new market brings customers who want to talk to someone in "
            "their own language, often before they buy. The business needed support that could "
            "follow the expansion, absorb demand peaks, and do it without a heavy hit to running "
            "costs.",
            "Then the heat arrived. Air conditioning demand peaks hard with the weather. Six days "
            "after go-live the agent took the busiest day on record: 973 calls.",
        ],
        "situation_points": [
            ("Every new market rings from day one",
             "France and Germany were producing calls within the first weeks, often from customers "
             "one step from buying. Support had to answer in French and German straight away, at "
             "the same standard as in Italy."),
            ("Peaks follow the weather",
             "A heatwave does not give weeks of notice. The most valuable calls arrive on exactly "
             "those days, from people ready to buy."),
            ("Four calls in ten ask the same question",
             "Where is my order accounts for 42.4% of the 12,127 calls the agent took in month one. "
             "It is the most frequent request of the day."),
        ],

        "stack_h2": "What went live",
        "stack": [
            ("languages", "Multilingual pre-sales and support",
             "The agent takes calls in Italian, French and German across all three queues (general "
             "information, order tracking and the product configurator), on the same catalogue and "
             "the same rules."),
            ("wismo", "Where is my order",
             "The most frequent question on the line. Order status read live from Shopify and "
             "confirmed back to the caller, with the detail sent as a text so nothing rests on the "
             "customer remembering it."),
            ("configurator", "Configuratore",
             "The configurator queue, on the phone. The agent takes a caller through sizing and "
             "compatibility to a specific unit for their space and system. It has the highest share "
             "of calls closed without an operator: 56.7%."),
        ],
        "stack_note": ("Connected to Shopify, so the agent reads the same catalogue, pricing and order "
                       "data the storefront does."),

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
                 ("agent", "Then 9000 BTU would be under-sized for that room: 12000 is the right "
                           "match. We have a single-split Hisense at 12000 with built-in Wi-Fi in "
                           "stock, and a Mitsubishi in the same class if you'd prefer that brand."),
                 ("caller", "What's the difference in price?"),
                 ("agent", "The Hisense is around €300 including VAT, the Mitsubishi starts at about "
                           "€500. Shall I text you both so you can compare?"),
                 ("caller", "Yes, send them over."),
             ]},
            {"label": "WISMO", "icon": "wismo",
             "caption": "Where is my order",
             "duration": "00:51",
             "lines": [
                 ("caller", "Hi, I ordered a heat pump last week and I've not heard anything."),
                 ("agent", "I can check that now. Do you have the order number to hand?"),
                 ("caller", "One moment... it's 48120."),
                 ("agent", "Thank you. Your order left the warehouse yesterday and it's due "
                           "Thursday. I'm sending you the tracking link by text now."),
                 ("caller", "And what if nobody's home when it arrives?"),
                 ("agent", "I'll log that and the team will get back to you to arrange the "
                           "delivery."),
             ]},
        ],
        "call_note": ("Product and order details here are illustrative. On a live call the agent "
                      "reads ClimaConvenienza's real catalogue, stock and order data, and takes "
                      "the same calls in French and German."),

        "results_eyebrow": "Results · 24 June to 24 July 2026",
        "results_h2": "The first month",
        "results": [
            ("44.7%", "Calls closed without an operator",
             "5,422 of 12,127 calls closed by the agent with no transfer to a person on the "
             "team."),
            ("12,127", "Calls handled by the agent",
             "In 30 days, for a total of 264 hours of conversation."),
            ("973", "Calls on the busiest day",
             "Taken by the agent on Tuesday 30 June 2026, six days after go-live, during a "
             "heatwave."),
        ],
        "results_foot": ("Measured on the Sabato platform from 24 June to 24 July 2026, test calls "
                         "excluded."),

        "quote": ("Sara helped us handle a sharp spike in requests and move part of the support team "
                  "onto complex requests and B2B sales growth. By automating the most repetitive "
                  "requests, we make the most of our people's skills and spend more time on customer "
                  "relationships and commercial growth."),

        "cta_h2": "Want the same for your e-commerce store?",
        "cta_sub": ("A pilot runs on your real calls and measures what changed against your own "
                    "baseline. No slideware."),
    },

    # ------------------------------------------------------------------ 2
    "creative-cables": {
        "name": "Creative Cables",
        "initials": "CC",
        "logo": "/customers/assets/creative-cables-logo.png",
        # White knockout for use on the black proof card. The stock logo is
        # dark ink on an OPAQUE near-white plate, so it lands as a grey
        # rectangle on anything dark. Generated once, not filtered in CSS.
        "logo_white": "/customers/assets/creative-cables-logo-white.png",
        "person": "Marco Logreco",
        "person_initials": "ML",
        "role": "Head of E-Commerce",
        "photo": "/customers/assets/marco-logreco.jpg",
        "coverage": None,
        "kb": {
            "title": "What Elena knows",
            "number": "~50,000 words",
            "topics": ["Shipping", "Returns & warranty", "Warranty by country", "Customs",
                       "Payments", "Store services", "Certifications", "Order tracking",
                       "Product education"],
            "note": "One knowledge base behind both agents, so the answer to a returns question "
                    "is the same at 9am on Monday as it is at 7pm on Friday.",
        },
        "storefront": None,
        "storefront_url": "",
        "platform": "",
        "platform_logo": None,
        "industry": "Furniture & Home",
        "industry_href": "/industries/furniture-home",
        "chip": "Customer story",
        "approved": True,
        "promotable": True,
        "title": "Creative Cables - Voice AI Case Study | Sabato AI",
        "description": "How Creative Cables put voice AI on its Italian customer line: 39% of calls resolved end to end in month one, 57% of order-status calls automated.",
        "h1": "Elena answers the calls that repeat, in [nb]55 seconds.[/nb]",
        "sub": ("Creative Cables sells decorative lighting, textile cables and lighting components "
                "from Turin - seven stores in Italy, one in Paris, shipping worldwide. Most of what "
                "the phone asks has a known answer. Now the known answers arrive instantly, and the "
                "team gets the rest."),

        "situation_eyebrow": "The situation",
        "situation_h2": "Most inbound calls have a known answer",
        "situation_body": [
            "Shipping windows. Return periods. Warranty terms, which differ by country. Customs. "
            "Payment methods. Store opening hours. None of these are "
            "hard questions - they are the same questions, arriving all day, each one occupying a "
            "person who could be handling something that genuinely needs judgement.",
            "Underneath them sits the most repetitive request of all: where is my order. It was "
            "entirely human-handled, and it is the single most predictable call a retailer takes. "
            "The answer already exists in the order system; it just needed someone, or something, "
            "to read it out.",
        ],
        "situation_points": [
            ("The same questions, all day",
             "Shipping, returns, warranty and payments repeat endlessly. The cost is not difficulty, "
             "it is volume against a finite team."),
            ("Where is my order was fully manual",
             "The most repetitive inbound reason on the line, answered by a person every single "
             "time, from data a machine can read directly."),
            ("Consistency is the real requirement",
             "Return windows, customs rules and warranty terms vary by country. They have to be "
             "right, and identical, on every call - not approximately right depending on who "
             "answered."),
        ],

        "stack_h2": "What went live",
        "stack": [
            ("languages", "Elena, on the general line",
             "An Italian-native agent handling company, shipping, returns, warranty, payments and "
             "store questions from a single knowledge base - so the answer does not depend on who "
             "picked up."),
            ("wismo", "Where is my order, with live data",
             "A dedicated order-status agent with a real-time lookup into the order system. The "
             "caller gets the actual status of their actual order, with no human in the loop."),
            ("configurator", "Triage that protects the team",
             "Damaged items, address changes and cancellations are recognised as genuine post-sale "
             "cases and routed to a person with the context already gathered."),
        ],
        "stack_note": "Two agents, live on the Italian customer line.",

        "call_h2": "What a Creative Cables call sounds like",
        "calls": [
            {"label": "WISMO", "icon": "wismo",
             "caption": "Order status, read live from the order system",
             "duration": "00:48",
             "lines": [
                 ("caller", "Hi, I ordered a pendant lamp and some cable last week and I'd like to "
                            "know where it is."),
                 ("agent", "Of course. I'm Elena from Creative Cables. Can I take the order "
                           "number?"),
                 ("caller", "It's 30294."),
                 ("agent", "Thank you. I can see the order - it left us on Tuesday and the courier "
                           "has it out for delivery today. I'm sending you the tracking link by "
                           "text now."),
                 ("caller", "Perfect. And the cable was on the same order?"),
                 ("agent", "It was, both items are in the same parcel."),
             ]},
            {"label": "General information", "icon": "languages",
             "caption": "A returns question, answered the same way every time",
             "duration": "01:02",
             "lines": [
                 ("caller", "If I order a lamp and it isn't right for the room, how long do I have "
                            "to send it back?"),
                 ("agent", "You have thirty days from delivery to request a return, and the item "
                           "needs to be unused and in its original packaging."),
                 ("caller", "I'm ordering from outside Italy - does that change anything?"),
                 ("agent", "The window is the same. What changes is the return shipping and any "
                           "customs charges, which depend on your country. If you tell me where "
                           "you're ordering from I'll give you the exact terms."),
                 ("caller", "Switzerland."),
                 ("agent", "Then customs applies on the way in and is refunded separately from the "
                           "order value. I'll text you the full terms so you have them in writing."),
             ]},
        ],
        "call_note": ("Order and policy details here are illustrative. On a live call Elena reads "
                      "the real order system and the real policy base."),

        "results_eyebrow": "Results · the first month live",
        "results_h2": "The first month",
        "results": [
            ("39%", "Calls resolved end to end",
             "Closed by the agent with no human involved, blended across both lines, in the first "
             "four weeks live."),
            ("57%", "Of order-status calls automated",
             "The highest-volume, most repetitive query on the line, answered from live order data."),
            ("55s", "Average handle time",
             "The time it takes the agent to answer and close a call."),
        ],
        "results_foot": "Measured over the first four weeks from go-live.",

        "quote": ("Elena handles our most repetitive calls - order status, shipping, returns - "
                  "on-brand and instantly. Our team now focuses on the cases that actually need a "
                  "person."),

        "cta_h2": "Want the same for your e-commerce store?",
        "cta_sub": ("A pilot runs on your real calls and measures what changed against your own "
                    "baseline. No slideware."),
    },
}

# Order on the homepage band and any future hub page.
ORDER = ["clima-convenienza", "creative-cables"]
