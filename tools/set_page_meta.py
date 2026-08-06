#!/usr/bin/env python3
"""Set per-page title, description, social tags and robots directives.

The Framer export gave six pages the HOMEPAGE's title, description, og:* and
twitter:* tags verbatim: /, /it, /privacy-policy, /terms, /thank-you-page and
/it/grazie. Search Console (5 Aug 2026) showed /terms indexed as one of only
five indexed pages on the domain, wearing the homepage's title and description
and therefore competing with it. Sharing any of them on LinkedIn rendered the
homepage sales pitch.

Separately, every Framer-exported Italian page shipped with an English title,
so Italian buyers saw English in Google.it.

    python3 tools/set_page_meta.py            # apply
    python3 tools/set_page_meta.py --check    # report only, write nothing

Idempotent: re-running changes nothing once applied. Run it again after any
re-export from Framer, which will overwrite these pages the same way it
overwrites the GA tag.

TWO NON-OBVIOUS POINTS, both deliberate:

1. The thank-you pages get `noindex`, not a better title. They are
   post-conversion confirmation pages. GA4 went live on this site in August; if
   Google indexes a thank-you page and anyone arrives on it from search, that
   fires as a conversion that never happened and quietly inflates the numbers
   used to make decisions. They are also removed from sitemap.xml by
   tools/prune_sitemap.py.

2. Titles carry the CATEGORY term, descriptions carry the PITCH. At low domain
   authority a title's job is matching what people type, not persuading them.
   Nobody searches "risolvi ogni chiamata senza assumere" - they search "agenti
   vocali AI". The hook belongs in the description, which is read after the
   title has already matched the query.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = "https://www.sabato.ai"

# path -> dict(title, desc, robots=None, canonical=True)
# desc=None means "leave the existing description alone" - used where the Italian
# copy was already correct and only the title was still English.
PAGES = {
    # ---- English pages wearing the homepage's identity --------------------
    "privacy-policy": dict(
        title="Privacy Policy | Sabato AI",
        desc="How Sabato AI collects, uses and protects personal data, including "
             "call recordings and customer information processed by our voice agents.",
    ),
    "terms": dict(
        title="Terms of Service | Sabato AI",
        desc="The terms governing use of Sabato AI's managed voice agents: service "
             "levels, data handling, subscriptions and cancellation.",
    ),
    "thank-you-page": dict(
        title="Thank You | Sabato AI",
        desc="Your request has been received. The Sabato AI team will be in touch shortly.",
        robots="noindex, nofollow",
    ),

    # ---- Italian pages shipped with English titles ------------------------
    "it": dict(
        title="Agenti vocali AI per l'e-commerce | Sabato AI",
        desc="Risolvi ogni chiamata senza assumere. Agenti vocali gestiti che guidano "
             "i clienti su taglie, compatibilità e specifiche. Li costruiamo e li gestiamo noi.",
    ),
    "it/prezzi": dict(
        title="Prezzi degli agenti vocali AI | Sabato AI",
        desc="Paghi l'utilizzo, non le persone. Tre piani con controlli enterprise, "
             "opzioni SLA e policy di conservazione dei dati. Operativi in due settimane.",
    ),
    "it/contatti": dict(
        title="Contatta Sabato AI | Prenota una demo",
        desc="Parla con il team commerciale o di supporto. Casi d'uso, tempi di "
             "attivazione e come gli agenti vocali si collegano al tuo catalogo.",
    ),
    "it/chi-siamo": dict(
        title="Il team dietro Sabato AI | Agenti vocali e-commerce",
        desc="Il team dietro Sabato, da Google, Meta e Leroy Merlin, costruisce agenti "
             "vocali AI per l'e-commerce europeo. Chi siamo e perché lo facciamo.",
    ),
    "it/grazie": dict(
        title="Grazie | Sabato AI",
        desc="Abbiamo ricevuto la tua richiesta. Il team Sabato AI ti contatterà a breve.",
        robots="noindex, nofollow",
    ),
    # DO NOT ADD GENERATED PAGES HERE. This tool patches built HTML, so anything
    # a generator rebuilds will silently revert to the generator's value on the
    # next run - and the revert is invisible until someone diffs the output.
    # Proven on 6 Aug 2026: /it/blog was set here, publish.py rebuilt it, and the
    # title went back to the English "Blog | Sabato AI"; running customers.py
    # likewise reverted both Italian case-study titles.
    #
    # Metadata belongs with whatever owns the page:
    #   /blog, /it/blog, blog posts  -> templates/blog-index-*.html, post frontmatter
    #   /industries/*, /it/settori/* -> industry_data.py / industry_data_it.py
    #   /customers/*, /it/clienti/*  -> customer_data.py / customer_data_it.py
    #   everything below             -> static, no generator, so this tool owns it

    # ---- use-case pages ----------------------------------------------------
    # These 18 have no generator: templates/use-case.html exists but nothing in
    # the repo renders it, so the pages are static and this tool is their only
    # metadata source. (Industry pages are the opposite - they regenerate from
    # industry_data.py, so their titles live there, not here.)
    #
    # Every one of them used to open with "Voice AI for" / "Voice AI per".
    # Thirty-six pages starting with the same three words are indistinguishable
    # in a results list once Google truncates, and it truncates from the end -
    # cutting off precisely the part that identifies the page. Distinguisher
    # first, keyword second, brand last.
    "use-cases/back-in-stock-notification": dict(
        title="Back-in-Stock Voice AI | Recapture Waitlist | Sabato AI", desc=None),
    "use-cases/cart-abandonment-recovery": dict(
        title="Cart Abandonment Voice AI | Recovery Calls | Sabato AI", desc=None),
    "use-cases/checkout-summary-via-text": dict(
        title="Checkout Summary Voice AI | Close the Call | Sabato AI", desc=None),
    "use-cases/managing-returns": dict(
        title="Returns Voice AI | Policy Check to Refund | Sabato AI", desc=None),
    "use-cases/open-a-complaint": dict(
        title="Complaints Voice AI | Capture, Ticket, Route | Sabato AI", desc=None),
    "use-cases/post-delivery-feedback": dict(
        title="Post-Delivery Voice AI | Earn More Reviews | Sabato AI", desc=None),
    "use-cases/pre-sales-consultation": dict(
        title="Pre-Sales Voice AI | Product Consultation Calls | Sabato AI", desc=None),
    "use-cases/qualify-and-collect-for-quote": dict(
        title="Quote Requests Voice AI | Qualify by Phone | Sabato AI", desc=None),
    "use-cases/where-is-my-order": dict(
        title="WISMO Voice AI | Order Status Calls, Automated | Sabato AI", desc=None),

    "it/casi-duso/apertura-reclamo": dict(
        title="Reclami: Voice AI | Raccolta e smistamento | Sabato AI", desc=None),
    "it/casi-duso/consulenza-pre-vendita": dict(
        title="Pre-vendita: Voice AI | Consulenza al telefono | Sabato AI", desc=None),
    "it/casi-duso/dove-e-il-mio-ordine": dict(
        title="WISMO: Voice AI | Stato ordine al telefono | Sabato AI", desc=None),
    "it/casi-duso/feedback-post-consegna": dict(
        title="Feedback post-consegna: Voice AI | Recensioni | Sabato AI", desc=None),
    "it/casi-duso/gestione-resi": dict(
        title="Gestione resi: Voice AI | Motivo, policy, reso | Sabato AI", desc=None),
    "it/casi-duso/notifica-ritorno-in-stock": dict(
        title="Ritorno in stock: Voice AI | Recupera la domanda | Sabato AI", desc=None),
    "it/casi-duso/preventivi-automatici": dict(
        title="Preventivi: Voice AI | Qualifica e raccolta dati | Sabato AI", desc=None),
    "it/casi-duso/recupero-carrelli-abbandonati": dict(
        title="Carrelli abbandonati: Voice AI | Recupero | Sabato AI", desc=None),
    "it/casi-duso/riepilogo-checkout-via-messaggio": dict(
        title="Riepilogo checkout via SMS: Voice AI | Sabato AI", desc=None),
}


def sub_meta(html, attr, key, value):
    """Replace the content="" of a <meta {attr}="{key}"> tag. Returns (html, hit).

    The delimiter is captured and closed with a BACKREFERENCE (\\2), not with the
    class ["\\'].  Using the class means a lazy match ends at the first quote of
    EITHER kind - so a value containing an apostrophe ("Sabato AI's", "l'e-commerce")
    terminated at the apostrophe, replaced only the leading fragment, and left the
    tail in place. Every re-run then appended the tail again. Silent content
    corruption, visible only by diffing two consecutive runs.
    """
    pat = re.compile(
        r'(<meta[^>]*\b' + attr + r'=["\']' + re.escape(key) + r'["\'][^>]*\bcontent=)(["\'])(.*?)\2',
        re.I | re.S)
    new, n = pat.subn(lambda m: m.group(1) + m.group(2) + value + m.group(2), html, count=1)
    if n:
        return new, True
    # Some exports order the attributes the other way round.
    pat2 = re.compile(
        r'(<meta[^>]*\bcontent=)(["\'])(.*?)\2([^>]*\b' + attr + r'=["\']' + re.escape(key) + r'["\'])',
        re.I | re.S)
    new, n = pat2.subn(lambda m: m.group(1) + m.group(2) + value + m.group(2) + m.group(4),
                       html, count=1)
    return new, bool(n)


def esc(s):
    return s.replace('"', "&quot;")


def apply(path, spec, check_only):
    fp = os.path.join(SITE, path + ".html")
    if not os.path.exists(fp):
        return f"MISSING FILE {path}", False
    src = open(fp, encoding="utf-8").read()
    out = src
    notes = []

    # A missing twitter:* tag is NOT a defect. X falls back to og:* when the
    # twitter equivalent is absent, and the authored pages (blog, case studies)
    # ship og:* plus twitter:card only. Flag it only if og:* is missing too,
    # because then nothing is set.
    title = spec["title"]
    out, n = re.subn(r"(<title[^>]*>)(.*?)(</title>)",
                     lambda m: m.group(1) + title + m.group(3), out, count=1, flags=re.S | re.I)
    if not n:
        notes.append("NO <title>")
    out, og_hit = sub_meta(out, "property", "og:title", esc(title))
    out, tw_hit = sub_meta(out, "name", "twitter:title", esc(title))
    if not og_hit:
        notes.append("NO og:title")
    elif not tw_hit:
        notes.append("og only (x falls back)")

    if spec.get("desc"):
        d = spec["desc"]
        out, hit = sub_meta(out, "name", "description", esc(d))
        if not hit:
            notes.append("NO description")
        out, og_d = sub_meta(out, "property", "og:description", esc(d))
        out, tw_d = sub_meta(out, "name", "twitter:description", esc(d))
        if not og_d:
            notes.append("NO og:description")

    if spec.get("robots"):
        out, hit = sub_meta(out, "name", "robots", spec["robots"])
        if not hit:
            out = out.replace("</head>",
                              f'<meta name="robots" content="{spec["robots"]}">\n</head>', 1)

    # /thank-you-page shipped with no canonical at all, unlike every other page.
    if 'rel="canonical"' not in out:
        url = f"{BASE}/{path}" if path != "index" else BASE + "/"
        out = out.replace("</head>", f'<link rel="canonical" href="{url}">\n</head>', 1)
        notes.append("added canonical")

    changed = out != src
    if changed and not check_only:
        open(fp, "w", encoding="utf-8").write(out)
    return ("; ".join(notes) or "ok"), changed


def main():
    check_only = "--check" in sys.argv
    problems = 0
    print(f"{'page':34s} {'len(T)':>6} {'len(D)':>6}  status")
    for path, spec in PAGES.items():
        note, changed = apply(path, spec, check_only)
        lt = len(spec["title"])
        ld = len(spec["desc"]) if spec.get("desc") else 0
        flags = []
        if lt > 60:
            flags.append(f"TITLE {lt}>60")
        if ld and ld > 160:
            flags.append(f"DESC {ld}>160")
        if ld and ld < 70:
            flags.append(f"DESC {ld}<70")
        if flags or "NO " in note or "MISSING" in note:
            problems += 1
        state = "changed" if changed else "unchanged"
        print(f"{'/' + path:34s} {lt:6d} {ld or '-':>6}  {state:9s} {note} {' '.join(flags)}")

    # No two pages may share a title or description afterwards.
    ts = [s["title"] for s in PAGES.values()]
    if len(ts) != len(set(ts)):
        print("\nDUPLICATE TITLES REMAIN", file=sys.stderr)
        problems += 1
    ds = [s["desc"] for s in PAGES.values() if s.get("desc")]
    if len(ds) != len(set(ds)):
        print("\nDUPLICATE DESCRIPTIONS REMAIN", file=sys.stderr)
        problems += 1

    print(f"\n{len(PAGES)} pages, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
