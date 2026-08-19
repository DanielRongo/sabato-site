#!/usr/bin/env python3
"""THE pricing page - one all-inclusive per-minute rate, and the arguments for it.

    python3 pricing.py          # print the English block
    python3 pricing.py it       # Italian

Import it: `from pricing import pricing_html, PAGES`.


WHY THIS REPLACES THE FRAMER PAGE RATHER THAN EDITING IT
--------------------------------------------------------
Framer's pricing page sells three monthly tiers with features gated per tier:
1 workflow and 1 language on Store, 3 and 2 on Merchant. That model is dead as
of 19 Aug 2026. It also contradicted the homepage FAQ we shipped on the 18th,
which already said "no separate platform fee and no per-seat license" - a buyer
reading both pages could not tell what they would pay.

The Framer bands stay in the file and never render. Editing them is not an
option: React re-renders the body at hydration and throws HTML edits away. Same
lesson as the homepage, learned the same expensive way.


WHY THIS IS STATIC AND NOT A JS PASS
------------------------------------
"How much does voice AI for e-commerce cost" is one of the highest-intent
queries in this category and one of the most-asked questions of answer engines.
Anything enhance.js builds is invisible to a crawler that does not run
JavaScript, and several of the engines that matter here do not. So the price,
the inclusion list, the invoice comparison and the FAQ all ship in the HTML,
injected by tools/apply_footer.py OUTSIDE React's root.

apply_footer can only inject in two places: the top of <body>, before the root,
and just before </body>, after it. There is no middle. Everything here goes in
the TOP block, immediately after the header, which is why the page reads
hero, minute, calculator, invoices, comparison, FAQ before any Framer content.
The only JavaScript is the volume slider and the dial reveal, and the page is
complete and correct with both switched off.


THE COMMERCIAL MODEL, AS AGREED
-------------------------------
  * One rate, everything in it. No tiers, no feature gating, no setup fee, no
    minimum, no lock-in. Billed by the second.
  * $0.65 on the English site, 0,55 EUR on the Italian one. At the 19 Aug 2026
    rate of 1.1575 those are within two per cent, which is parity, not a
    discount for the Italian market. Deliberate.
  * The headline is the TOP of the range, not the middle. Nobody is ever quoted
    more than the page says, and the volume bands then read as a reward for
    growing rather than a discount somebody had to negotiate.
  * NEVER a per-call price. A 40 second WISMO call and a 5 minute pre-sales
    call are not the same product, and an average invites an argument we lose.
    The three worked examples in the calculator teach the model instead, and
    turn billing by the second into a selling point.
  * Comparisons name categories, never brands. The invoice line items are a
    labelled composite of what this category charges, not a quote from anyone.


NAMESPACE
---------
Everything is prefixed sb-px-, which appears nowhere in footer.css, enhance.js,
any emitter or any built page - checked before a line was written. The footer
disaster of 18 Aug came from reusing .sb-col, a name the footer already owned,
and it shipped invisible links on 112 pages because the click test asserted
behaviour and never looked at a colour. Namespace first, always.

The one deliberate exception is the dial row, which reuses hero.py's card
component wholesale, including its class names, so the reveal script and the
no-JS fallback come along unchanged. Those cards are styled for the homepage's
black card; six overrides scoped under .sb-px-dial repaint them for a white
page and touch nothing outside it.

NO LONG DASHES. Standing rule, and tools/dedash.py enforces it site-wide.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from hero import _cards as dial_cards, REVEAL_SCRIPT  # noqa: E402

CAL = "https://cal.com/sabatoai/intro"

PAGES = {"pricing.html", "it/prezzi.html"}

# Framer's own bands on this page. "Pricing Section" carries the three dead
# tiers; "FAQ Section" is upper-case here and "Faq Section" on / and /about,
# which is why every selector in this file is case-insensitive. Testimonials is
# empty on /pricing and proof.py puts Success Stories in at the foot instead.
HIDE_FRAMER = (
    '<style id="sb-px-hide">'
    '[data-framer-name="Pricing Section" i],'
    '[data-framer-name="FAQ Section" i],'
    '[data-framer-name="Testimonials Section" i]{display:none !important}'
    "</style>")


# ---------------------------------------------------------------------------
# COPY
#
# English figures use US benchmarks, Italian ones European. The alternative was
# converting one set into the other, which would have put a euro-shaped number
# behind a dollar sign. The engineer is costed at HALF a person, not a whole
# one, because that is the honest read of what a DIY voice build actually
# consumes and because a number a technical buyer can attack is worth less than
# a smaller number they cannot.
# ---------------------------------------------------------------------------
COPY = {
    "en": dict(
        title="Pricing",
        eyebrow="PRICING",
        h1="You only pay when <br>the line is talking.",
        cur="$", rate="0.65", unit="per minute of talk",
        pill="ALL IN", pill_sub="managed service included",
        rate_sub=("billed by the second, so a 40 second call costs 40 seconds. "
                  "Volume brings the rate down to $0.55."),
        incl_head="everything below is already in that number",
        incl=["the build", "the integrations", "every workflow",
              "every language you sell in", "proactive human management",
              "agent evaluation and optimization"],
        nots=["platform fee", "setup fee", "per seat license",
              "per workflow charge", "language surcharge", "minimum contract"],
        nots_lab="not charged, ever",
        book="Book a call",
        dial_lab="or call the agent right now, it picks up",

        # --- the decomposed minute ---
        m_h2="Managed is not a tier. It is inside the minute.",
        m_lede=("Everyone in this category sells you software and then sells you "
                "the people to run it. We put both in one number."),
        m_a_lab="Sabato, one minute at $0.65",
        m_b_lab="A DIY build, one minute",
        m_shared=[(11, "telephony"), (15, "speech and reasoning"),
                  (10, "catalog and order lookups")],
        m_ours=[(16, "the build"), (14, "monitoring and QA"),
                (18, "weekly tuning"), (16, "proactive management")],
        m_ghost="you",
        m_outside="plus $6,000 a month of engineer, sitting outside the bar",
        m_fine=("Segment widths are illustrative, not a cost breakdown. The point "
                "is which work is inside the price."),

        # --- the calculator ---
        c_h2="What you would actually pay",
        c_lede=("Nobody knows their minutes. Everybody knows their calls. So the "
                "slider starts there."),
        c_calls="calls per month",
        c_avg="average call length",
        c_min="minutes", c_month="/ month",
        c_band="at $0.60, your volume band",
        c_note="No minimum, no monthly fee. A quiet month is a small invoice.",
        c_ex_lab="because it is billed by the second, short calls stay cheap",
        c_ex=[("Where is my order", "40 seconds", "$0.43"),
              ("Return request", "2 minutes", "$1.30"),
              ("Pre-sales question", "5 minutes", "$3.25")],
        c_bands=[("under 5,000 minutes", "$0.65", "most stores start here"),
                 ("5,000 to 20,000", "$0.60", "one busy line, or several workflows"),
                 ("above 20,000", "$0.55", "peak season, or a catalog that never sleeps")],

        # --- the invoices ---
        i_h2="Why are we more expensive? <br>We are not.",
        i_lede=("You are comparing our whole price with somebody else&rsquo;s first "
                "line. Here is the same month, 4,000 minutes, billed both ways."),
        i_their_h="A $0.15 a minute quote", i_their_sub="what actually arrives",
        i_ours_h="Sabato", i_ours_sub="what actually arrives",
        i_rows=[("platform, the advertised rate", "$0.15 / min", "$600", "on their pricing page"),
                ("telephony passthrough", "$0.02 / min", "$80", "billed at cost, on top"),
                ("speech and model usage", "$0.06 / min", "$240", "usage based, varies monthly"),
                ("management retainer", "monthly", "$1,500", "the part that makes it work"),
                ("agent evaluation tooling", "monthly", "$250", "per seat, often a separate product"),
                ("prompt and workflow changes", "6 hours", "$720", "billed hourly, or as change requests"),
                ("second language", "monthly", "$300", "an add-on"),
                ("setup fee, spread over 12 months", "$3,000 one off", "$250", "paid before anything answers")],
        i_ours_row=("4,000 minutes of talk", "$0.65 / min", "$2,600", "everything included"),
        i_nothing="nothing else",
        i_tot="total for the month",
        i_their_tot="$3,940", i_ours_tot="$2,600",
        i_eff="effective rate", i_eff_unit="per minute",
        i_their_eff="$0.99", i_ours_eff="$0.65",
        i_note=("The left column is a composite of what these line items typically "
                "cost in this category, not a quote from a named vendor. Ask any "
                "provider quoting you a low per minute rate for the same three "
                "numbers: what is the monthly retainer, what do prompt changes "
                "cost, and what is the effective rate once telephony and model "
                "usage land. If they cannot answer in one line, that is the answer."),

        # --- three ways ---
        t_h2="Three ways to answer the phone",
        t_lede="Same job. Very different bills. Category averages, not competitor bashing.",
        t_assume=("Priced for one store doing <b>4,000 minutes a month</b>, roughly "
                  "900 calls. Bar heights are the real monthly numbers, to scale."),
        t_cols=[
            dict(h="Sabato", acc=True, bars=[(87, "everything, all in", "lime")],
                 tot="$2,600", per="$0.65 per minute, managed included",
                 foot="One line on the invoice. The build, the tuning and the people are already in it."),
            dict(h="DIY voice platform", acc=False,
                 bars=[(24, "platform, models, telephony", "blue"),
                       (200, "half an engineer, loaded", "hatch")],
                 tot="$6,720", per="$0.18 per minute, plus $6,000 of engineer",
                 foot="Genuinely cheaper per minute. The person who builds and babysits it is the whole cost."),
            dict(h="Outsourced call center", acc=False,
                 bars=[(64, "direct labor", "clay"), (27, "supervisors, floor space, margin", "clay2"),
                       (16, "idle time you still pay for", "hatch2")],
                 tot="$3,200", per="$0.80 per minute of talk",
                 foot="An agent gives about 44 productive minutes in a paid hour. You buy the other 16 too."),
        ],
        t_rows=[("who builds it", "we do", "your engineer", "their trainers, from your script"),
                ("who answers at 2am in December", "the agent", "nobody", "a night shift, if you pay for one"),
                ("languages", "every one you sell in", "whatever you built", "one per team, priced separately"),
                ("time to live", "weeks", "3 to 6 months", "4 to 8 weeks of training"),
                ("what happens at peak", "every call at once", "your queue, your problem", "hold music, or overtime")],

        # --- FAQ ---
        f_eyebrow="FAQ",
        f_h2="Pricing questions",
        f_items=[
            ("How much does managed voice AI for e-commerce cost?",
             "Sabato costs $0.65 per minute of connected talk time, billed by the second, and the rate falls to $0.60 above 5,000 minutes a month and $0.55 above 20,000. That single rate covers the workflow build, the integrations, every language, every workflow, the proactive human management and the ongoing agent evaluation. There is no platform fee, no per-seat license, no setup fee and no minimum contract."),
            ("What exactly counts as a minute?",
             "Connected talk time, billed by the second. A 40 second call is billed as 40 seconds, not rounded up to a minute. Ringing is not billed. Hold time inside a call is billed, because the agent is still working that call."),
            ("Is the managed service really included in the per minute price?",
             "Yes. The workflow build, the integration work, the proactive human management, the agent evaluation and the ongoing optimization are all paid for out of the per minute rate. There is no separate retainer and no professional services line on a Sabato invoice."),
            ("Why is your per minute rate higher than other voice AI platforms?",
             "Because theirs is a platform rate and ours is a total. A platform rate covers software. It does not cover telephony, speech and model usage, the person who builds your workflows, the person who reviews the calls, or the changes you will want in month two. Once those land, the effective rate in this category is typically close to $1.00 a minute. Sabato is $0.65 and there is nothing else to add."),
            ("What if I need a second language or a third workflow?",
             "Both are included. Languages and workflows never change your rate. Volume is the only thing that does."),
            ("Is there a minimum contract or a setup fee?",
             "Neither. There is no lock-in, no onboarding fee and no minimum spend. You are billed monthly for the minutes you actually used."),
            ("How does this compare to a DIY build on a voice platform?",
             "A DIY build costs roughly $0.18 a minute in platform, model and telephony fees, plus the engineer who builds and maintains it. At 4,000 minutes a month that is about $6,720 against $2,600 with Sabato. A DIY build only becomes cheaper above roughly 14,000 minutes a month, and only if the build works."),
            ("How does it compare to an outsourced call center?",
             "An outsourced agent costs roughly $29 to $42 an hour and delivers about 44 productive minutes in each paid hour, which puts a real minute of conversation near $0.80 before supervisors and margin. Sabato is $0.65, answers every call at once, and bills nothing when the line is quiet."),
            ("What happens during peak season?",
             "Nothing. The line answers every call at once, with no queue and no overtime. You pay for the minutes, and your rate improves as the volume climbs."),
        ],
    ),
}

COPY["it"] = dict(
    title="Prezzi",
    eyebrow="PREZZI",
    h1="Paghi solo quando <br>la linea parla.",
    # Italian writes the symbol after the amount and uses a decimal comma. The
    # blog posts already do this; the emitter reads cur_after to place it.
    cur="&euro;", cur_after=True, rate="0,55", unit="al minuto di conversazione",
    pill="TUTTO INCLUSO", pill_sub="servizio gestito incluso",
    rate_sub=("fatturato al secondo, quindi una chiamata di 40 secondi costa 40 "
              "secondi. Con il volume la tariffa scende a 0,45 &euro;."),
    incl_head="tutto quello che vedi qui sotto &egrave; gi&agrave; in quel numero",
    incl=["la configurazione", "le integrazioni", "tutti i workflow",
          "tutte le lingue in cui vendi", "gestione umana proattiva",
          "valutazione e ottimizzazione dell&rsquo;agente"],
    nots=["costo di piattaforma", "costo di attivazione", "licenza per utente",
          "costo per workflow", "sovrapprezzo lingua", "contratto minimo"],
    nots_lab="mai in fattura",
    book="Prenota una call",
    dial_lab="oppure chiama l&rsquo;agente adesso, risponde",

    m_h2="La gestione non &egrave; un piano. &Egrave; dentro il minuto.",
    m_lede=("Tutti in questo settore ti vendono il software e poi ti vendono le "
            "persone per farlo funzionare. Noi mettiamo tutti e due in un numero solo."),
    m_a_lab="Sabato, un minuto a 0,55 &euro;",
    m_b_lab="Un progetto fai-da-te, un minuto",
    m_shared=[(11, "telefonia"), (15, "voce e ragionamento"),
              (10, "letture su catalogo e ordini")],
    m_ours=[(16, "la configurazione"), (14, "monitoraggio e QA"),
            (18, "tuning settimanale"), (16, "gestione proattiva")],
    m_ghost="tu",
    m_outside="pi&ugrave; 6.000 &euro; al mese di sviluppatore, fuori dalla barra",
    m_fine=("Le larghezze sono indicative, non una ripartizione dei costi. Il punto "
            "&egrave; quale lavoro sta dentro al prezzo."),

    c_h2="Quanto pagheresti davvero",
    c_lede=("Nessuno conosce i propri minuti. Tutti conoscono le proprie chiamate. "
            "Quindi si parte da l&igrave;."),
    c_calls="chiamate al mese",
    c_avg="durata media",
    c_min="minuti", c_month="/ mese",
    c_band="a 0,50 &euro;, la tua fascia di volume",
    c_note="Nessun minimo, nessun canone. Un mese tranquillo &egrave; una fattura piccola.",
    c_ex_lab="essendo fatturato al secondo, le chiamate brevi restano economiche",
    c_ex=[("Dov&rsquo;&egrave; il mio ordine", "40 secondi", "0,37 &euro;"),
          ("Richiesta di reso", "2 minuti", "1,10 &euro;"),
          ("Domanda pre-acquisto", "5 minuti", "2,75 &euro;")],
    c_bands=[("sotto 5.000 minuti", "0,55 &euro;", "qui parte la maggior parte degli store"),
             ("da 5.000 a 20.000", "0,50 &euro;", "una linea intensa, o pi&ugrave; workflow"),
             ("oltre 20.000", "0,45 &euro;", "alta stagione, o un catalogo che non dorme mai")],

    i_h2="Perch&eacute; costiamo di pi&ugrave;? <br>Non &egrave; vero.",
    i_lede=("Stai confrontando il nostro prezzo intero con la prima riga di "
            "qualcun altro. Ecco lo stesso mese, 4.000 minuti, fatturato nei due modi."),
    i_their_h="Un preventivo da 0,15 &euro; al minuto", i_their_sub="quello che arriva davvero",
    i_ours_h="Sabato", i_ours_sub="quello che arriva davvero",
    i_rows=[("piattaforma, la tariffa pubblicizzata", "0,15 &euro;/min", "600 &euro;", "quella sul loro sito"),
            ("telefonia", "0,02 &euro;/min", "80 &euro;", "ribaltata a costo, in pi&ugrave;"),
            ("voce e modelli", "0,06 &euro;/min", "240 &euro;", "a consumo, varia ogni mese"),
            ("retainer di gestione", "al mese", "1.500 &euro;", "la parte che lo fa funzionare"),
            ("strumenti di valutazione", "al mese", "250 &euro;", "per utente, spesso un prodotto a parte"),
            ("modifiche a prompt e workflow", "6 ore", "720 &euro;", "a ore, o come change request"),
            ("seconda lingua", "al mese", "300 &euro;", "un modulo aggiuntivo"),
            ("attivazione, spalmata su 12 mesi", "3.000 &euro; una tantum", "250 &euro;", "pagata prima che risponda qualcuno")],
    i_ours_row=("4.000 minuti di conversazione", "0,55 &euro;/min", "2.200 &euro;", "tutto incluso"),
    i_nothing="nient&rsquo;altro",
    i_tot="totale del mese",
    i_their_tot="3.940 &euro;", i_ours_tot="2.200 &euro;",
    i_eff="tariffa effettiva", i_eff_unit="al minuto",
    i_their_eff="0,99 &euro;", i_ours_eff="0,55 &euro;",
    i_note=("La colonna di sinistra &egrave; una composizione di quanto costano di "
            "solito queste voci nel settore, non il preventivo di un fornitore con "
            "nome e cognome. A chi ti propone una tariffa bassa al minuto chiedi tre "
            "numeri: quanto costa il retainer mensile, quanto costano le modifiche ai "
            "prompt, e qual &egrave; la tariffa effettiva una volta aggiunte telefonia "
            "e modelli. Se non sanno risponderti in una riga, quella &egrave; la risposta."),

    t_h2="Tre modi di rispondere al telefono",
    t_lede="Stesso lavoro. Fatture molto diverse. Medie di categoria, non attacchi ai concorrenti.",
    t_assume=("Conti fatti su uno store da <b>4.000 minuti al mese</b>, circa 900 "
              "chiamate. Le altezze delle barre sono i numeri mensili reali, in scala."),
    t_cols=[
        dict(h="Sabato", acc=True, bars=[(73, "tutto, incluso", "lime")],
             tot="2.200 &euro;", per="0,55 &euro; al minuto, gestione inclusa",
             foot="Una riga in fattura. La configurazione, il tuning e le persone sono gi&agrave; dentro."),
        dict(h="Piattaforma fai-da-te", acc=False,
             bars=[(24, "piattaforma, modelli, telefonia", "blue"),
                   (200, "mezzo sviluppatore, costo pieno", "hatch")],
             tot="6.720 &euro;", per="0,18 &euro; al minuto, pi&ugrave; 6.000 &euro; di sviluppatore",
             foot="Davvero pi&ugrave; economica al minuto. La persona che lo costruisce e lo sorveglia &egrave; tutto il costo."),
        dict(h="Call center in outsourcing", acc=False,
             bars=[(56, "lavoro diretto, minimo di legge 0,42 &euro;", "clay"),
                   (37, "supervisori, spazi, margine", "clay2"),
                   (20, "tempo morto che paghi comunque", "hatch2")],
             tot="3.400 &euro;", per="0,85 &euro; al minuto di conversazione",
             foot="Un operatore rende circa 44 minuti utili per ogni ora pagata. Gli altri 16 li paghi lo stesso."),
    ],
    t_rows=[("chi lo costruisce", "lo facciamo noi", "il tuo sviluppatore", "i loro formatori, dal tuo script"),
            ("chi risponde alle 2 di notte a dicembre", "l&rsquo;agente", "nessuno", "un turno di notte, se lo paghi"),
            ("lingue", "tutte quelle in cui vendi", "quelle che hai costruito", "una per team, a listino separato"),
            ("tempo per andare live", "settimane", "da 3 a 6 mesi", "da 4 a 8 settimane di formazione"),
            ("cosa succede nei picchi", "risponde a tutte insieme", "la coda &egrave; un tuo problema", "musica di attesa, o straordinari")],

    f_eyebrow="FAQ",
    f_h2="Domande sui prezzi",
    f_items=[
        ("Quanto costa una voice AI gestita per l’e-commerce?",
         "Sabato costa 0,55 euro per minuto di conversazione, fatturato al secondo, e la tariffa scende a 0,50 euro sopra i 5.000 minuti al mese e a 0,45 euro sopra i 20.000. Quella tariffa unica comprende la configurazione dei workflow, le integrazioni, tutte le lingue, tutti i workflow, la gestione umana proattiva e la valutazione continua dell’agente. Non c’è un costo di piattaforma, né una licenza per utente, né un costo di attivazione, né un contratto minimo."),
        ("Che cosa conta esattamente come minuto?",
         "Il tempo di conversazione connessa, fatturato al secondo. Una chiamata di 40 secondi viene fatturata 40 secondi, non arrotondata al minuto. Gli squilli non si pagano. L’attesa dentro una chiamata si paga, perché l’agente sta comunque lavorando su quella chiamata."),
        ("Il servizio gestito è davvero incluso nella tariffa al minuto?",
         "Sì. La configurazione dei workflow, il lavoro di integrazione, la gestione umana proattiva, la valutazione dell’agente e l’ottimizzazione continua sono tutti pagati dalla tariffa al minuto. Su una fattura Sabato non esiste una voce separata di retainer o di servizi professionali."),
        ("Perché la vostra tariffa al minuto è più alta di altre piattaforme di voice AI?",
         "Perché la loro è una tariffa di piattaforma e la nostra è un totale. Una tariffa di piattaforma copre il software. Non copre la telefonia, il consumo di voce e modelli, la persona che costruisce i tuoi workflow, la persona che riascolta le chiamate, né le modifiche che vorrai al secondo mese. Sommate quelle voci, la tariffa effettiva in questo settore arriva vicino a 1,00 euro al minuto. Sabato costa 0,55 euro e non c’è altro da aggiungere."),
        ("E se mi serve una seconda lingua o un terzo workflow?",
         "Sono inclusi. Lingue e workflow non cambiano mai la tua tariffa. L’unica cosa che la cambia è il volume."),
        ("C’è un contratto minimo o un costo di attivazione?",
         "Nessuno dei due. Non c’è vincolo di durata, non c’è costo di attivazione e non c’è spesa minima. Paghi ogni mese i minuti che hai effettivamente usato."),
        ("Come si confronta con un progetto fai-da-te su una piattaforma vocale?",
         "Un progetto fai-da-te costa circa 0,18 euro al minuto tra piattaforma, modelli e telefonia, più lo sviluppatore che lo costruisce e lo mantiene. Su 4.000 minuti al mese fanno circa 6.720 euro contro 2.200 euro con Sabato. Il fai-da-te diventa più economico solo oltre i 18.000 minuti al mese circa, e solo se quello che hai costruito funziona."),
        ("Come si confronta con un call center in outsourcing?",
         "Il decreto ministeriale del 31 dicembre 2017 fissa il costo del lavoro di un minuto di call center tra 0,33 e 0,50 euro, 0,42 euro al livello standard, e sono soltanto le retribuzioni: il decreto non comprende supervisori, formazione, spazi né margine. Considerato poi che un operatore rende circa 44 minuti utili per ogni ora pagata, il solo costo del lavoro per un minuto di conversazione vera vale tra 0,54 e 0,57 euro, e un minuto reale in outsourcing si colloca tra 0,70 e 1,00 euro. Sabato costa 0,55 euro tutto compreso, risponde a tutte le chiamate insieme e non fattura nulla quando la linea è ferma."),
        ("Cosa succede in alta stagione?",
         "Niente. La linea risponde a tutte le chiamate insieme, senza coda e senza straordinari. Paghi i minuti, e più il volume sale più la tariffa migliora."),
    ],
)


# ---------------------------------------------------------------------------
# CSS. Everything is sb-px-, which nothing else in the codebase uses. The only
# unprefixed names are hero.py's dial-card classes, repainted for a white page
# under .sb-px-dial and nowhere else.
# ---------------------------------------------------------------------------
CSS = """
.sb-px{background:#fff;padding:0 30px;font-family:Satoshi,Inter,-apple-system,sans-serif;
 color:rgb(11,11,12);-webkit-font-smoothing:antialiased}
.sb-px-in{max-width:1200px;margin:0 auto}
.sb-px-sec{padding:74px 0 0}
.sb-px h2{font-size:44px;line-height:1.1;letter-spacing:-1.4px;font-weight:700;margin:0}
.sb-px-lede{font-size:16.5px;line-height:1.55;color:rgb(90,86,82);margin:14px 0 0;max-width:680px}
.sb-px-fine{font-size:12.5px;color:rgb(138,132,126);margin:20px 0 0}

/* hero */
.sb-px-hero{text-align:center;padding:34px 0 0}
.sb-px-eyebrow{display:block;font-size:12px;font-weight:700;letter-spacing:.18em;color:rgb(111,106,102)}
.sb-px-h1{font-size:64px;line-height:1.04;letter-spacing:-2.4px;font-weight:700;margin:14px 0 0}
.sb-px-box{max-width:840px;margin:32px auto 0;border:2px solid rgb(11,11,12);border-radius:20px;overflow:hidden}
.sb-px-boxtop{padding:38px 30px 30px}
.sb-px-num{display:flex;align-items:baseline;justify-content:center;gap:9px;
 font-size:76px;font-weight:700;letter-spacing:-3px;line-height:1}
.sb-px-cur{font-size:38px;letter-spacing:-1px}
.sb-px-unit{font-size:17px;font-weight:700;color:rgb(111,106,102);letter-spacing:0;margin-left:4px}
.sb-px-pillwrap{margin-top:18px}
.sb-px-pill{display:inline-flex;align-items:center;gap:9px;background:rgb(204,255,0);color:rgb(11,11,12);
 border:1.5px solid rgb(11,11,12);border-radius:999px;padding:9px 17px;font-size:12.5px;font-weight:700;letter-spacing:.14em}
.sb-px-pill i{font-style:normal;font-size:11px;font-weight:700;letter-spacing:.02em;
 border-left:1px solid rgba(11,11,12,.35);padding-left:9px}
.sb-px-boxsub{margin:15px auto 0;font-size:14.5px;color:rgb(90,86,82);max-width:620px;line-height:1.5}
.sb-px-boxbot{background:rgb(204,255,0);padding:20px 30px 26px}
.sb-px-boxbot-h{font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
 color:rgba(11,11,12,.62);margin-bottom:14px}
.sb-px-incl{display:grid;grid-template-columns:repeat(3,1fr);gap:12px 22px;text-align:left}
.sb-px-incl div{display:flex;align-items:flex-start;gap:9px;font-size:14.5px;font-weight:700;line-height:1.3}
.sb-px-tick{font-size:13px;font-weight:700;line-height:1.45;flex:none}
.sb-px-nots{margin:18px auto 0;max-width:860px;display:flex;flex-wrap:wrap;gap:7px;
 justify-content:center;align-items:center}
.sb-px-not{font-size:12.5px;color:rgb(168,162,156);text-decoration:line-through}
.sb-px-not:not(:last-of-type)::after{content:"\\00b7";margin-left:7px;display:inline-block;
 text-decoration:none;color:rgb(201,195,189)}
.sb-px-notlab{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgb(111,106,102)}
.sb-px-book{display:inline-block;margin-top:30px;background:rgb(11,11,12);color:#fff;text-decoration:none;
 border-radius:999px;padding:14px 30px;font-size:14.5px;font-weight:700}
.sb-px-book:hover{background:rgb(38,38,40)}
.sb-px-diallab{margin-top:22px;font-size:13px;color:rgb(111,106,102)}

/* the dial row: hero.py's component, repainted for white. Scoped, so the
   homepage's black cards are untouched. */
.sb-px-dial{background:transparent;padding:0;margin:0 auto;max-width:840px}
.sb-px-dial .sb-hero-nums{width:min(840px,100%);margin:12px auto 0}
.sb-px-dial .sb-hero-num{background:#fff;border:1px solid rgb(222,217,211)}
.sb-px-dial .sb-hero-num:hover,.sb-px-dial .sb-hero-num:focus-visible{
 background:rgb(251,252,254);border-color:rgb(11,11,12)}
.sb-px-dial .sb-hero-cc{color:rgb(111,106,102)}
.sb-px-dial .sb-hero-no{color:rgb(11,11,12)}
.sb-px-dial .sb-hero-reveal{color:rgb(138,132,126)}
.sb-px-dial .sb-hero-call{color:rgb(11,11,12);background:rgb(204,255,0)}
.sb-px-dial.sb-js .sb-hero-num.is-open{background:rgb(251,252,254);border-color:rgb(11,11,12)}

/* the decomposed minute */
.sb-px-mrow{margin-top:30px}
.sb-px-mlab{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
 color:rgb(111,106,102);margin-bottom:9px}
.sb-px-bar{display:flex;height:74px;border-radius:12px;overflow:hidden;border:1px solid rgb(222,217,211)}
.sb-px-seg{display:flex;align-items:center;justify-content:center;text-align:center;padding:0 8px;
 font-size:11.5px;font-weight:700;line-height:1.25;color:rgb(74,70,66);background:rgb(243,241,238);
 border-right:1px solid #fff}
.sb-px-seg.is-ours{background:rgb(204,255,0);color:rgb(11,11,12)}
.sb-px-seg.is-ghost{background:repeating-linear-gradient(45deg,#fff,#fff 7px,rgb(240,237,233) 7px,rgb(240,237,233) 14px);
 color:rgb(162,156,150);font-size:15px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
 border:2px dashed rgb(213,208,202)}
.sb-px-outside{margin-top:10px;display:inline-block;background:rgb(251,234,226);color:rgb(140,68,35);
 border:1px solid rgb(240,203,184);border-radius:8px;padding:9px 14px;font-size:13px;font-weight:700}

/* calculator */
.sb-px-calc{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:28px;
 background:rgb(249,250,253);border-radius:18px;padding:30px}
.sb-px-cq{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:rgb(111,106,102)}
.sb-px-range{width:100%;margin:18px 0 0;accent-color:rgb(11,11,12);height:22px}
.sb-px-cval{margin-top:10px;font-size:36px;font-weight:700;letter-spacing:-1.2px;line-height:1}
.sb-px-cavg{margin-top:12px;font-size:13px;color:rgb(111,106,102)}
.sb-px-out{border-left:3px solid rgb(204,255,0);padding-left:16px}
.sb-px-omin{font-size:13px;font-weight:700;color:rgb(111,106,102);display:block}
.sb-px-ocost{display:block;margin-top:4px;line-height:1.05}
.sb-px-ocost b{font-size:42px;font-weight:700;letter-spacing:-1.6px}
.sb-px-ocost i{font-style:normal;font-size:17px;font-weight:700;color:rgb(111,106,102);margin-left:6px}
.sb-px-oband{font-size:13px;color:rgb(111,106,102);display:block;margin-top:6px}
.sb-px-cnote{margin-top:20px;font-size:14px;line-height:1.55;color:rgb(74,70,66)}
.sb-px-exlab{margin-top:26px;font-size:11px;font-weight:700;letter-spacing:.16em;
 text-transform:uppercase;color:rgb(111,106,102)}
.sb-px-ex{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:12px}
.sb-px-ex a,.sb-px-ex div{border:1px solid rgb(226,222,217);border-radius:12px;padding:16px 18px;
 display:flex;align-items:baseline;gap:10px}
.sb-px-ex b{font-size:14px;font-weight:700}
.sb-px-ex span{font-size:12.5px;color:rgb(138,132,126)}
.sb-px-ex i{margin-left:auto;font-style:normal;font-size:19px;font-weight:700;letter-spacing:-.5px}
.sb-px-bands{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:18px}
.sb-px-band{border:1px solid rgb(226,222,217);border-radius:12px;padding:18px}
.sb-px-band-r{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgb(111,106,102)}
.sb-px-band-n{font-size:30px;font-weight:700;letter-spacing:-1px;margin:6px 0 4px}
.sb-px-band-d{font-size:13px;color:rgb(111,106,102);line-height:1.45}

/* invoices */
.sb-px-inv{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:28px;align-items:stretch}
.sb-px-invcol{border:1px solid rgb(226,222,217);border-radius:16px;padding:22px 24px 24px}
.sb-px-invcol.is-ours{border:2px solid rgb(11,11,12);display:flex;flex-direction:column}
.sb-px-invh{font-size:17px;font-weight:700;letter-spacing:-.4px;padding-bottom:14px;
 border-bottom:1px solid rgb(239,236,232)}
.sb-px-invh span{display:block;font-size:11px;font-weight:700;letter-spacing:.14em;
 text-transform:uppercase;color:rgb(138,132,126);margin-top:5px}
.sb-px-invlist{list-style:none;margin:6px 0 0;padding:0}
.sb-px-invlist li{display:grid;grid-template-columns:1fr auto 88px;gap:8px;align-items:baseline;
 padding:11px 0;border-bottom:1px solid rgb(245,242,239)}
.sb-px-ln{font-size:14px;font-weight:700}
.sb-px-lu{font-size:12px;color:rgb(138,132,126)}
.sb-px-invlist b{text-align:right;font-size:15px;font-weight:700}
.sb-px-invlist em{grid-column:1/-1;font-style:normal;font-size:12px;color:rgb(162,156,150);margin-top:-4px}
.sb-px-nothing{flex:1;margin:18px 0 0;border:1px dashed rgb(213,208,202);border-radius:10px;min-height:120px;
 display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;
 color:rgb(162,156,150);letter-spacing:.06em}
.sb-px-invtot{display:flex;justify-content:space-between;align-items:baseline;margin-top:16px;
 padding-top:14px;border-top:2px solid rgb(11,11,12)}
.sb-px-invtot span{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:rgb(111,106,102)}
.sb-px-invtot b{font-size:30px;font-weight:700;letter-spacing:-1.1px}
.sb-px-eff{margin-top:8px;font-size:13.5px;color:rgb(111,106,102)}
.sb-px-eff b{font-size:16px;color:rgb(11,11,12)}
.sb-px-invcol.is-ours .sb-px-eff b{background:rgb(204,255,0);padding:2px 7px;border-radius:5px}
.sb-px-note{margin-top:20px;font-size:13.5px;line-height:1.6;color:rgb(74,70,66);max-width:860px;
 border-left:3px solid rgb(204,255,0);padding-left:16px}

/* three ways */
.sb-px-assume{margin-top:22px;display:inline-block;background:rgb(249,250,253);
 border:1px solid rgb(226,229,236);border-radius:10px;padding:11px 16px;font-size:13.5px;color:rgb(74,70,66)}
.sb-px-cols{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px;align-items:end}
.sb-px-col{border:1px solid rgb(226,222,217);border-radius:14px;padding:20px}
.sb-px-col.is-ours{border:2px solid rgb(11,11,12)}
.sb-px-colh{font-size:14px;font-weight:700;letter-spacing:-.2px}
.sb-px-stack{display:flex;flex-direction:column-reverse;gap:2px;margin:16px 0 14px}
.sb-px-cbar{border-radius:6px;display:flex;align-items:center;padding:0 12px;font-size:11.5px;
 font-weight:700;line-height:1.25;min-height:22px}
.sb-px-lime{background:rgb(204,255,0);color:rgb(11,11,12)}
.sb-px-blue{background:rgb(110,127,163);color:#fff}
.sb-px-clay{background:rgb(180,101,62);color:#fff}
.sb-px-clay2{background:rgb(217,161,132);color:rgb(74,42,24)}
.sb-px-hatch{background:repeating-linear-gradient(45deg,rgb(232,234,240),rgb(232,234,240) 6px,
 rgb(218,222,232) 6px,rgb(218,222,232) 12px);color:rgb(74,70,66)}
.sb-px-hatch2{background:repeating-linear-gradient(45deg,rgb(243,230,223),rgb(243,230,223) 6px,
 rgb(232,211,200) 6px,rgb(232,211,200) 12px);color:rgb(90,52,35)}
.sb-px-tot{font-size:28px;font-weight:700;letter-spacing:-.9px}
.sb-px-per{font-size:12.5px;font-weight:700;color:rgb(111,106,102);margin-top:2px}
.sb-px-cfoot{font-size:12.5px;color:rgb(111,106,102);line-height:1.5;margin-top:6px}
.sb-px-rows{margin-top:22px;border-top:1px solid rgb(231,228,224)}
.sb-px-row{display:grid;grid-template-columns:1.15fr 1fr 1fr 1fr;gap:14px;padding:13px 0;
 border-bottom:1px solid rgb(240,237,233);font-size:13.5px;align-items:baseline}
.sb-px-row span{color:rgb(111,106,102)}
.sb-px-row b{font-weight:700}
.sb-px-row i{font-style:normal;color:rgb(111,106,102)}

/* faq */
.sb-px-faqs{margin-top:24px;border-top:1px solid rgb(231,228,224)}
.sb-px-fq{padding:18px 0;border-bottom:1px solid rgb(240,237,233)}
.sb-px-fqq{font-size:16.5px;font-weight:700;letter-spacing:-.3px;margin:0}
.sb-px-fqa{font-size:14.5px;color:rgb(90,86,82);line-height:1.6;margin:7px 0 0;max-width:880px}

@media (max-width:900px){
  .sb-px{padding:0 20px}
  .sb-px-h1{font-size:34px;letter-spacing:-1.2px}
  .sb-px h2{font-size:27px;letter-spacing:-.8px}
  .sb-px-num{font-size:52px;letter-spacing:-2px;flex-wrap:wrap}
  .sb-px-unit{width:100%;margin:6px 0 0}
  .sb-px-incl,.sb-px-calc,.sb-px-ex,.sb-px-bands,.sb-px-inv,.sb-px-cols{grid-template-columns:1fr}
  .sb-px-row{grid-template-columns:1fr;gap:2px;padding:14px 0}
  .sb-px-row span{font-size:12px;letter-spacing:.06em;text-transform:uppercase}
  .sb-px-bar{height:auto;flex-direction:column}
  .sb-px-seg{padding:11px 8px;border-right:0;border-bottom:1px solid #fff}
  .sb-px-sec{padding:52px 0 0}
}
"""


# Volume bands, per language. Applied to the WHOLE month, not marginally: cross
# 5,000 minutes and the better rate applies to every minute, not just the ones
# above the line. Worse for us by a few per cent and much easier to explain,
# which is the trade the whole page is making.
BANDS = {
    "en": [(5000, 0.65), (20000, 0.60), (None, 0.55)],
    "it": [(5000, 0.55), (20000, 0.50), (None, 0.45)],
}
AVG_CALL = 4.5          # minutes; the slider's calls-to-minutes conversion
DEFAULT_CALLS = 1200

# The slider is the only scripted thing on this page besides the dial reveal.
# It ships with the default already rendered in the HTML, so with JS off the
# page still states a real, correct example rather than an empty box. Number
# formatting is passed in as data attributes rather than hard-coded, because
# English wants 1,200 and $3,240 while Italian wants 1.200 and 3.240 EUR.
SLIDER_SCRIPT = (
    "<script>(function(){"
    "var r=document.getElementById('sb-px-range');if(!r)return;"
    "var box=r.closest('.sb-px-calc');"
    "var g=box.getAttribute('data-group'),d=box.getAttribute('data-dec'),"
    "cur=box.getAttribute('data-cur'),after=box.getAttribute('data-after')==='1',"
    "avg=parseFloat(box.getAttribute('data-avg')),"
    "bands=JSON.parse(box.getAttribute('data-bands')),"
    "bandtpl=box.getAttribute('data-bandtpl');"
    "var vCalls=box.querySelector('.sb-px-cval'),vMin=box.querySelector('.sb-px-omin'),"
    "vCost=box.querySelector('#sb-px-cost'),vBand=box.querySelector('.sb-px-oband');"
    "var minLab=box.getAttribute('data-minlab');"
    "function grp(n){var s=String(n),o='',c=0;"
    "for(var i=s.length-1;i>=0;i--){o=s[i]+o;if(++c%3===0&&i>0)o=g+o;}return o;}"
    "function money(v){var t=v.toFixed(2).replace('.',d);"
    # Whole euros and dollars read better than 3240,00 on a headline number.
    "if(t.slice(-3)===d+'00')t=t.slice(0,-3);"
    "var parts=t.split(d);parts[0]=grp(parseInt(parts[0],10));t=parts.join(d);"
    "return after?t+' '+cur:cur+t;}"
    "function rate(m){for(var i=0;i<bands.length;i++){"
    "if(bands[i][0]===null||m<bands[i][0])return bands[i][1];}return bands[bands.length-1][1];}"
    "function draw(){var calls=parseInt(r.value,10),mins=Math.round(calls*avg),rt=rate(mins);"
    "vCalls.textContent=grp(calls);"
    "vMin.textContent=grp(mins)+' '+minLab;"
    "vCost.textContent=money(mins*rt);"
    "vBand.textContent=bandtpl.replace('%s',money(rt));}"
    "r.addEventListener('input',draw);draw();"
    "})();</script>")


def _fmt_money(lang, v):
    """Same rules the slider script uses, so the no-JS default matches exactly."""
    c = COPY[lang]
    dec, grp = (",", ".") if lang == "it" else (".", ",")
    t = f"{v:.2f}".replace(".", dec)
    if t.endswith(dec + "00"):
        t = t[: -3]
    whole, _, rest = t.partition(dec)
    out = ""
    for i, ch in enumerate(reversed(whole)):
        out = ch + out
        if (i + 1) % 3 == 0 and i + 1 < len(whole):
            out = grp + out
    t = out + ((dec + rest) if rest else "")
    return (t + " " + c["cur"]) if c.get("cur_after") else (c["cur"] + t)


def _grp(lang, n):
    grp = "." if lang == "it" else ","
    s, out = str(int(n)), ""
    for i, ch in enumerate(reversed(s)):
        out = ch + out
        if (i + 1) % 3 == 0 and i + 1 < len(s):
            out = grp + out
    return out


def _rate_for(lang, minutes):
    for cap, rate in BANDS[lang]:
        if cap is None or minutes < cap:
            return rate
    return BANDS[lang][-1][1]


def _hero(lang):
    c = COPY[lang]
    price = (f'<span class="sb-px-cur">{c["cur"]}</span>{c["rate"]}'
             if not c.get("cur_after") else
             f'{c["rate"]}<span class="sb-px-cur">{c["cur"]}</span>')
    incl = "".join(f'<div><span class="sb-px-tick">&#10003;</span>{t}</div>' for t in c["incl"])
    nots = "".join(f'<span class="sb-px-not">{t}</span>' for t in c["nots"])
    return (
      '<div class="sb-px-hero">'
      f'<span class="sb-px-eyebrow">{c["eyebrow"]}</span>'
      f'<h1 class="sb-px-h1">{c["h1"]}</h1>'
      '<div class="sb-px-box">'
        '<div class="sb-px-boxtop">'
          f'<div class="sb-px-num">{price}<span class="sb-px-unit">{c["unit"]}</span></div>'
          f'<div class="sb-px-pillwrap"><span class="sb-px-pill">{c["pill"]}'
          f'<i>{c["pill_sub"]}</i></span></div>'
          f'<p class="sb-px-boxsub">{c["rate_sub"]}</p>'
        '</div>'
        '<div class="sb-px-boxbot">'
          f'<div class="sb-px-boxbot-h">{c["incl_head"]}</div>'
          f'<div class="sb-px-incl">{incl}</div>'
        '</div>'
      '</div>'
      f'<div class="sb-px-nots">{nots}<span class="sb-px-notlab">{c["nots_lab"]}</span></div>'
      f'<a class="sb-px-book" href="{CAL}" target="_blank" rel="noopener">{c["book"]}</a>'
      f'<p class="sb-px-diallab">{c["dial_lab"]}</p>'
      # hero.py's component verbatim. The section carries sb-hero so its reveal
      # script finds it and so the .sb-js visibility rules in footer.css apply;
      # sb-px-dial repaints it for white and scopes every override to this page.
      f'<section class="sb-hero sb-px-dial" data-lang="{lang}">'
      f'<div class="sb-hero-nums">{dial_cards(lang)}</div></section>'
      '</div>')


def _minute(lang):
    c = COPY[lang]
    shared = "".join(f'<div class="sb-px-seg" style="flex:{w}"><span>{t}</span></div>'
                     for w, t in c["m_shared"])
    ours = "".join(f'<div class="sb-px-seg is-ours" style="flex:{w}"><span>{t}</span></div>'
                   for w, t in c["m_ours"])
    ghost_w = sum(w for w, _ in c["m_ours"])
    return (
      '<section class="sb-px-sec">'
      f'<h2>{c["m_h2"]}</h2><p class="sb-px-lede">{c["m_lede"]}</p>'
      f'<div class="sb-px-mrow"><div class="sb-px-mlab">{c["m_a_lab"]}</div>'
      f'<div class="sb-px-bar">{shared}{ours}</div></div>'
      f'<div class="sb-px-mrow"><div class="sb-px-mlab">{c["m_b_lab"]}</div>'
      f'<div class="sb-px-bar">{shared}'
      f'<div class="sb-px-seg is-ghost" style="flex:{ghost_w}"><span>{c["m_ghost"]}</span></div></div>'
      f'<div class="sb-px-outside">{c["m_outside"]}</div></div>'
      f'<p class="sb-px-fine">{c["m_fine"]}</p>'
      '</section>')


def _calc(lang):
    c = COPY[lang]
    mins = round(DEFAULT_CALLS * AVG_CALL)
    rate = _rate_for(lang, mins)
    bands = json.dumps([[cap, r] for cap, r in BANDS[lang]], separators=(",", ":"))
    band_tpl = c["c_band"].replace(_fmt_money(lang, rate), "%s")
    ex = "".join(f'<div><b>{n}</b><span>{d}</span><i>{p}</i></div>' for n, d, p in c["c_ex"])
    bnd = "".join(f'<div class="sb-px-band"><div class="sb-px-band-r">{r}</div>'
                  f'<div class="sb-px-band-n">{n}</div>'
                  f'<div class="sb-px-band-d">{d}</div></div>' for r, n, d in c["c_bands"])
    return (
      '<section class="sb-px-sec">'
      f'<h2>{c["c_h2"]}</h2><p class="sb-px-lede">{c["c_lede"]}</p>'
      f'<div class="sb-px-calc" data-group="{"." if lang == "it" else ","}" '
      f'data-dec="{"," if lang == "it" else "."}" data-cur="{c["cur"]}" '
      f'data-after="{"1" if c.get("cur_after") else "0"}" data-avg="{AVG_CALL}" '
      f"data-bands='{bands}' data-bandtpl=\"{html.escape(band_tpl, quote=True)}\" "
      f'data-minlab="{c["c_min"]}">'
        '<div>'
          f'<div class="sb-px-cq">{c["c_calls"]}</div>'
          f'<input class="sb-px-range" id="sb-px-range" type="range" min="100" max="8000" '
          f'step="100" value="{DEFAULT_CALLS}" aria-label="{c["c_calls"]}">'
          f'<div class="sb-px-cval">{_grp(lang, DEFAULT_CALLS)}</div>'
          f'<div class="sb-px-cavg">{c["c_avg"]} <b>{str(AVG_CALL).replace(".", "," if lang == "it" else ".")} min</b></div>'
        '</div>'
        '<div>'
          '<div class="sb-px-out">'
            f'<span class="sb-px-omin">{_grp(lang, mins)} {c["c_min"]}</span>'
            f'<span class="sb-px-ocost"><b id="sb-px-cost">{_fmt_money(lang, mins * rate)}</b>'
            f' <i>{c["c_month"]}</i></span>'
            f'<span class="sb-px-oband">{c["c_band"]}</span>'
          '</div>'
          f'<p class="sb-px-cnote">{c["c_note"]}</p>'
        '</div>'
      '</div>'
      f'<div class="sb-px-exlab">{c["c_ex_lab"]}</div>'
      f'<div class="sb-px-ex">{ex}</div>'
      f'<div class="sb-px-bands">{bnd}</div>'
      '</section>')


def _invoices(lang):
    c = COPY[lang]
    rows = "".join(
        f'<li><span class="sb-px-ln">{n}</span><span class="sb-px-lu">{u}</span>'
        f'<b>{a}</b><em>{note}</em></li>' for n, u, a, note in c["i_rows"])
    on, ou, oa, onote = c["i_ours_row"]
    return (
      '<section class="sb-px-sec">'
      f'<h2>{c["i_h2"]}</h2><p class="sb-px-lede">{c["i_lede"]}</p>'
      '<div class="sb-px-inv">'
        '<div class="sb-px-invcol">'
          f'<div class="sb-px-invh">{c["i_their_h"]}<span>{c["i_their_sub"]}</span></div>'
          f'<ul class="sb-px-invlist">{rows}</ul>'
          f'<div class="sb-px-invtot"><span>{c["i_tot"]}</span><b>{c["i_their_tot"]}</b></div>'
          f'<div class="sb-px-eff">{c["i_eff"]} <b>{c["i_their_eff"]}</b> {c["i_eff_unit"]}</div>'
        '</div>'
        '<div class="sb-px-invcol is-ours">'
          f'<div class="sb-px-invh">{c["i_ours_h"]}<span>{c["i_ours_sub"]}</span></div>'
          f'<ul class="sb-px-invlist"><li><span class="sb-px-ln">{on}</span>'
          f'<span class="sb-px-lu">{ou}</span><b>{oa}</b><em>{onote}</em></li></ul>'
          f'<div class="sb-px-nothing">{c["i_nothing"]}</div>'
          f'<div class="sb-px-invtot"><span>{c["i_tot"]}</span><b>{c["i_ours_tot"]}</b></div>'
          f'<div class="sb-px-eff">{c["i_eff"]} <b>{c["i_ours_eff"]}</b> {c["i_eff_unit"]}</div>'
        '</div>'
      '</div>'
      f'<p class="sb-px-note">{c["i_note"]}</p>'
      '</section>')


def _three(lang):
    c = COPY[lang]
    cols = []
    for col in c["t_cols"]:
        bars = "".join(f'<div class="sb-px-cbar sb-px-{cls}" style="height:{h}px">'
                       f'<span>{lab}</span></div>' for h, lab, cls in col["bars"])
        cols.append(
            f'<div class="sb-px-col{" is-ours" if col["acc"] else ""}">'
            f'<div class="sb-px-colh">{col["h"]}</div>'
            f'<div class="sb-px-stack">{bars}</div>'
            f'<div class="sb-px-tot">{col["tot"]}</div>'
            f'<div class="sb-px-per">{col["per"]}</div>'
            f'<div class="sb-px-cfoot">{col["foot"]}</div></div>')
    rows = "".join(f'<div class="sb-px-row"><span>{a}</span><b>{b}</b><i>{d}</i><i>{e}</i></div>'
                   for a, b, d, e in c["t_rows"])
    return (
      '<section class="sb-px-sec">'
      f'<h2>{c["t_h2"]}</h2><p class="sb-px-lede">{c["t_lede"]}</p>'
      f'<div class="sb-px-assume">{c["t_assume"]}</div>'
      f'<div class="sb-px-cols">{"".join(cols)}</div>'
      f'<div class="sb-px-rows">{rows}</div>'
      '</section>')


def _faq(lang):
    """Every answer visible, no accordion.

    The homepage FAQ collapses because it sits at the foot of a long page and
    nine open answers would bury the CTA. Here the FAQ IS the argument, the
    answers are short, and an accordion would hide the pricing detail a buyer
    came for behind a click. It also means no script and nothing to hydrate.
    """
    c = COPY[lang]
    items = "".join(
        f'<div class="sb-px-fq"><p class="sb-px-fqq">{html.escape(q)}</p>'
        f'<p class="sb-px-fqa">{html.escape(a)}</p></div>' for q, a in c["f_items"])
    return ('<section class="sb-px-sec" id="sb-px-faq">'
            f'<span class="sb-px-eyebrow">{c["f_eyebrow"]}</span>'
            f'<h2>{c["f_h2"]}</h2>'
            f'<div class="sb-px-faqs">{items}</div>'
            '</section>')


def _jsonld(lang):
    """FAQPage, built from the same strings the visible answers use."""
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in COPY[lang]["f_items"]]}
    return ('<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>")


def pricing_html(lang="en"):
    if lang not in COPY:
        raise ValueError(f"pricing.py: unknown language {lang!r}")
    return (
        HIDE_FRAMER
        + '<style id="sb-px-css">' + CSS + "</style>"
        + f'<div class="sb-px" data-lang="{lang}"><div class="sb-px-in">'
        + _hero(lang) + _minute(lang) + _calc(lang) + _invoices(lang)
        + _three(lang) + _faq(lang)
        + "</div></div>"
        + _jsonld(lang) + REVEAL_SCRIPT + SLIDER_SCRIPT)


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in COPY else "en"
    print(pricing_html(lang))
