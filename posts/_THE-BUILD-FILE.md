# The Build File - slug map and internal linking rules

Daniel's spec, 11 Aug 2026. **This is the record. The map lives here and nowhere
else.** Anything that contradicts this file is wrong, including a slug already
sitting in `posts/en/`.

Notes marked `[BUILD]` are added by the site build, not by Daniel - they are
where this repo's machinery touches the plan. They do not change the plan.

---

## 1. The slug map (fix this before anything else ships)

~~Season hub: `/blog/the-build-file`~~ **KILLED 11 Aug by Daniel - do not build it.**
The series has no hub page. Everything below that assumed one has been amended
in place; the original wording is kept where it still applies.

| #  | Post                              | Slug                                    |
|----|-----------------------------------|-----------------------------------------|
| 00 | The 20 calls                      | `/blog/voice-agent-acceptance-test`     |
| 01 | What a voice agent is made of     | `/blog/what-a-voice-agent-is-made-of`   |
| 02 | Your prototype works              | `/blog/voice-ai-prototype-to-production`|
| 03 | What it costs to run              | `/blog/voice-agent-cost-to-run`         |
| 04 | When you should build it yourself | `/blog/build-vs-buy-voice-ai`           |
| 05 | Pull 200 calls first              | `/blog/scoping-a-voice-agent`           |
| 06 | The data underneath               | `/blog/voice-agent-erp-data`            |
| 07 | Europe is not one market          | `/blog/voice-ai-europe-markets`         |
| 08 | Deflection is not resolution      | `/blog/deflection-containment-resolution`|
| 09 | Four numbers                      | `/blog/voice-agent-metrics`             |
| 10 | Three things we rebuilt           | `/blog/three-things-we-rebuilt`         |

**No issue numbers in slugs.** `/blog/build-file-issue-03` carries no search
meaning and it locks the publishing order - the moment you want to move an issue
you either break the URL or live with a number that lies. The number belongs in
the page, never in the address.

`[BUILD]` The `/blog/` prefix already matches this repo: `publish.py` writes
`posts/en/<slug>.md` to `site/blog/<slug>.html`. No find-and-replace needed.

`[BUILD]` No collisions. The six existing posts are `reduce-bracketing-returns`,
`multilingual-phone-support-eu-expansion`, `why-customers-call-instead-of-ordering-online`,
`should-you-remove-the-phone-number`, `what-a-conversation-actually-costs`,
`measure-your-voice-agent-latency`. None of the eleven slugs above touches them.

`[BUILD]` SUPERSEDED - the hub was killed on 11 Aug. Original note: the season hub is NOT a post. `publish.py` only renders what is in
`posts/en/` and `posts/it/`, so `/blog/the-build-file` needs either its own
generator or to be authored as a post-shaped page. Decide before issue 01,
because both fixed links point at it.

---

## 2. The shape: hub and spokes, not a chain

A chain - 01 links to 02 links to 03 - is what most series do, and it is the
weakest structure. Break one link and the reader is out. It also concentrates
all authority on the last post nobody reads.

```
                    /the-build-file          <- season index page
                     (links to all 11)
                            |
            +---------------+---------------+
            |               |               |
    voice-agent-       what-a-voice-     build-vs-buy-
    acceptance-test    agent-is-made-of   voice-ai        ... etc
            ^               |               |
            |               |               |
            +---------------+---------------+
             every post links back to 00 and to the hub
             plus 2-4 lateral links to siblings
```

Issue 00 is the second hub. It is the asset people link to from outside, so
pointing every post at it concentrates authority where you want it.

The dense cluster is also the point for AI answers. A tightly interlinked set of
pages on one narrow subject reads as a corpus rather than eleven loose articles,
and corpora are what get cited when someone asks a model how to run a voice
build in Europe.

---

## 3. The rules per post

**One fixed link, every time:**

1. ~~Back to the season hub.~~ There is no hub. Removed 11 Aug.
2. To issue 00, the acceptance test - because every issue eventually says "and
   then test it."

`[BUILD]` With the hub gone, issue 00 is the ONLY hub, and the standfirst of
every issue carries the series name as plain text rather than a link. This makes
the fixed link to 00 more load-bearing, not less - it is now the single thing
holding the eleven posts together as a cluster, and the category page is the
only other place they all appear.

**Two to four lateral links, chosen by reader question, not by quota.** Place a
link where the reader has just formed a question, not where a keyword happens to
appear. If a sentence raises "but what does that cost?", that is where 03 goes.

**Anchor text carries the term, never the mechanic.** Write *the twenty calls
any agent should survive*, not *click here* and not *read more*. The anchor is
what tells a search engine and a model what the destination is about, and it is
free positioning.

**Three to five links per post total.** More than that and readers stop treating
any of them as a recommendation.

**Forward links are allowed.** Once the slug map is fixed, issue 01 can link to
issue 06 before 06 exists. Two ways to keep that honest:

- Publish 00 and 01 first, so the two fixed links always resolve.
- Keep forward links in the draft but commented out, and switch them on at
  publish. One line in a checklist.

Either works. The mistake is not writing them at all and promising to come back
later, because nobody comes back later.

`[BUILD] THE SECOND OPTION IS NOT OPTIONAL HERE.` `tools/audit_links.py` runs
inside `tools/verify.sh` and fails the deploy gate on any internal link whose
target does not exist - `BROKEN TARGETS (fail)`. A live forward link to an
unpublished issue therefore blocks the whole site from shipping, not just that
post. So: write forward links, keep them commented in the markdown, uncomment on
the day the target publishes. The gate enforces the discipline for free - there
is no way to forget, because forgetting means nothing ships.

---

## 4. The link plan

Reading down: which lateral links each post carries, beyond the fixed hub + 00.

| Post | Links out to | Placed at                                         |
|------|--------------|---------------------------------------------------|
| 00   | 01, 09       | the diagnostic table; the re-run rule             |
| 01   | 00, 06, 02   | the memory section; the timing section            |
| 02   | 00, 05, 03   | the "what a demo omits" list; the cost sentence   |
| 03   | 04, 07       | the score; the per-language line                  |
| 04   | 03, 01, 00   | the volume question; the capability questions     |
| 05   | 06, 08       | the intent tagging; the escalation intents        |
| 06   | 01, 00       | the two-questions section; the failure modes      |
| 07   | 03, 06       | the language economics; the data availability     |
| 08   | 09, 00       | the metric definitions; the handoff test          |
| 09   | 00, 08       | the monthly regression; the banned metrics        |
| 10   | 00, 02       | wherever the rebuild maps to a scenario           |

Every post also earns inbound links, which is the half people forget. 00 and 01
should end up with the most.

---

## 5. Retrofitting

When a new issue publishes, go back and add one link to it from the two most
related existing posts. Five minutes each time. Over a season that turns eleven
posts into a genuine cluster rather than eleven pages that each happen to
mention the others once.

Keep this file as the record. It is the only place the map lives.

---

## `[BUILD]` Standing rules

**EVERY ISSUE SHIPS IN BOTH LANGUAGES. Daniel, 11 Aug: "blogs always must be
published in both languages."** Not a per-issue decision, not a nice-to-have. An
English-only issue is an unfinished issue.

What that means mechanically:

- `posts/en/<slug>.md` AND `posts/it/<slug>.md`, the SAME slug in both. The
  slug is the pairing key: `publish.py` matches siblings on it, and only then
  emits the reciprocal hreflang tags and the "Leggi in italiano" / "Read in
  English" switch. Different slugs means two orphans.
- The forward-link comments must be mirrored in the Italian file too, or the
  day issue 01 ships someone switches on the English links and quietly leaves
  the Italian post pointing nowhere. Grep `FORWARD LINK` across BOTH files.
- Category is translated like every other category on the site (Dati, Economia,
  Resi, Strategia). `Voice AI DIY` in English, `Voice AI fai-da-te` in Italian.
- Both URLs go in `tools/postdeploy_check.py` PAGES, so the sweep covers the
  pair rather than half of it.

The Italian is a real translation, not a machine pass: same register as the
English - direct, concrete, no corporate polish - with the examples localised
where they should be (accents, VAT number, CAP) and left alone where they
should not (Glasgow, Marseille, Andalusia stay).

---

## `[BUILD]` Decisions settled

1. ~~**Italian.**~~ SETTLED - both languages, always. See the standing rule above.
   Original note kept for the mechanics: All six existing posts have an `it` sibling and the two link to
   each other with reciprocal hreflang. Nothing in `publish.py` breaks on an
   EN-only post - `sibling_exists` is checked and the alternates are simply
   omitted - so this is a choice, not a constraint. But eleven EN-only posts
   will leave `/it/blog` visibly thinner than `/blog`, and the Italian market is
   one this series explicitly argues about (issue 07). Decide once, now, rather
   than per post.
2. ~~**The hub's build path.**~~ Moot - no hub.
3. **Category - SETTLED 11 Aug: `Voice AI DIY`.** Not "The Build File". The
   category is the reader-facing label on the card and the chip, and it should
   say what the season is ABOUT, not what it is called. "Voice AI DIY" also
   carries a search term; a series name carries none. Every issue uses it.
4. **Publishing cadence.** One a day, per Daniel. The retrofit step in section 5
   is a per-publish task, not an end-of-season task.
