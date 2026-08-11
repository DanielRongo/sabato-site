#!/usr/bin/env python3
"""Sabato blog publisher.

Reads markdown posts from posts/en/ and posts/it/, renders them through the
templates in blog-build/, writes post pages + blog indexes into site/, and
keeps site/sitemap.xml up to date. Re-run any time:  python3 publish.py
"""
import os, re, json, math, html
import urllib.parse
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
TPL = os.path.join(ROOT, "templates")
POSTS = os.path.join(ROOT, "posts")
BASE = "https://www.sabato.ai"
FAVICON = "/fuc/images/hWFOqN6Okd1QgfKhizqgIF1s.png"  # light-mode favicon (cards are off-white)

def load_dummy_slugs():
    p = os.path.join(ROOT, "dummy-posts.txt")
    if not os.path.exists(p):
        return set()
    out = set()
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line)
    return out

DUMMY_SLUGS = load_dummy_slugs()

LANGS = {
    "en": {
        "post_tpl": "blog-post-en.html",
        "index_tpl": "blog-index-en.html",
        "out_dir": os.path.join(SITE, "blog"),
        "index_out": os.path.join(SITE, "blog.html"),
        "url_prefix": "/blog",
        "read_label": lambda n: f"{n} min read",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "date_fmt": lambda d, m, y, mo: f"{mo} {d}, {y}",
        "byline": "<span>By Sabato AI</span>",
        "switch_label": "Leggi in italiano \U0001F1EE\U0001F1F9",
        "sibling_prefix": "/it/blog",
        "faq_heads": ("FAQ",),
        "src_heads": ("Sources",),
        "empty_state": (
            '<div style="grid-column:1/-1;text-align:center;padding:80px 20px;">\n'
            '  <p style="font-family:\'Satoshi\',sans-serif;font-weight:700;font-size:28px;'
            'color:rgb(18,10,11);margin:0 0 12px;">First posts are on the way.</p>\n'
            '  <p style="font-size:18px;color:rgb(69,65,64);margin:0;">Data-driven writing on '
            'voice AI and e-commerce operations. No fluff, sources on everything.</p>\n</div>'
        ),
        "inlang": "en",
        "labels": {
            "takeaway": "The takeaway",
            "action": "What to do",
            "source": "Source:",
            "chart_alt": "Bar chart.",
            "chart_credit": "\u00a9 2026 Sabato LTD \u00b7 sabato.ai",
            "share_label": "Share this chart",
            "share_native": "Share image",
            "share_copy": "Copy image",
            "share_copied": "Copied",
            "share_dl": "Download",
        },
    },
    "it": {
        "post_tpl": "blog-post-it.html",
        "index_tpl": "blog-index-it.html",
        "out_dir": os.path.join(SITE, "it", "blog"),
        "index_out": os.path.join(SITE, "it", "blog.html"),
        "url_prefix": "/it/blog",
        "read_label": lambda n: f"{n} min di lettura",
        "months": ["gen", "feb", "mar", "apr", "mag", "giu",
                   "lug", "ago", "set", "ott", "nov", "dic"],
        "date_fmt": lambda d, m, y, mo: f"{d} {mo} {y}",
        "byline": "<span>Di Sabato AI</span>",
        "switch_label": "Read in English \U0001F1EC\U0001F1E7",
        "sibling_prefix": "/blog",
        "faq_heads": ("FAQ", "Domande frequenti"),
        "src_heads": ("Fonti", "Sources"),
        "empty_state": (
            '<div style="grid-column:1/-1;text-align:center;padding:80px 20px;">\n'
            '  <p style="font-family:\'Satoshi\',sans-serif;font-weight:700;font-size:28px;'
            'color:rgb(18,10,11);margin:0 0 12px;">I primi articoli sono in arrivo.</p>\n'
            '  <p style="font-size:18px;color:rgb(69,65,64);margin:0;">Contenuti data-driven su '
            'voice AI e operazioni e-commerce. Zero fuffa, fonti per ogni numero.</p>\n</div>'
        ),
        "inlang": "it",
        "labels": {
            "takeaway": "In sintesi",
            "action": "Cosa fare",
            "source": "Fonte:",
            "chart_alt": "Grafico a barre.",
            "chart_credit": "\u00a9 2026 Sabato LTD \u00b7 sabato.ai",
            "share_label": "Condividi questo grafico",
            "share_native": "Condividi immagine",
            "share_copy": "Copia immagine",
            "share_copied": "Copiata",
            "share_dl": "Scarica",
        },
    },
}

COVERS = {  # cover_style -> (background, text color, extra css)
    "black": ("rgb(0,0,0)", "rgb(204,255,0)", ""),
    "lime": ("rgb(204,255,0)", "rgb(0,0,0)", ""),
    "offwhite": ("rgb(248,244,241)", "rgb(0,0,0)", "border-bottom:1px solid rgb(227,226,226);"),
}


def parse_post(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"﻿?---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    for req in ("title", "slug", "description", "category", "date", "cover_style"):
        if req not in fm:
            raise SystemExit(f"{path}: missing frontmatter key '{req}'")
    if fm["cover_style"] not in COVERS:
        raise SystemExit(f"{path}: cover_style must be one of {list(COVERS)}")
    return fm, m.group(2).strip()


def read_minutes(fm, body):
    if fm.get("read_time"):
        return int(re.sub(r"\D", "", fm["read_time"]) or 1)
    words = len(re.findall(r"[\wÀ-ſ']+", re.sub(r"<[^>]+>", " ", body)))
    return max(1, round(words / 200))


def fmt_date(iso, L):
    y, m, d = (int(x) for x in iso.split("-"))
    return L["date_fmt"](d, m, y, L["months"][m - 1])


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


MD = markdown.Markdown(extensions=["tables", "fenced_code"])
INLINE_MD = markdown.Markdown(extensions=[])

# ---------------------------------------------------------------------------
# Authored content blocks:   :::name [optional arg]  ...lines...  :::
# Each one renders as a designed component. Nothing is ever invented: the block
# renders exactly the text the markdown supplies. A malformed block falls back
# to plain paragraphs so a typo can never break the page.
# ---------------------------------------------------------------------------

BLOCK_RE = re.compile(r"^:::[ \t]*([A-Za-z][\w-]*)[ \t]*([^\n]*)\n(.*?)^:::[ \t]*$",
                      re.S | re.M)
BLOCK_TOKEN = "SABATOBLOCK%dENDBLOCK"
SRC_RE = re.compile(r"^\s*(?:sources?|fonte|fonti)\s*:\s*", re.I)
BULLET_RE = re.compile(r"^\s*(?:[-*• - ]|\d+[.)])\s+")


def esc(s):
    return html.escape(s, quote=False)


def inl(s):
    """Inline markdown (bold / links / code) for a single authored line."""
    INLINE_MD.reset()
    out = INLINE_MD.convert(s.strip()).strip()
    if out.startswith("<p>") and out.endswith("</p>"):
        out = out[3:-4]
    return out


def block_lines(raw):
    return [ln.strip() for ln in raw.strip("\n").splitlines() if ln.strip()]


def debullet(s):
    return BULLET_RE.sub("", s).strip()


def split_source(lines, L):
    """Pull a trailing/So-labelled 'Source: x' line out of a block."""
    rest, src = [], ""
    for ln in lines:
        if SRC_RE.match(ln):
            src = SRC_RE.sub("", ln).strip()
        else:
            rest.append(ln)
    return rest, src


def source_html(src, L, cls="stat-source"):
    if not src:
        return ""
    return (f'<p class="{cls}"><span class="src-lbl">{esc(L["labels"]["source"])}</span> '
            f'{inl(src)}</p>')


def parse_num(s):
    """Best-effort numeric value of a displayed figure ('57%', '1,240', '€4.2k')."""
    m = re.search(r"-?\d[\d.,\u00a0\u202f ]*", s)
    if not m:
        return None
    t = re.sub(r"[\u00a0\u202f ]", "", m.group(0)).rstrip(".,")
    if "," in t and "." in t:
        t = (t.replace(".", "").replace(",", ".") if t.rfind(",") > t.rfind(".")
             else t.replace(",", ""))
    elif "," in t:
        tail = t.rsplit(",", 1)[1]
        t = t.replace(",", "") if len(tail) == 3 else t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


# ---- individual blocks -----------------------------------------------------

def blk_keystat(arg, raw, L):
    groups = [g for g in re.split(r"\n[ \t]*\n", raw.strip("\n")) if g.strip()]
    cards = []
    for g in groups:
        lines, src = split_source(block_lines(g), L)
        if len(lines) < 2:
            raise ValueError("keystat needs a number line and a label line")
        number, label = lines[0], " ".join(lines[1:])
        cards.append(
            '<div class="stat-callout">'
            f'<p class="stat-number">{inl(number)}</p>'
            f'<p class="stat-label">{inl(label)}</p>'
            f'{source_html(src, L)}'
            '</div>')
    if len(cards) == 1:
        return cards[0]
    return '<div class="stat-grid">' + "".join(cards) + "</div>"


def blk_takeaway(arg, raw, L):
    lines = [debullet(x) for x in block_lines(raw)]
    if not lines:
        raise ValueError("empty takeaway")
    head = arg.strip() or L["labels"]["takeaway"]
    items = "".join(f"<li>{inl(x)}</li>" for x in lines)
    return ('<div class="takeaway">'
            f'<p class="tk-head">{esc(head)}</p>'
            f'<ul class="tk-list">{items}</ul></div>')


def blk_action(arg, raw, L):
    lines = block_lines(raw)
    if not lines:
        raise ValueError("empty action list")
    head = arg.strip()
    if not head:
        if BULLET_RE.match(lines[0]) or len(lines) == 1:
            head = L["labels"]["action"]
        else:
            head, lines = lines[0], lines[1:]
    if not lines:
        raise ValueError("action list has no steps")
    items = "".join(
        f'<li><span class="ab-num">{i}</span>'
        f'<span class="ab-text">{inl(debullet(x))}</span></li>'
        for i, x in enumerate(lines, 1))
    return ('<div class="action-block">'
            f'<p class="ab-head">{esc(head)}</p>'
            f'<ol class="ab-list">{items}</ol></div>')


def blk_compare(arg, raw, L):
    lines = block_lines(raw)
    if len(lines) < 2:
        raise ValueError("compare needs a heading line and at least one row")
    heads = [p.strip() for p in lines[0].split("|")]
    if len(heads) != 2 or not all(heads):
        raise ValueError("compare heading line needs exactly two columns")
    rows = []
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) != 3:
            raise ValueError("compare rows need 'label | left | right'")
        rows.append(parts)
    out = ['<div class="compare-wrap">']
    if arg.strip():
        out.append(f'<p class="cmp-title">{esc(arg.strip())}</p>')
    out.append('<div class="compare">')
    out.append('<div class="cmp-head"><div class="cmp-lbl"></div>'
               f'<div class="cmp-col">{inl(heads[0])}</div>'
               f'<div class="cmp-col accent">{inl(heads[1])}</div></div>')
    for label, left, right in rows:
        out.append(
            '<div class="cmp-row">'
            f'<div class="cmp-lbl">{inl(label)}</div>'
            f'<div class="cmp-cell"><span class="cmp-cap">{esc(heads[0])}</span>'
            f'<span class="cmp-val">{inl(left)}</span></div>'
            f'<div class="cmp-cell accent"><span class="cmp-cap">{esc(heads[1])}</span>'
            f'<span class="cmp-val">{inl(right)}</span></div>'
            '</div>')
    out.append("</div></div>")
    return "".join(out)


def blk_quote(arg, raw, L):
    lines = block_lines(raw)
    if not lines:
        raise ValueError("empty quote")
    attrib = ""
    if len(lines) > 1 and re.match(r"^( - | - |--)\s*", lines[-1]):
        attrib = re.sub(r"^( - | - |--)\s*", "", lines[-1]).strip()
        lines = lines[:-1]
    if not lines:
        raise ValueError("quote is attribution only")
    text = " ".join(lines)
    cap = f'<figcaption> - {inl(attrib)}</figcaption>' if attrib else ""
    return (f'<figure class="pullquote"><blockquote><p>{inl(text)}</p></blockquote>'
            f'{cap}</figure>')


def bar_svg(rows, cls, W, fs_lab, fs_val, fs_note, bar_h, gap):
    """Horizontal bar chart, no library. Bar length is exactly proportional."""
    top = max(abs(r[3]) for r in rows) or 1.0
    parts, y = [], 0.0
    for label, value, note, n in rows:
        base = y + fs_lab * 0.86
        parts.append(f'<text x="0" y="{base:g}" font-size="{fs_lab}" font-weight="700" '
                     f'fill="rgb(18,10,11)">{esc(label)}</text>')
        parts.append(f'<text x="{W}" y="{base:g}" text-anchor="end" font-size="{fs_val}" '
                     f'font-weight="900" fill="rgb(18,10,11)">{esc(value)}</text>')
        by = y + fs_lab + 7
        parts.append(f'<rect x="0" y="{by:g}" width="{W}" height="{bar_h}" '
                     f'rx="{bar_h / 2:g}" fill="rgba(18,10,11,.08)"/>')
        w = round(W * abs(n) / top, 1)
        if w > 0:
            parts.append(f'<rect x="0" y="{by:g}" width="{w:g}" height="{bar_h}" '
                         f'rx="{min(bar_h / 2, w / 2):g}" fill="rgb(204,255,0)"/>')
        y = by + bar_h
        if note:
            y += fs_note + 5
            parts.append(f'<text x="0" y="{y:g}" font-size="{fs_note}" '
                         f'fill="rgb(69,65,64)">{esc(note)}</text>')
        y += gap
    H = round(y - gap + 2, 1)
    alt = " ".join(f"{r[0]}: {r[1]}." for r in rows)
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H:g}" role="img" '
            f'aria-label="{html.escape(alt)}">' + "".join(parts) + "</svg>")


def blk_chart(arg, raw, L):
    kind = (arg.strip().split() or ["bar"])[0].lower()
    if kind != "bar":
        raise ValueError(f"unknown chart type '{kind}'")
    title, src, rows = "", "", []
    for ln in block_lines(raw):
        if SRC_RE.match(ln):
            src = SRC_RE.sub("", ln).strip()
        elif "|" in ln:
            parts = [p.strip() for p in ln.split("|")]
            label = parts[0]
            value = parts[1] if len(parts) > 1 else ""
            note = parts[2] if len(parts) > 2 else ""
            n = parse_num(value)
            if n is None or not label:
                raise ValueError(f"chart row without a number: {ln}")
            rows.append((label, value, note, n))
        elif not rows and not title:
            title = ln
        else:
            raise ValueError(f"chart line is not 'label | number': {ln}")
    if not rows:
        raise ValueError("chart has no data rows")
    head = f'<p class="chart-title">{esc(title)}</p>' if title else ""
    # Charts are the most shareable thing we publish, so every one carries its
    # own attribution (mark + copyright) INSIDE the figure. That way the credit
    # survives a screenshot or a right-click-save, not just a link.
    brand = (
        '<div class="chart-brand">'
        f'<img src="{FAVICON}" alt="Sabato" width="18" height="18" loading="lazy">'
        f'<span>{L["labels"]["chart_credit"]}</span>'
        "</div>"
    )
    return ('<figure class="chart-card" data-chart>' + head
            + bar_svg(rows, "chart-desktop", 628, 15, 15, 13, 16, 24)
            + bar_svg(rows, "chart-mobile", 310, 14, 14, 12, 15, 22)
            + source_html(src, L, "chart-source") + brand + "</figure>")


BLOCKS = {
    "keystat": blk_keystat,
    "takeaway": blk_takeaway,
    "action": blk_action,
    "compare": blk_compare,
    "quote": blk_quote,
    "chart": blk_chart,
}


def raw_fallback(name, arg, raw):
    lines = block_lines(raw)
    if not lines:
        lines = [(":::" + name + (" " + arg if arg else "")).strip()]
    return "".join(f"<p>{esc(ln)}</p>" for ln in lines)


def render_block(name, arg, raw, L):
    fn = BLOCKS.get(name.lower())
    if fn is None:
        return raw_fallback(name, arg, raw)
    try:
        return fn(arg, raw, L)
    except Exception as e:          # a malformed block must never break the page
        print(f"    ! :::{name} skipped ({e}) - rendered as plain text")
        return raw_fallback(name, arg, raw)


def extract_blocks(body, L):
    store = {}

    def repl(m):
        key = BLOCK_TOKEN % len(store)
        store[key] = render_block(m.group(1), m.group(2), m.group(3), L)
        return "\n" + key + "\n"

    return BLOCK_RE.sub(repl, body), store


def render_body(body, L):
    body, blocks = extract_blocks(body, L)
    # HTML comments are an AUTHORING tool, not output. The Build File series
    # parks forward links to unpublished issues in comments and switches them on
    # the day the target ships - markdown passes comments straight through, so
    # without this the whole publishing calendar ships in the page source of
    # every post. Stripped before conversion so nothing downstream ever sees it.
    # The trailing \n? is not cosmetic. A comment parked on its own line INSIDE a
    # paragraph leaves a blank line behind when only the comment is removed, and
    # markdown reads a blank line as a paragraph break - which split one sentence
    # across two paragraphs mid-clause. Eating the newline keeps the sentence
    # whole. Between paragraphs the surrounding blank line still survives, so
    # real paragraph breaks are unaffected.
    body = re.sub(r"[ \t]*<!--.*?-->[ \t]*\n?", "", body, flags=re.S)
    MD.reset()
    out = MD.convert(body)
    # wrap tables for horizontal scroll + rounded border; >=4 columns get
    # denser cells + wrapping headers so they fit the column without scrolling
    def _wrap_table(m):
        tbl = m.group(0)
        cols = tbl.split("</tr>", 1)[0].count("<th")
        cls = "table-wrap dense" if cols >= 4 else "table-wrap"
        return f'<div class="{cls}">{tbl}</div>'
    out = re.sub(r"<table>.*?</table>", _wrap_table, out, flags=re.S)

    faq_entries = []

    heads = "|".join(re.escape(h) for h in L["faq_heads"])

    def faq_repl(m):
        head, inner = m.group(1), m.group(2)
        items = []
        # Two authoring shapes are supported, because silently dropping the
        # section is far worse than accepting both:
        #   ### Question            -> <h3>Q</h3><p>A</p>
        #   **Question** Answer     -> <p><strong>Q</strong> A</p>
        pairs = []
        for qm in re.finditer(r"<h3>(.*?)</h3>\s*((?:<p>.*?</p>\s*)+)", inner, re.S):
            pairs.append((qm.group(1), re.findall(r"<p>(.*?)</p>", qm.group(2), re.S)))
        if not pairs:
            for pm in re.finditer(r"<p><strong>(.*?)</strong>(.*?)</p>", inner, re.S):
                ans = pm.group(2).strip()
                if ans:
                    pairs.append((pm.group(1), [ans]))
        for q, answers in pairs:
            faq_entries.append((strip_tags(q), " ".join(strip_tags(a) for a in answers)))
            a_html = "".join(f'<p class="faq-a">{a}</p>' for a in answers)
            items.append(f'<div class="faq-item"><p class="faq-q">{q}</p>{a_html}</div>')
        if not items:
            # Nothing parsed: drop the whole section rather than leave a naked
            # heading with no content under it.
            print(f"  ! FAQ heading '{strip_tags(head)}' had no parseable Q&A - section omitted")
            return ""
        return f'<section class="faq"><h2>{head}</h2>\n' + "\n".join(items) + "\n</section>"

    out = re.sub(rf"<h2>({heads})</h2>\s*(.*?)(?=<h2>|<section|\Z)", faq_repl, out, flags=re.S)

    sheads = "|".join(re.escape(h) for h in L["src_heads"])
    out = re.sub(
        rf"<h2>({sheads})</h2>\s*(<ol>.*?</ol>|<ul>.*?</ul>)",
        r'<section class="sources"><h2>\1</h2>\n\2\n</section>', out, flags=re.S)

    # swap the authored blocks back in (after FAQ/Sources so their markup is
    # never re-parsed), and keep the placeholders out of the JSON-LD text
    for key, blk in blocks.items():
        out = out.replace(f"<p>{key}</p>", blk).replace(key, blk)
    tok = re.compile(BLOCK_TOKEN.replace("%d", r"\d+"))
    faq_entries = [(tok.sub("", q).strip(), tok.sub("", a).strip())
                   for q, a in faq_entries]
    return out, faq_entries


def jsonld(fm, url, faq_entries, L):
    art = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": fm["title"],
        "description": fm["description"],
        "datePublished": fm["date"],
        "dateModified": fm["date"],
        "inLanguage": L["inlang"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@type": "Organization", "name": "Sabato AI", "url": "https://www.sabato.ai"},
        "publisher": {"@type": "Organization", "name": "Sabato AI", "url": BASE},
    }
    blocks = ['<script type="application/ld+json">%s</script>'
              % json.dumps(art, ensure_ascii=False)]
    if faq_entries:
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq_entries],
        }
        blocks.append('<script type="application/ld+json">%s</script>'
                      % json.dumps(faq, ensure_ascii=False))
    return "\n  ".join(blocks)


def add_chart_sharing(content, fm, url, L):
    """Give every chart a share row that shares the IMAGE, not the post URL.

    LinkedIn and X share-intents only accept a URL to unfurl - a site cannot push
    an image into their composer. So the buttons here move the PNG itself:
    the native share sheet with the file attached where the browser supports it
    (mobile), copy-to-clipboard to paste straight into a composer (desktop), and
    a plain download as the universal fallback. No post URL is involved.

    Done here rather than in blk_chart because only build_post knows the slug.
    """
    lbl = L["labels"]
    parts = content.split("</figure>")
    out, fig = [], 0
    for seg in parts[:-1]:
        if 'class="chart-card"' in seg:
            fig += 1
            img = f"{L['url_prefix']}/charts/{fm['slug']}-{fig}.png"
            seg = seg.replace('data-chart>', f'data-chart="{fig}" data-chart-img="{img}">')
            share = (
                '<div class="chart-share">'
                f'<span class="cs-label">{esc(lbl["share_label"])}</span>'
                f'<button type="button" class="cs-btn" data-share-native hidden>'
                f'{esc(lbl["share_native"])}</button>'
                f'<button type="button" class="cs-btn" data-share-copy '
                f'data-done="{esc(lbl["share_copied"])}">{esc(lbl["share_copy"])}</button>'
                f'<a class="cs-btn cs-dl" href="{img}" download>'
                f'&#8595; {esc(lbl["share_dl"])}</a>'
                "</div>"
            )
        else:
            share = ""
        out.append(seg + share + "</figure>")
    out.append(parts[-1])
    return "".join(out)


def build_post(fm, body, L, sibling_exists):
    tpl = open(os.path.join(TPL, L["post_tpl"]), encoding="utf-8").read()
    content, faq_entries = render_body(body, L)
    minutes = read_minutes(fm, body)
    url = f"{BASE}{L['url_prefix']}/{fm['slug']}"
    content = add_chart_sharing(content, fm, url, L)
    # {{TITLE}} is the editorial headline and stays on the <h1> exactly as
    # written. {{SEO_TITLE}} is what goes in <title> and og:title.
    #
    # They were the same field until Aug 2026, which meant a headline like
    # "Your Customers Aren't Calling Because Your Site Is Confusing. They're
    # Calling Because It's Wrong." became a 109-character <title>. Google
    # truncates from the end, so the tail was cut and the headline was doing a
    # job it is not shaped for. Set `seo_title` in a post's frontmatter to give
    # it a short search title; omit it and the old behaviour applies.
    seo_title = fm.get("seo_title") or f'{fm["title"]} | Sabato AI'
    page = (tpl
            .replace("{{SEO_TITLE}}", html.escape(seo_title, quote=False))
            .replace("{{TITLE}}", html.escape(fm["title"], quote=False))
            .replace("{{CATEGORY}}", html.escape(fm["category"], quote=False))
            .replace("{{DATE}}", fmt_date(fm["date"], L))
            .replace("{{READ_TIME}}", L["read_label"](minutes))
            .replace("{{DESCRIPTION}}", html.escape(fm["description"]))
            .replace("{{SLUG}}", fm["slug"])
            .replace("{{JSONLD}}", jsonld(fm, url, faq_entries, L))
            .replace("{{CONTENT}}", content))
    if sibling_exists:
        link = (f'<span><a href="{L["sibling_prefix"]}/{fm["slug"]}" '
                f'style="color:#fff;text-decoration:underline;text-underline-offset:3px;">'
                f'{L["switch_label"]}</a></span>')
        page = page.replace(L["byline"], L["byline"] + link)
        # hreflang, both directions, English as x-default - the same convention
        # the use-case and industry pages already follow. The visible "Read in
        # English" link is for humans; without these tags a search engine is
        # free to serve the wrong language version of the same slug.
        en = f"{BASE}/blog/{fm['slug']}"
        it = f"{BASE}/it/blog/{fm['slug']}"
        alts = (f'<link rel="alternate" hreflang="en" href="{en}">\n'
                f'  <link rel="alternate" hreflang="it" href="{it}">\n'
                f'  <link rel="alternate" hreflang="x-default" href="{en}">\n  ')
        page = page.replace('<link rel="canonical"', alts + '<link rel="canonical"', 1)
    return page, minutes


def card(fm, minutes, L):
    bg, fg, extra = COVERS[fm["cover_style"]]
    excerpt = fm["description"]
    if len(excerpt) > 150:
        excerpt = excerpt[:147].rsplit(" ", 1)[0].rstrip(",.;") + "…"
    return f"""      <a class="post-card" href="{L['url_prefix']}/{fm['slug']}">
        <div class="card-cover" style="aspect-ratio:16/9;display:flex;align-items:flex-end;padding:24px 28px;background:{bg};{extra}">
          <span style="font-size:32px;font-weight:900;letter-spacing:-1px;line-height:1.08;color:{fg};text-transform:uppercase;">{html.escape(fm['category'], quote=False)}</span>
        </div>
        <div class="card-body">
          <span class="tag">{html.escape(fm['category'], quote=False)}</span>
          <h2>{html.escape(fm['title'], quote=False)}</h2>
          <p class="excerpt">{html.escape(excerpt, quote=False)}</p>
          <p class="meta">{fmt_date(fm['date'], L)} &nbsp;&middot;&nbsp; {L['read_label'](minutes)}</p>
        </div>
      </a>"""


def build_index(posts, L):
    tpl = open(os.path.join(TPL, L["index_tpl"]), encoding="utf-8").read()
    tpl = re.sub(r"<!-- (Example card structure|Struttura card di esempio).*?-->\s*",
                 "", tpl, flags=re.S)
    if posts:
        cards = "\n".join(card(fm, minutes, L) for fm, minutes in posts)
    else:
        cards = L["empty_state"]
    return tpl.replace("<!-- POST_CARDS -->", cards.strip())


def update_sitemap(urls):
    """Add new post URLs, and drop post URLs whose markdown no longer exists.

    This used to only ever ADD. Delete a post and its <loc> stayed in the
    sitemap forever, pointing at a 404 - the site telling Google to go and fetch
    a page we removed on purpose. Pruning is scoped to /blog/ and /it/blog/ post
    URLs, which are exactly the ones this function owns; every other entry in the
    sitemap is written by hand or by another tool and is left alone.
    """
    path = os.path.join(SITE, "sitemap.xml")
    xml = open(path, encoding="utf-8").read()
    existing = set(re.findall(r"<loc>(.*?)</loc>", xml))
    keep = set(urls)

    def owned(u):
        # a POST url, not the two index pages this function also emits
        tail = u.replace(BASE, "")
        return ((tail.startswith("/blog/") or tail.startswith("/it/blog/"))
                and tail not in ("/blog", "/it/blog"))

    dead = [u for u in existing if owned(u) and u not in keep]
    for u in dead:
        xml = re.sub(r"\s*<url>\s*<loc>" + re.escape(u) + r"</loc>.*?</url>", "", xml, flags=re.S)

    add = [u for u in urls if u not in existing]
    if add:
        xml = xml.replace("</urlset>",
                          "".join(f"<url><loc>{u}</loc></url>" for u in add) + "</urlset>")
    if add or dead:
        open(path, "w", encoding="utf-8").write(xml)
    if dead:
        print(f"  sitemap: {len(dead)} stale post URL(s) removed")
    return len(add)


def main():
    slugs = {}       # lang -> set of slugs
    parsed = {}      # lang -> list of (fm, body)
    for lang in LANGS:
        parsed[lang] = []
        d = os.path.join(POSTS, lang)
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if f.endswith(".md"):
                parsed[lang].append(parse_post(os.path.join(d, f)))
        slugs[lang] = {fm["slug"] for fm, _ in parsed[lang]}

    sitemap_urls = [f"{BASE}/blog", f"{BASE}/it/blog"]
    for lang, L in LANGS.items():
        other = "it" if lang == "en" else "en"
        os.makedirs(L["out_dir"], exist_ok=True)
        rendered = []
        for fm, body in parsed[lang]:
            page, minutes = build_post(fm, body, L, fm["slug"] in slugs[other])
            if fm["slug"] in DUMMY_SLUGS and "noindex" not in page:
                page = page.replace("</head>", '<meta name="robots" content="noindex">\n</head>', 1)
            out = os.path.join(L["out_dir"], fm["slug"] + ".html")
            open(out, "w", encoding="utf-8").write(page)
            rendered.append((fm, minutes))
            if fm["slug"] not in DUMMY_SLUGS:
                sitemap_urls.append(f"{BASE}{L['url_prefix']}/{fm['slug']}")
            print(f"  wrote {os.path.relpath(out, ROOT)}")
        rendered.sort(key=lambda t: t[0]["date"], reverse=True)
        open(L["index_out"], "w", encoding="utf-8").write(build_index(rendered, L))
        print(f"  wrote {os.path.relpath(L['index_out'], ROOT)}  ({len(rendered)} cards)")

    added = update_sitemap(sitemap_urls)
    print(f"  sitemap: {added} new URL(s) added")


if __name__ == "__main__":
    main()
