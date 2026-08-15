#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Product pages: /product/<slug> and /it/prodotto/<slug>.

    python3 product.py

WHY THIS FILE IS SO SHORT
Because it borrows almost everything. Daniel, 13 Aug: "can't you reuse existing
modules for similar pages and just change content and graphics?" - so this
imports the playbook generator's stylesheet, its section renderers, its proof
widget and its CTA band, and adds exactly three things a playbook does not have:

  1. `section_shot`  - the full-bleed platform screenshot under the hero
  2. `section_hands` - the "who actually touches this" band
  3. `TOOLS_VIZ`     - a live-HTML diagram of the agent's tools

LAYOUT: OPTION A, chosen 14 Aug
    hero (text only)  ->  screenshot  ->  3 blocks  ->  hands  ->  FAQ  ->  CTA

The hero deliberately carries NO screenshot. A UI in the hero says "here is the
tool you will operate", which is the opposite of what this business sells; a
screenshot placed AFTER a claim reads as evidence for that claim instead. Same
image, opposite promise.

WHY THE TOOLS DIAGRAM IS HTML AND THE PLATFORM SHOT IS AN IMAGE
An image of a UI scales with its column. On a 390px phone the content column is
about 346px, so a 1560px-wide screenshot renders at ~0.22x and its 12px labels
land at under 3px. tools/phone_render_audit.py exists precisely because that
bug shipped twice. The platform shot survives it by having a separate, much
tighter phone crop; the tools diagram survives it by not being a picture at all
- it is real text in real elements, so it reflows and stays readable.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from product_data import PRODUCTS, ORDER                      # noqa: E402
from product_data_it import PRODUCTS_IT, ORDER_IT             # noqa: E402
import playbooks as pb                                        # noqa: E402

SITE = os.path.join(ROOT, "site")
CAL = pb.CAL
esc = pb.esc
nb = pb.nb

LANGS = {
    "en": dict(out=os.path.join(SITE, "product"), base="/product/%s",
               locale="en_US", lang="en",
               cta_btn="Start Free Pilot", hand="live in two weeks"),
    "it": dict(out=os.path.join(SITE, "it", "prodotto"), base="/it/prodotto/%s",
               locale="it_IT", lang="it",
               cta_btn="Inizia il Pilota Gratuito", hand="online in due settimane"),
}

# ---------------------------------------------------------------------------
# CSS - only what the playbook stylesheet does not already provide.
# ---------------------------------------------------------------------------
PRODUCT_CSS = """
    /* ============ Product: the full-bleed platform shot ============ */
    .pr-shot { max-width: 1200px; margin: 0 auto; padding: 64px 40px 0; }
    .pr-shot figure { margin: 0; }
    /* The frame is what makes a flat PNG read as a screenshot rather than as
       an illustration that happens to have a sidebar in it. */
    .pr-shot img { display: block; width: 100%; height: auto; border-radius: 16px;
      border: 1px solid rgba(18,10,11,.10);
      box-shadow: 0 24px 60px rgba(18,10,11,.13), 0 2px 6px rgba(18,10,11,.06); }
    .pr-shot figcaption { color: rgb(120,118,117); font-size: 14.5px;
      line-height: 1.6; margin: 18px auto 0; max-width: 62ch; text-align: center; }

    /* ============ Product: the tools diagram ============ */
    .tv { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .tv-card { border: 1px solid rgba(18,10,11,.12); border-radius: 14px;
      background: #fff; padding: 18px 18px 16px; }
    .tv-card .tv-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 1.4px;
      color: rgb(120,118,117); margin: 0 0 14px; }
    .tv-tool { display: flex; align-items: flex-start; gap: 11px; padding: 9px 0;
      border-bottom: 1px solid rgba(18,10,11,.07); }
    .tv-tool:last-child { border-bottom: 0; padding-bottom: 0; }
    .tv-ic { width: 30px; height: 30px; flex: 0 0 30px; border-radius: 9px;
      display: flex; align-items: center; justify-content: center; }
    .tv-ic svg { width: 16px; height: 16px; fill: none; stroke-width: 1.8;
      stroke-linecap: round; stroke-linejoin: round; }
    .tv-tool code { display: block; font-family: ui-monospace, SFMono-Regular,
      Menlo, monospace; font-size: 13.5px; font-weight: 600; color: var(--ink); }
    .tv-tool em { display: block; font-style: normal; font-size: 13px;
      line-height: 1.4; color: rgb(120,118,117); margin-top: 2px; }
    .tv-rule { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 11px; }
    .tv-rule:last-of-type { margin-bottom: 0; }
    .tv-n { width: 21px; height: 21px; flex: 0 0 21px; border-radius: 999px;
      background: var(--ink); color: #fff; font-size: 11px; font-weight: 700;
      line-height: 21px; text-align: center; }
    .tv-rule p { font-size: 14.5px; line-height: 1.45; margin: 0; color: var(--ink); }
    .tv-say { margin-top: 16px; border-top: 1px solid rgba(18,10,11,.07); padding-top: 14px; }
    .tv-bubble { background: rgb(250,249,247); border: 1px solid rgba(18,10,11,.10);
      border-radius: 12px 12px 12px 4px; padding: 10px 13px; font-size: 14.5px;
      line-height: 1.45; font-style: italic; color: rgb(61,57,54); }
    .tv-foot { grid-column: 1 / -1; display: flex; align-items: center; gap: 10px;
      border: 1px solid rgba(18,10,11,.12); border-radius: 12px;
      background: rgb(250,249,247); padding: 12px 15px; font-size: 14.5px;
      line-height: 1.4; }
    .tv-foot b { color: var(--ink); }
    .tv-foot em { font-style: normal; color: rgb(120,118,117); }
    .tv-dot { width: 8px; height: 8px; flex: 0 0 8px; border-radius: 999px;
      background: rgb(200,240,74); box-shadow: 0 0 0 3px rgba(200,240,74,.3); }

    /* ============ Product: the release flow ============ */
    /* Block 3 had no visual, so section_blocks rendered it as a centred
       statement - correct for one short line, wrong for two paragraphs, and
       with block 1 already centred the page read as two walls of centred text
       in a row. This gives block 3 something to sit beside. */
    .rf { display: flex; flex-direction: column; gap: 10px; }
    .rf-step { display: flex; align-items: flex-start; gap: 13px;
      border: 1px solid rgba(248,244,241,.16); border-radius: 13px;
      padding: 15px 16px; background: rgba(248,244,241,.04); }
    .rf-k { width: 26px; height: 26px; flex: 0 0 26px; border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 12px; font-weight: 700; background: rgba(248,244,241,.11);
      color: rgb(248,244,241); }
    .rf-step.is-live .rf-k { background: rgb(200,240,74); color: rgb(18,10,11); }
    .rf-step b { display: block; color: rgb(248,244,241); font-size: 16px;
      letter-spacing: -.2px; }
    .rf-step em { display: block; font-style: normal; color: rgba(248,244,241,.66);
      font-size: 14.5px; line-height: 1.5; margin-top: 3px; }
    .rf-arrow { height: 14px; margin: -6px 0 -6px 25px;
      border-left: 1px dashed rgba(248,244,241,.28); }

    /* ============ Product: centred hero ============ */
    /* Daniel, 14 Aug: "hero text should be centered." The template's .split-hero
       is a two-column grid with an empty .hero-visual on the right - option A
       puts no picture in the hero - so left-aligned copy sat in the left half
       of a page whose next element is a full-bleed screenshot. Collapse the grid
       to one centred column and the hero reads as a title card for the shot
       underneath it. */
    .split-hero { display: block; text-align: center; }
    .split-hero .hero-copy { max-width: 780px; margin: 0 auto; }
    .split-hero .hero-visual { display: none; }
    .split-hero .sub { margin-left: auto; margin-right: auto; max-width: 62ch; }
    .split-hero .hero-cta { justify-content: center; }

    /* ============ Product: statement + a pair of panels ============ */
    /* Daniel, 14 Aug: "after the full width screenshot, I don't want another
       full width widget - lead with a statement, and below it two screenshots
       half width each." So exactly one full-bleed image on the page, and the
       second look at the product arrives as two half-width panels under a line
       that says what they prove.
       These are LIVE HTML dressed as dialogs, not images: at half width on a
       390px phone a picture of this UI would render its 13px labels at ~6px. */
    .pr-pair { max-width: 1200px; margin: 0 auto; padding: 104px 40px 104px;
      text-align: center; }
    /* Daniel, 14 Aug: the dark band started flush against the panels above it.
       .pr-pair had no bottom padding, so two sections touched. */
    .pr-pair .eyebrow { color: rgb(120,118,117); font-size: 13px; font-weight: 700;
      letter-spacing: 2.5px; margin: 0 0 18px; }
    .pr-pair h2 { color: var(--ink); font-size: 44px; font-weight: 700;
      letter-spacing: -1.5px; line-height: 1.1; margin: 0 auto 20px; max-width: 22ch; }
    .pr-pair .pb-lede { color: var(--gray); font-size: 17.5px; line-height: 1.7;
      margin: 0 auto 44px; max-width: 60ch; }
    .pr-pair-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 22px;
      text-align: left; }

    /* a panel, dressed as one of the product's own dialogs */
    .dlg { border: 1px solid rgba(18,10,11,.13); border-radius: 16px; background: #fff;
      box-shadow: 0 12px 34px rgba(18,10,11,.08), 0 1px 3px rgba(18,10,11,.05);
      padding: 20px 20px 18px; display: flex; flex-direction: column; }
    .dlg-h { margin-bottom: 16px; }
    .dlg-h b { display: block; font-size: 16px; letter-spacing: -.25px; color: var(--ink); }
    .dlg-h span { display: block; font-size: 13.5px; color: rgb(120,118,117); margin-top: 2px; }
    .dlg-l { font-size: 13px; font-weight: 700; color: var(--ink); margin: 0 0 8px; }
    .dlg-sel { border: 1px solid rgba(18,10,11,.13); border-radius: 10px;
      background: rgb(238,247,205); padding: 11px 13px; font-size: 14px;
      color: rgb(120,118,117); display: flex; align-items: center; }
    .dlg-sel::after { content: "\2303\2304"; margin-left: auto; font-size: 11px;
      letter-spacing: -2px; color: rgb(140,136,132); }
    .dlg-menu { border: 1px solid rgba(18,10,11,.13); border-top: 0;
      border-radius: 0 0 10px 10px; overflow: hidden; }
    .dlg-search { padding: 10px 13px; font-size: 13.5px; color: rgb(150,146,142);
      border-bottom: 1px solid rgba(18,10,11,.09); background: #fff; }
    .dlg-item { padding: 9px 13px; font-size: 14px; color: var(--ink);
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    .dlg-item + .dlg-item { border-top: 1px solid rgba(18,10,11,.055); }
    .dlg-item.on { background: rgb(246,250,232); font-weight: 700; }
    .dlg-btns { display: flex; gap: 9px; justify-content: flex-end; margin-top: auto;
      padding-top: 18px; }
    .dlg-b { border-radius: 9px; padding: 9px 18px; font-size: 13.5px; font-weight: 700; }
    .dlg-b.gh { border: 1px solid rgba(18,10,11,.15); color: var(--ink); }
    .dlg-b.go { background: rgb(139,185,159); color: #fff; }

    .dlg-field { border: 1px solid rgba(18,10,11,.13); border-radius: 9px;
      padding: 10px 12px; font-size: 14px; font-family: ui-monospace, SFMono-Regular,
      Menlo, monospace; color: var(--ink); }
    .dlg-hint { font-size: 12.5px; color: rgb(140,136,132); margin: 7px 0 0; }
    .dlg-row { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
    .dlg-row .dlg-l { margin: 0; flex: 1; }
    .dlg-tog { width: 34px; height: 20px; border-radius: 999px; background: rgb(95,187,116);
      position: relative; flex: 0 0 34px; }
    .dlg-tog i { position: absolute; top: 2.5px; left: 16.5px; width: 15px; height: 15px;
      border-radius: 999px; background: #fff; }
    .dlg-box { border: 1px solid rgba(18,10,11,.13); border-radius: 9px;
      padding: 12px 13px; background: rgb(250,249,247); }
    .dlg-box p { margin: 0 0 7px; font-size: 13.5px; line-height: 1.5; color: rgb(70,66,62); }
    .dlg-box p:last-child { margin-bottom: 0; }
    .dlg-box b { color: var(--ink); }
    .dlg-sect { font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
      color: rgb(140,136,132); margin: 20px 0 10px; }
    .dlg-msg { border: 1px solid rgba(18,10,11,.13); border-radius: 9px;
      padding: 10px 12px; font-size: 14px; color: rgb(70,66,62); font-style: italic; }

    /* the rows that show the tool reading a real order record */
    .dlg-db { border: 1px solid rgba(18,10,11,.13); border-radius: 9px; overflow: hidden; }
    .dlg-db div { display: flex; align-items: center; gap: 9px; padding: 8px 12px;
      font-size: 13px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      color: rgb(70,66,62); }
    .dlg-db div + div { border-top: 1px solid rgba(18,10,11,.07); }
    .dlg-db i { width: 6px; height: 6px; border-radius: 999px; flex: 0 0 6px;
      background: rgb(139,185,159); font-style: normal; }
    .dlg-db em { margin-left: auto; font-style: normal; font-family: Inter, sans-serif;
      font-size: 12.5px; color: rgb(140,136,132); }

    /* ---- animation ------------------------------------------------------
       Runs only when the block is on screen, only above 900px, and never when
       the visitor has asked for reduced motion. Nothing here changes the size
       of anything: the search text sits in a fixed-height row and filtering
       dims rows rather than removing them, so the animation cannot move the
       page under someone's cursor. */
    .dlg-caret { display: inline-block; width: 1px; height: 1em; margin-left: 1px;
      background: rgb(120,116,112); vertical-align: -2px; opacity: 0; }
    .pr-anim .dlg-caret { animation: prBlink 1s steps(1) infinite; }
    @keyframes prBlink { 0%,49% { opacity: 1 } 50%,100% { opacity: 0 } }
    .dlg-item { transition: opacity .35s ease, background-color .35s ease; }
    .dlg-item.dim { opacity: .28; }
    .dlg-b.go { transition: transform .18s ease, box-shadow .18s ease; }
    .dlg-b.go.hit { transform: translateY(1px);
      box-shadow: 0 0 0 4px rgba(139,185,159,.28); }
    .dlg-db div { opacity: 1; transition: opacity .4s ease; }
    .pr-anim .dlg-db div.pending { opacity: .22; }

    @media (max-width: 900px) {
      .pr-pair { padding: 72px 22px 72px; }
      .pr-pair h2 { font-size: 31px; letter-spacing: -.8px; }
      .pr-pair-grid { grid-template-columns: 1fr; gap: 16px; }
    }

    /* ============ Product: the two chapters as ONE dark section ============ */
    /* Daniel, 14 Aug: "consolidate this into one section only and break it from
       the previous one with a section title." Two consecutive full-width dark
       bands read as two unrelated things; they are one idea - what the agent is
       told, and how that changes. So: one band, one title, two rows inside it,
       and the rows still alternate sides. */
    .pr-group { padding-top: 104px; padding-bottom: 104px; }
    .pr-group-head { text-align: center; max-width: 780px; margin: 0 auto 72px; }
    .pr-group-head .eyebrow { color: rgb(200,240,74); font-size: 13px;
      font-weight: 700; letter-spacing: 2.5px; margin: 0 0 16px; }
    .pr-group-head h2 { color: rgb(248,244,241); font-size: 44px; font-weight: 700;
      letter-spacing: -1.5px; line-height: 1.1; margin: 0; }
    .pr-row + .pr-row { margin-top: 84px; padding-top: 84px;
      border-top: 1px solid rgba(248,244,241,.13); }
    .pr-row .eyebrow { color: rgb(200,240,74); }
    /* The rows are h2-in-column, so the headline and the illustration start on
       the same line. Flip moves the illustration to the left on alternate rows;
       DOM order stays copy-first so a screen reader is unaffected. */
    .pr-row.flip .queue-grid > .qcopy { order: 2; }
    .pr-row.flip .queue-grid > .queue-viz { order: 1; }
    @media (max-width: 900px) {
      .pr-group { padding-top: 72px; padding-bottom: 72px; }
      .pr-group-head { margin-bottom: 48px; }
      .pr-group-head h2 { font-size: 31px; letter-spacing: -.8px; }
      .pr-row + .pr-row { margin-top: 56px; padding-top: 56px; }
      .pr-row.flip .queue-grid > .qcopy,
      .pr-row.flip .queue-grid > .queue-viz { order: 0; }
    }

    /* ============ Product: the brief card (chapter 01) ============ */
    .bf { border: 1px solid rgba(248,244,241,.16); border-radius: 14px;
      background: rgba(248,244,241,.04); padding: 16px 17px 15px; }
    .bf-h { display: flex; align-items: center; gap: 9px; padding-bottom: 12px;
      border-bottom: 1px solid rgba(248,244,241,.13); margin-bottom: 13px; }
    .bf-h b { color: rgb(248,244,241); font-size: 14.5px; letter-spacing: -.15px; }
    .bf-h span { margin-left: auto; font-size: 11.5px; letter-spacing: 1.1px;
      color: rgba(248,244,241,.5); }
    .bf-row { display: flex; align-items: baseline; gap: 11px; padding: 7px 0; }
    .bf-n { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px; color: rgb(200,240,74); flex: 0 0 auto; }
    .bf-row p { margin: 0; color: rgba(248,244,241,.86); font-size: 15px;
      line-height: 1.45; }
    .bf-foot { margin-top: 13px; padding-top: 12px;
      border-top: 1px solid rgba(248,244,241,.13); display: flex;
      align-items: center; gap: 8px; font-size: 13.5px;
      color: rgba(248,244,241,.6); }
    .bf-dot { width: 7px; height: 7px; border-radius: 999px; flex: 0 0 7px;
      background: rgb(200,240,74); }

    /* ============ Product: alternating sides ============ */
    /* Daniel, 14 Aug: "the first screenshot should be full width, but not the
       rest - too many full widths are not good for readability." So exactly one
       full-bleed image on the page (.pr-shot) and every chapter after it runs as
       a two-column row, with the side flipping so the page does not read as a
       stack down one edge. Ordering is done in CSS, not in the markup, so the
       copy stays first in the DOM and a screen reader still hears headline ->
       prose -> illustration. */
    .pr-flip .queue-grid > .qcopy { order: 2; }
    .pr-flip .queue-grid > .queue-viz { order: 1; }
    @media (max-width: 900px) {
      /* On one column the flip would put the picture above its own headline. */
      .pr-flip .queue-grid > .qcopy { order: 0; }
      .pr-flip .queue-grid > .queue-viz { order: 0; }
    }

    /* ============ Product: the managed-service steps ============ */
    /* Was "who actually touches this" - three cards splitting the work between
       us and the customer. Daniel, 14 Aug: make it read as the PROCESS they can
       expect, and make it obvious we do all of it and the only thing they supply
       is guidance and what they know. So: four numbered steps, three of them
       ours, each with an icon. */
    .pr-hands { max-width: 1200px; margin: 0 auto; padding: 104px 40px 0; }
    .pr-hands-head { text-align: center; max-width: 760px; margin: 0 auto 48px; }
    .pr-hands .eyebrow { color: rgb(120,118,117); font-size: 13px; font-weight: 700;
      letter-spacing: 2.5px; margin: 0 0 16px; }
    .pr-hands h2 { color: var(--ink); font-size: 44px; font-weight: 700;
      letter-spacing: -1.5px; line-height: 1.1; margin: 0 0 18px; }
    .pr-hands .pb-lede { color: var(--gray); font-size: 17.5px; line-height: 1.7;
      margin: 0 auto; max-width: 58ch; }
    .pr-hands-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr));
      gap: 18px; }
    .pr-step { border: 1px solid rgba(18,10,11,.12); border-radius: 16px;
      padding: 24px 22px 26px; background: #fff; position: relative; }
    .pr-step-ic { width: 46px; height: 46px; border-radius: 13px; display: flex;
      align-items: center; justify-content: center; margin-bottom: 18px;
      background: rgb(238,247,205); }
    .pr-step-ic svg { width: 23px; height: 23px; fill: none; stroke: rgb(60,74,20);
      stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
    /* The customer's own step is the one that looks different - it is the only
       thing being asked of them, so it should be the one the eye lands on. */
    .pr-step.is-you { background: rgb(18,10,11); border-color: rgb(18,10,11); }
    .pr-step.is-you .pr-step-ic { background: rgb(200,240,74); }
    .pr-step.is-you .pr-step-ic svg { stroke: rgb(18,10,11); }
    .pr-step.is-you h3 { color: rgb(248,244,241); }
    .pr-step.is-you p { color: rgba(248,244,241,.72); }
    .pr-step.is-you .pr-step-n { color: rgb(200,240,74); }
    .pr-step-n { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px; font-weight: 700; color: rgb(150,146,142);
      letter-spacing: .5px; display: block; margin-bottom: 8px; }
    .pr-step h3 { color: var(--ink); font-size: 18px; font-weight: 700;
      letter-spacing: -.3px; line-height: 1.25; margin: 0 0 10px; }
    .pr-step p { color: var(--gray); font-size: 15px; line-height: 1.6; margin: 0; }

    @media (max-width: 1100px) {
      .pr-hands-grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
    }
    @media (max-width: 640px) {
      .pr-hands { padding: 72px 22px 0; }
      .pr-hands h2 { font-size: 31px; letter-spacing: -.8px; }
      .pr-hands-grid { grid-template-columns: 1fr; }
    }

    @media (max-width: 900px) {
      .tv { grid-template-columns: 1fr; }
      .pr-shot { padding: 44px 22px 0; }
      /* The two-column flex squeezes the bold half into a three-line column on
         a phone. Stack it instead. */
      .tv-foot { display: block; position: relative; padding-left: 32px; }
      .tv-foot .tv-dot { position: absolute; left: 15px; top: 19px; }
      .tv-foot b { display: block; margin-bottom: 2px; }
    }
"""

# ---------------------------------------------------------------------------
# The tools diagram. Abstract, drawn from the real "Assign tool" dialog and the
# transfer_call settings screen - the five conditions below are the same shape
# as the real rule, rewritten from 200 words of prompt into something a CEO
# reads in six seconds.
# ---------------------------------------------------------------------------
_TOOL_ICONS = {
    "search": ('#e9f1fa', '#3d81c9',
               '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>'),
    "order":  ('#e8f4ec', '#3f9a63',
               '<path d="M4 5h16v14H4z"/><path d="M8 10h8M8 14h5"/>'),
    "track":  ('#e8f4ec', '#3f9a63',
               '<path d="M3 8h13v9H3zM16 11h3.5L21 14v3h-5"/>'
               '<circle cx="7" cy="18.5" r="1.8"/><circle cx="18" cy="18.5" r="1.8"/>'),
    "person": ('#f7ebf1', '#b2557f',
               '<path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/>'
               '<circle cx="10" cy="7" r="3.6"/><path d="M20 8v6M23 11h-6"/>'),
    "hook":   ('#fdf1d9', '#e8981f',
               '<path d="M12 20V9M8 13l4-4 4 4"/><path d="M4 5h16"/>'),
}

TOOLS_VIZ_TEXT = {
    "en": dict(
        tools_h="TOOLS ON THIS AGENT",
        rule_h="WHEN <code>TRANSFER_CALL</code> FIRES",
        say_h="AND IT SAYS, BEFORE IT TRANSFERS",
        tools=[("search", "search_products", "Search the catalogue"),
               ("order", "get_order", "Find an order by number"),
               ("track", "where_is_my_order", "Live tracking status"),
               ("person", "transfer_call", "Hand over to a person"),
               ("hook", "webhook", "Write the outcome to your systems")],
        rules=["The answer isn't in the knowledge base.",
               "They ask about a specific model, price or stock level.",
               "The product sits outside the categories we cover.",
               "An order needs changing, or something arrived damaged.",
               "They ask for a person - or they're clearly annoyed."],
        say="&ldquo;One moment &mdash; I&rsquo;m putting you through to a "
            "colleague now.&rdquo;",
        foot_b="You never write any of this.",
        foot_e="We do, and we keep it current as your catalogue changes.",
    ),
    "it": dict(
        tools_h="STRUMENTI DI QUESTO AGENTE",
        rule_h="QUANDO SCATTA <code>TRANSFER_CALL</code>",
        say_h="E PRIMA DI PASSARE, DICE",
        tools=[("search", "search_products", "Cerca a catalogo"),
               ("order", "get_order", "Trova un ordine dal numero"),
               ("track", "where_is_my_order", "Stato spedizione, live"),
               ("person", "transfer_call", "Passa a una persona"),
               ("hook", "webhook", "Scrive l'esito nei tuoi sistemi")],
        rules=["La risposta non \u00e8 nella knowledge base.",
               "Chiedono un modello, un prezzo o una disponibilita' precisa.",
               "Il prodotto \u00e8 fuori dalle categorie che copriamo.",
               "Un ordine va modificato, o \u00e8 arrivato qualcosa di rotto.",
               "Chiedono una persona - o si sono chiaramente innervositi."],
        say="&ldquo;Un attimo, le passo subito un collega.&rdquo;",
        foot_b="Tutto questo non lo scrivi tu.",
        foot_e="Lo scriviamo noi, e lo aggiorniamo quando cambia il catalogo.",
    ),
}


def tools_viz(lang):
    t = TOOLS_VIZ_TEXT[lang]
    tools = ""
    for key, name, line in t["tools"]:
        bg, stroke, path = _TOOL_ICONS[key]
        tools += ('<div class="tv-tool"><span class="tv-ic" style="background:%s">'
                  '<svg viewBox="0 0 24 24" stroke="%s" aria-hidden="true">%s</svg>'
                  '</span><span><code>%s</code><em>%s</em></span></div>'
                  % (bg, stroke, path, esc(name), esc(line)))
    rules = "".join('<div class="tv-rule"><span class="tv-n">%d</span><p>%s</p></div>'
                    % (i + 1, esc(r)) for i, r in enumerate(t["rules"]))
    return ('<div class="tv">'
            '<div class="tv-card"><p class="tv-eyebrow">%s</p>%s</div>'
            '<div class="tv-card"><p class="tv-eyebrow">%s</p>%s'
            '<div class="tv-say"><p class="tv-eyebrow">%s</p>'
            '<div class="tv-bubble">%s</div></div></div>'
            '<div class="tv-foot"><span class="tv-dot"></span>'
            '<span><b>%s</b> <em>%s</em></span></div>'
            '</div>'
            % (esc(t["tools_h"]), tools, t["rule_h"], rules,
               esc(t["say_h"]), t["say"], esc(t["foot_b"]), esc(t["foot_e"])))


RELEASE_FLOW_TEXT = {
    "en": [("Draft", "A change is written. Nothing about the live agent moves.", False),
           ("Test", "Call the draft yourself and hear it handle the awkward one.", False),
           ("Publish", "It goes live. The version before it is still kept.", True)],
    "it": [("Bozza", "La modifica \u00e8 scritta. Sull'agente vero non cambia niente.", False),
           ("Prova", "Chiami la bozza e te la senti gestire il caso scomodo.", False),
           ("Pubblica", "Va online. La versione precedente resta comunque l\u00ec.", True)],
}


BRIEF_TEXT = {
    "en": dict(title="System message", chip="PLAIN ENGLISH",
               rows=["Who you are, and who you are answering for.",
                     "How to talk. Short sentences. No jargon.",
                     "What you must never promise.",
                     "When to stop and pass the call to a person."],
               foot="Every edit dated and kept."),
    "it": dict(title="Istruzioni", chip="IN ITALIANO",
               rows=["Chi sei, e per conto di chi rispondi.",
                     "Come parlare. Frasi corte. Niente tecnicismi.",
                     "Cosa non devi promettere mai.",
                     "Quando fermarti e passare la chiamata a una persona."],
               foot="Ogni modifica registrata, con la data."),
}


def brief_viz(lang):
    t = BRIEF_TEXT[lang]
    rows = "".join('<div class="bf-row"><span class="bf-n">%d.</span><p>%s</p></div>'
                   % (i + 1, esc(r)) for i, r in enumerate(t["rows"]))
    return ('<div class="bf"><div class="bf-h"><b>%s</b><span>%s</span></div>%s'
            '<div class="bf-foot"><span class="bf-dot"></span>%s</div></div>'
            % (esc(t["title"]), esc(t["chip"]), rows, esc(t["foot"])))


def release_flow(lang):
    parts = []
    for i, (title, line, live) in enumerate(RELEASE_FLOW_TEXT[lang]):
        if i:
            parts.append('<div class="rf-arrow"></div>')
        parts.append('<div class="rf-step%s"><span class="rf-k">%d</span>'
                     '<span><b>%s</b><em>%s</em></span></div>'
                     % (" is-live" if live else "", i + 1, esc(title), esc(line)))
    return '<div class="rf">%s</div>' % "".join(parts)


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# The pair of dialogs that follow the anchor screenshot. Drawn from the real
# "Assign a tool to this agent" dialog and the transfer_call settings screen,
# rebuilt as markup so they stay readable at half width on a phone.
# ---------------------------------------------------------------------------
PAIR_TEXT = {
    "en": dict(
        assign_t="Assign", assign_s="Assign a tool to this agent",
        tools_l="Tools", select="Select", search="Search for a tool",
        typed="where",
        items=["search_products", "get_order", "where_is_my_order",
               "transfer_call", "webhook"], on="where_is_my_order",
        cancel="Cancel", add="Add",
        set_t="Settings \u00b7 where_is_my_order", set_s="This tool\u2019s settings",
        fn_l="Function name", fn="where_is_my_order",
        fn_hint="Called by the model, never by the caller.",
        en_l="Enabled",
        when_l="When to call this tool",
        when=["<b>Do</b> call it the moment somebody asks where their order is, "
              "when it will arrive, or why it is late.",
              "<b>Don\u2019t</b> call it before you have an order number \u2014 "
              "ask for it, or use the number they are calling from."],
        db_l="READS FROM YOUR ORDER SYSTEM",
        db=[("order.status", "Packed"),
            ("order.carrier", "BRT"),
            ("order.tracking", "0A47\u20268812"),
            ("order.promised_date", "Thu 21 Aug")],
        msg_l="FILLER MESSAGE",
        msg="\u201cLet me look that up \u2014 one second.\u201d"),
    "it": dict(
        assign_t="Assegna", assign_s="Assegna uno strumento a questo agente",
        tools_l="Strumenti", select="Seleziona", search="Cerca uno strumento",
        typed="where",
        items=["search_products", "get_order", "where_is_my_order",
               "transfer_call", "webhook"], on="where_is_my_order",
        cancel="Annulla", add="Aggiungi",
        set_t="Impostazioni \u00b7 where_is_my_order",
        set_s="Impostazioni dello strumento",
        fn_l="Nome della funzione", fn="where_is_my_order",
        fn_hint="La chiama il modello, mai il cliente.",
        en_l="Attivo",
        when_l="Quando usare questo strumento",
        when=["<b>Usalo</b> appena qualcuno chiede dov\u2019\u00e8 il suo "
              "ordine, quando arriva o perch\u00e9 \u00e8 in ritardo.",
              "<b>Non usarlo</b> senza un numero d\u2019ordine: chiedilo, "
              "oppure parti dal numero da cui stanno chiamando."],
        db_l="LEGGE DAL TUO GESTIONALE ORDINI",
        db=[("order.status", "Imballato"),
            ("order.carrier", "BRT"),
            ("order.tracking", "0A47\u20268812"),
            ("order.promised_date", "gio 21 ago")],
        msg_l="MESSAGGIO DI ATTESA",
        msg="\u201cGuardo subito, un attimo solo.\u201d"),
}


def pair_panels(lang):
    """The two dialogs, drawn from the real Assign and tool-settings screens.

    Live markup, not pictures: at half width on a 390px phone an image of this
    UI would render its 13px labels at about 6px.
    """
    t = PAIR_TEXT[lang]
    items = "".join('<div class="dlg-item%s" data-tool="%s">%s</div>'
                    % (" on" if i == t["on"] else "", esc(i), esc(i))
                    for i in t["items"])
    assign = ('<div class="dlg">'
              '<div class="dlg-h"><b>%s</b><span>%s</span></div>'
              '<p class="dlg-l">%s</p>'
              '<div class="dlg-sel">%s</div>'
              '<div class="dlg-menu">'
              '<div class="dlg-search"><span data-typed>%s</span>'
              '<span class="dlg-caret"></span></div>%s</div>'
              '<div class="dlg-btns"><span class="dlg-b gh">%s</span>'
              '<span class="dlg-b go">%s</span></div></div>'
              % (esc(t["assign_t"]), esc(t["assign_s"]), esc(t["tools_l"]),
                 esc(t["select"]), esc(t["search"]), items,
                 esc(t["cancel"]), esc(t["add"])))
    when = "".join("<p>%s</p>" % w for w in t["when"])
    db = "".join('<div><i></i>%s<em>%s</em></div>' % (esc(k), esc(v))
                 for k, v in t["db"])
    settings = ('<div class="dlg">'
                '<div class="dlg-h"><b>%s</b><span>%s</span></div>'
                '<div class="dlg-row"><p class="dlg-l">%s</p>'
                '<p class="dlg-l" style="flex:0 0 auto">%s</p>'
                '<span class="dlg-tog"><i></i></span></div>'
                '<div class="dlg-field">%s</div>'
                '<p class="dlg-hint">%s</p>'
                '<p class="dlg-sect">%s</p>'
                '<div class="dlg-box">%s</div>'
                '<p class="dlg-sect">%s</p>'
                '<div class="dlg-db">%s</div>'
                '<p class="dlg-sect">%s</p>'
                '<div class="dlg-msg">%s</div></div>'
                % (esc(t["set_t"]), esc(t["set_s"]), esc(t["fn_l"]), esc(t["en_l"]),
                   esc(t["fn"]), esc(t["fn_hint"]), esc(t["when_l"]), when,
                   esc(t["db_l"]), db, esc(t["msg_l"]), esc(t["msg"])))
    return ('<div class="pr-pair-grid" data-typed-word="%s">%s%s</div>'
            % (esc(t["typed"]), assign, settings))


# ---------------------------------------------------------------------------
# The animation. Deliberately small.
#
# Rules it obeys, because an animation that breaks any of them is worse than a
# static picture:
#   - never runs below 900px. A cursor-and-typing sequence on a touch device is
#     nonsense, and it is where most of this traffic actually is.
#   - never runs under prefers-reduced-motion.
#   - only runs while on screen, so it is not burning a phone battery three
#     screens above the fold.
#   - moves NOTHING. Filtering dims rows instead of removing them, and the typed
#     text sits in a fixed-height row, so no step can shift the page.
# ---------------------------------------------------------------------------
ANIM_JS = """<script>(function(){
var g=document.querySelector('.pr-pair-grid');if(!g)return;
var mq=window.matchMedia('(min-width:901px)'),rm=window.matchMedia('(prefers-reduced-motion:reduce)');
var typed=g.querySelector('[data-typed]'),base=typed?typed.textContent:'',
    items=[].slice.call(g.querySelectorAll('.dlg-item')),
    add=g.querySelector('.dlg-b.go'),rows=[].slice.call(g.querySelectorAll('.dlg-db div')),
    word=g.getAttribute('data-typed-word')||'',t=[],on=false;
function clear(){t.forEach(clearTimeout);t=[];}
function at(ms,fn){t.push(setTimeout(fn,ms));}
function reset(){if(typed)typed.textContent=base;items.forEach(function(e){e.classList.remove('dim');});
  rows.forEach(function(r){r.classList.add('pending');});if(add)add.classList.remove('hit');}
function run(){
  clear();reset();
  var d=700;
  for(var i=1;i<=word.length;i++)(function(i){at(d+i*110,function(){
    if(typed)typed.textContent=word.slice(0,i);});})(i);
  d+=word.length*110+260;
  at(d,function(){items.forEach(function(e){
    if(e.getAttribute('data-tool').indexOf(word)!==0)e.classList.add('dim');});});
  at(d+700,function(){if(add)add.classList.add('hit');});
  at(d+1000,function(){if(add)add.classList.remove('hit');});
  rows.forEach(function(r,i){at(d+1200+i*330,function(){r.classList.remove('pending');});});
  at(d+1200+rows.length*330+2600,function(){if(on)run();});
}
function stop(){on=false;clear();if(typed)typed.textContent=base;
  items.forEach(function(e){e.classList.remove('dim');});
  rows.forEach(function(r){r.classList.remove('pending');});g.classList.remove('pr-anim');}
function start(){if(on)return;on=true;g.classList.add('pr-anim');run();}
function eligible(){return mq.matches&&!rm.matches;}
if('IntersectionObserver' in window){
  new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting&&eligible())start();else stop();});},{threshold:.35}).observe(g);
} 
['change'].forEach(function(){});
mq.addEventListener&&mq.addEventListener('change',function(){if(!eligible())stop();});
rm.addEventListener&&rm.addEventListener('change',function(){if(!eligible())stop();});
})();</script>"""


def section_pair(d, lang):
    """A statement, then two half-width panels proving it."""
    p = d["pair"]
    return """
    <section class="pr-pair">
      <p class="eyebrow">%s</p>
      <h2>%s</h2>
      <p class="pb-lede">%s</p>
      %s
      %s
    </section>""" % (esc(p["eyebrow"]), nb(esc(p["h2"])), esc(p["lede"]),
                     pair_panels(lang), ANIM_JS)


def section_blocks(d):
    """Every chapter inside ONE dark band, under one section title.

    Replaces the previous one-section-per-chapter rendering. Each chapter keeps
    its own eyebrow, headline and illustration, and alternate rows flip the
    illustration to the left; what goes away is the second full-width dark
    background, which made two halves of one argument look like two subjects.
    """
    g = d["group"]
    rows = []
    for i, b in enumerate(d["blocks"]):
        body = "".join('<p class="qbody">%s</p>' % p for p in b["body"])
        fine = '<p class="fine">%s</p>' % b["fine"] if b.get("fine") else ""
        grid = ('<div class="queue-grid pb-h2col">'
                '<div class="qcopy"><p class="eyebrow">%s</p><h2>%s</h2>%s</div>'
                '<div class="queue-viz">%s%s</div></div>'
                % (esc(b["eyebrow"]), nb(esc(b["h2"])), body, b["viz"], fine))
        rows.append('<div class="pr-row%s">%s</div>'
                    % (" flip" if b.get("flip") else "", grid))
    return """
    <section class="queue-band pr-group">
      <div class="queue-inner">
        <div class="pr-group-head">
          <p class="eyebrow">%s</p>
          <h2>%s</h2>
        </div>
        %s
      </div>
    </section>""" % (esc(g["eyebrow"]), nb(esc(g["h2"])), "".join(rows))


def section_shot(d):
    """The platform screenshot, full-bleed, directly under the hero.

    <picture> with a phone-specific crop, not one image scaled down. The wide
    shot at 390px renders its UI labels below 3px - see the module docstring.
    """
    s = d["shot"]
    return """
    <section class="pr-shot">
      <figure>
        <picture>
          <source media="(max-width: 810px)" srcset="%s-phone.webp">
          <img src="%s.webp" alt="%s" width="1560" height="796" loading="lazy" decoding="async">
        </picture>
        <figcaption>%s</figcaption>
      </figure>
    </section>""" % (s["src"], s["src"], esc(s["alt"]), esc(s["caption"]))


STEP_ICONS = {
    # 1 - the customer talking: a speech bubble with a spark
    "talk": '<path d="M20 12a8 8 0 0 1-8.5 8 8.6 8.6 0 0 1-3.7-.9L3 21l1.8-4.8A8 8 0 0 1 4 12a8 8 0 0 1 16 0z"/>'
            '<path d="M12 8.4l.8 1.9 1.9.8-1.9.8-.8 1.9-.8-1.9-1.9-.8 1.9-.8z"/>',
    # 2 - us building: blocks being assembled
    "build": '<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/>'
             '<rect x="3" y="13" width="8" height="8" rx="2"/><path d="M17 13v8M13 17h8"/>',
    # 3 - listening to the draft before it ships
    "hear": '<path d="M4 13v-1a8 8 0 0 1 16 0v1"/><rect x="2.5" y="13" width="4.5" height="6" rx="2"/>'
            '<rect x="17" y="13" width="4.5" height="6" rx="2"/><path d="M19.2 19v.6a2.6 2.6 0 0 1-2.6 2.6H13"/>',
    # 4 - running it and keeping it current
    "run": '<path d="M20.5 12a8.5 8.5 0 1 1-2.6-6.1"/><path d="M20.8 4.2v4.4h-4.4"/>'
           '<path d="M8.5 14.5l2.6-2.9 2.2 1.9 3.1-3.6"/>',
}


def section_hands(d):
    """The managed-service process, in four steps.

    Replaces the old three-card us/you split. Daniel, 14 Aug: it should read as
    the process they can expect, and make plain that we do all of it and the
    only thing they supply is guidance and what only they know.

    Step one is styled differently from the other three ON PURPOSE - it is the
    only thing being asked of the customer, so it should be the tile the eye
    lands on. The other three being visually identical is the argument.
    """
    h = d["hands"]
    cards = []
    for i, (icon, title, body, mine) in enumerate(h["steps"], 1):
        cards.append('<div class="pr-step%s"><span class="pr-step-ic">'
                     '<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span>'
                     '<span class="pr-step-n">%s %d</span>'
                     '<h3>%s</h3><p>%s</p></div>'
                     % (" is-you" if mine else "", STEP_ICONS[icon],
                        esc(h["step_word"]), i, esc(title), esc(body)))
    return """
    <section class="pr-hands">
      <div class="pr-hands-head">
        <p class="eyebrow">%s</p>
        <h2>%s</h2>
        <p class="pb-lede">%s</p>
      </div>
      <div class="pr-hands-grid">%s</div>
    </section>""" % (esc(h["eyebrow"]), nb(esc(h["h2"])), esc(h["lede"]),
                     "".join(cards))


def template(lang):
    t = pb.template(lang)                       # playbook CSS + hero furniture
    base = LANGS[lang]["base"] % "{{SLUG}}"
    t = t.replace("https://www.sabato.ai" + (pb.LANGS[lang]["base"] % "{{SLUG}}"),
                  "https://www.sabato.ai" + base)
    t = t.replace(">%s<" % esc(pb.LANGS[lang]["hand"]),
                  ">%s<" % esc(LANGS[lang]["hand"]))
    t = t.replace("  </style>", PRODUCT_CSS + "  </style>", 1)
    return t


def jsonld(slug, d, lang):
    url = "https://www.sabato.ai" + (LANGS[lang]["base"] % slug)
    out = [{
        "@context": "https://schema.org", "@type": "WebPage",
        "name": re.sub(r"\[/?nb\]", "", d["h1"].replace("[br]", " ")).strip(),
        "description": d["description"],
        "url": url,
        "inLanguage": lang,
        "isPartOf": {"@type": "WebSite", "name": "Sabato AI",
                     "url": "https://www.sabato.ai"},
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
    """Both directions or neither - a one-sided hreflang is worse than none."""
    en = slug if lang == "en" else PRODUCTS_IT[slug]["en"]
    it = slug if lang == "it" else PRODUCTS[slug].get("it")
    if not it:
        return ""
    return ('<link rel="alternate" hreflang="en" href="https://www.sabato.ai/product/%s">'
            '<link rel="alternate" hreflang="it" href="https://www.sabato.ai/it/prodotto/%s">'
            '<link rel="alternate" hreflang="x-default" href="https://www.sabato.ai/product/%s">'
            % (en, it, en))


def build(lang, slug, d):
    cfg = LANGS[lang]
    # The viz token is swapped for real markup here rather than in the data
    # file, so the copy file never has to hold a line of HTML.
    d = dict(d)
    d["blocks"] = [dict(b) for b in d["blocks"]]
    for b in d["blocks"]:
        if b.get("viz") == "TOOLS_VIZ":
            b["viz"] = tools_viz(lang)
        elif b.get("viz") == "RELEASE_FLOW":
            b["viz"] = release_flow(lang)
        elif b.get("viz") == "BRIEF_VIZ":
            b["viz"] = brief_viz(lang)

    sections = "".join([
        section_shot(d),
        section_pair(d, lang),
        section_blocks(d),
        section_hands(d),
        pb.section_proof(d, lang),
        pb.section_faq(d),
        pb.section_cta(d, lang),
    ])
    page = (template(lang)
            .replace("{{TITLE}}", html.escape(d["title"]))
            .replace("{{DESCRIPTION}}", html.escape(d["description"]))
            .replace("{{SLUG}}", slug)
            .replace("{{JSONLD}}", jsonld(slug, d, lang) + hreflang(slug, lang))
            .replace("{{CHIP}}", esc(d["chip"]))
            .replace("{{H1}}", nb(esc(d["h1"])))
            .replace("{{SUB}}", esc(d["sub"]))
            .replace("{{HERO_VISUAL}}", d.get("hero_visual", ""))
            .replace("{{SECTIONS}}", sections))
    os.makedirs(cfg["out"], exist_ok=True)
    p = os.path.join(cfg["out"], slug + ".html")
    open(p, "w", encoding="utf-8").write(page)
    print("  wrote %s" % p)
    return "https://www.sabato.ai" + (cfg["base"] % slug)


def main():
    urls = []
    for slug in ORDER:
        urls.append(build("en", slug, PRODUCTS[slug]))
    for slug in ORDER_IT:
        urls.append(build("it", slug, PRODUCTS_IT[slug]))
    print("  sitemap: %d new URL(s) added" % pb.sitemap_add(urls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
