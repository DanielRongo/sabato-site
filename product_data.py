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

    # The statement + two half-width panels that follow the anchor shot.
    pair=dict(
        eyebrow="THE TOOLS",
        h2="It does things.[br]It doesn't just say things.",
        lede="A chatbot with a phone number can only talk. An agent with tools "
             "reads the actual order out of your system while the customer is "
             "still on the line - status, carrier, the date you promised - and "
             "writes back what happened before it hangs up.",
    ),

    # The two chapters below share one dark band and one title.
    group=dict(
        eyebrow="UNDER THE HOOD",
        h2="How it is built,[br]and how it changes.",
    ),

    blocks=[
        # ---- 1. the brief ------------------------------------------------
        dict(
            eyebrow="01 · THE BRIEF",
            viz="BRIEF_VIZ",
            h2_in_col=True,
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


        # ---- 3. release control -------------------------------------------
        dict(
            eyebrow="02 · NOTHING SHIPS BY ACCIDENT",
            h2="Draft it. Hear it. Then publish it.",
            h2_in_col=True,
            flip=True,
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

    # ---- the managed-service process ---------------------------------------
    # Not a feature list: the sequence a customer actually goes through, with
    # the one step that is theirs marked out. Three of the four are ours, and
    # that ratio IS the argument - do not "balance" it.
    hands=dict(
        eyebrow="FULLY MANAGED",
        h2="All we need from you[br]is what you already know.",
        lede="Four steps from the first conversation to an agent answering real "
             "calls. Three of them are ours. You never have to open the tool.",
        step_word="STEP",
        steps=[
            ("talk", "You tell us how it should go",
             "One session. How you want customers spoken to, what must never be "
             "promised, and the answers that only exist in your team's heads.",
             True),
            ("build", "We build the whole thing",
             "The instructions, the tools, the connection to your catalogue and "
             "your order system. Nothing lands on your engineers, because there "
             "is nothing for them to do.", False),
            ("hear", "You hear it before anyone else",
             "We call you with the draft and you listen to it handle your "
             "awkward cases. It does not go live until you say it can.", False),
            ("run", "We run it and keep it current",
             "New products, new prices, new edge cases. It stays right as your "
             "catalogue moves - and every call is transcribed for you to read.",
             False),
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
         "Yes, in full, and in whatever language the agent works in - we "
         "are not limited to any particular set. It is a written brief, "
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


# ---------------------------------------------------------------------------
# 2. WORKFLOW BUILDER
#
# The clean line between this page and the Voice Agent Builder: that one is
# what the agent does WHILE the customer is on the phone. This one is what
# happens AFTER they hang up. Keep that split - it is the reason two pages
# exist rather than one long one, and it is also the honest description of the
# product's two canvases.
# ---------------------------------------------------------------------------
WORKFLOW_BUILDER = dict(
    slug="workflow-builder",
    it="workflow-builder",
    chip="Workflow Builder",

    title="Workflow Builder | Sabato AI",
    description="What happens after the customer hangs up: the call is read, "
                "the facts are pulled out, and your systems are updated. Nobody "
                "types anything. Live in two weeks.",

    # 14 and 17 characters.
    h1="The call ends.[br]The work starts.",
    sub="Most phone systems stop when the line goes dead. That is the moment "
        "the actual work begins - the note, the message, the ticket, the field "
        "somebody has to update. The Workflow Builder is where that work stops "
        "being anybody's job.",

    hero_visual="",

    shot=dict(
        src="/product/assets/workflow-builder",
        alt="The Sabato post-call workflow canvas: a Call Ended trigger "
            "branching into reading the call, checking consent, sending a "
            "WhatsApp summary, writing to a CRM and raising an issue.",
        caption="One store's post-call workflow. Everything on this canvas "
                "runs in the seconds after the customer hangs up.",
    ),

    pair_kind="workflow",
    pair=dict(
        eyebrow="AFTER THE CALL",
        h2="Nobody types this up.[br]It is already done.",
        lede="The agent hands the call to a workflow the moment it ends. The "
             "call gets read, the conditions get checked, and every system that "
             "should know about it is told - before your team would have "
             "finished writing the first note.",
    ),

    group=dict(
        eyebrow="HOW A WORKFLOW IS PUT TOGETHER",
        h2="Read the call.[br]Then act on it.",
    ),

    blocks=[
        dict(
            eyebrow="01 · WHAT IT READS",
            h2="A summary is useless.[br]Labels are not.",
            h2_in_col=True,
            viz="LABELS_VIZ",
            body=[
                "A paragraph of \u201chere is what happened on the call\u201d "
                "cannot be filtered, counted or acted on. So every conversation "
                "gets labelled instead: the product category, what they "
                "actually asked for, whether they have bought before, what "
                "they are worth, which country they are calling from.",
                "Those labels are what everything downstream branches on - and "
                "they are what lets you ask, at the end of the month, which "
                "category generated the most calls and which of them sold.",
            ],
        ),
        dict(
            eyebrow="02 · WHAT IT DOES",
            h2="Different calls deserve different endings.",
            h2_in_col=True,
            flip=True,
            viz="BRANCH_VIZ",
            body=[
                "A good call and a bad one should not produce the same "
                "aftermath. The labels decide. A VIP asking about a bulk order "
                "gets the account manager texted before they have put the phone "
                "down; an escalation gets summarised to the Head of Support "
                "with the transcript attached; the ticket and the CRM are "
                "updated either way.",
                "Adding a branch is a change like any other - it sits in draft, "
                "you can test it against a real call, and it goes live when you "
                "publish.",
            ],
        ),
    ],

    hands=dict(
        eyebrow="FULLY MANAGED",
        h2="You describe the outcome.[br]We wire it up.",
        lede="Four steps from the first conversation to a workflow running "
             "after every call. Three of them are ours. You never have to open "
             "the tool.",
        step_word="STEP",
        steps=[
            ("talk", "You say what should happen",
             "What your team does after a call today, and which of it should "
             "stop being a person's job. That list is the whole brief.", True),
            ("build", "We wire it to your systems",
             "Your CRM, your helpdesk, your messaging, your order system. "
             "Through whatever they expose - an API, a webhook, an export. No "
             "work for your engineers.", False),
            ("hear", "You test it on a real call",
             "We run the workflow against a call that already happened and show "
             "you exactly what it wrote and where. Nothing runs live until you "
             "publish it.", False),
            ("run", "It runs on every call after that",
             "Silently, in seconds, and every run is logged - so when something "
             "looks wrong you can see which step did it.", False),
        ],
    ),

    faq_h2="Questions operators actually ask",
    faq=[
        ("What can it actually connect to?",
         "Anything with an API or a webhook - and that is most things: Shopify, "
         "your helpdesk, your CRM, WhatsApp, a Google Sheet if that is genuinely "
         "where the work lives. If a system has no API we will tell you rather "
         "than pretend."),
        ("What if the workflow does the wrong thing?",
         "Every run is logged step by step, so you can see what fired and what "
         "it wrote. Changes go through the same draft-test-publish path as the "
         "agent itself, so a bad change is caught before it reaches a customer "
         "rather than after."),
        ("Can it decide differently depending on the call?",
         "That is the point of it. Conditions read the fields pulled out of the "
         "conversation - what they asked for, how it ended, whether they "
         "consented, what they are worth - and each branch does something "
         "different."),
        ("Do we have to build these ourselves?",
         "No. You tell us what should happen after a call and we build it. You "
         "get an account and can watch every run, but there is nothing you have "
         "to configure."),
        ("How fast does it run?",
         "Seconds after the call ends. A customer who agreed to a summary "
         "usually has it before they have put the phone down properly."),
        ("What happens to the recording and the transcript?",
         "Both are kept against the conversation and available to you. "
         "Retention is set to whatever your policy says, not ours."),
    ],

    cta=dict(
        hand="live in two weeks",
        h2="What does your team do after a call?",
        sub="Whatever the answer is, it is probably a list. Send it to us and "
            "we will tell you which parts stop being anyone's job.",
    ),
)


# ---------------------------------------------------------------------------
# 3. CALL DATA INTELLIGENCE
#
# The angle: your phone line is the only place a customer tells you, in their
# own words, what they wanted and could not find. Search logs show what they
# typed; calls show what they meant. That is the whole page.
# ---------------------------------------------------------------------------
CALL_DATA_INTELLIGENCE = dict(
    slug="call-data-intelligence",
    it="call-data-intelligence",
    chip="Call Data Intelligence",
    pair_kind="insight",

    title="Call Data Intelligence | Sabato AI",
    description="Every call read, labelled and counted. See which questions keep "
                "coming, which products confuse people, and what your catalogue "
                "is missing. Live in two weeks.",

    # 14 and 18 characters.
    h1="Your customers[br]already told you.",
    sub="Your search bar shows you what people typed. Your phone line shows you "
        "what they meant - and it is the only place they say it in full "
        "sentences. Call Data Intelligence is where a thousand of those "
        "conversations become something you can act on.",

    hero_visual="",

    shot=dict(
        src="/product/assets/call-data-intelligence",
        alt="The Sabato conversations view: label filters across the top, a row "
            "of headline numbers, and a ranked list of what customers rang "
            "about, with the individual calls behind it.",
        caption="Filtered to one category and one customer tier. The ranking is "
                "what those 412 callers actually asked for.",
    ),

    pair=dict(
        eyebrow="WHAT IT LOOKS LIKE",
        h2="Every call, counted.[br]Every count, checkable.",
        lede="Filter by category, by what they asked for, by whether they have "
             "bought before, by country. The ranking updates. And any number in "
             "it opens into the calls it came from, so nobody has to take your "
             "word for it.",
    ),

    group=dict(
        eyebrow="WHAT THE PHONE KNOWS",
        h2="Ask it anything.[br]It has been listening.",
    ),

    blocks=[
        dict(
            eyebrow="01 · THE QUESTIONS",
            h2="You never needed a research panel.",
            h2_in_col=True,
            viz="QUESTIONS_VIZ",
            body=[
                "Companies pay agencies to run panels that ask customers what "
                "confuses them. You have hundreds of customers a month "
                "volunteering it down a phone line, unprompted, in their own "
                "words - and until now none of it was written down anywhere you "
                "could count.",
                "Now it is. Not as a pile of recordings nobody opens, but as "
                "labels you can filter and totals you can sort.",
            ],
        ),
        dict(
            eyebrow="02 · WHAT YOU DO WITH IT",
            h2="A number nobody acts on is trivia.",
            h2_in_col=True,
            flip=True,
            viz="ACTIONS_VIZ",
            body=[
                "One hundred and thirty-four people ringing to ask which unit "
                "fits their room is not an interesting statistic. It is a "
                "missing paragraph on a product page, a size that keeps selling "
                "out, and a question your agent should be handling before "
                "anyone picks up.",
                "The point of measuring the phone is not the dashboard. It is "
                "the four or five changes a month that come out of it.",
            ],
        ),
    ],

    hands=dict(
        eyebrow="FULLY MANAGED",
        h2="No analyst.[br]No export. No waiting.",
        lede="Four steps from the first conversation to numbers you trust. "
             "Three of them are ours. You never have to open the tool.",
        step_word="STEP",
        steps=[
            ("talk", "You say what you want to know",
             "The questions you would ask if somebody were transcribing every "
             "call by hand. Those become the labels.", True),
            ("build", "We set the labels up",
             "Categories that match your catalogue, tiers that match your "
             "customers, whatever else you need counted. Not a generic taxonomy "
             "bolted onto your business.", False),
            ("hear", "You check them against real calls",
             "We show you the labels against calls that already happened, so "
             "you can see they are right before anyone reports on them.", False),
            ("run", "Then it counts everything, forever",
             "Every call from that day on, labelled the same way, so the month "
             "to month comparison actually means something.", False),
        ],
    ),

    faq_h2="Questions operators actually ask",
    faq=[
        ("Is this just call recording with a search box?",
         "No. Recordings are a haystack - a hundred hours nobody will ever "
         "listen to. This reads every call into labels you can filter and count, "
         "then lets you open the calls behind any number. The recording is the "
         "evidence, not the product."),
        ("Do you analyse how the customer sounded?",
         "No, and deliberately. Inferring somebody's emotional state is "
         "contested ground under the EU AI Act and we would rather not build on "
         "it. Everything we label is a fact about the call - what was asked, "
         "what category it was, whether it was resolved."),
        ("Can we get the data out?",
         "Yes. Export it, or have it pushed into your warehouse or your "
         "reporting stack through a webhook. It is your data about your "
         "customers; holding it hostage would be a strange way to earn a "
         "renewal."),
        ("How far back does it go?",
         "From the day the agent goes live. There is no way to label calls that "
         "were never recorded, so the sooner it starts the sooner a month-on-"
         "month comparison exists."),
        ("Who can see the transcripts?",
         "Whoever you say. Access is per person, and you can keep the "
         "transcripts open to a manager while the raw recordings stay closed."),
        ("Does this work if we still answer most calls ourselves?",
         "Yes - the agent labels what it handles, and calls transferred to your "
         "team are labelled too, up to the point of transfer. You do not have to "
         "automate everything to measure everything."),
    ],

    cta=dict(
        hand="live in two weeks",
        h2="What is the question you cannot answer?",
        sub="Most operators have one - why people abandon, what they ask before "
            "buying, which product confuses everyone. It is probably already on "
            "your phone line.",
    ),
)

PRODUCTS = {p["slug"]: p for p in [VOICE_AGENT_BUILDER, WORKFLOW_BUILDER,
                                   CALL_DATA_INTELLIGENCE]}

ORDER = ["voice-agent-builder", "workflow-builder", "call-data-intelligence"]
