#!/usr/bin/env python3
"""THE homepage FAQ - eight questions, and the FAQPage JSON-LD that goes with them.

    python3 faq.py          # print the English block
    python3 faq.py it       # Italian

Import it: `from faq import faq_html, PAGES`.

WHY THIS IS STATIC AND NOT A JS PASS
------------------------------------
The product showcase and the workflows band are built by enhance.js, because
they are visual and a visitor is the only audience. This one is different: its
job is to be QUOTED by a search engine or an answer engine, and a crawler that
does not run JavaScript sees nothing a JS pass produced. Google executes JS;
several of the answer engines that matter here do not. Structured data that
appears only after hydration is worth a fraction of structured data that ships
in the HTML.

So this follows the hero's pattern instead: rendered at build time, injected by
tools/apply_footer.py as the FIRST thing in <body>, OUTSIDE React's root, where
hydration cannot reach it. Framer's own FAQ is hidden by a page-local style
block emitted below - page-local rather than in footer.css because /about and
/pricing carry a "Faq Section" too and theirs must survive.

WHY THESE EIGHT QUESTIONS
-------------------------
The nine Framer shipped are written for somebody already on the page ("What's
Sabato AI"). Answer engines get asked category questions by people who have
never heard of us, so every question here is phrased the way a buyer would type
it, and every ANSWER is self-contained: it names the entity, it does not say
"as mentioned above", and it can be lifted alone and still make sense. That is
the whole trick, and most FAQ sections fail it.

Deliberate choices worth keeping:
  * The pricing answer carries a real number. Pricing queries are one of the
    largest categories in answer engines and we were answering them nowhere.
    "No platform fee, no per-seat licence" is load-bearing: without it a reader
    assumes a subscription is hiding behind the per-minute rate.
  * The managed-vs-DIY question replaces the comparison table that used to sit
    on the homepage. Comparison questions get cited disproportionately, and this
    makes the argument without naming a competitor or maintaining a grid.
  * Nothing claims a deployment time. "Live in two weeks" was killed on
    17 Aug 2026 - it undersold the work. The answer sells the scoping instead.

NO LONG DASHES. Standing rule, and tools/dedash.py enforces it site-wide.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Only the two homepages. /about and /pricing keep Framer's own FAQ.
PAGES = {"index.html", "it.html"}

COPY = {
    "en": dict(
        eyebrow="FAQ",
        h2="Questions buyers actually ask.",
        sub="Pricing, integrations, and what a managed service does that a "
            "platform does not.",
        items=[
            ("What is a voice AI agent for e-commerce?",
             "A voice AI agent answers your store's phone line and does what a support "
             "agent would: it looks up a live order, checks a return against your policy, "
             "answers a product question, and hands the call to a person when it should. "
             "Sabato builds these agents for e-commerce and retail brands, connects them "
             "to the catalog and order system, and runs them as a managed service."),
            ("Can AI answer “where is my order” calls?",
             "Yes. It is the highest-volume call in e-commerce and the one most completely "
             "automatable. Sabato's agent reads the live order from Shopify or your order "
             "system, tells the caller where the parcel is and when it arrives, and can "
             "send the tracking link by text before the call ends. No hold time, at any "
             "hour, in any language you sell in."),
            ("How much does voice AI for customer service cost?",
             "Sabato charges $0.55 to $0.65 per minute of call time, depending on the type "
             "of call. That price includes the managed service: we build the agent, connect "
             "it to your systems, review the calls and publish the fixes. There is no "
             "separate platform fee and no per-seat licence. Custom integrations are quoted "
             "separately."),
            ("Does voice AI integrate with Shopify?",
             "Sabato is native with Shopify. The agent reads live orders, customers and "
             "products, and writes back order notes, tags and draft orders. Everything else "
             "connects through Zapier, which covers more than 8,500 apps including Zendesk, "
             "Salesforce and Zoho, or through a webhook to any endpoint you control. "
             "Magento, WooCommerce and BigCommerce connect the same way."),
            ("What is the difference between a managed voice AI service and a DIY platform?",
             "A DIY platform gives you a builder and leaves the operation to you: your team "
             "writes the prompts, watches the calls, finds the failures and ships the fixes. "
             "A managed service does that work. With Sabato the demo is about 5% of the job. "
             "The other 95% is reviewing every call, finding the gaps and publishing "
             "corrections daily, which is what keeps an agent right on the ten-thousandth "
             "call rather than the tenth."),
            ("Will AI replace my customer service team?",
             "No. It takes the repetitive half of the queue: order status, delivery dates, "
             "return eligibility, opening hours. Your team handles the half that needs "
             "judgement: the angry customer, the high-value order, the exception. Most "
             "Sabato customers redeploy people rather than cut headcount, and stop hiring "
             "temporary staff for peak season."),
            ("How long does it take to deploy a voice agent?",
             "It depends on how many workflows you start with and how your systems are set "
             "up. One workflow on a Shopify store is quick, because the connection is native "
             "and the rules are your existing policy. More workflows, more languages or a "
             "custom ERP integration take longer. We scope it on the first call, and you "
             "hear the agent yourself before it goes live."),
            ("What languages can a voice AI agent handle?",
             "Every language you sell in. One Sabato agent handles multiple languages on the "
             "same phone number, so opening a market does not mean hiring a native speaker "
             "for the support desk or running a separate line per country. Agents are live "
             "today in English, Italian and Spanish."),
        ],
    ),
    "it": dict(
        eyebrow="FAQ",
        h2="Le domande che fanno davvero.",
        sub="Prezzi, integrazioni e cosa fa un servizio gestito che una "
            "piattaforma non fa.",
        items=[
            ("Che cos'è un agente vocale AI per l'e-commerce?",
             "Un agente vocale AI risponde al telefono del tuo store e fa il lavoro che "
             "farebbe un operatore: apre l'ordine in tempo reale, verifica un reso contro la "
             "tua policy, risponde a una domanda sul prodotto e passa la chiamata a una "
             "persona quando serve. Sabato costruisce questi agenti per e-commerce e retail, "
             "li collega al catalogo e al sistema ordini e li gestisce per te."),
            ("L'AI può rispondere alle chiamate “dov'è il mio ordine”?",
             "Sì. È la chiamata più frequente nell'e-commerce e quella che si "
             "automatizza meglio dall'inizio alla fine. L'agente di Sabato legge l'ordine da "
             "Shopify o dal tuo gestionale, dice al cliente dov'è il pacco e quando "
             "arriva, e può mandare il link di tracking via messaggio prima di chiudere. "
             "Nessuna attesa, a qualsiasi ora, in tutte le lingue in cui vendi."),
            ("Quanto costa la voice AI per l'assistenza clienti?",
             "Sabato costa da 0,55 a 0,65 euro al minuto di conversazione, a seconda del tipo "
             "di chiamata. Il prezzo include il servizio gestito: costruiamo l'agente, lo "
             "colleghiamo ai tuoi sistemi, rivediamo le chiamate e pubblichiamo le "
             "correzioni. Non c'è un canone di piattaforma separato né una licenza "
             "per utente. Le integrazioni su misura sono quotate a parte."),
            ("La voice AI si integra con Shopify?",
             "Sabato è nativo con Shopify. L'agente legge ordini, clienti e prodotti in "
             "tempo reale, e scrive note ordine, tag e bozze d'ordine. Tutto il resto passa "
             "da Zapier, che copre oltre 8.500 app tra cui Zendesk, Salesforce e Zoho, "
             "oppure da un webhook verso qualsiasi endpoint controlli tu. Magento, "
             "WooCommerce e BigCommerce si collegano allo stesso modo."),
            ("Qual è la differenza tra un servizio di voice AI gestito e una piattaforma "
             "fai-da-te?",
             "Una piattaforma fai-da-te ti dà un editor e lascia a te l'operatività: "
             "il tuo team scrive i prompt, ascolta le chiamate, trova gli errori e pubblica "
             "le correzioni. Un servizio gestito fa quel lavoro. Con Sabato la demo è "
             "circa il 5% del lavoro. L'altro 95% è rivedere ogni chiamata, trovare le "
             "lacune e pubblicare le correzioni ogni giorno, che è quello che tiene "
             "l'agente preciso alla diecimillesima chiamata e non solo alla decima."),
            ("L'AI sostituirà il mio team di assistenza?",
             "No. Prende la metà ripetitiva della coda: stato ordine, tempi di consegna, "
             "condizioni di reso, orari. Il tuo team gestisce la metà che richiede "
             "giudizio: il cliente arrabbiato, l'ordine importante, l'eccezione. La maggior "
             "parte dei clienti Sabato sposta le persone su attività più utili "
             "invece di ridurre l'organico, e smette di assumere stagionali per i picchi."),
            ("Quanto tempo serve per attivare un agente vocale?",
             "Dipende da quanti workflow accendi e da come sono messi i tuoi sistemi. Un solo "
             "workflow su uno store Shopify è veloce, perché il collegamento "
             "è nativo e le regole sono la tua policy attuale. Più workflow, "
             "più lingue o un'integrazione con un ERP su misura richiedono più "
             "tempo. Lo definiamo nella prima call, e l'agente lo ascolti tu prima che vada "
             "online."),
            ("Quante lingue può gestire un agente vocale AI?",
             "Tutte quelle in cui vendi. Un solo agente Sabato gestisce più lingue sullo "
             "stesso numero, quindi aprire un mercato non significa assumere un madrelingua "
             "per l'assistenza né tenere una linea per paese. Oggi gli agenti sono "
             "attivi in inglese, italiano e spagnolo."),
        ],
    ),
}

# Framer's own FAQ on the two homepages. data-framer-name is written by React
# itself, so unlike a class hash or an attribute we add it survives hydration -
# same reasoning as the Framer hero rule in footer.css. Emitted page-local
# rather than in footer.css because /about and /pricing carry a "Faq Section"
# too, and those must keep rendering.
HIDE_FRAMER = (
    '<style id="sb-faq-hide">'
    '[data-framer-name="Faq Section" i]{display:none !important}'
    "</style>"
)

CSS = """
/* The section sits outside Framer's root, so it inherits nothing: the face
   has to be named here the way footer.css names it. */
.sb-faq{background:#fff;padding:96px 0 104px;
  font-family:"Satoshi","Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  -webkit-font-smoothing:antialiased}
.sb-faq-in{max-width:900px;margin:0 auto;padding:0 24px}
.sb-faq-eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:12px;line-height:1.2;
  font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:rgb(111,106,102);margin:0}
.sb-faq-eyebrow:before{content:"";width:7px;height:7px;border-radius:50%;
  background:rgb(204,255,0);flex:none}
.sb-faq h2{font-size:46px;line-height:1.16;letter-spacing:-1.4px;font-weight:700;
  color:rgb(11,11,12);margin:16px 0 0}
.sb-faq-sub{font-size:17px;line-height:1.6;color:rgb(111,106,102);margin:14px 0 0;max-width:620px}
.sb-faq-list{margin:38px 0 0;border-top:1px solid rgba(11,11,12,.10)}
.sb-faq-item{border-bottom:1px solid rgba(11,11,12,.10)}
.sb-faq-q{width:100%;display:flex;align-items:flex-start;gap:20px;background:none;border:0;
  padding:22px 0;text-align:left;cursor:pointer;font-family:inherit;font-size:18px;
  line-height:1.4;font-weight:700;color:rgb(11,11,12)}
.sb-faq-q span{flex:1}
.sb-faq-q i{flex:none;width:20px;height:20px;position:relative;margin-top:2px;font-style:normal}
.sb-faq-q i:before,.sb-faq-q i:after{content:"";position:absolute;left:2px;top:9px;width:16px;
  height:2px;border-radius:2px;background:rgb(11,11,12);transition:transform .22s ease}
.sb-faq-q i:after{transform:rotate(90deg)}
.sb-faq-q[aria-expanded="true"] i:after{transform:rotate(0deg)}
.sb-faq-a{padding:0 40px 24px 0;margin:0;font-size:16.5px;line-height:1.65;
  color:rgb(111,106,102);max-width:760px}
.sb-faq-a[hidden]{display:none}
@media (max-width:809px){
  .sb-faq{padding:64px 0 72px}
  .sb-faq-in{padding:0 22px}
  .sb-faq h2{font-size:30px;letter-spacing:-.8px}
  .sb-faq-sub{font-size:16px}
  .sb-faq-q{font-size:16.5px;gap:14px;padding:18px 0}
  .sb-faq-a{font-size:15.5px;padding-right:24px}
}
"""

# Plain, inline and tiny, for the same reason the hero's reveal script is: this
# markup lives outside React's root and a separate file would be a third request
# for ten lines. First item open on load so the section never reads as empty.
SCRIPT = (
    "<script>(function(){var r=document.getElementById('sb-faq');if(!r)return;"
    "r.addEventListener('click',function(e){"
    "var b=e.target.closest&&e.target.closest('.sb-faq-q');if(!b)return;"
    "var open=b.getAttribute('aria-expanded')==='true';"
    "b.setAttribute('aria-expanded',open?'false':'true');"
    "var a=document.getElementById(b.getAttribute('aria-controls'));"
    "if(a){if(open){a.setAttribute('hidden','');}else{a.removeAttribute('hidden');}}"
    "});}());</script>"
)


def _jsonld(lang):
    """FAQPage, from the same strings the visible answers use.

    Built from COPY rather than typed twice on purpose: a JSON-LD block that
    drifts from the visible copy is worse than none, because it is the version
    an engine quotes.
    """
    c = COPY[lang]
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in c["items"]
        ],
    }
    return ('<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "</script>")


def faq_html(lang="en"):
    if lang not in COPY:
        raise ValueError(f"unknown lang {lang!r}")
    c = COPY[lang]
    rows = []
    for i, (q, a) in enumerate(c["items"], 1):
        opened = i == 1
        rows.append(
            f'<div class="sb-faq-item">'
            f'<button class="sb-faq-q" type="button" aria-expanded="{"true" if opened else "false"}" '
            f'aria-controls="sb-faq-a{i}" id="sb-faq-q{i}">'
            f"<span>{html.escape(q)}</span><i aria-hidden=\"true\"></i></button>"
            f'<p class="sb-faq-a" id="sb-faq-a{i}" role="region" aria-labelledby="sb-faq-q{i}"'
            f'{"" if opened else " hidden"}>{html.escape(a)}</p>'
            f"</div>"
        )
    return (
        HIDE_FRAMER
        + '<style id="sb-faq-css">' + CSS + "</style>"
        + '<section class="sb-faq" id="sb-faq" data-lang="' + lang + '">'
        + '<div class="sb-faq-in">'
        + f'<p class="sb-faq-eyebrow">{c["eyebrow"]}</p>'
        + f'<h2>{c["h2"]}</h2>'
        + f'<p class="sb-faq-sub">{c["sub"]}</p>'
        + '<div class="sb-faq-list">' + "".join(rows) + "</div>"
        + "</div></section>"
        + _jsonld(lang)
        + SCRIPT
    )


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in COPY else "en"
    print(faq_html(lang))
