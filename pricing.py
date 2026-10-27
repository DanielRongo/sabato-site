#!/usr/bin/env python3
"""THE pricing page, both languages.

    python3 pricing.py          # writes site/pricing.html and site/it/prezzi.html

WHY THIS IS AN AUTHORED PAGE NOW
--------------------------------
/pricing and /it/prezzi were Framer exports selling three monthly tiers. The
19 Aug rewrite (one flat per-minute rate, no setup fee) never went live and is
superseded by the model as of 20 Oct 2026: billed per AI token (roughly a minute
of talk), a setup fee that includes a starting token package, and custom work
quoted separately. Pilots run 30 to 45 days on a testing token package. Rewriting a Framer page in place means fighting
React's hydration for every node, so both pages are generated here instead, the
same way the product and playbook pages are, and Framer is out of the loop.

Consequences elsewhere, all deliberate:
  * proof.py and cta.py no longer list these two pages. The proof card is
    rendered INLINE here with proof_inline_html(), and the page closes with its
    own CTA band, so the generic one would stack a second close on top.
  * tools/set_page_meta.py no longer patches it/prezzi: this file owns the
    metadata now, and a post-build patcher would silently revert it.
  * tools/postdeploy_check.py drops both paths from PROOF_PATHS. That check
    asserts the widget sits directly above a Framer FAQ; here the FAQ is ours
    and the team strip sits between the two on purpose.

SECTION ORDER follows the buyer, not the brand: what it costs (hero), what you
actually get (the desk strip), is it worth it for me (calculator), does it work
for real (proof), who built it (team), what is the catch (FAQ), what next (CTA).

THE CALCULATOR assumes the agent resolves 55% of calls end to end, the rate at
our largest live client, and bills Sabato on EVERY call because the agent
answers all of them, including the ones it transfers. The page says so in a
footnote. Change RESOLVE_RATE here and the footnote follows.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from hero import NUMBERS, FLAG  # noqa: E402
from proof import proof_inline_html  # noqa: E402

SITE = os.path.join(ROOT, "site")
BASE = "https://www.sabato.ai"
CAL = "https://cal.com/sabatoai/intro"
OG_IMAGE = BASE + "/fuc/assets/8Q4ofjOgRTqsr8FpanTJF9nzLwU.png"
RESOLVE_RATE = 55          # percent, see the module docstring
PRICES = (("wismo", 0.39), ("post", 0.53), ("pre", 0.77))

OUT = {"en": "pricing.html", "it": "it/prezzi.html"}
URL = {"en": BASE + "/pricing", "it": BASE + "/it/prezzi"}

# Same line icons the homepage workflow tiles use, 24px grid, round caps.
ICON = {
    "box": '<path d="M3 8.5 12 4l9 4.5v7L12 20l-9-4.5z"/><path d="M3 8.5 12 13l9-4.5M12 13v7"/>',
    "return": '<path d="M3 10h11a5 5 0 0 1 0 10H9"/><path d="M7 6 3 10l4 4"/>',
    "headset": ('<path d="M4 12a8 8 0 0 1 16 0v5a3 3 0 0 1-3 3h-2"/>'
                '<rect x="2" y="12" width="4" height="6" rx="1.6"/>'
                '<rect x="18" y="12" width="4" height="6" rx="1.6"/>'),
    "bubble": '<path d="M20 15a2 2 0 0 1-2 2H8l-4 3V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z"/>',
    "bars": '<path d="M4 20V10M9.5 20V4M15 20v-7M20.5 20v-4"/>',
    "check": '<path d="M21 12a9 9 0 1 1-3.2-6.9"/><path d="M8.5 11.8 11.4 15 21 5.4"/>',
}
TYPE_ICON = {"wismo": "box", "post": "return", "pre": "headset"}

TEAM = [("google.png", "Google", 26), ("meta.png", "Meta", 22),
        ("microsoft.png", "Microsoft", 22), ("thomson-reuters.png", "Thomson Reuters", 18),
        ("leroy-merlin.png", "Leroy Merlin", 32), ("techstars.png", "Techstars", 19)]

COPY = {
    "en": dict(
        title="Pricing for Managed Voice AI | Sabato AI",
        desc="Billed per AI token, about a minute of talk: around €0.39 for an "
             "order status call. See what an agent saves you, then start with a pilot.",
        og_locale="en_US",
        h1="Every call answered.<br>Pay for the conversation.",
        price_int="0", price_dec=".39",
        price_note="a where is my order call, start to finish",
        hero_p=("A post sales call is <b>€0.53</b>. A pre-sales question is "
                "<b>€0.77</b>. Billed per AI token, about a minute of talk, "
                "so a ring costs nothing."),
        book="Book a call",
        call_now="or call the agent now",
        show="show number", hide="hide number",
        desk_h2="Much more than voice AI.<br>A real customer service desk, run by AI.",
        desk=[("headset", "Picks up every call"), ("bubble", "Sells like your best rep"),
              ("return", "Transfers when it matters"), ("bars", "Turns calls into data"),
              ("check", "Gets better every day")],
        desk_link="See the product", desk_href="/product/voice-agent-builder",
        calc_h2="Calculate your savings",
        calc_sub="See what an agent saves you each month against a human team.",
        step1="1. Pick your main call type",
        step2="2. Set your volume and team",
        types={"wismo": "Where is my order", "post": "Post sales support", "pre": "Pre-sales"},
        f_calls=("Calls per month", "How many calls your line receives each month."),
        f_cost=("Operator cost / month",
                "Fully loaded: salary, taxes, benefits, holidays, sick days and equipment."),
        f_handled=("Calls one operator handles",
                   "Per month, after breaks, training and admin. Around 40 to 60 calls a day."),
        keep="You keep, every month*", extra="Extra cost, every month*",
        today="Today, per month", with_us="With Sabato, per month",
        op_call="Operator, per call", us_call="Sabato, per call (average)",
        v_clear="Clear saving", v_small="Small saving", v_more="Costs more",
        v_clear_t="{p}% off your monthly cost, and it answers at 9pm on a Sunday.",
        v_small_t="{p}% off your monthly cost. The bigger win is out of hours and peak weeks.",
        v_more_t=("{p}% more per month. At this cost, voice pays for out of hours "
                  "and overflow, not your day shift."),
        footnote=("*Assumes the agent resolves {r}% of calls end to end, the rate it "
                  "holds today at our largest client. Operator cost per call uses your "
                  "two numbers only. Evenings, weekends and peak queues push it higher."),
        team_label="Built by people from", team_link="Meet the team", team_href="/about",
        faq_eyebrow="Pricing FAQ",
        faq_h2="What buyers ask before they sign.",
        faq_sub="Anything else, ask on the call.",
        faq=[
            ("How is it billed?",
             "Per AI token. One token is roughly a minute of conversation, sometimes a "
             "little more or less depending on the call. A ring nobody answers costs "
             "nothing. The call prices above are averages across our client calls, so a "
             "long call costs more and a short one less."),
            ("Is there a setup fee?",
             "Yes, and it is usually low. It covers the build and includes a starting "
             "package of tokens. The amount depends on the use case: custom integrations "
             "and bespoke workflows are quoted and billed separately."),
            ("Is there a minimum or a contract term?",
             "You buy a package of tokens and have a set number of months to use them. "
             "We will agree the details with you on the call."),
            ("Can we run a pilot first?",
             "Yes. You get a standard testing package of tokens to see whether Sabato is "
             "a fit on your real calls. A typical pilot runs 30 to 45 days, depending on "
             "how complex the workflow is."),
            ("How fast can we go live?",
             "It depends on the use case, the implementation and how much customization "
             "you need. Typically from two weeks to 45 days from kickoff to the first "
             "live call."),
            ("Who runs the agent once it is live?",
             "We do. Proactive human management, call reviews and fixes are part of the "
             "service."),
            ("Do other languages cost more?",
             "No. Every language you sell in is included at the same price."),
            ("Does Sabato only work for e-commerce?",
             "No. E-commerce is where we started, but Sabato fits any business with a "
             "high volume of inbound calls that still runs on phone lines and customer "
             "service operators."),
        ],
        cta_h2="Stop burning out your team.<br>Give them the calls that matter.",
        cta_p=("The agent takes order status, returns and the same question at 2am. "
               "Your people take the customers who need a person. When peak season hits, "
               "Black Friday, sales or the holidays, it absorbs the spike with no extra hires."),
        cta_pilot_a="or start with a ", cta_pilot_b="30 to 45 day pilot",
        locale="en-GB",
    ),
    "it": dict(
        title="Prezzi degli agenti vocali AI | Sabato AI",
        desc="Paghi a token AI, circa un minuto di conversazione: in media €0,39 per "
             "una chiamata sullo stato dell'ordine. Calcola quanto risparmi e parti con un pilot.",
        og_locale="it_IT",
        h1="Rispondiamo a ogni chiamata.<br>Paghi solo quando si parla.",
        price_int="0", price_dec=",39",
        price_note="una chiamata “dov'è il mio ordine”, dall'inizio alla fine",
        hero_p=("Una chiamata di assistenza post-vendita costa <b>€0,53</b>, una "
                "domanda prevendita <b>€0,77</b>. Si paga a token AI, circa un "
                "minuto di conversazione: uno squillo a vuoto non costa nulla."),
        book="Prenota una call",
        call_now="oppure chiama subito l'agente",
        show="mostra il numero", hide="nascondi il numero",
        desk_h2="Molto più di un agente vocale.<br>Un vero servizio clienti, gestito dall'AI.",
        desk=[("headset", "Risponde a ogni chiamata"),
              ("bubble", "Vende come il tuo commerciale migliore"),
              ("return", "Passa la chiamata quando serve"),
              ("bars", "Trasforma le chiamate in dati"),
              ("check", "Migliora ogni giorno")],
        desk_link="Scopri il prodotto", desk_href="/it/prodotto/voice-agent-builder",
        calc_h2="Calcola quanto risparmi",
        calc_sub="Scopri quanto ti fa risparmiare un agente ogni mese rispetto a un team di operatori.",
        step1="1. Scegli il tipo di chiamata più frequente",
        step2="2. Imposta volumi e team",
        types={"wismo": "Dov'è il mio ordine", "post": "Assistenza post-vendita",
               "pre": "Prevendita"},
        f_calls=("Chiamate al mese", "Quante chiamate riceve la tua linea ogni mese."),
        f_cost=("Costo mensile di un operatore",
                "Costo aziendale: stipendio lordo, contributi, TFR, ferie, malattia e attrezzatura."),
        f_handled=("Chiamate gestite da un operatore",
                   "Al mese, al netto di pause, formazione e attività amministrative. "
                   "Tra 40 e 60 al giorno."),
        keep="Risparmi ogni mese*", extra="Costo in più ogni mese*",
        today="Oggi, al mese", with_us="Con Sabato, al mese",
        op_call="Operatore, a chiamata", us_call="Sabato, a chiamata (media)",
        v_clear="Risparmio netto", v_small="Risparmio contenuto", v_more="Costa di più",
        v_clear_t="{p}% in meno sul costo mensile, e risponde anche la domenica alle 21.",
        v_small_t=("{p}% in meno sul costo mensile. Il vero vantaggio è fuori orario "
                   "e nei picchi."),
        v_more_t=("{p}% in più al mese. A questi costi l'agente conviene fuori orario "
                  "e nei picchi, non nel turno di giorno."),
        footnote=("*Ipotizza che l'agente risolva in autonomia il {r}% delle chiamate, il "
                  "tasso che registra oggi presso il nostro cliente più grande. Il costo "
                  "per chiamata dell'operatore usa solo i tuoi due numeri: sere, weekend e "
                  "code nei picchi lo fanno salire."),
        team_label="Il team arriva da", team_link="Conosci il team", team_href="/it/chi-siamo",
        faq_eyebrow="Domande sui prezzi",
        faq_h2="Le domande che arrivano prima della firma.",
        faq_sub="Per tutto il resto, ne parliamo in call.",
        faq=[
            ("Come funziona la fatturazione?",
             "A token AI. Un token corrisponde più o meno a un minuto di conversazione, "
             "a volte qualcosa in più o in meno a seconda della chiamata. Uno squillo a "
             "cui nessuno risponde non costa nulla. I prezzi per chiamata qui sopra sono "
             "medie calcolate sulle chiamate dei nostri clienti: una chiamata lunga costa "
             "di più, una breve costa meno."),
            ("C'è un costo di attivazione?",
             "Sì, e di solito è contenuto. Copre la configurazione e include un "
             "pacchetto iniziale di token. L'importo dipende dal caso d'uso: integrazioni "
             "e flussi su misura vengono preventivati e fatturati a parte."),
            ("C'è un minimo o un vincolo contrattuale?",
             "Acquisti un pacchetto di token e hai un certo numero di mesi per usarlo. "
             "I dettagli li definiamo insieme in call."),
            ("Posso fare prima un pilot?",
             "Sì. Ricevi un pacchetto di token di prova per capire se Sabato fa al caso "
             "tuo sulle tue chiamate reali. Un pilot dura in genere tra 30 e 45 giorni, a "
             "seconda della complessità del flusso."),
            ("In quanto tempo si parte?",
             "Dipende dal caso d'uso, dall'integrazione e da quanta personalizzazione "
             "serve. Di solito tra due settimane e 45 giorni dal kickoff alla prima "
             "chiamata reale."),
            ("Chi gestisce l'agente una volta attivo?",
             "Noi. Gestione proattiva, revisione delle chiamate e correzioni fanno parte "
             "del servizio."),
            ("Le altre lingue costano di più?",
             "No. Tutte le lingue in cui vendi sono incluse, allo stesso prezzo."),
            ("Sabato funziona solo per l'e-commerce?",
             "No. Siamo partiti dall'e-commerce, ma Sabato è adatto a qualsiasi azienda "
             "con un alto volume di chiamate in entrata che lavora ancora con linee "
             "telefoniche e operatori."),
        ],
        cta_h2="Smetti di logorare il tuo team.<br>Lascia a loro le chiamate che contano.",
        cta_p=("L'agente si occupa di stato degli ordini, resi e della solita domanda alle "
               "2 di notte. Il tuo team si dedica ai clienti che hanno bisogno di parlare con "
               "qualcuno. Nei picchi, dal Black Friday ai saldi fino alle feste, regge il "
               "carico senza nuove assunzioni."),
        cta_pilot_a="oppure inizia con un ", cta_pilot_b="pilot da 30 a 45 giorni",
        locale="it-IT",
    ),
}

FONTS = """
@font-face{font-family:"Satoshi";src:url("/fuc/third-party-assets/fontshare/wf/TTX2Z3BF3P6Y5BQT3IV2VNOK6FL22KUT/7QYRJOI3JIMYHGY6CH7SOIFRQLZOLNJ6/KFIAZD4RUMEZIYV6FQ3T3GP5PDBDB6JY.woff2") format("woff2");font-display:swap;font-style:normal;font-weight:400}
@font-face{font-family:"Satoshi";src:url("/fuc/third-party-assets/fontshare/wf/P2LQKHE6KA6ZP4AAGN72KDWMHH6ZH3TA/ZC32TK2P7FPS5GFTL46EU6KQJA24ZYDB/7AHDUZ4A7LFLVFUIFSARGIWCRQJHISQP.woff2") format("woff2");font-display:swap;font-style:normal;font-weight:500}
@font-face{font-family:"Satoshi";src:url("/fuc/third-party-assets/fontshare/wf/LAFFD4SDUCDVQEXFPDC7C53EQ4ZELWQI/PXCT3G6LO6ICM5I3NTYENYPWJAECAWDD/GHM6WVH6MILNYOOCXHXB5GTSGNTMGXZR.woff2") format("woff2");font-display:swap;font-style:normal;font-weight:700}
@font-face{font-family:"Satoshi";src:url("/fuc/third-party-assets/fontshare/wf/NHPGVFYUXYXE33DZ75OIT4JFGHITX5PE/PSUTMASCDJTVPERDYJZPN23BVUFUCQIF/J64QX5IPOHK56I2KYUNBQ5M2XWZEYKYX.woff2") format("woff2");font-display:swap;font-style:normal;font-weight:900}
@font-face{font-family:"Inter";src:url("/fuc/assets/GrgcKwrN6d3Uz8EwcLHZxwEfC4.woff2") format("woff2");font-display:swap;font-style:normal;font-weight:400;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+20AC,U+2122}
"""

CSS = """
:root{--lime:#ccff00;--black:#000;--ink:#0b0b0c;--soft:#454140;--muted:#6f6a66;--cool:#f9fafd;--line:#e3e2e2;--faint:rgba(11,11,12,.1);--cream:#f8f4f1}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font-family:"Satoshi","Inter",-apple-system,"Helvetica Neue",sans-serif;-webkit-font-smoothing:antialiased}
.pc{padding:16px 16px 72px;display:flex;flex-direction:column;align-items:center;gap:64px}
.pc h1,.pc h2,.pc h3,.pc p{margin:0}
.pc>section,.pc>.pc-head{width:100%;max-width:1200px}
.pc-eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:13px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.pc-eyebrow::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--lime);flex:0 0 auto}
.pc-h2{font-size:40px;line-height:1.1;font-weight:700;letter-spacing:-1.4px}
.pc-head{display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px}
.pc-head p{font-size:16px;line-height:1.55;color:var(--muted);max-width:560px}
.pc-lnk{color:var(--ink);font-weight:700;font-size:15px;text-decoration:none;border-bottom:2px solid var(--lime);padding-bottom:2px}
.pc-lnk:hover{border-bottom-color:var(--ink)}
.pc-btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 30px;border-radius:999px;font:700 17px "Satoshi","Inter",sans-serif;text-decoration:none}
.pc a:focus-visible,.pc button:focus-visible,.pc input:focus-visible{outline:none;box-shadow:0 0 0 2px #fff,0 0 0 4px var(--ink)}
.pc-hero a:focus-visible,.pc-hero button:focus-visible{box-shadow:0 0 0 2px #000,0 0 0 4px var(--lime)}

/* hero */
.pc-hero{background:#000;border-radius:24px;padding:72px 24px 56px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:24px;color:#fff}
.pc-hero h1{font-size:clamp(40px,5.4vw,64px);font-weight:700;letter-spacing:-2.2px;line-height:1.04}
.pc-price{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;margin-top:16px}
.pc-amount{display:flex;align-items:flex-start;color:var(--lime)}
.pc-cur{font-size:clamp(32px,3.6vw,44px);font-weight:700;letter-spacing:-1.4px;line-height:1.1;margin:8px 6px 0 0}
.pc-num{font-size:clamp(84px,12vw,120px);font-weight:900;letter-spacing:-5px;line-height:.9}
.pc-price p{font-size:17px;line-height:1.55;text-align:left;font-weight:700;color:rgba(248,244,241,.85);max-width:170px}
.pc-hero>p{font-size:17px;line-height:1.55;color:rgba(248,244,241,.75);max-width:560px}
.pc-hero>p b{color:#fff}
.pc-hero .pc-btn{background:#fff;color:#000;margin-top:12px}
.pc-callnow{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:8px}
.pc-callnow>span{font-size:13px;line-height:1.5;color:rgba(248,244,241,.7);margin-right:6px}
.pc-phones{display:inline-flex;gap:8px;flex-wrap:wrap;justify-content:center}
.pc-ph{display:inline-flex;align-items:center;gap:8px;font:700 13px "Satoshi","Inter",sans-serif;letter-spacing:.02em;color:var(--cream);background:transparent;border:1px solid rgba(248,244,241,.28);border-radius:999px;padding:0 14px;min-height:44px;cursor:pointer;font-variant-numeric:tabular-nums}
.pc-ph:hover{border-color:var(--cream)}
.pc-ph svg{display:block;width:18px;height:12px}
.pc-ph .pc-ph-no{display:none;white-space:nowrap}
.pc-ph[aria-expanded="true"]{background:var(--lime);border-color:var(--lime);color:#000}
.pc-ph[aria-expanded="true"] .pc-ph-no{display:inline}

/* desk strip */
.pc-desk{display:flex;flex-direction:column;align-items:center;gap:24px;padding:8px 0}
.pc-desk h2{text-align:center;max-width:760px}
.pc-pills{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;list-style:none;margin:0;padding:0}
.pc-pills li{display:flex;align-items:center;gap:10px;padding:12px 18px 12px 12px;border-radius:999px;background:#000;color:#fff;font-size:15px;line-height:1.2;font-weight:700}
.pc-pills svg{flex:0 0 auto;width:22px;height:22px}

/* calculator */
.pc-calc{display:flex;flex-wrap:wrap;gap:16px;align-items:stretch}
.pc-in{flex:999 1 480px;min-width:0;background:var(--cool);border-radius:20px;padding:48px 40px;display:flex;flex-direction:column;gap:16px}
.pc-step{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.pc-types{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.pc-type{font-family:inherit;color:var(--ink);background:#fff;border:1px solid var(--line);padding:20px 18px;min-height:176px;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-end;gap:6px;text-align:left;border-radius:20px;cursor:pointer;transition:transform .15s}
.pc-type:hover{transform:translateY(-3px)}
.pc-type[aria-pressed="true"]{background:var(--lime);border-color:var(--lime);color:#000}
.pc-type i{display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:#000;margin-bottom:auto}
.pc-type i svg{width:28px;height:28px}
.pc-type b{display:block;font-size:13px;font-weight:700;line-height:1.3}
.pc-type strong{display:block;font-size:40px;font-weight:900;letter-spacing:-1.6px;margin-top:14px;line-height:1}
.pc-fields{display:flex;flex-direction:column;gap:16px}
.pc-field{display:flex;flex-direction:column;gap:14px;padding:24px;background:#fff;border-radius:16px;border:1px solid rgba(11,11,12,.08)}
.pc-fhead{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.pc-fhead label{display:block;font-size:15px;font-weight:700}
.pc-fhead small{display:block;margin-top:4px;font-size:13px;line-height:1.4;color:var(--muted)}
.pc-fhead output{font-size:26px;font-weight:700;letter-spacing:-.8px;white-space:nowrap}
.pc-field input{width:100%;margin:0;accent-color:var(--ink);height:24px;cursor:pointer}
.pc-out{flex:1 1 440px;min-width:0;background:#000;color:#fff;border-radius:20px;padding:44px 40px;display:flex;flex-direction:column;gap:28px;justify-content:space-between}
.pc-lab{font-size:13px;font-weight:700;color:rgba(248,244,241,.7)}
.pc-big{font-size:clamp(56px,8vw,96px);line-height:1;font-weight:900;letter-spacing:-4px;margin-top:8px;color:var(--lime);font-variant-numeric:tabular-nums}
.pc-split{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;padding-top:24px;border-top:1px solid rgba(248,244,241,.16)}
.pc-split strong{display:block;font-size:28px;font-weight:700;letter-spacing:-.8px;margin-top:4px}
.pc-split .pc-was{color:rgba(248,244,241,.6)}
.pc-bars{display:flex;flex-direction:column;gap:10px}
.pc-barlab{display:flex;justify-content:space-between;font-size:13px;font-weight:700}
.pc-barlab+.pc-track+.pc-barlab{margin-top:4px}
.pc-track{height:10px;border-radius:999px;background:rgba(255,255,255,.14)}
.pc-track span{display:block;height:10px;border-radius:999px;min-width:3%;transition:width .2s}
.pc-track .pc-t{background:rgba(255,255,255,.5)}
.pc-track .pc-s{background:var(--lime)}
.pc-verdict{border-radius:16px;padding:18px 20px;background:rgba(204,255,0,.1)}
.pc-verdict[data-tone="small"]{background:rgba(255,179,92,.12)}
.pc-verdict[data-tone="more"]{background:rgba(255,255,255,.08)}
.pc-vtag{font-size:12px;font-weight:700;letter-spacing:2.16px;text-transform:uppercase;color:var(--lime)}
.pc-verdict[data-tone="small"] .pc-vtag{color:#ffb35c}
.pc-verdict[data-tone="more"] .pc-vtag{color:#ff8a80}
.pc-vtext{font-size:16px;line-height:1.45;font-weight:700;margin-top:6px}
.pc-note{font-size:12.5px;line-height:1.5;color:rgba(248,244,241,.6)}

/* team */
.pc-team{display:flex;flex-wrap:wrap;align-items:center;gap:20px 40px;padding:22px 8px;border-top:1px solid var(--faint);border-bottom:1px solid var(--faint)}
.pc-logos{flex:1 1 560px;min-width:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));align-items:center;justify-items:center;gap:16px 24px}
.pc-logos img{display:block;width:auto;max-width:100%;filter:grayscale(1);opacity:.6}
.pc-team .pc-lnk{margin-left:auto}

/* faq */
.pc-faq{display:flex;flex-wrap:wrap;gap:32px 64px;padding-top:32px;border-top:1px solid var(--faint)}
.pc-faq-head{flex:1 1 300px;min-width:0;display:flex;flex-direction:column;gap:12px;align-items:flex-start}
.pc-faq-head p{font-size:16px;line-height:1.55;color:var(--muted)}
.pc-faq-list{flex:999 1 560px;min-width:0}
.pc-q{border-bottom:1px solid var(--faint)}
.pc-q summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:24px;padding:22px 0;font-size:18px;line-height:1.4;font-weight:700;cursor:pointer}
.pc-q summary::-webkit-details-marker{display:none}
.pc-q summary::after{content:"";flex:0 0 18px;height:18px;background:linear-gradient(var(--ink),var(--ink)) center/16px 1.8px no-repeat,linear-gradient(var(--ink),var(--ink)) center/1.8px 16px no-repeat}
.pc-q[open] summary::after{background:linear-gradient(var(--ink),var(--ink)) center/16px 1.8px no-repeat}
.pc-q p{margin:0 0 26px;max-width:720px;font-size:16px;line-height:1.7;color:var(--muted)}

/* closing band */
.pc-close{border-radius:40px;background:linear-gradient(90deg,#f7fd47 0%,#8dfe44 50%,#2bfe41 100%);padding:56px 24px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:18px;color:#000}
.pc-close h2{font-size:clamp(36px,4.6vw,56px);line-height:1.06;font-weight:700;letter-spacing:-2px;max-width:820px}
.pc-close>p{font-size:17px;line-height:1.55;max-width:560px}
.pc-close .pc-btn{background:var(--ink);color:#fff}
.pc-close .pc-pilot{font-size:15px;line-height:1.5;margin-top:-4px}
.pc-close .pc-pilot a{color:#000;font-weight:700}
.pc .sb-proof-inline{width:100%;max-width:1200px}

@media (max-width:809px){
  .pc{gap:48px;padding:12px 12px 56px}
  .pc-hero{padding:48px 20px 40px}
  .pc-h2{font-size:30px;letter-spacing:-1px}
  .pc-in,.pc-out{padding:28px 20px}
  .pc-types{grid-template-columns:1fr;gap:10px}
  .pc-type{min-height:0;flex-direction:row;align-items:center;justify-content:flex-start;gap:14px;padding:14px 16px}
  .pc-type i{margin:0;width:40px;height:40px;flex:0 0 40px}
  .pc-type i svg{width:22px;height:22px}
  .pc-type b{flex:1}
  .pc-type strong{font-size:26px;margin:0}
  .pc-field{padding:18px}
  .pc-fhead{flex-direction:column;gap:6px}
  .pc-big{letter-spacing:-2px}
  .pc-split strong{font-size:22px}
  .pc-logos{grid-template-columns:repeat(3,minmax(0,1fr));flex-basis:100%}
  .pc-team .pc-lnk{margin-left:0}
  .pc-q summary{font-size:16px}
  .pc-close{border-radius:24px;padding:40px 20px}
}
"""

# One small script, no framework. State lives in the DOM: the pressed type
# button carries its price, the three ranges carry their own values.
CALC_JS = r"""
(function(){
var root=document.getElementById('pc-calc');if(!root)return;
var L=root.dataset,R=+L.rate/100,fmt=new Intl.NumberFormat(L.locale,{maximumFractionDigits:0}),
two=new Intl.NumberFormat(L.locale,{minimumFractionDigits:2,maximumFractionDigits:2});
function eur(n){return '€'+fmt.format(Math.round(n));}
function eur2(n){return '€'+two.format(n);}
function $(s){return root.querySelector(s);}
var types=root.querySelectorAll('.pc-type'),calls=$('#pc-calls'),cost=$('#pc-cost'),hand=$('#pc-handled');
function run(){
  var t=root.querySelector('.pc-type[aria-pressed="true"]')||types[0],price=+t.dataset.price;
  var c=+calls.value,sc=+cost.value,sh=+hand.value;
  var perOp=sc/sh,today=c*perOp,withUs=c*(1-R)*perOp+c*price,diff=today-withUs,save=today?diff/today:0;
  $('#pc-o-calls').textContent=fmt.format(c);
  $('#pc-o-cost').textContent=eur(sc);
  $('#pc-o-handled').textContent=fmt.format(sh);
  $('#pc-head').textContent=diff>=0?L.keep:L.extra;
  $('#pc-big').textContent=eur(Math.abs(diff));
  $('#pc-today').textContent=eur(today);
  $('#pc-with').textContent=eur(withUs);
  $('#pc-opcall').textContent=eur2(perOp);
  $('#pc-uscall').textContent=eur2(price);
  var m=Math.max(perOp,price);
  $('#pc-bt').style.width=Math.max(3,Math.round(perOp/m*100))+'%';
  $('#pc-bs').style.width=Math.max(3,Math.round(price/m*100))+'%';
  var v=$('.pc-verdict'),tone=save>=.3?'clear':(save>=0?'small':'more'),p=Math.round(Math.abs(save)*100);
  v.setAttribute('data-tone',tone);
  $('.pc-vtag').textContent=L['tag'+tone];
  $('.pc-vtext').textContent=L['txt'+tone].replace('{p}',p);
}
for(var i=0;i<types.length;i++)types[i].addEventListener('click',function(){
  for(var j=0;j<types.length;j++)types[j].setAttribute('aria-pressed','false');
  this.setAttribute('aria-pressed','true');run();});
[calls,cost,hand].forEach(function(el){el.addEventListener('input',run);});
run();
})();
(function(){
var b=document.querySelectorAll('.pc-ph');
for(var i=0;i<b.length;i++)b[i].addEventListener('click',function(){
  var open=this.getAttribute('aria-expanded')==='true';
  for(var j=0;j<b.length;j++){b[j].setAttribute('aria-expanded','false');b[j].setAttribute('aria-label',b[j].dataset.show);}
  if(!open){this.setAttribute('aria-expanded','true');this.setAttribute('aria-label',this.dataset.hide);}
});
})();
"""


def esc(s):
    return html.escape(s, quote=True)


def svg(name, stroke="#ccff00", w=1.8):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false">{ICON[name]}</svg>')


def price_label(p, lang):
    s = f"€{p:.2f}"
    return s.replace(".", ",") if lang == "it" else s


def hero(c, lang):
    phones = "".join(
        f'<button type="button" class="pc-ph" aria-expanded="false" '
        f'aria-label="{esc((lab_en if lang == "en" else lab_it) + ", " + c["show"])}" '
        f'data-show="{esc((lab_en if lang == "en" else lab_it) + ", " + c["show"])}" '
        f'data-hide="{esc((lab_en if lang == "en" else lab_it) + ", " + c["hide"])}">'
        f'{FLAG[code]}<span class="pc-ph-no">{esc(disp)}</span></button>'
        for code, lab_en, lab_it, disp, _tel in NUMBERS)
    return (
        '<section class="pc-hero">'
        f'<h1>{c["h1"]}</h1>'
        '<div class="pc-price">'
        f'<div class="pc-amount" aria-label="€{c["price_int"]}{c["price_dec"]}">'
        f'<span class="pc-cur" aria-hidden="true">€</span>'
        f'<span class="pc-num" aria-hidden="true">{c["price_int"]}{c["price_dec"]}</span></div>'
        f'<p>{esc(c["price_note"])}</p></div>'
        f'<p>{c["hero_p"]}</p>'
        f'<a class="pc-btn" href="{CAL}" target="_blank" rel="noopener">{c["book"]}</a>'
        f'<div class="pc-callnow"><span>{esc(c["call_now"])}</span>'
        f'<div class="pc-phones">{phones}</div></div>'
        '</section>')


def desk(c):
    pills = "".join(f'<li>{svg(icon, w=1.9 if icon in ("bars", "check") else 1.8)}{esc(t)}</li>'
                    for icon, t in c["desk"])
    return (
        '<section class="pc-desk">'
        f'<h2 class="pc-h2">{c["desk_h2"]}</h2>'
        f'<ul class="pc-pills">{pills}</ul>'
        f'<a class="pc-lnk" href="{c["desk_href"]}">{esc(c["desk_link"])} →</a>'
        '</section>')


def calculator(c, lang):
    types = "".join(
        f'<button type="button" class="pc-type" data-price="{p}" '
        f'aria-pressed="{"true" if i == 0 else "false"}">'
        f'<i>{svg(TYPE_ICON[k])}</i><b>{esc(c["types"][k])}</b>'
        f'<strong>{price_label(p, lang)}</strong></button>'
        for i, (k, p) in enumerate(PRICES))

    def field(fid, out, label_sub, lo, hi, step, val):
        lab, sub = label_sub
        return (f'<div class="pc-field"><div class="pc-fhead"><div>'
                f'<label for="{fid}">{esc(lab)}</label><small>{esc(sub)}</small></div>'
                f'<output id="{out}" for="{fid}"></output></div>'
                f'<input id="{fid}" type="range" min="{lo}" max="{hi}" step="{step}" value="{val}">'
                f'</div>')

    data = {
        "rate": RESOLVE_RATE, "locale": c["locale"], "keep": c["keep"], "extra": c["extra"],
        "tagclear": c["v_clear"], "tagsmall": c["v_small"], "tagmore": c["v_more"],
        "txtclear": c["v_clear_t"], "txtsmall": c["v_small_t"], "txtmore": c["v_more_t"],
    }
    attrs = " ".join(f'data-{k}="{esc(str(v))}"' for k, v in data.items())
    return (
        '<div class="pc-head">'
        f'<h2 class="pc-h2">{esc(c["calc_h2"])}</h2>'
        f'<p>{esc(c["calc_sub"])}</p></div>'
        f'<section class="pc-calc" id="pc-calc" {attrs}>'
        '<div class="pc-in">'
        f'<p class="pc-step">{esc(c["step1"])}</p>'
        f'<div class="pc-types">{types}</div>'
        f'<p class="pc-step">{esc(c["step2"])}</p>'
        '<div class="pc-fields">'
        + field("pc-calls", "pc-o-calls", c["f_calls"], 100, 5000, 50, 1200)
        + field("pc-cost", "pc-o-cost", c["f_cost"], 1500, 7000, 100, 3000)
        + field("pc-handled", "pc-o-handled", c["f_handled"], 200, 2500, 50, 900)
        + '</div></div>'
        '<div class="pc-out" aria-live="polite">'
        f'<div><p class="pc-lab" id="pc-head">{esc(c["keep"])}</p><p class="pc-big" id="pc-big"></p></div>'
        '<div class="pc-split">'
        f'<div><p class="pc-lab">{esc(c["today"])}</p><strong class="pc-was" id="pc-today"></strong></div>'
        f'<div><p class="pc-lab">{esc(c["with_us"])}</p><strong id="pc-with"></strong></div></div>'
        '<div class="pc-bars">'
        f'<div class="pc-barlab"><span>{esc(c["op_call"])}</span><span id="pc-opcall"></span></div>'
        '<div class="pc-track"><span class="pc-t" id="pc-bt"></span></div>'
        f'<div class="pc-barlab"><span>{esc(c["us_call"])}</span><span id="pc-uscall"></span></div>'
        '<div class="pc-track"><span class="pc-s" id="pc-bs"></span></div></div>'
        f'<div class="pc-verdict" data-tone="clear"><p class="pc-vtag">{esc(c["v_clear"])}</p><p class="pc-vtext"></p></div>'
        f'<p class="pc-note">{esc(c["footnote"].format(r=RESOLVE_RATE))}</p>'
        '</div></section>')


def team(c):
    logos = "".join(
        f'<img src="/brand/team/{f}" alt="{esc(alt)}" height="{h}" style="height:{h}px" '
        f'loading="lazy" decoding="async">'
        for f, alt, h in TEAM)
    return (
        '<section class="pc-team">'
        f'<p class="pc-eyebrow">{esc(c["team_label"])}</p>'
        f'<div class="pc-logos">{logos}</div>'
        f'<a class="pc-lnk" href="{c["team_href"]}">{esc(c["team_link"])} →</a>'
        '</section>')


def faq(c):
    items = "".join(
        f'<details class="pc-q"{" open" if i == 0 else ""}><summary>{esc(q)}</summary>'
        f'<p>{esc(a)}</p></details>'
        for i, (q, a) in enumerate(c["faq"]))
    return (
        '<section class="pc-faq">'
        '<div class="pc-faq-head">'
        f'<p class="pc-eyebrow">{esc(c["faq_eyebrow"])}</p>'
        f'<h2 class="pc-h2">{esc(c["faq_h2"])}</h2>'
        f'<p>{esc(c["faq_sub"])}</p></div>'
        f'<div class="pc-faq-list">{items}</div>'
        '</section>')


def close(c):
    return (
        '<section class="pc-close">'
        f'<h2>{c["cta_h2"]}</h2>'
        f'<p>{esc(c["cta_p"])}</p>'
        f'<a class="pc-btn" href="{CAL}" target="_blank" rel="noopener">{c["book"]}</a>'
        f'<p class="pc-pilot">{esc(c["cta_pilot_a"])}'
        f'<a href="{CAL}" target="_blank" rel="noopener">{esc(c["cta_pilot_b"])}</a></p>'
        '</section>')


def jsonld(c, lang):
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "inLanguage": lang,
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}}
                             for q, a in c["faq"]]}
    return ('<script type="application/ld+json">'
            + json.dumps(faq_ld, ensure_ascii=False).replace("</", "<\\/")
            + '</script>')


def enhance_src():
    """Whatever version the rest of the site currently loads; version_enhance.py
    rewrites it on every build anyway."""
    p = os.path.join(SITE, "product", "voice-agent-builder.html")
    import re
    m = re.search(r'<script src="(/js/enhance\.js[^"]*)" defer></script>',
                  open(p, encoding="utf-8").read())
    return m.group(1) if m else "/js/enhance.js"


def page(lang):
    c = COPY[lang]
    head = (
        '<!DOCTYPE html>\n'
        f'<html lang="{lang}">\n<head>\n'
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'  <title>{esc(c["title"])}</title>\n'
        f'  <meta name="description" content="{esc(c["desc"])}">\n'
        f'  <link rel="canonical" href="{URL[lang]}">\n'
        '  <meta property="og:type" content="website">\n'
        f'  <meta property="og:title" content="{esc(c["title"])}">\n'
        f'  <meta property="og:description" content="{esc(c["desc"])}">\n'
        f'  <meta property="og:url" content="{URL[lang]}">\n'
        f'  <meta property="og:image" content="{OG_IMAGE}">\n'
        f'  <meta property="og:locale" content="{c["og_locale"]}">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        '  <link href="/fuc/images/hWFOqN6Okd1QgfKhizqgIF1s.png" rel="icon" media="(prefers-color-scheme: light)">\n'
        '  <link href="/fuc/images/dEcuqc3xAQ3JJoX4xQDYrMQefA.png" rel="icon" media="(prefers-color-scheme: dark)">\n'
        '  <link rel="apple-touch-icon" href="/fuc/images/dEcuqc3xAQ3JJoX4xQDYrMQefA.png">\n'
        f'  <link rel="alternate" hreflang="en" href="{URL["en"]}">'
        f'<link rel="alternate" hreflang="it" href="{URL["it"]}">'
        f'<link rel="alternate" hreflang="x-default" href="{URL["en"]}">\n'
        f'  {jsonld(c, lang)}\n'
        f'  <style>{FONTS}{CSS}</style>\n'
        '</head>\n')
    body = (
        '<body>\n'
        '<main class="pc">\n'
        f'{hero(c, lang)}\n{desk(c)}\n{calculator(c, lang)}\n'
        f'{proof_inline_html(lang)}\n{team(c)}\n{faq(c)}\n{close(c)}\n'
        '</main>\n'
        f'<script>{CALC_JS}</script>\n'
        f'<script src="{enhance_src()}" defer></script>\n'
        '</body>\n</html>\n')
    return head + body


def main():
    for lang, rel in OUT.items():
        path = os.path.join(SITE, rel)
        open(path, "w", encoding="utf-8").write(page(lang))
        print(f"  wrote site/{rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
