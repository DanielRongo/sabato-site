---
title: "The twenty calls: what to test before a voice agent answers a real customer"
seo_title: "Voice Agent Acceptance Test: The 20 Calls | Sabato AI"
slug: voice-agent-acceptance-test
description: "Twenty phone calls that turn a feeling into a number. Most of them test failing well rather than working - which is the half a demo never shows you."
category: Voice AI DIY
date: 2026-08-11
cover_style: black
---

*The Build File, issue 00. A season on running a voice build without being an engineer.*

There is a moment near the end of every voice project where somebody asks whether it's ready,
and nobody in the room has an answer that isn't a feeling.

The demos went well. The team is tired and would like to ship. The person who has to decide has
no way to check, because everything he's been shown was chosen by the people showing it.

So here is the checklist I'd want in that room. Twenty calls. Make them, score them, and the
feeling turns into a number.

One thing to notice before you start: almost every one of these is a test of failing well, not of
working. Teams test whether the agent can do the job. Nobody tests what happens when the caller
mumbles, changes his mind, gets angry, or asks something the agent has no business answering.
That's where the whole risk lives, and it's the half that never makes it into a demo.

---

## How to run it

**Actually phone the number.** Not a test harness, not a web widget. The phone line is the
product. Half of these failures only appear over a real carrier.

**Use people who aren't on the project.** Anyone who built it will unconsciously speak clearly,
wait politely, and ask the questions it can answer. Borrow people from the warehouse and from
sales. Ideally one person who is genuinely impatient.

**Score binary.** Pass or fail, no partial credit, no "well, it nearly did." An agent that nearly
handles an interruption doesn't.

**Record everything and listen back.** The person on the call is concentrating on talking and
will miss half of it.

Two hours, two people, one afternoon. That's the whole cost.

---

## Group one: does it behave like a conversation

**1. The interrupter.** Start talking over it, mid-sentence, halfway through its longest answer.
*Pass: it stops within about a beat and listens. Fail: it finishes its sentence while you're
speaking.*

**2. The silence.** Say nothing for six seconds after it asks you something.
*Pass: one calm prompt, then it waits again. Fail: nervous filler, repeating itself, or hanging
up on a customer who was reading his order number off a box.*

**3. The correction.** Give it a number, let it confirm, then say "no, sorry, it's actually…".
*Pass: the correction wins everywhere, including in whatever record gets written at the end.
Fail: the first value survives somewhere downstream and nobody notices for a week.*

**4. The multi-intent.** "I want to check my order, ask about the warranty, and change my
delivery address." All in one breath.
*Pass: all three handled, or two of them explicitly parked and returned to. Fail: it answers the
last one and the other two evaporate.*

**5. The mid-transaction hang-up.** Give it half the details, then drop the call.
*Pass: clean state, nothing half-written, and a follow-up someone can pick up. Fail: a ghost
order, or a record that exists but is missing the parts that matter.*

---

## Group two: does it cope with real people on real lines

**6. The bad line.** Call from a moving car, a lift, or a basement. Somewhere with genuinely poor
signal.
*Pass: it asks you to repeat rather than guessing. Fail: it invents a plausible sentence out of
half-heard words and proceeds confidently.*

**7. The background.** Call from the warehouse. Or a showroom with music. Or a street.
*Pass: still gets the essentials. Fail: everything after the noise starts is wrong.*

**8. The accent.** Not a colleague reading a script. Somebody from Napoli, from Bari, from
Bergamo. Glasgow, Marseille, Andalusia — whichever markets you actually sell into.
*Pass: comparable to how it handles a neutral speaker. Fail: it works for the people who built it
and not for the people who buy from you.*

**9. The code-switch.** Speak your local language and drop English product names into the middle
of sentences, the way every customer in this industry actually talks.
*Pass: the product name survives. Fail: the model name comes out as something that doesn't exist
in your catalogue.*

**10. The alphanumeric.** Read an order reference, a VAT number and a postcode aloud, once, at
normal speed.
*Pass: right the first time, or a confirmation that doesn't feel like being interrogated. Fail:
three attempts and the caller reaching for the keypad.*

**11. The spelling.** Spell a surname letter by letter. Use one with near neighbours — Rossi,
Rosso, Russo.
*Pass: it gets it, and it knows when to ask. Fail: silent substitution, which is worse than
asking.*

---

## Group three: does it tell the truth

This group matters more than the other three put together. A slow agent annoys people. A
confident, fluent, wrong agent costs you money and reputation, and it does it in a voice that
sounds like your company.

**12. The wrong premise.** Ask about a product you don't sell, or a policy that doesn't exist.
"What's your price match on this?" when you don't do price matching.
*Pass: says so plainly. Fail: invents a policy, which it will do beautifully.*

**13. The stale record.** Set it up so the system says in stock and it isn't, or the tracking is
out of date.
*Pass: the agent commits to nothing it can't verify, and says where the information comes from.
Fail: a statement you now have to walk back.*

**14. The commitment trap.** Push it. "So you guarantee it arrives Friday?" Then push again.
*Pass: bounded language that survives being repeated back to you. Fail: a sentence your lawyer
would have liked to see first.*

**15. The price probe.** "Can you do better on that price?" Then: "the other place does it
cheaper."
*Pass: a defined boundary, held under pressure. Fail: improvisation, in either direction —
inventing a discount, or being rude about it.*

---

## Group four: does it know its limits

**16. The fitment question.** Ask something that needs reasoning across the catalogue, not a
lookup. "Will this fit my model X?" "Is this compatible with what I bought last year?"
*Pass: a correct answer, or a clean admission it can't be sure and a route to someone who can.
Fail: a confident guess.* This is where the commercial value of pre-sales voice sits, and it's
where most builds stop without anyone deciding to stop.

**17. The angry caller.** Be genuinely annoyed. Interrupt. Raise your voice. Say this is the
third time you've called.
*Pass: it escalates. Fail: it stays cheerful and keeps trying to help, which is the most
infuriating possible response and the default behaviour of almost every agent I've heard.*

**18. The handoff.** Get transferred to a person, and listen to what the person says first.
*Pass: they open already knowing what the call is about. Fail: "so, tell me what this is
regarding" — the most expensive sentence in customer service, because it undoes everything the
agent just achieved and tells the customer the last four minutes were wasted.*

**19. The out-of-hours case.** Run the same escalation at 9pm on a Saturday, when there is nobody
to transfer to.
*Pass: a fallback the caller actually accepts, with a commitment the business can keep. Fail: a
loop, or a promise of a callback that nothing in your system will generate.*

**20. The repeat caller.** Call twice in an hour about the same thing.
*Pass: it knows, and doesn't make you start again. Fail: a stranger, every time.*

---

## Reading the results

The score is the least interesting output. What matters is the shape of the failures, because
each group points at a different part of the system.

| Failures cluster in | The weak part is | Which means |
|---|---|---|
| Group one (1–5) | Timing and turn-taking | Nobody owns the pause. Usually nobody has been asked to. |
| Group two (6–11) | Speech recognition, and what it was tuned on | It was tested on the team, not on your customers |
| Group three (12–15) | The data underneath, and what the agent may promise | The most expensive category, and the least visible |
| Group four (16–20) | Escalation design and what the agent knows about itself | Someone treated the human handoff as an afterthought |

That mapping is the five parts of a voice agent from the other end. If the pattern here doesn't
mean much yet, what a voice agent is actually made of
<!-- FORWARD LINK - issue 01. On the day /blog/what-a-voice-agent-is-made-of publishes, restore:
     [what a voice agent is actually made of](/blog/what-a-voice-agent-is-made-of) -->
walks through the same five layers in plain language.

A first run at twelve or thirteen out of twenty is normal and not a disaster. A first run where
group three is clean and group one is a mess is a project with a fixable problem. A first run
where group three is a mess is a project that should not be taking customer calls yet, whatever
the timeline says.

---

## The part everyone skips

Run it again every month.

Models change underneath you. Someone edits the instructions. A supplier's data format shifts. A
new product category arrives that nobody thought to test. None of these announce themselves, and
all of them are invisible until a customer finds them for you.

An agent that passed in March and was never re-tested isn't a system. It's a memory.

Twenty calls, once a month, by someone who isn't attached to the outcome. It's the cheapest line
in the whole operation and it's the first one to quietly disappear from the calendar.

This is also the only honest way to read the numbers on your dashboard, because a monthly score
against a fixed test is the one measurement that can't drift while looking healthy — which is
more than can be said for the metrics most voice agents report.
<!-- FORWARD LINK - issue 09. On the day /blog/voice-agent-metrics publishes, restore:
     [the metrics most voice agents report](/blog/voice-agent-metrics) -->

---

Take this and use it. Run it against a build your own team is doing, or against something a
supplier is showing you, or against the agent you already have in production and have never
tested this way. It works the same in all three cases, which is rather the point.

*Next: what a voice agent is actually made of — the five parts, and the one that isn't a part at
all.*
<!-- FORWARD LINK - issue 01. On publish, restore:
     *Next: [what a voice agent is actually made of](/blog/what-a-voice-agent-is-made-of) - the
     five parts, and the one that isn't a part at all.* -->
