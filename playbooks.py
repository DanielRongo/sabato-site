#!/usr/bin/env python3
"""Playbook pages - the TRIGGER half of the Use Cases menu.

    python3 playbooks.py

TWO TAXONOMIES, ONE MENU
------------------------
The nine pages under /use-cases/ answer "what does the agent do on a call":
Where is my order, Managing returns, Cart abandonment. They are WORKFLOWS.

A playbook answers a different question - "why am I looking at this at all".
Peak season is coming. We are opening a market. Care costs are out of control.
Same buyer, earlier moment, completely different page.

Both live under the Use Cases menu in two columns. Deliberately NOT a rename of
the /use-cases/ URL space: those nine pages are a week into being indexed and
moving them now would reset that for a label change nobody outside the company
would ever notice.

DERIVED FROM templates/use-case.html AT BUILD TIME, not copied. A snapshot of a
stylesheet is a bug with a delay on it - the Italian customer template was
already learned that way, where new CSS added to the English file left the
Italian page rendering ink-on-black. Playbooks get every token, breakpoint and
component the use-case pages get, forever, because they read the same file.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from playbook_data import PLAYBOOKS, ORDER                     # noqa: E402
from playbook_data_it import PLAYBOOKS_IT, ORDER_IT            # noqa: E402
from proof import proof_inline_html                            # noqa: E402

SITE = os.path.join(ROOT, "site")
CAL = "https://cal.com/sabatoai/intro"

LANGS = {
    "en": dict(out=os.path.join(SITE, "playbooks"), base="/playbooks/%s",
               locale="en_US", lang="en",
               cta_btn="Book a Call", hand="live in two weeks"),
    "it": dict(out=os.path.join(SITE, "it", "playbook"), base="/it/playbook/%s",
               locale="it_IT", lang="it",
               cta_btn="Prenota una call", hand="online in due settimane"),
}

# Playbook-only components. Everything else - tokens, hero, dark band, CTA band,
# every breakpoint - comes from the use-case stylesheet unchanged.
EXTRA_CSS = """
    /* ============ Playbook: light problem block ============ */
    /* Same geometry as the dark band so the two alternate without the page
       stepping. Only the colours change. */
    .pb-light { max-width: 1200px; margin: 0 auto; padding: 96px 40px 0; }
    .pb-light .eyebrow { color: rgb(120,118,117); font-size: 13px; font-weight: 700;
      letter-spacing: 2.5px; margin: 0 0 18px; }
    .pb-light h2 { color: var(--ink); font-size: 38px; font-weight: 700;
      letter-spacing: -1.1px; line-height: 1.15; margin: 0 0 26px; }
    /* .queue-grid .qcopy .qbody in the use-case stylesheet is specificity 0,3,0
       and paints near-white for the dark band. Reusing .queue-grid inside a light
       block therefore inherited white-on-white and the copy vanished - obvious in
       a screenshot, invisible to every automated check in this repo. Match the
       specificity rather than reaching for !important. */
    .pb-light .queue-grid .qcopy .qbody,
    .pb-light .qcopy .qbody {
      color: var(--gray); font-size: 17.5px; line-height: 1.75; margin: 0;
    }
    .pb-light .qcopy .qbody b { color: var(--ink); }
    /* 16px lost against a 1.75 line-height on 17.5px copy - the paragraph gap
       came out the same as the line gap, so two paragraphs read as one.
       SPECIFICITY, 14 Aug: this rule is 0,3,0 and the `margin: 0` two rules
       above it is 0,4,0 (.pb-light .queue-grid .qcopy .qbody), so inside a
       light block WITH a visual the gap silently lost and never applied. Five
       pages were live in that state in both languages - measured gap 0px on
       international-expansion, support-costs, multilingual-support and their
       Italian siblings. Exactly the same failure mode as the white-on-white
       note above: match the specificity, do not reach for !important. */
    .pb-light .queue-grid .qcopy .qbody + .qbody,
    .pb-light .qcopy .qbody + .qbody,
    .pb-light .qbody + .qbody { margin-top: 24px; }
    /* TOP-aligned, not centred. The use-case stylesheet centres .queue-grid,
       which is right for a short caption beside a tall drawing. It is wrong for
       copy beside a chart that opens with its own label: centring pushed the
       first line of body copy 70px below the first line of the chart, so the
       column read as though it had been dropped in by accident. */
    .pb-light .queue-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 64px;
      align-items: start; }
    /* .pb-light carries no bottom padding (it is normally the last block before
       a section that brings its own 96px top padding). A dark band brings none -
       it is a full-bleed card with internal padding only - so a light block
       followed by one had its source line touching the black edge. */
    .pb-light + .queue-band { margin-top: 104px; }
    /* Source lines are small print, not decoration - if a reader cannot read the
       citation the number might as well be unsourced. rgb(110,108,107) clears
       4.5:1 on white; the 140-grey it replaced sat at 3.4:1 and failed AA. */
    .pb-light .fine, .pb-light .queue-viz .fine {
      color: rgb(110,108,107); font-size: 12px; line-height: 1.6; margin: 26px 0 0;
    }
    /* Same reasoning on the dark bands: .45 alpha over black is 4.1:1. */
    .queue-band .queue-viz .fine, .queue-band .fine { color: rgba(248,244,241,.66); }
    /* The use-case stylesheet only paints .qbody near-white INSIDE .queue-grid
       (.queue-grid .qcopy .qbody). A wide block has no grid, so its text fell
       back to body ink - black on black, contrast 1.07, found by the AA audit.
       Scope by band, not by grid, so the colour follows the background. */
    .queue-band .qcopy .qbody { color: rgba(248, 244, 241, .82); font-size: 17.5px;
      line-height: 1.75; margin: 0; }
    .queue-band .qbody + .qbody { margin-top: 16px; }
    /* A block with no picture gets a reading measure instead of the full 1060px,
       and is centred and sized up: it is a statement, not a caption. */
    .pb-wide { max-width: 820px; }
    .pb-statement { margin: 0 auto; text-align: center; }
    .queue-band .pb-statement .qbody,
    .pb-light .pb-statement .qbody { font-size: 22px; line-height: 1.6; }
    .pb-statement .qbody + .qbody { margin-top: 22px; }
    .queue-band:has(.pb-statement) .eyebrow,
    .queue-band:has(.pb-statement) h2,
    .pb-light:has(.pb-statement) .eyebrow,
    .pb-light:has(.pb-statement) h2 { text-align: center; }
    @media (max-width: 809px) {
      .queue-band .pb-statement .qbody,
      .pb-light .pb-statement .qbody { font-size: 18.5px; }
    }
    .queue-viz .fine a, .pb-light .fine a { color: inherit; text-decoration: underline;
      text-underline-offset: 2px; }

    /* Headline inside the left column (see h2_in_col in section_blocks). The
       eyebrow stays full width above; the headline and the graphic then start
       on the same line. .pb-light h2 already styles it - only the margins
       change, because it is now the first thing in a grid cell rather than a
       block sitting above one. */
    .pb-light .pb-h2col .qcopy .eyebrow { margin: 0 0 18px; }
    .pb-light .pb-h2col .qcopy h2 { margin: 0 0 24px; }
    /* Optical, not mechanical. Both cells start at the same y, but half-leading
       scales with font-size: a 38px headline at line-height 1.15 sits ~2.9px
       below its box, a 17.5px label at 1.75 sits ~6.5px below its own. Left
       alone, the label's cap-top lands ~5px lower than the headline's and the
       two first lines read as not-quite-level - which is exactly the complaint.
       Measured, not eyeballed: see the h2InkTop/labelInkTop probe in the notes. */
    /* Retuned when the eyebrow moved into the column: the graphic now aligns
       against 13px letterspaced type, not a 38px headline, so there is almost
       no half-leading left to cancel. */
    .pb-light .pb-h2col .queue-viz { margin-top: -1px; }
    @media (max-width: 809px) {
      /* Single column - the graphic sits under the copy, so there is nothing
         to align to and the negative margin would just eat the gap. */
      .pb-light .pb-h2col .qcopy h2 { margin-bottom: 18px; }
      .pb-light .pb-h2col .queue-viz { margin-top: 0; }
    }

    /* ============ Playbook: HTML bar chart ============ */
    /* The label is typed EXACTLY like .qbody in the column beside it - same
       size, same line-height - because that is the whole point of building this
       in HTML rather than SVG. Change one and change the other, or the two
       columns stop sharing a baseline and the block looks broken again. */
    .pb-bars { margin: 0; }
    .pb-bar-l { font-size: 17.5px; line-height: 1.75; font-weight: 700;
      color: var(--ink); margin: 0 0 12px; }
    .pb-bar-track { background: rgb(233,232,232); border-radius: 14px; height: 52px; }
    /* width is set inline from the same number the label quotes, so the bar
       cannot drift out of sync with the figure it is drawing. */
    .pb-bar-fill { background: var(--black); border-radius: 14px; height: 52px;
      display: flex; align-items: center; justify-content: flex-end;
      padding-right: 18px; box-sizing: border-box; }
    .pb-bar-fill span { color: var(--lime); font-size: 30px; font-weight: 700;
      letter-spacing: -.5px; line-height: 1; }
    .pb-bar + .pb-bar { margin-top: 30px; }
    /* Caveat line under a bar - the things the source does NOT count. Same
       role as .fine but inside the graphic, so it reads as part of the chart
       rather than as its citation. */
    .pb-note { font-size: 14.5px; line-height: 1.6; color: var(--gray);
      margin: 18px 0 0; }
    @media (max-width: 809px) {
      .pb-bar-l { font-size: 16.5px; margin-bottom: 10px; }
      .pb-bar-track, .pb-bar-fill { height: 46px; }
      .pb-bar-fill span { font-size: 25px; }
      .pb-bar + .pb-bar { margin-top: 24px; }
      .pb-note { font-size: 14px; margin-top: 14px; }
    }
    @media (max-width: 809px) {
      .pb-light { padding: 64px 22px 0; }
      .pb-light h2 { font-size: 29px; letter-spacing: -.9px; }
      .pb-light .queue-grid { grid-template-columns: 1fr; gap: 34px; }
      .pb-light .qbody { font-size: 16.5px; }
      .pb-light + .queue-band { margin-top: 64px; }
    }

    /* ============ Playbook: the fork ============ */
    /* One inbound enquiry, two endings. HTML, not SVG, so the labels share the
       copy column's type scale instead of being scaled by a viewBox. */
    .pb-fork-in { display: inline-block; font-size: 15px; font-weight: 700;
      letter-spacing: .3px; text-transform: uppercase; color: var(--gray);
      background: var(--off); border-radius: 100px; padding: 9px 18px; }
    .pb-fork-out { display: grid; gap: 14px; margin-top: 16px; }
    .pb-fork-a, .pb-fork-b { border-radius: var(--radius); padding: 22px 24px;
      border: 1px solid var(--line); }
    .pb-fork-b { background: var(--black); border-color: var(--black); }
    .pb-fork-a b, .pb-fork-b b { display: block; font-size: 17.5px;
      font-weight: 700; line-height: 1.4; }
    .pb-fork-a b { color: var(--gray); }
    .pb-fork-b b { color: rgb(204,255,0); }
    .pb-fork-a i, .pb-fork-b i { display: block; margin-top: 6px;
      font-style: normal; font-size: 16px; line-height: 1.6; }
    .pb-fork-a i { color: rgb(120,118,117); }
    .pb-fork-b i { color: rgba(248,244,241,.82); }
    @media (max-width: 809px) {
      .pb-fork-in { font-size: 13.5px; padding: 8px 15px; }
      .pb-fork-a, .pb-fork-b { padding: 18px 20px; border-radius: 18px; }
      .pb-fork-a b, .pb-fork-b b { font-size: 16.5px; }
      .pb-fork-a i, .pb-fork-b i { font-size: 15px; }
    }

    /* ============ Playbook: slim mid-page CTA ============ */
    .pb-mid { max-width: 1200px; margin: 0 auto; padding: 76px 40px 0; text-align: center; }
    .pb-mid p { font-size: 21px; font-weight: 700; letter-spacing: -.4px; color: var(--ink);
      margin: 0 0 18px; }

    /* ============ Playbook: visible FAQ ============ */
    .pb-faqs { max-width: 1200px; margin: 0 auto; padding: 96px 40px 0; }
    .pb-faqs h2 { font-size: 38px; font-weight: 700; letter-spacing: -1.1px;
      color: var(--ink); margin: 0 0 34px; text-align: center; }
    .pb-faq-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .pb-qa { background: var(--off); border-radius: var(--radius); padding: 28px 30px; }
    .pb-qa h3 { font-size: 18px; font-weight: 700; letter-spacing: -.3px;
      color: var(--ink); margin: 0 0 10px; }
    .pb-qa p { font-size: 15.5px; line-height: 1.65; color: var(--gray); margin: 0; }
    @media (max-width: 809px) {
      .pb-mid { padding: 56px 22px 0; }
      .pb-mid p { font-size: 18px; }
      .pb-faqs { padding: 64px 22px 0; }
      .pb-faqs h2 { font-size: 29px; margin-bottom: 24px; }
      .pb-faq-grid { grid-template-columns: 1fr; }
    }

    /* ============ Playbook: the countdown ============ */
    .pb-steps { max-width: 1200px; margin: 0 auto; padding: 104px 40px 0; }
    .pb-steps h2 { font-size: 38px; font-weight: 700; letter-spacing: -1.1px; line-height: 1.2;
      color: var(--ink); margin: 0 0 12px; text-align: center; }
    .pb-steps .pb-lede { font-size: 16.5px; line-height: 1.7; color: var(--gray);
      max-width: 680px; margin: 0 auto 46px; text-align: center; }
    .pb-step { display: grid; grid-template-columns: 190px 1fr; gap: 40px;
      padding: 30px 0; border-top: 1px solid var(--line); align-items: start; }
    .pb-step:last-child { border-bottom: 1px solid var(--line); }
    .pb-when { font-size: 14px; font-weight: 700; letter-spacing: 1.6px;
      text-transform: uppercase; color: var(--ink); padding-top: 4px; }
    .pb-when span { display: block; font-weight: 500; letter-spacing: 0;
      text-transform: none; font-size: 14.5px; color: var(--gray); margin-top: 6px; }
    .pb-step h3 { font-size: 23px; font-weight: 700; letter-spacing: -.5px;
      line-height: 1.3; color: var(--ink); margin: 0 0 10px; }
    .pb-step p { font-size: 16.5px; line-height: 1.7; color: var(--gray); margin: 0; }
    .pb-step p + p { margin-top: 10px; }
    .pb-step a { color: var(--blue); text-decoration: underline; text-underline-offset: 2px; }

    /* ============ Playbook: the workflow row ============ */
    .pb-wf { max-width: 1200px; margin: 0 auto; padding: 96px 40px 0; }
    .pb-wf h2 { font-size: 38px; font-weight: 700; letter-spacing: -1.1px; line-height: 1.2;
      color: var(--ink); margin: 0 0 12px; text-align: center; }
    .pb-wf .pb-lede { font-size: 16.5px; line-height: 1.7; color: var(--gray);
      max-width: 700px; margin: 0 auto 40px; text-align: center; }
    .pb-wf-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
    .pb-card { display: block; background: var(--off); border-radius: var(--radius);
      padding: 30px 32px; transition: transform .15s ease; }
    .pb-card:hover { transform: translateY(-2px); }
    .pb-ic { display: flex; align-items: center; justify-content: center;
      width: 44px; height: 44px; border-radius: 12px; background: var(--black);
      margin: 0 0 18px; }
    .pb-ic svg { width: 22px; height: 22px; display: block; }
    .pb-card h3 { font-size: 20px; font-weight: 700; letter-spacing: -.4px;
      color: var(--ink); margin: 0 0 8px; }
    .pb-card p { font-size: 16px; line-height: 1.65; color: var(--gray); margin: 0; }
    .pb-card .pb-go { display: inline-block; margin-top: 14px; font-size: 15px;
      font-weight: 700; color: var(--blue); }


    @media (max-width: 809px) {
      .pb-steps { padding: 72px 22px 0; }
      .pb-steps h2, .pb-wf h2 { font-size: 29px; }
      .pb-step { grid-template-columns: 1fr; gap: 10px; padding: 24px 0; }
      .pb-when span { display: inline; margin: 0 0 0 8px; }
      .pb-step h3 { font-size: 20px; }
      .pb-wf { padding: 72px 22px 0; }
      .pb-wf-grid { grid-template-columns: 1fr; }
      .pb-proofline { padding: 0 16px; margin-top: 72px; }
      .pb-proofline .pb-inner { padding: 34px 24px 32px; }
      .pb-proofline blockquote { font-size: 19px; }
      .pb-proofline .pb-nums { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
      .pb-proofline .pb-n { font-size: 26px; letter-spacing: -.8px; }
      .pb-proofline .pb-l { font-size: 11.5px; }
    }
"""


# One 24x24 lime line-glyph per workflow tile, on the same grid and the same 2px
# stroke as industry_icons.py - a mixed set of stroke widths is the fastest way
# to make a glyph family look bought rather than drawn. The glyph sits in a black
# badge because these tiles are light grey: lime on near-white is unreadable,
# and lime on black is the site's own pairing.
_ICW = ('<svg viewBox="0 0 24 24" fill="none" stroke="rgb(204,255,0)" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>')
ICONS = {
    # parcel in transit
    "wismo": _ICW % ('<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/>'
                     '<path d="M3 7.5 12 12l9-4.5"/><path d="M12 12v9"/>'),
    # speech bubble with a question - someone deciding, out loud
    "presales": _ICW % ('<path d="M3.5 6.5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-6.5'
                        'L7.5 20v-3.5H5.5a2 2 0 0 1-2-2z"/>'
                        '<path d="M10.2 9a2 2 0 1 1 2.4 2.4c-.6.2-.8.6-.8 1.1"/>'
                        '<path d="M11.8 14.2h.02"/>'),
    # counter-clockwise arrow: undo, send back
    "returns": _ICW % ('<path d="M3.5 12a8.5 8.5 0 1 0 2.5-6"/><path d="M3.5 3.5v5h5"/>'),
    # bell
    "restock": _ICW % ('<path d="M18 9.5a6 6 0 1 0-12 0c0 5.5-2.2 6.8-2.2 6.8h16.4S18 15 18 9.5z"/>'
                       '<path d="M13.8 19.6a2.1 2.1 0 0 1-3.6 0"/>'),
    # speech bubble with a star: asking how it went
    "feedback": _ICW % ('<path d="M3.5 6.2a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-6.4'
                        'L7.6 19.8V16.2H5.5a2 2 0 0 1-2-2z"/>'
                        '<path d="m12 7.6 1.35 2.74 3.02.44-2.18 2.13.51 3-2.7-1.42-2.7 1.42'
                        '.51-3-2.18-2.13 3.02-.44z"/>'),
    # clipboard with a line of figures: a quote being put together
    "quote": _ICW % ('<path d="M8 4.5H6.5a1.5 1.5 0 0 0-1.5 1.5v13a1.5 1.5 0 0 0 1.5 1.5h11a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H16"/>'
                     '<rect x="8" y="2.6" width="8" height="3.8" rx="1.2"/>'
                     '<path d="M8.5 12h7"/><path d="M8.5 15.6h4.5"/>'),
    # a document with a tick: the order, confirmed in writing
    "checkout": _ICW % ('<path d="M6 3h7l5 5v12a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/>'
                        '<path d="M13 3v5h5"/><path d="M8.6 14.4l2.2 2.2 4.4-4.4"/>'),
}


def esc(s):
    return html.escape(s, quote=False)


def nb(s):
    """[nb]...[/nb] keeps a phrase on one line, same convention as every other
    template here. [br] forces a break.

    The two are not interchangeable and the difference matters. [nb] is a
    REQUEST - it stops a phrase splitting if the line happens to be tight, and
    does nothing at all when the container is wide enough to fit everything.
    A 38px h2 in a 1060px column fits a lot, so a two-clause headline written
    with [nb] alone renders as one long line on desktop and only breaks on a
    phone, which is the opposite of the intent. [br] is the instruction: break
    here, at every width.
    """
    return (s.replace("[nb]", '<span class="nb">')
             .replace("[/nb]", "</span>")
             .replace("[br]", "<br>"))


def template(lang):
    """The use-case template, re-pointed at /playbooks/ and given its own CSS."""
    t = open(os.path.join(ROOT, "templates", "use-case.html"), encoding="utf-8").read()
    base = LANGS[lang]["base"] % "{{SLUG}}"
    t = t.replace("https://www.sabato.ai/use-cases/{{SLUG}}",
                  "https://www.sabato.ai" + base)
    if lang == "it":
        t = t.replace('<html lang="en">', '<html lang="it">')
        t = t.replace('<meta property="og:locale" content="en_US">',
                      '<meta property="og:locale" content="it_IT">')
    # The hero's hand-written note and button live in the template, not the data.
    t = t.replace(">live in two weeks<", ">%s<" % esc(LANGS[lang]["hand"]))
    if lang == "it":
        t = t.replace(">Start Free Pilot<", ">%s<" % esc(LANGS[lang]["cta_btn"]))
    t = t.replace("  </style>", EXTRA_CSS + "  </style>", 1)
    return t


def section_blocks(d):
    """The problem, in as many blocks as it takes.

    A playbook has to earn the reader before it sells anything, and the problem
    is the part they recognise. Dark and light blocks alternate so a long
    argument still reads as a page rather than an essay.

    `fine` is not decoration either: every figure on these pages carries its
    source and its date underneath it, because a claim about somebody's payroll
    that cannot be checked is worth less than no claim at all.
    """
    out = []
    for b in d["blocks"]:
        body = "".join('<p class="qbody">%s</p>' % b_p for b_p in b["body"])
        fine = '<p class="fine">%s</p>' % b["fine"] if b.get("fine") else ""
        h2 = "<h2>%s</h2>" % nb(esc(b["h2"]))
        head_h2 = h2                      # full-width above the grid, by default
        head_eyebrow = '<p class="eyebrow">%s</p>' % esc(b["eyebrow"])
        if b.get("viz"):
            # h2_in_col: the headline moves INSIDE the left column, so the
            # graphic starts level with it instead of below it.
            #
            # Daniel, 12 Aug: "the graphic ... is still not aligned in height
            # with They read English. They still won't call in it." With the
            # headline spanning the full width, the graphic could only ever
            # begin below it - roughly 170px lower - so the two halves read as
            # stacked rather than side by side.
            #
            # It also fixes the height imbalance that top-aligning exposed: the
            # copy column was 153px against a 299px graphic. Adding the headline
            # to that column brings the two within a few pixels of each other,
            # so the block finally reads as one row.
            #
            # OPT-IN, not automatic. At half width a 38px headline only has room
            # for about 27 characters a line, and peak-season's is longer - it
            # would silently rewrap there. Blocks declare this when their
            # headline is short enough to survive the narrower column.
            if b.get("h2_in_col"):
                # The EYEBROW moves into the column too, not just the headline.
                # Daniel, 13 Aug: "align the graphic on the right with the top
                # text on the left (AND IT GOT WORSE EVERYWHERE)". With the
                # eyebrow spanning the full width above, the graphic could only
                # start level with the headline beneath it - still a step down
                # from the block's actual first line.
                head_h2 = ""
                head_eyebrow = ""
                grid = ('<div class="queue-grid pb-h2col">'
                        '<div class="qcopy"><p class="eyebrow">%s</p>%s%s</div>'
                        '<div class="queue-viz">%s%s</div></div>'
                        % (esc(b["eyebrow"]), h2, body, b["viz"], fine))
            else:
                grid = ('<div class="queue-grid"><div class="qcopy">%s</div>'
                        '<div class="queue-viz">%s%s</div></div>'
                        % (body, b["viz"], fine))
        else:
            # A block with no picture still has to carry its source. The first
            # version attached `fine` to the visual, so the one block without one
            # - the block with the 48.9% figure on it - published an unsourced
            # number. Every figure on these pages cites itself or it does not ship.
            # A block with no picture IS the statement - centred and a size up,
            # because at body-copy size a lone column of text reads as a caption
            # for a graphic that never arrives.
            grid = '<div class="qcopy pb-wide pb-statement">%s%s</div>' % (body, fine)
        cls = "queue-band" if b.get("tone", "dark") == "dark" else "pb-light"
        out.append("""
    <section class="%s">
      <div class="queue-inner">
        %s
        %s
        %s
      </div>
    </section>""" % (cls, head_eyebrow, head_h2, grid))
    return "".join(out)




def section_faq(d):
    """The FAQ, VISIBLE. The FAQPage schema in <head> must describe content
    that is actually on the page - schema for invisible answers is what rich-
    result penalties are made of, and it was the one dishonest inch in the
    first version of this page. Rendered from the same list the JSON-LD reads,
    so the two cannot drift."""
    if not d.get("faq"):
        return ""
    items = "".join(
        '<div class="pb-qa"><h3>%s</h3><p>%s</p></div>' % (esc(q), esc(a))
        for q, a in d["faq"])
    return """
    <section class="pb-faqs">
      <h2>%s</h2>
      <div class="pb-faq-grid">%s</div>
    </section>""" % (esc(d.get("faq_h2", "FAQ")), items)


def section_workflows(d):
    w = d["workflows"]
    cards = "".join(
        '<a class="pb-card" href="%s"><span class="pb-ic">%s</span>'
        '<h3>%s</h3><p>%s</p><span class="pb-go">%s &rarr;</span></a>'
        % (href, ICONS.get(icon, ""), esc(label), esc(line), esc(w["go"]))
        for label, href, line, icon in w["items"])
    return """
    <section class="pb-wf">
      <h2>%s</h2>
      <p class="pb-lede">%s</p>
      <div class="pb-wf-grid">%s</div>
    </section>""" % (nb(esc(w["h2"])), esc(w["lede"]), cards)


def section_proof(d, lang):
    """THE homepage testimonial widget, not a copy of it.

    This used to be a bespoke `.pb-proofline` block: same content, hand-rebuilt
    in this file's own CSS. Two implementations of one component is how a design
    system rots - the homepage gets a fix and the playbook quietly keeps the old
    look. Now it renders proof.py's markup, inherits footer.css, and any change
    to the widget lands on both surfaces at once.
    """
    return proof_inline_html(lang)

def section_cta(d, lang):
    c = d["cta"]
    return """
    <section class="cta-band">
      <p class="hand">%s</p>
      <h2>%s</h2>
      <p>%s</p>
      <a class="btn-pill" href="%s" target="_blank" rel="noopener">%s</a>
    </section>""" % (esc(c["hand"]), nb(esc(c["h2"])), esc(c["sub"]),
                     CAL, esc(LANGS[lang]["cta_btn"]))


def jsonld(slug, d, lang):
    """Article + a FAQPage when the playbook carries questions.

    No datePublished and no aggregateRating: we hold neither, and decorating a
    rich result with a number we invented is the one SEO shortcut that is
    actually punished rather than merely useless.
    """
    import json
    url = "https://www.sabato.ai" + (LANGS[lang]["base"] % slug)
    out = [{
        "@context": "https://schema.org", "@type": "Article",
        # Strip EVERY layout token, not just [nb] - a headline that ships
        # "...countries.[br]Answer..." to Google is worse than no schema at all.
        # [br] becomes a space because it is a sentence boundary on the page.
        "headline": re.sub(r"\[/?nb\]", "", d["h1"].replace("[br]", " ")).strip(),
        "description": d["description"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "inLanguage": lang,
        "image": "https://www.sabato.ai/fuc/assets/8Q4ofjOgRTqsr8FpanTJF9nzLwU.png",
        "publisher": {"@type": "Organization", "name": "Sabato AI"},
    }]
    if d.get("faq"):
        out.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in d["faq"]],
        })
    return "".join('<script type="application/ld+json">%s</script>'
                   % json.dumps(o, ensure_ascii=False) for o in out)


def hreflang(slug, lang):
    """Both directions or neither. A one-sided hreflang is worse than none."""
    en = slug if lang == "en" else PLAYBOOKS_IT[slug]["en"]
    it = slug if lang == "it" else PLAYBOOKS[slug].get("it")
    if not it:
        return ""
    return ('<link rel="alternate" hreflang="en" href="https://www.sabato.ai/playbooks/%s">'
            '<link rel="alternate" hreflang="it" href="https://www.sabato.ai/it/playbook/%s">'
            '<link rel="alternate" hreflang="x-default" href="https://www.sabato.ai/playbooks/%s">'
            % (en, it, en))


def build(lang, slug, d):
    cfg = LANGS[lang]
    tpl = template(lang)
    sections = "".join([section_blocks(d), section_workflows(d),
                        section_proof(d, lang), section_faq(d),
                        section_cta(d, lang)])
    page = (tpl
            .replace("{{TITLE}}", html.escape(d["title"]))
            .replace("{{DESCRIPTION}}", html.escape(d["description"]))
            .replace("{{SLUG}}", slug)
            .replace("{{JSONLD}}", jsonld(slug, d, lang) + hreflang(slug, lang))
            .replace("{{CHIP}}", esc(d["chip"]))
            .replace("{{H1}}", nb(esc(d["h1"])))
            .replace("{{SUB}}", esc(d["sub"]))
            .replace("{{HERO_VISUAL}}", d["hero_visual"])
            .replace("{{SECTIONS}}", sections))
    os.makedirs(cfg["out"], exist_ok=True)
    p = os.path.join(cfg["out"], slug + ".html")
    open(p, "w", encoding="utf-8").write(page)
    print("  wrote %s" % p)
    return "https://www.sabato.ai" + (cfg["base"] % slug)


# ---------------------------------------------------------------------------
# THE HUB: /playbooks and /it/playbook
# ---------------------------------------------------------------------------
HUB = {
    "en": dict(
        tpl="use-case-index.html",
        out=os.path.join(SITE, "playbooks", "index.html"),
        url="https://www.sabato.ai/playbooks/",
        old_url="https://www.sabato.ai/use-cases/",
        title="Voice AI Playbooks for E-Commerce | Sabato AI",
        old_title="Voice AI Use Cases for E-Commerce | Sabato AI",
        description="Six situations that send e-commerce operators looking for "
                    "voice AI - peak season, new markets, missed calls, support "
                    "costs - and what to do about each.",
        h1="Six reasons operators come looking.",
        intro="Nobody wakes up wanting a voice agent. They wake up with a "
              "problem: a queue that will not clear, a market they cannot "
              "answer, a phone nobody picks up. Each playbook below is one of "
              "those situations, and what we would actually do about it.",
        # The inherited band asks "which one to START with" and talks about
        # queues - correct for the workflow hub, wrong here. A playbook is a
        # situation you are already in, not an option you pick.
        cta_h2="Not sure which one you are in?",
        old_cta_h2="Not sure which one to start with?",
        cta_p="Most operators recognise two of these at once. Bring your call "
              "log to the intro call and we will tell you which one is costing "
              "you most.",
        old_cta_p="Most stores start with one and add a second inside a month. "
                  "Bring your call log to the intro call and we&rsquo;ll tell "
                  "you which queue is costing you most.",
    ),
    "it": dict(
        tpl="use-case-index-it.html",
        out=os.path.join(SITE, "it", "playbook", "index.html"),
        url="https://www.sabato.ai/it/playbook/",
        old_url="https://www.sabato.ai/it/casi-duso/",
        title="Playbook Voice AI per l'e-commerce | Sabato AI",
        old_title="Casi d'uso Voice AI per l'e-commerce | Sabato AI",
        description="Sei situazioni che portano chi gestisce un e-commerce a "
                    "cercare una voice AI: alta stagione, nuovi mercati, "
                    "chiamate perse, costi. E cosa fare per ciascuna.",
        h1="Sei motivi per cui ci si mette a cercare.",
        intro="Nessuno si sveglia volendo un agente vocale. Ci si sveglia con "
              "un problema: una coda che non si smaltisce, un mercato a cui non "
              "sai rispondere, un telefono che nessuno alza. Ogni playbook qui "
              "sotto è una di quelle situazioni, e cosa faremmo davvero.",
        cta_h2="Non sai in quale ti trovi?",
        old_cta_h2="Non sai da quale partire?",
        cta_p="Quasi tutti se ne riconoscono due insieme. Porta il tuo log "
              "chiamate alla call e ti diciamo quale ti sta costando di più.",
        old_cta_p="Quasi tutti iniziano da uno e aggiungono il secondo entro un "
                  "mese. Porta il tuo log chiamate alla call e ti diciamo quale "
                  "coda ti sta costando di più.",
    ),
}

HERO_RX = re.compile(
    r'(<section class="ix-hero"><div class="shell">\s*<h1>).*?(</h1>\s*<p>).*?(</p>)',
    re.S)


def _card_lead(d):
    """The playbook's own h1, with the layout tokens removed.

    Same principle as the use-case hub, which uses each page's <h1> as its card
    line: those headlines are the most worked-over copy on the site and there is
    no reason to write a second version that can drift from the first.
    """
    return re.sub(r"\[/?nb\]", "", d["h1"].replace("[br]", " ")).strip()


def build_hub(lang):
    cfg = HUB[lang]
    src, order, base = ((PLAYBOOKS, ORDER, LANGS["en"]["base"]) if lang == "en"
                        else (PLAYBOOKS_IT, ORDER_IT, LANGS["it"]["base"]))
    cards = "".join(
        '<a class="ix-card" href="%s"><h3>%s</h3>'
        '<p class="ix-lead">%s</p></a>'
        % (base % s, esc(src[s]["nav"]), esc(_card_lead(src[s])))
        for s in order)

    # DERIVED from the use-case index at build time, never copied - the same
    # rule the playbook pages follow. A snapshot of a template is a bug with a
    # delay on it: the Italian customer template was learned that way.
    t = open(os.path.join(ROOT, "templates", cfg["tpl"]), encoding="utf-8").read()
    t = t.replace(cfg["old_url"], cfg["url"])
    t = t.replace(cfg["old_title"], cfg["title"])
    t = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + html.escape(cfg["description"]) + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
               lambda m: m.group(1) + html.escape(cfg["description"]) + m.group(2), t, count=1)
    new_hero = HERO_RX.sub(
        lambda m: m.group(1) + esc(cfg["h1"]) + m.group(2) + esc(cfg["intro"]) + m.group(3),
        t, count=1)
    if new_hero == t:
        sys.exit("playbook hub: the ix-hero block did not match - template changed?")
    t = new_hero
    for k in ("cta_h2", "cta_p"):
        before = cfg["old_" + k]
        if before not in t:
            sys.exit("playbook hub: CTA text %r not found - template changed?" % k)
        t = t.replace(before, esc(cfg[k]), 1)
    t = t.replace("{{CARDS}}", cards).replace("{{CAL}}", CAL)
    os.makedirs(os.path.dirname(cfg["out"]), exist_ok=True)
    open(cfg["out"], "w", encoding="utf-8").write(t)
    print("  wrote %s  (%d cards)" % (cfg["out"], len(order)))
    # WITH the trailing slash. The canonical this page carries is
    # .../playbooks/ and both existing hubs (/use-cases/, /industries/) are
    # listed that way, so stripping it here would have put a URL in the sitemap
    # that disagrees with the canonical on the page it points at.
    return cfg["url"]


def sitemap_add(urls):
    path = os.path.join(SITE, "sitemap.xml")
    if not os.path.exists(path):
        return 0
    xml = open(path, encoding="utf-8").read()
    have = set(re.findall(r"<loc>(.*?)</loc>", xml))
    add = [u for u in urls if u not in have]
    if add:
        xml = xml.replace("</urlset>",
                          "".join("<url><loc>%s</loc></url>" % u for u in add) + "</urlset>")
        open(path, "w", encoding="utf-8").write(xml)
    return len(add)


def main():
    urls = []
    for slug in ORDER:
        urls.append(build("en", slug, PLAYBOOKS[slug]))
    for slug in ORDER_IT:
        urls.append(build("it", slug, PLAYBOOKS_IT[slug]))
    for lang in ("en", "it"):
        urls.append(build_hub(lang))
    print("  sitemap: %d new URL(s) added" % sitemap_add(urls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
