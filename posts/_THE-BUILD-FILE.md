# The Build File - slug map and internal linking rules

Daniel's spec, 11 Aug 2026. **This is the record. The map lives here and nowhere
else.** Anything that contradicts this file is wrong, including a slug already
sitting in `posts/en/`.

Notes marked `[BUILD]` are added by the site build, not by Daniel - they are
where this repo's machinery touches the plan. They do not change the plan.

---

## 1. The slug map (fix this before anything else ships)

Season hub: **`/blog/the-build-file`**

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

`[BUILD]` The season hub is NOT a post. `publish.py` only renders what is in
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

**Two fixed links, every time:**

1. Back to the season hub (in the standfirst or the footer).
2. To issue 00, the acceptance test - because every issue eventually says "and
   then test it."

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

## `[BUILD]` Open decisions, to settle before or with issue 00

1. **Italian.** All six existing posts have an `it` sibling and the two link to
   each other with reciprocal hreflang. Nothing in `publish.py` breaks on an
   EN-only post - `sibling_exists` is checked and the alternates are simply
   omitted - so this is a choice, not a constraint. But eleven EN-only posts
   will leave `/it/blog` visibly thinner than `/blog`, and the Italian market is
   one this series explicitly argues about (issue 07). Decide once, now, rather
   than per post.
2. **The hub's build path.** See the `[BUILD]` note in section 1.
3. **Category.** Existing posts use a single `category` field (Operations, and
   others). A dedicated `The Build File` category would let the blog index group
   the season without new template work. Cheapest way to make eleven posts read
   as one thing.
4. **Publishing cadence.** One a day, per Daniel. The retrofit step in section 5
   is a per-publish task, not an end-of-season task.
