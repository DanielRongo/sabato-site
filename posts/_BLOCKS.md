# Blog blocks - authoring cheat-sheet

Paste these straight into a post body (`posts/en/*.md`, `posts/it/*.md`) or into a
Google Sheet cell. Every block is a fence: a line that starts with `:::name`, then
one item per line, then a closing line with just `:::`.

Rules that apply to all blocks:

* **One item per line.** No indentation needed. Blank lines inside a block are ignored
  (except in `:::keystat`, where a blank line starts a second stat card).
* **Nothing is invented.** A block renders exactly the text you give it - numbers, labels,
  sources, order. If you don't supply a source line, no source line appears.
* **A typo can't break the page.** If a block is malformed, its lines are rendered as
  ordinary paragraphs and `publish.py` prints a warning in the build log.
* Inline markdown works on every line: `**bold**`, `*italic*`, `[link](https://…)`, `` `code` ``.
* Fixed labels follow the post's language automatically: *The takeaway* / *In sintesi*,
  *What to do* / *Cosa fare*, *Source:* / *Fonte:*.
* Leading `-` or `1.` bullets are optional - they're stripped either way.

---

## 1. `:::keystat` - big lime number on a black card

```
:::keystat
68%
of European shoppers have returned an online purchase
Source: DHL, 2025
:::
```

Line 1 = the number. Line 2 = the label. `Source:` (or `Fonte:`) is optional and always last.
Separate two stats with a **blank line** to get a two-up card row:

```
:::keystat
57%
of German shoppers buy only in their own language
Source: CSA Research, 2020

29
countries surveyed
Source: CSA Research, 2020
:::
```

## 2. `:::takeaway` - the save-worthy summary box

```
:::takeaway
Localise the market that already buys from you, not the biggest one on the map.
Germany goes first if it's in your top three.
One language at a time. Prove it, then add the next.
:::
```

Off-white card with a lime rule. The heading is automatic (*The takeaway* / *In sintesi*).
Override it if you must: `:::takeaway What this means for you`.

## 3. `:::action` - numbered "do this" checklist

```
:::action
What to do Monday morning
Pull last year's revenue by shipping country from your OMS.
Book five mystery calls in the buyer's language.
Score each market: revenue × language dependence × AOV.
:::
```

**First line = the heading**, every line after it is a numbered step.
Start the first line with `-` (or skip the heading entirely) to get the default
heading *What to do* / *Cosa fare*.

## 4. `:::compare` - two-column comparison card

```
:::compare Same question, two channels
Email flow | Voice call
First response | 4-12 hours | Under 30 seconds
Turns to resolve | 3 messages | One call
Data captured | Whatever they type | Order number, issue, photos
:::
```

First line = the two column headings, pipe-separated (exactly two).
Every line after = `row label | left value | right value` (exactly three).
The right-hand column is the highlighted one. Text after `:::compare` is an optional
title above the card. On mobile the rows stack into labelled cards.

## 5. `:::quote` - pull quote

```
:::quote
A monolingual line doesn't produce complaints. It produces silence.
 - Daniel Rongo, Sabato AI
:::
```

Large italic Satoshi with a lime vertical rule. A last line starting with ` - ` (em dash)
becomes the attribution; leave it out and you just get the quote.

## 6. Markdown tables - no fence needed

```
| Market | Share of revenue | AOV |
| --- | --- | --- |
| Germany | 34% | €142 |
| France | 21% | €118 |
```

Renders as a rounded card: uppercase header row on off-white with a lime underline,
striped rows, bold first column, horizontal scroll on mobile.

## 7. `:::chart bar` - horizontal bar chart

```
:::chart bar
Share who buy only at local-language sites
Germany | 57% | highest of 29 countries surveyed
France | 41%
Italy | 40%
Spain | 30%
Source: CSA Research, "Can't Read, Won't Buy", 2020
:::
```

* Optional **first line without a pipe** = the chart title.
* Data lines: `label | number | optional note`. The number is shown exactly as you type it
  (`57%`, `€1,240`, `4.2`); the bar length is scaled against the largest value in the block.
* Optional `Source:` / `Fonte:` line anywhere.
* Rendered as inline SVG (no libraries, no external requests) with a separate mobile
  variant so it stays legible at 390px.

---

## Publishing

```
pip install markdown
python3 publish.py
```

Warnings that read `! :::name skipped (…)` mean a block was malformed and got rendered as
plain text - fix the line the message quotes and re-run.
