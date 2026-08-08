---
title: "Human Conversation Runs on a 208-Millisecond Clock. Your Voice Agent Doesn't."
seo_title: "How to Measure Voice Agent Latency on Your Own Line | Sabato AI"
slug: measure-your-voice-agent-latency
description: "The human turn-taking gap is +208 ms across 10 languages. No independently verified latency benchmark exists for commercial voice agents - so here is the protocol to measure p50 and p90 on your own line in an afternoon."
category: Operations
date: 2026-08-08
cover_style: offwhite
---

Across 10 languages and 101 natural conversations, the mean gap between one speaker finishing and the next starting is +208 milliseconds, and the single most common gap is zero ([Stivers et al., PNAS, 2009](https://www.pnas.org/doi/full/10.1073/pnas.0903616106)). Almost nobody evaluating a voice agent has put a stopwatch on that gap on their own line.

Operators test two things. Does it understand my part numbers, my accents, my customers. Does it sound like a person. Both fair, both answered inside a five-minute demo.

The gap doesn't get answered, and the gap is what your caller reacts to.

The protocol is at the bottom of this post: p50 and p90, measured from the end of the caller's speech to the start of the agent's speech, on your own network path, with your own customers on the other end. An afternoon.

:::keystat
+208 ms
mean gap between speakers across 10 languages
Source: Stivers et al., PNAS, 2009

0 ms
the single most common gap
Source: Stivers et al., PNAS, 2009
:::

## What is the normal gap between speakers in human conversation?

Across 10 languages, sampling 350 consecutive questions per language from 101 natural conversations, the mean gap between one speaker finishing and the next beginning is +208 ms, with an overall median of +100 ms and an overall modal gap of zero (Stivers et al., PNAS, 2009). Language means ran from +7 ms in Japanese up to roughly +468 ms at the slow end. This is naturalistic conversation, not commercial phone calls.

The number is old. 2009, and I'll flag it before anyone else does.

Here is why it still holds, and the distinction matters more than the date. Stivers et al. is foundational descriptive linguistics, extensively replicated. It is not a market statistic. Market statistics decay because markets move - a 2009 figure on channel preference or contact volumes is worthless today. A measurement of how humans time their turns doesn't decay that way, because the thing measured is the mechanics of human speech, not the behaviour of a market. That's the test I'd apply to any old number before republishing it, and this one passes.

The spread is what makes the finding hard to argue with. Language means ran from +7 ms in Japanese to roughly +468 ms at the other end. Even the slowest language in the study sits under half a second. All ten fall within roughly 250 ms either side of the cross-language mean - a difference the paper describes as approximately the length of time it takes to produce a single English syllable.

So the window isn't a cultural preference you can design around by market. It's close to a constant.

Two limits, stated plainly.

This is naturalistic conversation, recorded between people who know each other, not inbound calls to a supplier about a delivery date. Nobody has measured turn timing on commercial phone calls. Treat +208 ms as the human baseline your caller's ear was trained on, not as a spec for your line.

And the human baseline is measured more generously than the yardstick this post hands you. Stivers et al. coded response onset from video, counting early visual responses - a nod - and audible pre-utterance inbreaths as the response beginning. The protocol below measures speech to speech, because a phone line carries nothing else. So the human number is, if anything, slightly flattered relative to your measurement. Don't read a gap between your p50 and +208 ms as entirely yours.

If a supplier tells you their agent hits the human number, they are quoting a linguistics paper about informal face-to-face conversation, and they should say so.

## Is 400 ms a good target for a voice agent?

ITU-T Recommendation G.114 (2003) sets 150 ms of one-way mouth-to-ear delay as the point below which interactivity is essentially transparent, and states that delays above 400 ms "are unacceptable for general network planning purposes". That budget covers getting audio from one mouth to one ear - network transmission plus the codec and buffering the network itself adds. It carries no speech recognition, no model inference, no database lookup, no synthesis. For a voice agent it is a floor, not a target.

This is the number the industry half-remembers, and it gets quoted at buyers with the word "benchmark" attached to it.

ITU-T Recommendation G.114 (05/2003, still in force) is a network-planning recommendation. It measures one-way mouth-to-ear delay: getting audio from one mouth to one ear, including the codec, packetisation and de-jitter buffering the network itself adds. It carries none of the work a voice agent does. No endpointing wait. No speech recognition. No model inference. No catalogue or ERP lookup. No speech synthesis.

So 400 ms is not a target your agent should aim at - it's the telecoms industry's own threshold for delivering audio and nothing else, a floor sitting underneath your budget. The network has already spent part of your response time before your agent has begun to think.

Our reasoning, not a finding from either source: if delivering the audio alone is unacceptable past 400 ms, then a total mouth-to-ear response that includes endpointing, recognition, inference, a stock lookup and synthesis lands well above the human 208 ms. Not sometimes. Always. Which means the useful question stops being "can we hit the human number" and becomes "where exactly is our time going, and which stage do we attack".

Everyone on page one of Google asserts a threshold - 300 ms, 200-500 ms, pick one. I went looking for the study behind the 300 ms figure. I could not find one: every trail I followed ended at another article asserting the same number, or at nothing at all. That is not proof no such study exists. It is a statement that nobody quoting the number is citing one. Both numbers in this post trace to a primary source, and neither of them is a voice-AI benchmark.

## Why a demo can't show you this

Comprehension and naturalness are the right things to test. They are also the only two things a demo can test, and that's structural, not a conspiracy.

Demos are short and single-turn. Latency compounds across a real fifteen-turn call, and the turn that kills you is turn eleven, not turn one.

Demos run on the supplier's network path, usually from the supplier's country, usually mid-morning on a weekday. Your callers are on a different carrier, in a different country, at 16:50 on a Friday. And demo questions almost never trigger a live stock, price or delivery-date lookup - the exact turns where the number blows out, and the turns that decide whether the call converts.

On a demo call, you fill the silence yourself. You will say "mm" or "right" into a two-second gap without noticing you did it, because you are a polite person on a sales call. A customer who has already been on hold once today does not do that. They say "hello?" and then they talk over the agent.

Naturalness gets assessed in seconds. Latency lives in milliseconds. The format is blind to it.

## Why the latency number you were quoted is not the one your caller hears

Measure latency from the caller's last word, not from the moment your system decides the caller has stopped. Between those two points sits the endpointing wait - the silence threshold a voice agent uses to detect end of turn - and it is often the largest single block of delay. Vendor figures that begin after endpointing can understate the caller's experience by hundreds of milliseconds.

A voice agent does not know the caller has finished talking. It waits for silence to persist long enough to conclude the turn is over. That is endpointing, driven by voice activity detection, and only once it fires does anything else start: recognition, inference, lookup, synthesis.

The caller's clock starts at their last word. Many quoted latency figures start after endpointing fires. The difference between the two is the silence threshold, and it is frequently the biggest single block in the chain. Two systems both quoting "500 ms" can be a second apart from the caller's seat.

:::quote
Does your latency figure start at the caller's last word, or after your endpointing fires?
:::

Not a gotcha, and it shouldn't be delivered as one, because there is a real trade-off underneath it. Shorten the silence threshold to feel faster and you raise false interruptions: the agent talking over a caller who was mid-thought. That failure is worse than the wait, because it forces the caller to repeat themselves and makes the agent sound like it isn't listening.

The evidence that this trade-off is unavoidable comes from turn-taking research, and it needs its flags attached. Across three European corpora, 40.0-41.7% of between-speaker transitions were overlaps rather than clean gaps, and only 0.4-0.7% were clean no-gap-no-overlap handoffs ([Heldner & Edlund, Journal of Phonetics, 2010](https://staff.fnwi.uva.nl/r.fernandezrovira/teaching/cosp/cosp2016/docs/HeldnerEdlund2010.pdf)). Single-source: that percentage rests on this paper alone. It is 2010. Two of the three corpora are task-oriented map dialogues rather than commercial calls, so the load-bearing corpus is the Spoken Dutch Corpus (321 speakers, 234 pairs); the Swedish sub-corpus is only 8 speakers. Stivers et al. corroborates the general picture - modal gap of zero, systematic avoidance of long gaps - but not that percentage.

Read it for what it is. Human speakers overlap each other roughly four times in ten transitions. A system tuned to wait for confident silence is fighting the way people actually talk, and one tuned to jump in early is going to cut people off. There is no threshold setting that wins both. The job is to know which way yours is tuned, and to have chosen it deliberately.

## How to measure your voice agent's latency on your own line

To measure a voice agent's latency: record real calls in stereo, open them in a waveform editor, and for each turn take T1 as the last audio sample of the caller's final word and T2 as the first sample of the agent's reply. Latency is T2 - T1. Log at least 60 turns, split by turn type, and report p50 and p90 separately.

An afternoon. A phone, a free waveform editor, a spreadsheet. No engineer.

### What you need (about 20 minutes to set up)

Call recordings with the audio intact. Your telephony provider's recordings are usually fine - check they are not mixed down to a single mono channel in a way that smears the boundary between caller and agent. Stereo or dual-channel recording makes this far easier: the caller lands on one track, the agent on the other, and you can see the handoff.

A free waveform editor that displays millisecond timestamps. Audacity is the obvious one - set the selection toolbar to hh:mm:ss + milliseconds before you start, or you will be reading seconds to two decimal places and arguing about rounding. And a spreadsheet.

If you can't get clean recordings out of your provider, put a second phone on speaker next to the first and record that. Accurate enough. You are looking for differences of hundreds of milliseconds, not tens.

### Define the two timestamps once, then stop arguing about it

**T1** = the last audio sample of the caller's final word. Not the end of the silence window. Not where the transcript claims the turn ended. The waveform.

**T2** = the first audio sample of the agent's reply. Including filler. If the agent says "let me check that", that is the reply starting - mark it, and note in the log that the turn opened with a holding phrase, because that matters later.

**Latency = T2 - T1.** One turn, one number.

Paste those three lines into your own doc. Every argument about latency you will ever have with a supplier comes down to which definition each side is using.

### How many turns you need before p50 and p90 mean anything

Measure turns, not calls. Ten real calls of six turns each gives you 60 turns.

Be honest about what 60 buys you, because nobody else writing about this is: p50 is reasonably stable at around 30 turns. A p90 on 60 turns is the sixth-slowest turn you happened to record. That is indicative, not a metric. For a p90 you would put in front of a supplier and defend, aim for 100+ turns.

Use the mean for nothing. The whole point of this exercise is the tail.

### Split the turns into four types before you average anything

A single blended number hides the failure. Log every turn as one of:

* **acknowledgement** - confirmations, yes/no, "got it"
* **retrieval** - anything needing a live lookup: stock, price, order status, delivery date, fitment or compatibility ([order-status and returns lookups](/blog/reduce-bracketing-returns) are the same turn type)
* **post-long-utterance** - the caller talked for 15+ seconds before stopping
* **post-interruption** - the caller cut the agent off

Retrieval turns are where the number blows out, and they are disproportionately the ones that decide whether the call converts. Report p50 and p90 per type.

### Measure on the path your customers actually use

Not the supplier's demo line. Not office wifi at 08:30 on a Tuesday.

From a phone on the network your customers are on, in the country they call from, at the hour they call. Run one batch at your genuine peak - the hour your call volume is highest - and one off-peak, and compare.

If you serve more than one country, run the batch separately per market and per language - [run it per language](/blog/multilingual-phone-support-eu-expansion). The carrier is different, the path is different, and the model handling the language is different. One blended European number tells you nothing about the Danish line.

### The output: one small table

| Turn type | n | p50 | p90 | Slowest turn | What happened on the slowest turn |
| --- | --- | --- | --- | --- | --- |
| acknowledgement | 22 | 610 ms | 940 ms | 1.1 s | caller trailed off mid-word, endpointer held |
| retrieval | 19 | 1,450 ms | 3,900 ms | 5.2 s | stock check on a part number, two lookups chained |
| post-long-utterance | 11 | 780 ms | 1,600 ms | 1.9 s | 40-second fault description |
| post-interruption | 8 | 1,900 ms | 3,100 ms | 3.4 s | caller cut in, agent restarted its sentence |
| all turns | 60 | 900 ms | 3,200 ms | 5.2 s | - |

Illustrative format only. The numbers above are invented to show the shape of the table, not measured results.

The last column is where the diagnosis lives. Everything else is bookkeeping.

## What your p50 and p90 are telling you

Read the table as if/then, not as a score.

**p50 acceptable, p90 several times higher, and the slow turns are all retrieval** - not a speech problem. A data-access problem. The fix sits in your catalogue or ERP path, and changing supplier does not touch it. People switch platforms over this and get the same p90 back.

**Every turn type uniformly slow** - architecture or network path. Ask where the components are hosted relative to your callers, and whether the answer is "a US region".

**p90 only degrades at peak hour** - capacity. It is degrading exactly when the calls are worth the most.

**Post-interruption turns are the worst by a distance** - endpointing and barge-in handling. See the section above, and ask the verbatim question.

Then the part that gives you a second lever.

Humans don't hit +208 ms on hard questions either. They hold the floor. "Let me check that for you." "One second." An audible keyboard. The gap stays short even when the answer is slow, because what breaks a conversation is the silence, not the wait. This is our reasoning built on the Stivers finding, not a finding in itself - the paper measures gaps between turns, it does not test floor-holding on commercial calls.

But it changes what you do with a retrieval turn you cannot make fast. The fix is often not more speed. It is getting the agent to say something inside the human window and then take the four seconds it needs. That is a prompt change and a day of work, against a re-architecture of your stock integration.

Two levers. One of them is cheap.

:::takeaway
The human baseline is +208 ms and your agent will not hit it. Stop shopping for a benchmark that doesn't exist and measure your own p50 and p90, split by turn type.
Ask every supplier one question: does your latency figure start at the caller's last word, or after endpointing fires?
Where a retrieval turn can't be made fast, make the agent speak inside the human window and then take its time. A prompt change beats re-architecting your stock integration.
:::

## What this protocol won't tell you

Nothing about whether the answer was correct. A fast wrong answer about stock or fitment costs you more than a slow right one, and latency and accuracy trade against each other at several points in the chain - shorter endpointing windows clip words, smaller models answer sooner and worse. Measure both or you will optimise yourself into a confident, rapid liar.

It does not give you a conversion threshold, and I want to be exact about why. No dataset was found linking measured voice-agent latency to call abandonment or conversion on European commercial calls. Not a European one, not an American one. If you have one, send it and I'll publish it.

So the number to beat is your own baseline, re-measured after every change.

We run this protocol on our own lines at Sabato. The reason it's written down at all is that we had to build it for ourselves before we could argue with anyone about latency, including with ourselves.

:::action
What to do this week
Record ten real calls on the network and at the hour your customers actually use. Not the demo line, not office wifi on a Tuesday morning.
Mark T1 and T2 in a waveform editor for 60 turns, tagging each as acknowledgement, retrieval, post-long-utterance or post-interruption.
Report p50 and p90 per turn type, and write down what happened on the single slowest turn. That sentence is the diagnosis.
Ask your supplier whether their quoted figure starts at the caller's last word or after endpointing fires, and write the answer down.
Re-run it after every model, prompt, telephony or catalogue change, and at minimum once a quarter.
:::

What you now own, including the part nobody budgets for: this is not a one-off. An hour of waveform-scrubbing per quarter, forever. That is the actual cost, and it is still cheaper than finding out from a customer.

## FAQ

**What is a good latency for an AI voice agent?** There is no independently verified benchmark for commercial phone calls. The two defensible anchors are the human conversational norm - a +208 ms mean gap across 10 languages (Stivers et al., PNAS, 2009) - and ITU-T G.114's 400 ms ceiling on one-way mouth-to-ear delay, which covers delivering the audio only. Measure your own p50 and p90 and improve against that baseline.

**How do you measure voice agent response latency?** Record calls in stereo, open them in a waveform editor, and per turn measure from the last audio sample of the caller's final word to the first sample of the agent's reply. Log 60 turns minimum, split into acknowledgement, retrieval, post-long-utterance and post-interruption, then report p50 and p90 for each type separately.

**Is 400 ms the standard for voice AI latency?** No. The 400 ms figure comes from ITU-T Recommendation G.114 (2003) and describes one-way mouth-to-ear delay for network planning - transmission plus the codec and buffering the network adds. It excludes endpointing, speech recognition, model inference, database lookups and speech synthesis. For a voice agent it is a floor beneath the total response time, not a performance target.

**Why does my voice agent feel slow when the vendor quoted a low number?** Most likely the measurement windows differ. Many quoted figures start after endpointing - the moment the system decides the caller has stopped talking. The caller's experience starts at their last word. The silence threshold between those two points is often the largest single block of delay in the chain.

**Is a faster voice agent always better?** No. Reducing the endpointing threshold to shorten the gap increases false interruptions, where the agent talks over a caller mid-thought and forces them to repeat themselves. Human conversation overlaps constantly - 40.0-41.7% of transitions across three European corpora were overlaps (Heldner & Edlund, 2010, single-source). Both failures cost calls.

**Does the +208 ms figure apply to phone calls?** Not directly. Stivers et al. measured naturalistic face-to-face and recorded conversation between people who know each other, and counted nods and audible inbreaths as a response beginning. Nobody has published equivalent timing for commercial inbound calls. Treat it as the baseline your caller's ear was trained on, not as a specification for your line.

## Sources

* Stivers, T. et al., *Universals and cultural variation in turn-taking in conversation*, Proceedings of the National Academy of Sciences, 2009 - [pnas.org](https://www.pnas.org/doi/full/10.1073/pnas.0903616106)
* ITU-T Recommendation G.114 (05/2003), *One-way transmission time* - [itu.int](https://www.itu.int/rec/T-REC-G.114-200305-I/en)
* Heldner, M. & Edlund, J., *Pauses, gaps and overlaps in conversations*, Journal of Phonetics, 2010 - [staff.fnwi.uva.nl](https://staff.fnwi.uva.nl/r.fernandezrovira/teaching/cosp/cosp2016/docs/HeldnerEdlund2010.pdf)
