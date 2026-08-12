#!/usr/bin/env python3
"""Playbook content, English. LANDING PAGE, not an article.

Daniel's brief, 11 Aug, after reading the long version: "this reads like a
blog post - nobody is going to read all of that. Shorter text, straight to the
point, CTAs. And don't mention Italy, we're global."

So the rules for this file:

  * Every body paragraph is ONE sentence, two at most. If a point needs a third
    sentence it is an article point, not a landing point - cut it or move it to
    a Build File issue.
  * Three CTAs on the page: hero, mid-page, closing band. The reader who is
    convinced at any scroll depth has a button in reach.
  * GLOBAL. No jurisdiction-specific law on the page. The Italy research
    (DPR 1525/1963, the 20% cap, NASpI) is real and verified but it is one
    market's version of a global truth - it lives in the git history and can
    become a Build File issue or a localised variant later.
  * The verification rule still holds: the one external figure left on the page
    (the January returns wave) keeps its source line. Everything else is
    structural - true by how the world works, not by somebody's survey.
"""

ORDER = ["peak-season", "international-expansion"]

# --------------------------------------------------------------------------
# Hero: fourteen days of December. The cut-off is one day; the calls are the
# week after it - and still before Christmas, which is the whole point. Dec 11
# 2026 is a real Friday and the week that follows really does end on the 18th,
# because a calendar graphic that does not survive someone checking it is worse
# than no calendar at all.
# --------------------------------------------------------------------------
HERO_SVG = """
<svg viewBox="0 0 560 330" role="img" aria-label="Two weeks of December. One day is the last order date; the calls peak across the following week, still before Christmas.">
  <rect x="0" y="0" width="560" height="330" rx="24" fill="rgb(249,250,253)"/>
  <text x="40" y="52" font-size="19" font-weight="700" letter-spacing="2.2" fill="rgb(69,65,64)">TWO WEEKS IN DECEMBER</text>

  <g font-size="19" fill="rgb(140,138,137)" font-weight="500">
    <text x="52" y="86">M</text><text x="118" y="86">T</text><text x="184" y="86">W</text>
    <text x="250" y="86">T</text><text x="316" y="86">F</text><text x="382" y="86">S</text>
    <text x="448" y="86">S</text>
  </g>

  <g>
    <rect x="40" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
    <rect x="106" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
    <rect x="172" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
    <rect x="238" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
    <rect x="304" y="96" width="52" height="52" rx="12" fill="rgb(0,0,0)"/>
    <text x="330" y="129" font-size="20" font-weight="700" fill="#fff" text-anchor="middle">11</text>
    <rect x="370" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
    <rect x="436" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
  </g>
  <text x="330" y="174" font-size="19" font-weight="700" fill="rgb(18,10,11)" text-anchor="middle">last order date</text>

  <g>
    <rect x="40" y="196" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
    <rect x="106" y="196" width="52" height="52" rx="12" fill="rgb(204,255,0)"/>
    <rect x="172" y="196" width="52" height="52" rx="12" fill="rgb(204,255,0)"/>
    <rect x="238" y="196" width="52" height="52" rx="12" fill="rgb(204,255,0)"/>
    <rect x="304" y="196" width="52" height="52" rx="12" fill="rgb(204,255,0)"/>
    <rect x="370" y="196" width="52" height="52" rx="12" fill="rgb(204,255,0)"/>
    <rect x="436" y="196" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
  </g>
  <path d="M132 268 L396 268" stroke="rgb(18,10,11)" stroke-width="2"/>
  <path d="M132 268 L132 260 M396 268 L396 260" stroke="rgb(18,10,11)" stroke-width="2"/>
  <text x="264" y="294" font-size="19" font-weight="700" fill="rgb(18,10,11)" text-anchor="middle">the phone calls</text>
</svg>
"""

BAND_SVG = """
<svg viewBox="0 0 560 300" role="img" aria-label="Two curves. Orders peak on the sale day; calls peak roughly a week later and stay high.">
  <line x1="40" y1="250" x2="540" y2="250" stroke="rgba(248,244,241,.25)"/>
  <path d="M40 244 C 110 240 150 150 180 84 C 210 150 250 232 300 240 C 360 246 460 247 540 248"
        fill="none" stroke="rgba(248,244,241,.5)" stroke-width="2.5" stroke-dasharray="6 5"/>
  <path d="M40 247 C 120 245 170 236 220 214 C 275 190 320 112 366 100 C 420 88 470 142 540 168"
        fill="none" stroke="rgb(204,255,0)" stroke-width="3.5"/>
  <circle cx="180" cy="84" r="5" fill="rgba(248,244,241,.7)"/>
  <circle cx="366" cy="100" r="6" fill="rgb(204,255,0)"/>
  <text x="180" y="64" font-size="19" font-weight="700" fill="rgba(248,244,241,.75)" text-anchor="middle">orders</text>
  <text x="374" y="80" font-size="19" font-weight="700" fill="rgb(204,255,0)" text-anchor="middle">calls</text>
  <g font-size="19" fill="rgba(248,244,241,.45)" font-weight="500">
    <text x="40" y="274">week before</text>
    <text x="255" y="274" text-anchor="middle">sale</text>
    <text x="540" y="274" text-anchor="end">two weeks after</text>
  </g>
</svg>
"""

# --------------------------------------------------------------------------
# International expansion. One line per market on the left, one agent on the
# right - the whole argument of the page in a picture, before a word is read.
# --------------------------------------------------------------------------
INTL_HERO_SVG = """
<svg viewBox="0 0 560 330" role="img" aria-label="Five local phone numbers in five different languages, all answered by one voice agent.">
  <rect x="0" y="0" width="560" height="330" rx="24" fill="rgb(249,250,253)"/>
  <text x="40" y="48" font-size="19" font-weight="700" letter-spacing="2.2" fill="rgb(69,65,64)">FIVE COUNTRIES, ONE LINE</text>

  <g fill="none" stroke="rgb(203,202,202)" stroke-width="2">
    <path d="M240 93 C 288 93 288 185 322 185"/>
    <path d="M240 139 C 288 139 288 185 322 185"/>
    <path d="M240 185 L 322 185"/>
    <path d="M240 231 C 288 231 288 185 322 185"/>
    <path d="M240 277 C 288 277 288 185 322 185"/>
  </g>

  <g>
    <rect x="40" y="74" width="200" height="38" rx="11" fill="#fff" stroke="rgb(227,226,226)"/>
    <text x="58" y="99" font-size="19" font-weight="700" fill="rgb(18,10,11)">+49</text>
    <text x="110" y="99" font-size="19" font-weight="500" fill="rgb(100,98,97)">German</text>

    <rect x="40" y="120" width="200" height="38" rx="11" fill="#fff" stroke="rgb(227,226,226)"/>
    <text x="58" y="145" font-size="19" font-weight="700" fill="rgb(18,10,11)">+33</text>
    <text x="110" y="145" font-size="19" font-weight="500" fill="rgb(100,98,97)">French</text>

    <rect x="40" y="166" width="200" height="38" rx="11" fill="#fff" stroke="rgb(227,226,226)"/>
    <text x="58" y="191" font-size="19" font-weight="700" fill="rgb(18,10,11)">+34</text>
    <text x="110" y="191" font-size="19" font-weight="500" fill="rgb(100,98,97)">Spanish</text>

    <rect x="40" y="212" width="200" height="38" rx="11" fill="#fff" stroke="rgb(227,226,226)"/>
    <text x="58" y="237" font-size="19" font-weight="700" fill="rgb(18,10,11)">+31</text>
    <text x="110" y="237" font-size="19" font-weight="500" fill="rgb(100,98,97)">Dutch</text>

    <rect x="40" y="258" width="200" height="38" rx="11" fill="#fff" stroke="rgb(227,226,226)"/>
    <text x="58" y="283" font-size="19" font-weight="700" fill="rgb(18,10,11)">+46</text>
    <text x="110" y="283" font-size="19" font-weight="500" fill="rgb(100,98,97)">Swedish</text>
  </g>

  <rect x="322" y="145" width="216" height="80" rx="18" fill="rgb(18,10,11)"/>
  <text x="430" y="180" font-size="21" font-weight="700" fill="#fff" text-anchor="middle">one voice agent</text>
  <text x="430" y="206" font-size="19" font-weight="500" fill="rgb(204,255,0)" text-anchor="middle">every language</text>
</svg>
"""

# Two bars, drawn for a LIGHT block: black fill on grey track, lime numerals
# inside the fill. Lime on near-white is unreadable, which is why the peak-season
# chart recolours itself for the light band rather than reusing the dark palette.
# Widths are the percentages: 560 * .60 = 336, 560 * .75 = 420. If a figure ever
# changes, the bar changes with it - nobody has to remember to redraw it.
#
# TYPE SIZE IS NOT A TASTE DECISION HERE. An SVG scales to its container, so the
# font-size in this file is not the size anybody reads. The viz column is ~498px
# on desktop and ~346px on a 390px phone, so everything below is multiplied by
# 0.89 and 0.62 respectively. The first draft set these labels at 15px, which is
# a comfortable 13px on desktop and an unreadable 9.3px on a phone - measured,
# not guessed, and invisible to every automated check in this gate because the
# contrast audit does not look inside SVGs. 21px is the floor that clears ~13px
# on a phone; the ceiling is ~19px, above which desktop overtakes the 17.5px body
# copy next to it. That leaves almost no room, which is why the labels are also
# cut short enough to fit two lines at that size.
INTL_BARS_SVG = """
<svg viewBox="0 0 560 286" role="img" aria-label="Two bars. Sixty per cent of the shoppers most confident reading English still want customer care in their own language; seventy-five per cent are more likely to buy the brand again when they get it.">
  <text x="0" y="24" font-size="21" font-weight="700" fill="rgb(18,10,11)">Confident English readers who still</text>
  <text x="0" y="52" font-size="21" font-weight="700" fill="rgb(18,10,11)">want care in their own language</text>
  <rect x="0" y="70" width="560" height="52" rx="14" fill="rgb(233,232,232)"/>
  <rect x="0" y="70" width="336" height="52" rx="14" fill="rgb(18,10,11)"/>
  <text x="318" y="106" font-size="30" font-weight="700" fill="rgb(204,255,0)" text-anchor="end">60%</text>

  <text x="0" y="178" font-size="21" font-weight="700" fill="rgb(18,10,11)">More likely to buy the brand again</text>
  <text x="0" y="206" font-size="21" font-weight="700" fill="rgb(18,10,11)">when care is in their language</text>
  <rect x="0" y="224" width="560" height="52" rx="14" fill="rgb(233,232,232)"/>
  <rect x="0" y="224" width="420" height="52" rx="14" fill="rgb(18,10,11)"/>
  <text x="402" y="260" font-size="30" font-weight="700" fill="rgb(204,255,0)" text-anchor="end">75%</text>
</svg>
"""

_EVRI = "https://www.evri.com/press/return-to-sender-four-million-gifts-to-be-sent-back-in-january-2025"

# CSA Research, "Can't Read, Won't Buy - B2C", 2020. A primary study by a
# research firm - 8,709 consumers in 29 countries, respondents vetted by Kantar -
# not a vendor blog recycling somebody else's number, which is the bar four
# widely-circulated peak-season figures failed to clear. Confirmed against CSA's
# own release and Slator's independent write-up before it went on the page.
# The 60% is the one that matters here and the one nobody quotes: it kills the
# "our buyers speak English anyway" objection using the study's own data.
_CSA = "https://csa-research.com/l/media/Consumers-Prefer-their-Own-Language"

PLAYBOOKS = {
    "peak-season": {
        "it": "picchi-stagionali",
        # Verb-led, to read as one family with "Expand Into New Countries".
        # LABEL ONLY - /playbooks/peak-season is untouched, so nothing
        # re-indexes and no redirect is needed.
        "nav": "Handle Peak Season",
        "chip": "Playbook",
        "title": "Peak Season Support Without Seasonal Hires | Sabato AI",
        "description": "The call surge lands after the sale and runs through "
                       "January returns. Put a voice agent on the line in two "
                       "weeks - no recruiting, no training, no layoffs.",
        "h1": "Peak season, handled. [nb]Zero seasonal hires.[/nb]",
        "sub": "The call surge lands the week after your sale and runs through "
               "January returns. A voice agent takes the repetitive volume - live "
               "in two weeks, no recruiting, no training calendar, no layoffs.",
        "hero_visual": HERO_SVG,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "WHY THE HIRING PLAN FAILS",
                "h2": "Seasonal hiring is a trap.",
                "body": [
                    "You recruit in the tightest labour market of the year - "
                    "against every warehouse, store and courier chasing the same "
                    "people in the same eight weeks.",
                    "You train for weeks so people can leave in January. On a "
                    "ten-week contract, the training never pays itself back.",
                    "And temps are not the cheap option: agency margin sits on top "
                    "of full wages. You pay more per hour for less experience.",
                ],
            },
            {
                "tone": "light",
                "eyebrow": "AND THE TIMING IS AGAINST IT",
                "h2": "The calls arrive [nb]after the sale.[/nb]",
                "body": [
                    "Orders peak in a day. Calls peak about a week later - a call "
                    "about an order can only exist once the order does.",
                    "So seasonal staff are trained for the sale, and the queue "
                    "builds as their rota thins. Then January lands the returns "
                    "wave - more than double normal volumes - right after the "
                    "temp contracts end.",
                ],
                "viz": BAND_SVG.replace("rgba(248,244,241,.25)", "rgb(227,226,226)")
                                .replace("rgba(248,244,241,.5)", "rgb(160,158,157)")
                                .replace("rgba(248,244,241,.75)", "rgb(69,65,64)")
                                .replace("rgba(248,244,241,.45)", "rgb(120,118,117)")
                                .replace("rgb(204,255,0)", "rgb(122,153,0)"),
                "fine": ('Curves illustrative. Returns: <a href="' + _EVRI + '" '
                         'rel="nofollow noopener" target="_blank">Evri network '
                         'data</a>, 3.9m parcels in the four weeks after Christmas '
                         '2023, over double typical volumes.'),
            },
        ],


        "workflows": {
            "h2": "What Sabato can take off your team",
            "lede": "Peak is four ordinary problems arriving at once. Each one is "
                    "a workflow the agent already runs.",
            "go": "See the workflow",
            "items": [
                ("Where Is My Order", "/use-cases/where-is-my-order",
                 "The call that defines the week. Status read live from your "
                 "store, confirmed by text.", "wismo"),
                ("Pre-Sales Consultation", "/use-cases/pre-sales-consultation",
                 "Peak buyers ask before they order - will it fit, will it "
                 "arrive in time. Answered on the call, not after it.", "presales"),
                ("Managing Returns", "/use-cases/managing-returns",
                 "January's peak. Booked on the phone the moment the portal says "
                 "no.", "returns"),
                ("Back-in-Stock Notification", "/use-cases/back-in-stock-notification",
                 "Sellouts are peak's other face. Callers get notified the moment "
                 "it's back.", "restock"),
            ],
        },

        "proof": {
            "eyebrow": "PROOF",
            "quote": "Elena handles our most repetitive calls - order status, "
                     "shipping, returns - on-brand and instantly. Our team now "
                     "focuses on the cases that actually need a person.",
            "who": "Marco Logreco",
            "role": "Head of E-Commerce, Creative Cables",
            "nums": [("39%", "Calls resolved end to end"),
                     ("57%", "Of order-status calls automated"),
                     ("55s", "Average handle time")],
            "href": "/customers/creative-cables",
            "link": "Read the full case study",
        },

        "faq_h2": "Questions operators ask",
        # Rendered ON the page and mirrored into FAQPage schema - the two read
        # the same list, so they cannot drift apart.
        "faq": [
            ("How fast can we be live before peak?",
             "Two weeks from kickoff. Four weeks before your sale is the last "
             "comfortable start - it leaves a fortnight of real calls to tune on "
             "before the volume arrives."),
            ("Does it replace my support team?",
             "No. It absorbs the repetitive volume - order status above all - so "
             "your people spend peak week on the calls that need judgement. "
             "Anything sensitive escalates to a human with full context."),
            ("What happens after peak?",
             "Nothing to lay off. Capacity scales down with the calls, and the "
             "same agent handles the January returns wave your temps would have "
             "missed."),
            ("What if it doesn't know the answer?",
             "It says so and hands the call to your team with the caller's "
             "details and intent attached - the customer never starts over."),
        ],

        "cta": {
            "hand": "before the queue builds",
            "h2": "The capacity you can't hire, [nb]you can switch on.[/nb]",
            "sub": "We build it, we run it, you see the numbers. Live in two "
                   "weeks.",
        },
    },

    # ----------------------------------------------------------------------
    # This page owns the commercial keyword. /blog/multilingual-phone-support-
    # eu-expansion is deliberately SUPPORTING content underneath it - the blog
    # post is the how-to with the GA4 click-paths and the market-sequencing
    # steps, this is the page someone lands on when they are deciding. Two
    # pages chasing the same phrase would only compete with each other, so the
    # post links up to here and this page does not repeat the post's steps.
    # ----------------------------------------------------------------------
    "international-expansion": {
        "it": "espansione-internazionale",
        "nav": "Expand Into New Countries",
        "chip": "Playbook",
        "title": "Expand Into New Countries Without Hiring Abroad | Sabato AI",
        "description": "Open a market and answer its phone line the same week. "
                       "A voice agent takes calls in the local language from day "
                       "one - no hiring abroad, no agency, no minimum volume.",
        # [br], NOT [nb]. "Answer in five languages." inside a nowrap span is
        # 430px wide at the 37px phone h1 size, which made the whole page scroll
        # sideways on a 390px screen. [nb] is only safe on a phrase short enough
        # to survive the narrowest column it will ever sit in.
        "h1": "Sell in five countries.[br]Answer in five languages.",
        "sub": "Opening a market takes an afternoon. Covering its phone line "
               "takes a headcount you cannot justify at launch volume. A voice "
               "agent answers in the caller's language from day one - live in "
               "two weeks.",
        "hero_visual": INTL_HERO_SVG,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "WHY THE HIRE NEVER HAPPENS",
                "h2": "A new country can't pay for its own phone line.",
                "body": [
                    "At launch volume a native speaker is a full salary for a "
                    "fraction of a role, and one hire per language is one point "
                    "of failure - a holiday, a resignation, and that market goes "
                    "quiet.",
                    "So the line waits for the volume, and the volume waits for "
                    "the line.",
                    "Nobody complains about a number they can't use in their own "
                    "language. They just don't call, and don't come back - which "
                    "reads exactly like a market that was never there.",
                ],
            },
            {
                "tone": "light",
                "eyebrow": "AND ENGLISH DOESN'T CLOSE THE GAP",
                "h2": "They read English.[br]They still won't call in it.",
                "body": [
                    "Reading a product page in a second language is easy. "
                    "Explaining a delivery problem down a phone line in one is "
                    "not.",
                    "Even among the shoppers most confident reading English, "
                    "<b>60% still want customer care in their own language</b> - "
                    "and 75% say they are more likely to buy the brand again "
                    "when they get it.",
                ],
                "viz": INTL_BARS_SVG,
                "fine": ('<a href="' + _CSA + '" rel="nofollow noopener" '
                         'target="_blank">CSA Research, &ldquo;Can&rsquo;t Read, '
                         'Won&rsquo;t Buy &ndash; B2C&rdquo;</a>, 2020 &ndash; '
                         '8,709 consumers in 29 countries.'),
            },
            {
                "tone": "dark",
                "eyebrow": "THE COST OF THE NEXT COUNTRY",
                "h2": "One more language, [nb]not one more headcount.[/nb]",
                "body": [
                    "With people, every language is a step cost: a hire, a rota, "
                    "a training calendar, and cover for the weeks that one person "
                    "isn't there.",
                    "With an agent it's configuration. The fifth country costs "
                    "what the second one did.",
                ],
            },
        ],

        "workflows": {
            "h2": "What Sabato can take off your team",
            "lede": "A new market asks the same four questions your home market "
                    "does - in a language you don't have on the rota.",
            "go": "See the workflow",
            "items": [
                ("Pre-Sales Consultation", "/use-cases/pre-sales-consultation",
                 "A first order from a foreign site starts with a question. "
                 "Answered on the call, in their language.", "presales"),
                ("Where Is My Order", "/use-cases/where-is-my-order",
                 "Cross-border delivery is slower and harder to read. Status "
                 "pulled live from your store, confirmed in writing.", "wismo"),
                ("Managing Returns", "/use-cases/managing-returns",
                 "The one thing that stops a first order from abroad. Booked on "
                 "the phone, in their language.", "returns"),
                ("Checkout Summary via Text", "/use-cases/checkout-summary-via-text",
                 "The order read back and sent in writing, so nothing rides on a "
                 "second-language phone call.", "checkout"),
            ],
        },

        "faq_h2": "Questions operators ask",
        "faq": [
            ("How many languages can it handle?",
             "As many as you sell in. The agent picks up the caller's language "
             "in the first sentence and stays in it for the whole call, written "
             "summary included."),
            ("Does it sound native, or translated?",
             "Native. Each language is built and tested by someone who speaks "
             "it - a translated script read out loud is exactly what makes a "
             "caller hang up."),
            ("Do we need a local number in every country?",
             "You don't have to, but a local number is the cheapest trust signal "
             "a foreign site can buy. The agent answers whichever line rings."),
            ("What if we already have someone covering that language?",
             "Then they stop being the single point of failure. The agent takes "
             "the repetitive volume and the out-of-hours calls; your person "
             "takes the ones that need judgement."),
        ],

        "cta": {
            "hand": "before you write the market off",
            "h2": "Open the country. [nb]The line opens with it.[/nb]",
            "sub": "We build it, we run it, you see the numbers. Live in two "
                   "weeks.",
        },
    },
}
