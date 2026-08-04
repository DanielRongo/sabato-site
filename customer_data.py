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
        "logo": None,
        "person": "Alessio Perrucci",
        "person_initials": "AP",
        "role": "CEO",
        "photo": None,
        "industry": "Home Improvement",
        "industry_href": "/industries/home-improvement",
        "chip": "Customer story",
        "title": "ClimaConvenienza — Voice AI Case Study | Sabato AI",
        "description": ("How ClimaConvenienza scaled phone support across Italy, France and Germany "
                        "without hiring — nine multilingual agents live, 53.1% of calls handled "
                        "autonomously in the first month."),
        "h1": "Growing across three markets faster than a phone team can be hired.",
        "sub": ("ClimaConvenienza sells climate equipment into Italy, France and Germany. Demand "
                "was climbing in all three — and then a heatwave pushed it to a record eight days "
                "after go-live. The phone line scaled with the business instead of capping it."),

        "situation_eyebrow": "The situation",
        "situation_h2": "Expansion moves faster than hiring does",
        "situation_body": [
            "ClimaConvenienza sells heat pumps, boilers and air conditioning on Shopify, and the "
            "business has been growing well beyond Italy. New markets generate phone calls long "
            "before they generate the volume that justifies a native-speaking hire — a French line "
            "and a German line are a full salary each on the day they open, and a fraction of the "
            "traffic. Growth arrives first; the business case for headcount arrives later.",
            "Then the weather intervened. Climate equipment has one demand curve and it is the "
            "temperature. The agent went live on 22 June 2026 and eight days later took 1,074 calls "
            "in a single day — the busiest day on record, in its second week of operation, absorbed "
            "without a single additional hire.",
        ],
        "situation_points": [
            ("New markets ring before they pay for themselves",
             "France and Germany were producing calls from customers already far enough down the "
             "funnel to pick up the phone — well before the volume in either market justified "
             "dedicated headcount."),
            ("Demand is set by the weather, not the plan",
             "A heatwave does not give notice. The volume that matters most arrives in the days you "
             "could not have staffed for, and it arrives from people ready to buy today."),
            ("Half the phone traffic is one question",
             "Where is my order accounts for 48% of every call. Answering it well is not a support "
             "nicety — it is the single largest claim on the team's day."),
        ],

        "stack_h2": "What went live",
        "stack": [
            ("Multilingual pre-sales and support",
             "The agent takes calls in Italian, French and German across all three queues — general "
             "information, order tracking and the product configurator — on the same catalogue and "
             "the same rules."),
            ("Where is my order",
             "The biggest queue by far. Order status read live from Shopify and confirmed back to "
             "the caller, with the detail sent as a text so nothing rests on the customer "
             "remembering it."),
            ("Configuratore",
             "The configurator queue, on the phone. The agent takes a caller through sizing and "
             "compatibility to a specific unit for their space and system. It is the "
             "highest-autonomy queue on the line, at 57.8%."),
        ],
        "stack_note": ("Connected to Shopify, so the agent reads the same catalogue, pricing and order "
                       "data the storefront does. Live from 22 June 2026."),

        "call_h2": "What a ClimaConvenienza call sounds like",
        "call_caption": "Example call · order tracking",
        "call": [
            ("caller", "Bonjour, j'ai commandé une pompe à chaleur la semaine dernière et je n'ai "
                       "aucune nouvelle."),
            ("agent", "Bien sûr, je peux vérifier. Vous avez le numéro de commande, ou l'adresse "
                      "e-mail utilisée pour commander ?"),
            ("caller", "L'e-mail, oui."),
            ("agent", "Merci. Votre commande est partie de l'entrepôt hier et la livraison est prévue "
                      "jeudi. Je vous envoie le lien de suivi par SMS tout de suite."),
            ("caller", "Parfait. Et si personne n'est là à la livraison ?"),
            ("agent", "Le transporteur laisse un avis et repasse le lendemain. Si vous préférez une "
                      "date précise, je note la demande et l'équipe vous confirme le créneau."),
        ],
        "call_note": ("Order details here are illustrative. The call above is in French because France "
                      "is one of the markets growing fastest — on a live call the agent reads "
                      "ClimaConvenienza's real catalogue and order data."),

        "results_eyebrow": "Results · 22 June – 23 July 2026",
        "results_h2": "The first month",
        "results": [
            ("53.1%", "Calls handled autonomously",
             "Resolved by the agent with no operator involved, in the first month live "
             "(22–30 June 2026)."),
            ("9", "Multilingual agents live",
             "Three workflows — general information, order tracking and the configurator — running "
             "in Italian, French and German."),
            ("435", "Hours of support time returned",
             "Phone time the agent absorbed instead of an operator, redeployed into B2B sales. "
             "[[Confirm derivation before publication: resolved calls × average handle time.]]"),
        ],
        "results_foot": ("Measured from go-live on 22 June 2026 to 23 July 2026. The autonomy figure "
                         "above is the first month; it was 46.8% in July as volume grew — the reason "
                         "is below. "
                         "[[Figures to be confirmed in writing with ClimaConvenienza before publication.]]"),

        "quote": ("We faced a massive demand spike without hiring anyone — and we moved a large part "
                  "of the customer support team into B2B sales, so they are growing the business "
                  "instead of repeating the same thing on the phone all day."),
        "quote_pending": True,

        "honest_h2": "What the numbers do not say",
        "honest_body": ("This is one month of live service, and publishing only the flattering half "
                        "of it would make the rest less believable. So here is the whole picture."),
        "honest_points": [
            "Autonomy fell, not rose. The agent resolved 53.1% of calls without a human in June and "
            "46.8% in July. The reason is mix: volume grew and the growth landed in the hardest "
            "Italian queues — general information sits at 39.2% autonomy and is now the largest "
            "queue on the line.",
            "Where is my order got harder as it got bigger. Italian WISMO volume more than doubled "
            "and its autonomy fell from 56.6% to 46.3% — scale surfaced order scenarios the agent "
            "had not been taught. Those are being mapped into the prompt; that work is ongoing, "
            "not finished.",
            "French and German show 100% autonomy partly because there is no French or German "
            "speaker to transfer to. It means those callers got a complete answer instead of no "
            "answer — it does not mean the agent handles every case a native speaker could.",
            "It does not give installation advice, and it does not approve exceptions. Discounts, "
            "out-of-policy returns and disputed orders are captured with full context and routed to "
            "a person, never decided.",
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
