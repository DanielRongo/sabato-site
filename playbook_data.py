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

ORDER = ["peak-season"]

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
  <text x="40" y="52" font-size="13" font-weight="700" letter-spacing="2.2" fill="rgb(69,65,64)">TWO WEEKS IN DECEMBER</text>

  <g font-size="12" fill="rgb(140,138,137)" font-weight="500">
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
    <text x="330" y="128" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">11</text>
    <rect x="370" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
    <rect x="436" y="96" width="52" height="52" rx="12" fill="#fff" stroke="rgb(227,226,226)"/>
  </g>
  <text x="330" y="172" font-size="13" font-weight="700" fill="rgb(18,10,11)" text-anchor="middle">last order date</text>

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
  <text x="264" y="292" font-size="14" font-weight="700" fill="rgb(18,10,11)" text-anchor="middle">the phone calls</text>
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
  <text x="180" y="66" font-size="13" font-weight="700" fill="rgba(248,244,241,.75)" text-anchor="middle">orders</text>
  <text x="372" y="82" font-size="13" font-weight="700" fill="rgb(204,255,0)" text-anchor="middle">calls</text>
  <g font-size="12" fill="rgba(248,244,241,.45)" font-weight="500">
    <text x="40" y="274">week before</text>
    <text x="255" y="274" text-anchor="middle">sale</text>
    <text x="540" y="274" text-anchor="end">two weeks after</text>
  </g>
</svg>
"""

_EVRI = "https://www.evri.com/press/return-to-sender-four-million-gifts-to-be-sent-back-in-january-2025"

PLAYBOOKS = {
    "peak-season": {
        "it": "picchi-stagionali",
        "nav": "Peak Season",
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
            "h2": "What it takes off your team",
            "lede": "Peak is four ordinary problems arriving at once. Each one is "
                    "a workflow the agent already runs.",
            "go": "See the workflow",
            "items": [
                ("Where Is My Order", "/use-cases/where-is-my-order",
                 "The call that defines the week. Status read live from your "
                 "store, confirmed by text."),
                ("Managing Returns", "/use-cases/managing-returns",
                 "January's peak. Booked on the phone the moment the portal says "
                 "no."),
                ("Back-in-Stock Notification", "/use-cases/back-in-stock-notification",
                 "Sellouts are peak's other face. Callers get notified the moment "
                 "it's back."),
                ("Cart Abandonment Recovery", "/use-cases/cart-abandonment-recovery",
                 "Peak carts stall on delivery dates and stock. One sixty-second "
                 "call answers both."),
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
}
