# -*- coding: utf-8 -*-
"""Copy for the Product pages. English here, Italian in product_data_it.py.

WHY THIS FILE EXISTS SEPARATELY FROM THE GENERATOR
Same reason playbook_data.py does: the copy changes weekly, the layout does
not. Anyone rewording a headline should never have to open the file that
builds the HTML.

THE ONE THING EVERY PRODUCT PAGE HAS TO SOLVE
Sabato is sold as a managed service - "we build it, we run it, you see the
numbers" appears on roughly thirty pages. A page called a *Builder* argues the
opposite: that there is a tool, and therefore a job, waiting for the customer.
Every page in this section must answer "so do I have to build it?" ON THE PAGE,
not on the sales call. That is what the `hands` block is for, and it is not
optional. Delete it and the section quietly starts contradicting the rest of
the site.

NAMING, 14 Aug
Two of the five product names are still provisional (Daniel's words: "to be
renamed") - Workflow Builder and Agent Evaluation were settled, the others
were not. Do NOT add slugs for the unsettled ones. A slug is the single most
expensive thing on this site to change once Google has indexed it, which is
exactly why /use-cases kept its URL when the menu was reorganised.
"""

# ---------------------------------------------------------------------------
# 1. VOICE AGENT BUILDER
# ---------------------------------------------------------------------------
VOICE_AGENT_BUILDER = dict(
    slug="voice-agent-builder",
    it="voice-agent-builder",          # product names are not translated
    chip="Voice Agent Builder",

    title="Voice Agent Builder | Sabato AI",
    description="Where your phone agent gets its instructions, its tools and "
                "its limits. You set the rules, we build it and keep it "
                "current. Live in two weeks.",

    # 18 and 19 characters. The hero column is 549px at 1440 and 497px at 1100,
    # which is about 22 characters a line at 54px - measured, not guessed, after
    # four separate headlines shipped as three lines. [br] forces the break;
    # never use [nb] here, it cannot wrap at all and overflows a 390px phone.
    h1="You set the rules.[br]We build the agent.",
    sub="The Voice Agent Builder is where a phone agent gets its brief, its "
        "tools and its limits. You describe how a call should go. We do the "
        "building - and the keeping-up-to-date after that.",

    hero_visual="",   # Option A: no visual in the hero. See product.py.

    # ---- the full-bleed platform shot, straight after the hero -------------
    shot=dict(
        src="/product/assets/voice-agent-builder",
        alt="The Sabato agent designer: an entry agent connected to three "
            "handoff agents, with the selected agent's configuration open "
            "beside it.",
        caption="One store's pre-sales agent. The entry agent picks up; three "
                "specialists take the calls it should not handle alone.",
    ),

    blocks=[
        # ---- 1. the brief ------------------------------------------------
        dict(
            tone="dark",
            eyebrow="THE BRIEF",
            h2="An agent is only as good as its instructions.",
            body=[
                "Underneath every agent is a written brief: who it is, what it "
                "is for, how it should talk, and the things it must never say. "
                "Not code - sentences. The kind of thing you would hand a new "
                "hire on their first morning, except this one reads it before "
                "every single call.",
                "You can read yours at any time, and so can we. Every edit is "
                "dated and kept, so \"when did it start saying that?\" is a "
                "question with an answer.",
            ],
        ),

        # ---- 2. the tools (visual 2 lives here) ---------------------------
        dict(
            tone="light",
            eyebrow="THE TOOLS",
            h2="It does things. It doesn't just say things.",
            h2_in_col=True,     # short enough to survive the narrower column
            body=[
                "A chatbot with a phone number can only talk. An agent with "
                "tools can look a customer's order up, check whether the thing "
                "they want is in stock, hand the call to a person, and write "
                "what happened back into your systems before it hangs up.",
                "Each tool carries its own rule about when to reach for it - "
                "and, just as importantly, when not to.",
            ],
            viz="TOOLS_VIZ",    # substituted by product.py
        ),

        # ---- 3. release control -------------------------------------------
        dict(
            tone="dark",
            eyebrow="NOTHING SHIPS BY ACCIDENT",
            h2="Draft it. Hear it. Then publish it.",
            h2_in_col=True,
            viz="RELEASE_FLOW",
            body=[
                "Changes sit in a draft until somebody publishes them. Before "
                "that you can call the draft and listen to it handle the thing "
                "you are worried about, which is a better test than reading "
                "the brief and hoping.",
                "Staged changes are listed before they go out, and every "
                "version is kept. If a change makes things worse, the previous "
                "one is still there.",
            ],
        ),
    ],

    # ---- the band that answers "do I have to do this?" --------------------
    hands=dict(
        h2="Who actually touches this",
        lede="You are looking at our tool, not your new job. Here is the "
             "honest split.",
        cards=[
            ("You bring the rules",
             "How you want customers spoken to. What must never be promised. "
             "Which calls should always reach a person. You know these; we "
             "don't."),
            ("We do the building",
             "Writing the brief, wiring the tools to your catalogue and your "
             "order system, testing it, and changing it as your range moves."),
            ("You see all of it",
             "Every call transcribed, every tool the agent used, every change "
             "with a date on it. Read-only unless you want otherwise."),
        ],
    ),

    faq_h2="Questions operators actually ask",
    faq=[
        ("Do we have to build the agent ourselves?",
         "No. This is the tool we build it in. You get an account and can read "
         "everything - the brief, the tools, the transcripts - but nobody on "
         "your side has to configure anything. If you would rather make small "
         "edits yourself, you can, and that is a choice rather than a "
         "requirement."),
        ("Can we see exactly what it has been told to say?",
         "Yes, in full, in plain English or Italian. It is a written brief, "
         "not a black box, and every edit to it is dated and kept."),
        ("What happens when it doesn't know the answer?",
         "It says so and passes the call to one of your people, warm, with "
         "what the customer already told it. It is set up to hand over rather "
         "than guess - a wrong answer delivered confidently costs far more "
         "than a transfer."),
        ("Can it do anything, or only talk?",
         "It can look up orders and stock, send a follow-up message, open a "
         "ticket, transfer the call, and push what happened into your systems "
         "through a webhook. What it can reach is decided when we build it."),
        ("Our catalogue changes constantly. Does the agent go stale?",
         "It reads your catalogue rather than a copy of it, so new products "
         "and price changes are there as soon as they are live in your store. "
         "The brief itself we maintain as part of the service."),
        ("How long until it is answering real calls?",
         "Two weeks from the intro call, on your own number, with a real "
         "catalogue behind it."),
    ],

    cta=dict(
        hand="live in two weeks",
        h2="Bring us one call you keep getting.",
        sub="Tell us the call your team is tired of taking, and we will show "
            "you the agent that takes it instead. No slides.",
    ),
)

PRODUCTS = {p["slug"]: p for p in [VOICE_AGENT_BUILDER]}

# Display order for the section, and for the cross-links at the foot of each
# page. Only pages that EXIST belong here - the remaining four are listed in
# HANDOFF.md with two names still unsettled.
ORDER = ["voice-agent-builder"]
