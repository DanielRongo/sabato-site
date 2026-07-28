#!/usr/bin/env python3
"""Sabato blog publisher.

Reads markdown posts from posts/en/ and posts/it/, renders them through the
templates in blog-build/, writes post pages + blog indexes into site/, and
keeps site/sitemap.xml up to date. Re-run any time:  python3 publish.py
"""
import os, re, json, math, html
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
TPL = os.path.join(ROOT, "templates")
POSTS = os.path.join(ROOT, "posts")
BASE = "https://www.sabato.ai"

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
        "byline": '<span>By <a href="https://www.linkedin.com/in/danielrongo/" target="_blank" rel="author" style="color:inherit;text-decoration:underline;text-underline-offset:3px;">Daniel Rongo</a></span>',
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
        "byline": '<span>Di <a href="https://www.linkedin.com/in/danielrongo/" target="_blank" rel="author" style="color:inherit;text-decoration:underline;text-underline-offset:3px;">Daniel Rongo</a></span>',
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


def render_body(body, L):
    MD.reset()
    out = MD.convert(body)
    # wrap tables for horizontal scroll + rounded border
    out = out.replace("<table>", '<div class="table-wrap"><table>')
    out = out.replace("</table>", "</table></div>")

    faq_entries = []

    heads = "|".join(re.escape(h) for h in L["faq_heads"])

    def faq_repl(m):
        head, inner = m.group(1), m.group(2)
        items = []
        for qm in re.finditer(r"<h3>(.*?)</h3>\s*((?:<p>.*?</p>\s*)+)", inner, re.S):
            q = qm.group(1)
            answers = re.findall(r"<p>(.*?)</p>", qm.group(2), re.S)
            faq_entries.append((strip_tags(q), " ".join(strip_tags(a) for a in answers)))
            a_html = "".join(f'<p class="faq-a">{a}</p>' for a in answers)
            items.append(f'<div class="faq-item"><p class="faq-q">{q}</p>{a_html}</div>')
        return f'<section class="faq"><h2>{head}</h2>\n' + "\n".join(items) + "\n</section>"

    out = re.sub(rf"<h2>({heads})</h2>\s*(.*?)(?=<h2>|<section|\Z)", faq_repl, out, flags=re.S)

    sheads = "|".join(re.escape(h) for h in L["src_heads"])
    out = re.sub(
        rf"<h2>({sheads})</h2>\s*(<ol>.*?</ol>|<ul>.*?</ul>)",
        r'<section class="sources"><h2>\1</h2>\n\2\n</section>', out, flags=re.S)
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
        "author": {"@type": "Person", "name": "Daniel Rongo", "url": "https://www.sabato.ai/about", "sameAs": ["https://www.linkedin.com/in/danielrongo/"]},
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


def build_post(fm, body, L, sibling_exists):
    tpl = open(os.path.join(TPL, L["post_tpl"]), encoding="utf-8").read()
    content, faq_entries = render_body(body, L)
    minutes = read_minutes(fm, body)
    url = f"{BASE}{L['url_prefix']}/{fm['slug']}"
    page = (tpl
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
    path = os.path.join(SITE, "sitemap.xml")
    xml = open(path, encoding="utf-8").read()
    existing = set(re.findall(r"<loc>(.*?)</loc>", xml))
    add = [u for u in urls if u not in existing]
    if add:
        xml = xml.replace("</urlset>",
                          "".join(f"<url><loc>{u}</loc></url>" for u in add) + "</urlset>")
        open(path, "w", encoding="utf-8").write(xml)
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
