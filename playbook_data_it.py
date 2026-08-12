#!/usr/bin/env python3
"""Playbook content, Italian. Mirrors the English landing rules exactly:
one-sentence paragraphs, three CTAs, global framing - nothing
jurisdiction-specific. See playbook_data.py for the full brief.

SVGs are imported and relabelled, never copied: the coordinates are identical
in both languages and a translator has no business editing path data.
"""
from playbook_data import HERO_SVG, BAND_SVG, INTL_HERO_SVG, INTL_BARS_SVG

ORDER_IT = ["picchi-stagionali", "espansione-internazionale"]


def _it(svg, pairs):
    for a, b in pairs:
        svg = svg.replace(a, b)
    return svg


HERO_SVG_IT = _it(HERO_SVG, [
    ("TWO WEEKS IN DECEMBER", "DUE SETTIMANE DI DICEMBRE"),
    (">last order date<", ">ultimo giorno utile<"),
    (">the phone calls<", ">le telefonate<"),
    ('>M</text><text x="118" y="86">T</text><text x="184" y="86">W</text>',
     '>L</text><text x="118" y="86">M</text><text x="184" y="86">M</text>'),
    ('x="250" y="86">T</text><text x="316" y="86">F</text><text x="382" y="86">S</text>',
     'x="250" y="86">G</text><text x="316" y="86">V</text><text x="382" y="86">S</text>'),
    ('x="448" y="86">S<', 'x="448" y="86">D<'),
    ('aria-label="Two weeks of December. One day is the last order date; the calls peak across the following week, still before Christmas."',
     'aria-label="Due settimane di dicembre. Un giorno è l\'ultimo giorno utile per ordinare; le chiamate arrivano la settimana dopo, ancora prima di Natale."'),
])

BAND_SVG_IT = _it(BAND_SVG, [
    (">orders<", ">ordini<"), (">calls<", ">chiamate<"),
    (">week before<", ">settimana prima<"), (">sale<", ">promo<"),
    (">two weeks after<", ">due settimane dopo<"),
    ('aria-label="Two curves. Orders peak on the sale day; calls peak roughly a week later and stay high."',
     'aria-label="Due curve. Gli ordini salgono il giorno della promo; le chiamate una settimana dopo e restano alte."'),
])

INTL_HERO_SVG_IT = _it(INTL_HERO_SVG, [
    ("FIVE COUNTRIES, ONE LINE", "CINQUE PAESI, UNA LINEA"),
    (">German<", ">tedesco<"), (">French<", ">francese<"),
    (">Spanish<", ">spagnolo<"), (">Dutch<", ">olandese<"),
    (">Swedish<", ">svedese<"),
    (">one voice agent<", ">un agente vocale<"),
    (">answers in their language<", ">risponde nella sua lingua<"),
    ('aria-label="Five local phone numbers in five different languages, all answered by one voice agent."',
     'aria-label="Cinque numeri locali in cinque lingue diverse, tutti gestiti da un solo agente vocale."'),
])

INTL_BARS_SVG_IT = _it(INTL_BARS_SVG, [
    # Same length discipline as the English: at 21px in a 560 viewBox a line
    # runs out of room past ~36 characters, and Italian is the longer language.
    ("Confident English readers who still",
     "Chi legge bene l’inglese e vuole"),
    ("want care in their own language",
     "assistenza nella propria lingua"),
    ("More likely to buy the brand again",
     "Più propensi a ricomprare quando"),
    ("when care is in their language",
     "l’assistenza è nella loro lingua"),
    ('aria-label="Two bars. Sixty per cent of the shoppers most confident reading English still want customer care in their own language; seventy-five per cent are more likely to buy the brand again when they get it."',
     'aria-label="Due barre. Il sessanta per cento di chi legge l\'inglese con più sicurezza vuole comunque assistenza nella propria lingua; il settantacinque per cento è più propenso a ricomprare dal marchio quando la ottiene."'),
])

_EVRI = "https://www.evri.com/press/return-to-sender-four-million-gifts-to-be-sent-back-in-january-2025"
_CSA = "https://csa-research.com/l/media/Consumers-Prefer-their-Own-Language"

PLAYBOOKS_IT = {
    "picchi-stagionali": {
        "en": "peak-season",
        # Verb-led, to match "Espandi in nuovi Paesi". Label only - the URL
        # /it/playbook/picchi-stagionali does not move.
        "nav": "Gestisci l'alta stagione",
        "chip": "Playbook",
        "title": "Alta stagione senza assumere stagionali | Sabato AI",
        "description": "Il picco di chiamate arriva dopo la promo e dura fino ai "
                       "resi di gennaio. Un agente vocale in linea in due "
                       "settimane: niente selezione, formazione o esuberi.",
        "h1": "Picco gestito. [nb]Zero stagionali.[/nb]",
        "sub": "Il picco di chiamate arriva la settimana dopo la promo e dura "
               "fino ai resi di gennaio. Un agente vocale assorbe il volume "
               "ripetitivo: online in due settimane, senza selezione, senza "
               "formazione, senza esuberi.",
        "hero_visual": HERO_SVG_IT,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "PERCHÉ IL PIANO ASSUNZIONI FALLISCE",
                "h2": "Assumere stagionali è una trappola.",
                "body": [
                    "Cerchi personale nel mercato del lavoro più stretto "
                    "dell'anno - contro ogni magazzino, negozio e corriere che "
                    "vuole le stesse persone nelle stesse otto settimane.",
                    "Formi per settimane persone che a gennaio se ne vanno. Su "
                    "un contratto da dieci settimane, la formazione non si "
                    "ripaga mai.",
                    "E i somministrati non sono l'opzione economica: il margine "
                    "dell'agenzia sta sopra la paga piena. Paghi di più all'ora "
                    "per meno esperienza.",
                ],
            },
            {
                "tone": "light",
                "eyebrow": "E I TEMPI REMANO CONTRO",
                "h2": "Le chiamate arrivano [nb]dopo la promo.[/nb]",
                "body": [
                    "Gli ordini fanno picco in un giorno. Le chiamate circa una "
                    "settimana dopo: una chiamata su un ordine può esistere solo "
                    "quando l'ordine esiste.",
                    "Così gli stagionali sono formati per la promo, e la coda si "
                    "forma mentre i loro turni si alleggeriscono. Poi gennaio "
                    "porta l'ondata dei resi - più del doppio dei volumi normali "
                    "- subito dopo la fine dei contratti.",
                ],
                "viz": _it(BAND_SVG_IT, [
                    ("rgba(248,244,241,.25)", "rgb(227,226,226)"),
                    ("rgba(248,244,241,.5)", "rgb(160,158,157)"),
                    ("rgba(248,244,241,.75)", "rgb(69,65,64)"),
                    ("rgba(248,244,241,.45)", "rgb(120,118,117)"),
                    ("rgb(204,255,0)", "rgb(122,153,0)"),
                ]),
                "fine": ('Curve illustrative. Resi: <a href="' + _EVRI + '" '
                         'rel="nofollow noopener" target="_blank">rete Evri</a>, '
                         '3,9 mln di pacchi nelle quattro settimane dopo Natale '
                         '2023, oltre il doppio dei volumi tipici.'),
            },
        ],


        "workflows": {
            "h2": "Cosa Sabato può togliere al tuo team",
            "lede": "Il picco è quattro problemi ordinari che arrivano insieme. "
                    "Ognuno è un flusso che l'agente già gestisce.",
            "go": "Vedi il flusso",
            "items": [
                ("Dov'è il mio ordine", "/it/casi-duso/dove-e-il-mio-ordine",
                 "La chiamata che definisce la settimana. Stato letto in tempo "
                 "reale, confermato via messaggio.", "wismo"),
                ("Consulenza pre-vendita", "/it/casi-duso/consulenza-pre-vendita",
                 "In alta stagione si chiede prima di ordinare: se va bene, se "
                 "arriva in tempo. Risposta durante la chiamata, non dopo.", "presales"),
                ("Gestione resi", "/it/casi-duso/gestione-resi",
                 "Il picco di gennaio. Prenotato al telefono nel momento in cui "
                 "il portale dice no.", "returns"),
                ("Notifica ritorno in stock", "/it/casi-duso/notifica-ritorno-in-stock",
                 "L'altra faccia del picco è finire le scorte. Chi chiama viene "
                 "avvisato appena torna.", "restock"),
            ],
        },

        "proof": {
            "eyebrow": "LA PROVA",
            "quote": "Elena gestisce le nostre chiamate più ripetitive - stato "
                     "ordine, spedizioni, resi - in linea con il brand e "
                     "all'istante. Il nostro team ora si concentra sui casi che "
                     "hanno davvero bisogno di una persona.",
            "who": "Marco Logreco",
            "role": "Head of E-Commerce, Creative Cables",
            "nums": [("39%", "Chiamate risolte dall'inizio alla fine"),
                     ("57%", "Delle richieste stato ordine automatizzate"),
                     ("55s", "Durata media della chiamata")],
            "href": "/it/clienti/creative-cables",
            "link": "Leggi il caso studio completo",
        },

        "faq_h2": "Le domande che fanno gli operatori",
        "faq": [
            ("Quanto in fretta possiamo essere online prima del picco?",
             "Due settimane dal kickoff. Quattro settimane prima della promo è "
             "l'ultimo momento comodo: lascia quindici giorni di chiamate vere "
             "per tarare prima che arrivi il volume."),
            ("Sostituisce il mio team di supporto?",
             "No. Assorbe il volume ripetitivo - lo stato ordine su tutto - così "
             "le tue persone passano la settimana di picco sulle chiamate che "
             "richiedono giudizio. I casi delicati passano a un umano con tutto "
             "il contesto."),
            ("Cosa succede dopo il picco?",
             "Niente esuberi. La capacità scende con le chiamate, e lo stesso "
             "agente gestisce l'ondata di resi di gennaio che gli stagionali "
             "avrebbero mancato."),
            ("E se non sa la risposta?",
             "Lo dice e passa la chiamata al tuo team con dati e intento del "
             "cliente allegati: il cliente non ricomincia mai da capo."),
        ],

        "cta": {
            "hand": "prima che si formi la coda",
            "h2": "La capacità che non puoi assumere, [nb]puoi accenderla.[/nb]",
            "sub": "Lo costruiamo noi, lo gestiamo noi, tu vedi i numeri. Online "
                   "in due settimane.",
        },
    },

    # Gemella di /playbooks/international-expansion. Il post
    # /it/blog/multilingual-phone-support-eu-expansion resta contenuto di
    # supporto sotto questa pagina, non un concorrente sulla stessa chiave.
    "espansione-internazionale": {
        "en": "international-expansion",
        "nav": "Espandi in nuovi Paesi",
        "chip": "Playbook",
        "title": "Espandere all'estero senza assumere in loco | Sabato AI",
        "description": "Apri un mercato e rispondi al telefono la stessa "
                       "settimana. Un agente vocale prende le chiamate nella "
                       "lingua locale dal primo giorno: nessuna assunzione "
                       "all'estero, nessuna agenzia, nessun volume minimo.",
        "h1": "Vendi in cinque Paesi. [nb]Rispondi in cinque lingue.[/nb]",
        "sub": "Aprire un mercato richiede un pomeriggio. Coprirne il telefono "
               "richiede una persona che ai volumi di lancio non puoi "
               "giustificare. Un agente vocale risponde nella lingua di chi "
               "chiama dal primo giorno: online in due settimane.",
        "hero_visual": INTL_HERO_SVG_IT,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "PERCHÉ QUELL'ASSUNZIONE NON ARRIVA MAI",
                "h2": "Un mercato nuovo non si paga il centralino.",
                "body": [
                    "Ai volumi di lancio un madrelingua è uno stipendio pieno per "
                    "una frazione di ruolo, e una persona per lingua è un unico "
                    "punto di rottura: una vacanza, una dimissione, e quel "
                    "mercato resta muto.",
                    "Così la linea aspetta i volumi, e i volumi aspettano la "
                    "linea.",
                    "Nessuno si lamenta di un numero a cui non può parlare nella "
                    "propria lingua. Semplicemente non chiama, e non torna - che "
                    "è esattamente come si legge un mercato che non c'era.",
                ],
            },
            {
                "tone": "light",
                "eyebrow": "E L'INGLESE NON COLMA IL DIVARIO",
                "h2": "Leggono l'inglese. [nb]Non ci telefonano.[/nb]",
                "body": [
                    "Leggere una scheda prodotto in una seconda lingua è facile. "
                    "Spiegare al telefono un problema di consegna, molto meno.",
                    "Anche tra chi legge l'inglese con più sicurezza, <b>il 60% "
                    "vuole comunque assistenza nella propria lingua</b> - e il "
                    "75% dice di essere più propenso a ricomprare dal marchio "
                    "che gliela dà.",
                ],
                "viz": INTL_BARS_SVG_IT,
                "fine": ('<a href="' + _CSA + '" rel="nofollow noopener" '
                         'target="_blank">CSA Research, &ldquo;Can&rsquo;t Read, '
                         'Won&rsquo;t Buy &ndash; B2C&rdquo;</a>, 2020 &ndash; '
                         '8.709 consumatori in 29 Paesi.'),
            },
            {
                "tone": "dark",
                "eyebrow": "IL COSTO DEL PAESE SUCCESSIVO",
                "h2": "Una lingua in più, [nb]non una persona in più.[/nb]",
                "body": [
                    "Con le persone ogni lingua è un costo a gradino: "
                    "un'assunzione, un turno, un percorso di formazione e la "
                    "copertura per le settimane in cui quella persona non c'è.",
                    "Con un agente è configurazione. Il quinto Paese costa quanto "
                    "il secondo.",
                ],
            },
        ],

        "workflows": {
            "h2": "Cosa Sabato può togliere al tuo team",
            "lede": "Un mercato nuovo fa le stesse quattro domande del mercato "
                    "di casa - in una lingua che non hai a turno.",
            "go": "Vedi il flusso",
            "items": [
                ("Consulenza pre-vendita", "/it/casi-duso/consulenza-pre-vendita",
                 "Il primo ordine su un sito straniero comincia con una domanda. "
                 "Risposta durante la chiamata, nella sua lingua.", "presales"),
                ("Dov'è il mio ordine", "/it/casi-duso/dove-e-il-mio-ordine",
                 "La consegna transfrontaliera è più lenta e meno leggibile. "
                 "Stato letto in tempo reale, confermato per iscritto.", "wismo"),
                ("Gestione resi", "/it/casi-duso/gestione-resi",
                 "L'unica cosa che blocca un primo ordine dall'estero. Prenotato "
                 "al telefono, nella sua lingua.", "returns"),
                ("Riepilogo checkout via messaggio",
                 "/it/casi-duso/riepilogo-checkout-via-messaggio",
                 "L'ordine riletto e mandato per iscritto, così niente dipende da "
                 "una telefonata in seconda lingua.", "checkout"),
            ],
        },

        "faq_h2": "Le domande che fanno gli operatori",
        "faq": [
            ("Quante lingue può gestire?",
             "Quante ne servono. L'agente riconosce la lingua di chi chiama alla "
             "prima frase e ci resta per tutta la chiamata, riepilogo scritto "
             "compreso."),
            ("Suona madrelingua o tradotto?",
             "Madrelingua. Ogni lingua è costruita e testata da chi la parla: un "
             "copione tradotto e letto ad alta voce è esattamente ciò che fa "
             "riattaccare."),
            ("Serve un numero locale in ogni Paese?",
             "Non è obbligatorio, ma un numero locale è il segnale di fiducia "
             "più economico che un sito straniero possa comprare. L'agente "
             "risponde a qualunque linea squilli."),
            ("E se abbiamo già qualcuno che copre quella lingua?",
             "Allora smette di essere l'unico punto di rottura. L'agente prende "
             "il volume ripetitivo e le chiamate fuori orario; la tua persona "
             "prende quelle che richiedono giudizio."),
        ],

        "cta": {
            "hand": "prima di archiviare il mercato",
            "h2": "Apri il Paese. [nb]La linea apre con lui.[/nb]",
            "sub": "Lo costruiamo noi, lo gestiamo noi, tu vedi i numeri. Online "
                   "in due settimane.",
        },
    },
}
