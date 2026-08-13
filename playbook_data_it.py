#!/usr/bin/env python3
"""Playbook content, Italian. Mirrors the English landing rules exactly:
one-sentence paragraphs, three CTAs, global framing - nothing
jurisdiction-specific. See playbook_data.py for the full brief.

SVGs are imported and relabelled, never copied: the coordinates are identical
in both languages and a translator has no business editing path data.
"""
from playbook_data import (HERO_SVG, BAND_SVG, INTL_HERO_SVG, _bar,
                           MISSED_HERO_SVG, MISSED_BAND_SVG, TEAM_HERO_SVG,
                           HIVAL_HERO_SVG, MULTI_HERO_SVG)

ORDER_IT = ["picchi-stagionali", "espansione-internazionale", "chiamate-perse",
             "costi-assistenza", "attivita-di-valore",
             "assistenza-multilingue"]


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
    (">every language<", ">ogni lingua<"),
    ('aria-label="Five local phone numbers in five different languages, all answered by one voice agent."',
     'aria-label="Cinque numeri locali in cinque lingue diverse, tutti gestiti da un solo agente vocale."'),
])

# Stesse barre in HTML: le etichette sono copy, non testo SVG, quindi seguono
# la stessa griglia tipografica della colonna di sinistra. Vedi playbook_data.py.
INTL_BARS_IT = (
    '<div class="pb-bars">'
    + _bar("Chi legge bene l\u2019inglese e vuole comunque "
           "assistenza nella propria lingua", 60)
    + _bar("Pi\u00f9 propensi a ricomprare dal marchio quando "
           "l\u2019assistenza \u00e8 nella loro lingua", 75)
    + '</div>')

MISSED_HERO_SVG_IT = _it(MISSED_HERO_SVG, [
    ("TWO WAYS TO LOSE ONE ORDER", "DUE MODI DI PERDERE UN ORDINE"),
    (">Abandoned online<", ">Carrello abbandonato<"),
    (">session<", ">sessione<"), (">email<", ">email<"),
    (">retargeting<", ">retargeting<"),
    (">Call rings out<", ">Telefono che squilla a vuoto<"),
    (">no record at all<", ">nessuna traccia<"),
    ('aria-label="An abandoned online cart leaves a session, an email and a retargeting audience. A call that rings out leaves no record of any kind."',
     'aria-label="Un carrello abbandonato lascia una sessione, un\'email e un pubblico di retargeting. Una telefonata che squilla a vuoto non lascia alcuna traccia."'),
])

MISSED_BAND_SVG_IT = _it(MISSED_BAND_SVG, [
    ("4-6% for fifteen years", "4-6% per quindici anni"),
    ('aria-label="Call abandonment at UK contact centres sat between four and six per cent from 2004 to 2019, then rose to over eight per cent after 2020 and stayed there."',
     'aria-label="Nei contact centre britannici le chiamate abbandonate sono rimaste tra il quattro e il sei per cento dal 2004 al 2019, poi sono salite oltre l\'otto per cento dopo il 2020 e non sono piu\' scese."'),
])

TEAM_HERO_SVG_IT = _it(TEAM_HERO_SVG, [
    ("WHAT THE QUEUE NEEDS", "QUANTO SERVE ALLA CODA"),
    (">three people, and a bit<", ">tre persone e mezza, quasi<"),
    ("WHAT YOU CAN HIRE", "QUANTO PUOI ASSUMERE"),
    ('aria-label="The queue needs three people and a bit. Headcount is only sold whole, so you hire four and pay for four."',
     'aria-label="Alla coda servono tre persone e mezza. Le persone si assumono intere: ne assumi quattro e ne paghi quattro."'),
])

TEAM_BARS_IT = (
    '<div class="pb-bars">'
    + _bar("Quota del costo di una persona che non arriva mai nella sua "
           "busta paga, media UE", 24.5, "24,5%")
    + '<p class="pb-note">E questo prima della postazione, delle licenze, della '
      'ricerca del candidato e della copertura per le settimane in cui quella '
      'persona non c&rsquo;&egrave; &ndash; nessuna delle quali Eurostat conta.</p>'
    + '</div>')

HIVAL_HERO_SVG_IT = _it(HIVAL_HERO_SVG, [
    ("THE SAME EIGHT HOURS", "LE STESSE OTTO ORE"),
    (">Today<", ">Oggi<"), (">Instead<", ">Invece<"),
    (">order status<", ">stato dell&#8217;ordine<"),
    (">where is my refund<", ">dov&#8217;&#232; il rimborso<"),
    (">back in stock?<", ">&#232; tornato in stock?<"),
    (">wholesale enquiries<", ">richieste all&#8217;ingrosso<"),
    (">VIP concierge<", ">servizio VIP<"),
    (">win-back calls<", ">chiamate di recupero<"),
    ('aria-label="The same eight hours. Today: order status, refund chasing, back-in-stock questions. Instead: wholesale enquiries, VIP concierge, win-back calls."',
     'aria-label="Le stesse otto ore. Oggi: stato ordine, rimborsi, richieste di riassortimento. Invece: richieste all\'ingrosso, servizio VIP, chiamate di recupero."'),
])

HIVAL_SPLIT_IT = (
    '<div class="pb-fork">'
    '<div class="pb-fork-row"><span class="pb-fork-in">Chiama una richiesta '
    'all&rsquo;ingrosso</span></div>'
    '<div class="pb-fork-out">'
    '<div class="pb-fork-a"><b>Risponde una coda</b><i>Registrata, evasa, chiusa. '
    'Non &egrave; di nessuno.</i></div>'
    '<div class="pb-fork-b"><b>Risponde una persona che ha tempo</b><i>Preventivo, '
    'richiamo, diventa un cliente.</i></div>'
    '</div></div>')

MULTI_HERO_SVG_IT = _it(MULTI_HERO_SVG, [
    ("WHAT YOUR GERMAN BUYER GETS", "COSA RICEVE IL TUO CLIENTE TEDESCO"),
    (">ads in German<", ">annunci in tedesco<"),
    (">checkout in German<", ">checkout in tedesco<"),
    (">prices in euros<", ">prezzi in euro<"),
    (">delivery in two days<", ">consegna in due giorni<"),
    (">support in English only<", ">assistenza solo in inglese<"),
    ('aria-label="A German customer gets ads, checkout, prices and delivery in German - and support in English only."',
     'aria-label="Un cliente tedesco riceve annunci, checkout, prezzi e consegna in tedesco, e l\'assistenza solo in inglese."'),
])

MULTI_FORK_IT = (
    '<div class="pb-fork">'
    '<div class="pb-fork-row"><span class="pb-fork-in">Lo stesso cliente, '
    'due canali</span></div>'
    '<div class="pb-fork-out">'
    '<div class="pb-fork-a"><b>Ti scrive un&rsquo;email</b><i>Un dizionario, una '
    'scheda col traduttore e tutto il tempo che gli serve.</i></div>'
    '<div class="pb-fork-b"><b>Ti telefona</b><i>Niente di tutto questo, in tempo '
    'reale, mentre prova a spiegare un problema.</i></div>'
    '</div></div>')

_EUROSTAT = "https://ec.europa.eu/eurostat/databrowser/view/lc_lci_lev/default/table"
_GARTNER = ("https://www.gartner.com/en/newsroom/press-releases/"
            "2024-08-19-gartner-survey-finds-only-14-percent-of-customer-service-"
            "issues-are-fully-resolved-in-self-service")

_CB = "https://www.contactbabel.com/the-uk-contact-centre-decision-makers-guide/"

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
        # [br], non [nb]: vedi la nota in playbook_data.py - un [nb] su questa
        # frase fa scorrere la pagina in orizzontale su uno schermo da 390px.
        "h1": "Apri cinque Paesi.[br]Nella loro lingua.",
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
                "h2": "Leggono l'inglese.[br]Non ci telefonano.",
                "body": [
                    "Leggere una scheda prodotto in una seconda lingua è facile. "
                    "Spiegare al telefono un problema di consegna, molto meno.",
                    "Anche tra chi legge l'inglese con più sicurezza, <b>il 60% "
                    "vuole comunque assistenza nella propria lingua</b> - e il "
                    "75% dice di essere più propenso a ricomprare dal marchio "
                    "che gliela dà.",
                ],
                "viz": INTL_BARS_IT,
                "h2_in_col": True,
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

    # Gemella di /playbooks/missed-calls. Vedi la nota di ricerca nel file
    # inglese: quasi tutte le statistiche in circolazione su questo tema sono
    # state verificate e SCARTATE. La pagina regge sulla struttura, con una sola
    # cifra esterna.
    "chiamate-perse": {
        "en": "missed-calls",
        "nav": "Rispondi a ogni chiamata",
        "chip": "Playbook",
        "title": "Rispondi a ogni chiamata senza assumere | Sabato AI",
        "description": "Una chiamata persa è un carrello abbandonato con un "
                       "numero di telefono - e non la registra nessuno. Un "
                       "agente vocale risponde sempre, giorno e notte.",
        # Non una traduzione: l'italiano è più lungo e non entra nella
        # colonna. Questa versione dice la tesi della pagina in meno battute.
        "h1": "La chiamata persa[br]non lascia traccia.",
        "sub": "Qualcuno ha chiamato per un ordine che era pronto a fare, non "
               "ha ricevuto risposta e ha comprato altrove. Nelle tue "
               "analytics non comparirà mai. Un agente vocale risponde a ogni "
               "chiamata, giorno e notte: online in due settimane.",
        "hero_visual": MISSED_HERO_SVG_IT,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "PERCHÉ QUESTO NUMERO NON L'HAI MAI VISTO",
                "h2": "L'unica perdita senza una dashboard.",
                "body": [
                    "Un carrello abbandonato online lascia una sessione, "
                    "un'email e un pubblico di retargeting: tre modi per "
                    "andarselo a riprendere.",
                    "Una telefonata che squilla a vuoto non lascia niente: "
                    "nessun ticket, perché non c'è stata conversazione, e "
                    "nessun follow-up, perché non hai mai avuto il suo "
                    "contatto.",
                    "Così non compare in nessun report che possiedi - e una "
                    "perdita che nessuno misura è una perdita che nessuno mette "
                    "in agenda.",
                ],
            },
            {
                "tone": "light",
                "h2_in_col": True,
                "eyebrow": "ED È PEGGIORATO OVUNQUE",
                "h2": "Chi riattacca prima di parlare[br]è raddoppiato dal 2009.",
                "body": [
                    "Nei contact centre britannici chi rinuncia prima che "
                    "qualcuno risponda è passato da circa il <b>4% a oltre "
                    "l'8%</b> dopo il 2020, e non è più tornato indietro.",
                    "E sono aziende che presidiano una coda e la misurano. Un "
                    "team di tre persone su una linea condivisa non sta facendo "
                    "meglio: semplicemente non ha un numero da guardare.",
                ],
                "viz": MISSED_BAND_SVG_IT,
                "fine": ('Chiamate abbandonate, valore medio. <a href="' + _CB +
                         '" rel="nofollow noopener" target="_blank">ContactBabel, '
                         'UK Contact Centre Decision-Makers&rsquo; Guide '
                         '2024</a> &ndash; 225 contact centre britannici, '
                         'rilevazione ott&ndash;nov 2023; mediana 6,0%. Dati del '
                         'settore contact centre, non e-commerce.'),
            },
            {
                "tone": "dark",
                "eyebrow": "IL CONTO CHE NON FA NESSUNO",
                "h2": "Il tuo scontrino medio lo conosci già.",
                "body": [
                    "Moltiplicalo per le chiamate senza risposta del mese "
                    "scorso: quelle fuori orario, quelle durante il turno di "
                    "pranzo, quelle mentre erano occupate entrambe le linee.",
                    "Nessuno strumento di analytics ti darà quel numero. Il tuo "
                    "centralino ce l'ha già.",
                ],
            },
        ],

        "workflows": {
            "h2": "Cosa Sabato può togliere al tuo team",
            "lede": "La chiamata che non puoi permetterti di perdere è in coda "
                    "dietro a quelle che potrebbero rispondersi da sole.",
            "go": "Vedi il flusso",
            "items": [
                ("Consulenza pre-vendita", "/it/casi-duso/consulenza-pre-vendita",
                 "La chiamata che è l'ordine. Risposta in diretta, con il tuo "
                 "catalogo dietro.", "presales"),
                ("Riepilogo checkout via messaggio",
                 "/it/casi-duso/riepilogo-checkout-via-messaggio",
                 "L'ordine riletto e mandato per iscritto, così si chiude "
                 "durante la chiamata invece che con un \u00abci penso\u00bb.",
                 "checkout"),
                ("Notifica ritorno in stock",
                 "/it/casi-duso/notifica-ritorno-in-stock",
                 "Un esaurito non deve diventare un cliente perso. Chi ha "
                 "chiamato lo sa appena rientra.", "restock"),
                ("Dov'è il mio ordine", "/it/casi-duso/dove-e-il-mio-ordine",
                 "Il motivo per cui nessuno risponde quando chiama chi vuole "
                 "comprare. Si gestisce da sola.", "wismo"),
            ],
        },

        "faq_h2": "Le domande che fanno gli operatori",
        "faq": [
            ("Come faccio a sapere quante chiamate stiamo perdendo?",
             "Il tuo centralino lo sa già. Esporta il registro chiamate del mese "
             "scorso e conta quelle senza risposta e fuori orario: quasi tutti i "
             "gestori e i cruscotti VoIP lo fanno in due clic, ed è di solito la "
             "prima volta che qualcuno ci guarda."),
            ("Prende l'ordine o lascia solo un messaggio?",
             "Prende l'ordine. Legge il catalogo in tempo reale, risponde alla "
             "domanda che bloccava l'acquisto e manda il riepilogo per iscritto "
             "prima di qualsiasi addebito."),
            ("E fuori orario?",
             "Risponde. È fuori orario che si concentra la perdita invisibile, "
             "perché quei clienti non raggiungono nessuno e non compaiono da "
             "nessuna parte."),
            ("E se chi chiama vuole una persona?",
             "La ottiene, con il contesto della chiamata già passato. Tutto ciò "
             "che l'agente non può chiudere viene inoltrato, non lasciato "
             "cadere."),
        ],

        "cta": {
            "hand": "prima che squilli a vuoto di nuovo",
            "h2": "La chiamata che perdi stasera[br]è l'ordine di qualcun altro.",
            "sub": "Lo costruiamo noi, lo gestiamo noi, tu vedi i numeri. Online "
                   "in due settimane.",
        },
    },

    # Gemella di /playbooks/support-costs. Vedi la nota nel file inglese per le
    # cifre verificate e per quelle scartate.
    "costi-assistenza": {
        "en": "support-costs",
        "nav": "Riduci i costi di assistenza",
        "chip": "Playbook",
        "title": "Ridurre il costo per contatto senza tagliare il team | Sabato AI",
        # 160 caratteri è il limite: la prima stesura ne aveva 161.
        "description": "La capacità si compra a persone intere: o sei sotto "
                       "organico o paghi troppo. Un agente vocale assorbe il "
                       "volume ripetitivo e ti restituisce le ore.",
        "h1": "Non puoi assumere[br]un terzo di persona.",
        "sub": "La capacità di assistenza si compra a persone intere: o sei "
               "sotto organico o paghi capacità che nessuno usa. Un agente "
               "vocale assorbe il volume ripetitivo e ti restituisce le ore: "
               "online in due settimane.",
        "hero_visual": TEAM_HERO_SVG_IT,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "PERCHÉ IL CONTO NON TORNA MAI",
                "h2": "La capacità si compra a persone intere.",
                "body": [
                    "Non puoi comprare il venti per cento di copertura in più. "
                    "Compri una persona, quindi il team è sempre o indietro o "
                    "sovradimensionato.",
                    "È per questo che la coda peggiora a scatti invece che "
                    "gradualmente, e che nessuno sa indicare il momento in cui "
                    "si è rotta.",
                ],
            },
            {
                "tone": "light",
                "h2_in_col": True,
                "eyebrow": "E QUEL BLOCCO COSTA PIÙ DI QUANTO SEMBRI",
                "h2": "Un quarto del costo[br]non è sulla busta paga.",
                "body": [
                    # Vedi la nota sull'aritmetica in playbook_data.py: 24,5% è
                    # la quota sul costo TOTALE, non un'aggiunta sopra la paga.
                    "In Europa circa <b>un quarto di quello che una persona costa "
                    "all'azienda non arriva mai nella sua busta paga</b> - e la "
                    "quota va dal 17% in Polonia al 28% in Francia.",
                    "I team si dimensionano sugli stipendi. L'unità di cui non "
                    "puoi comprare una frazione costa circa un terzo in più del "
                    "numero che c'è nel piano.",
                ],
                "viz": TEAM_BARS_IT,
                "fine": ('<a href="' + _EUROSTAT + '" rel="nofollow noopener" '
                         'target="_blank">Eurostat, costo del lavoro per attività '
                         'NACE Rev.&nbsp;2</a>, 2024 &ndash; Sezione N, il settore '
                         'che comprende i call centre. È un valore di settore, non '
                         'specifico dei contact centre.'),
            },
            {
                "tone": "dark",
                "eyebrow": "E LA SOLUZIONE ECONOMICA NON SVUOTA LA CODA",
                "h2": "Il self-service te li rimanda indietro.",
                "body": [
                    "Solo il 14% dei problemi di assistenza si risolve "
                    "completamente in self-service - e tra quelli che i clienti "
                    "stessi hanno definito molto semplici, appena il 36%.",
                    "Quindi il centro assistenza non toglie il contatto. Lo "
                    "rimanda, e te lo restituisce con una persona più "
                    "innervosita.",
                ],
                "fine": ('<a href="' + _GARTNER + '" rel="nofollow noopener" '
                         'target="_blank">Gartner</a>, indagine su 5.728 clienti, '
                         'dicembre 2023.'),
            },
        ],

        "workflows": {
            "h2": "Cosa Sabato può togliere al tuo team",
            "lede": "Decidi a cosa serviranno le ore liberate prima di "
                    "liberarle, o avrai un team più silenzioso e nessun numero "
                    "che si muove.",
            "go": "Vedi il flusso",
            "items": [
                ("Dov'è il mio ordine", "/it/casi-duso/dove-e-il-mio-ordine",
                 "Il blocco più grosso di volume ripetitivo. Stato letto in "
                 "tempo reale, confermato per iscritto.", "wismo"),
                ("Gestione resi", "/it/casi-duso/gestione-resi",
                 "Prenotato al telefono appena il portale dice no, senza una "
                 "persona in mezzo.", "returns"),
                ("Notifica ritorno in stock",
                 "/it/casi-duso/notifica-ritorno-in-stock",
                 "Oggi è pura burocrazia. Gestita senza che nessuno tenga una "
                 "lista.", "restock"),
                ("Consulenza pre-vendita", "/it/casi-duso/consulenza-pre-vendita",
                 "Quella su cui vuoi le tue persone - una volta che non sono "
                 "sepolte dalle altre tre.", "presales"),
            ],
        },

        "faq_h2": "Le domande che fanno gli operatori",
        "faq": [
            ("Significa che tagliamo il team?",
             "No, e i conti non ne hanno bisogno. Toglie il volume ripetitivo "
             "così le persone che hai già coprono di più senza crescere - che è "
             "la versione che sopravvive al confronto con il tuo staff."),
            ("Come facciamo a sapere quali contatti sono ripetitivi?",
             "Etichettane due settimane. Quasi tutti i team sanno già la "
             "risposta prima di finire - sono sempre le stesse domande - ma è il "
             "conteggio che convince chi deve firmare."),
            ("A cosa dovrebbero servire davvero le ore liberate?",
             "Decidilo prima di partire. Di solito la risposta è la pre-vendita "
             "e i clienti importanti che nessuno ha tempo di richiamare: se non "
             "sai dirlo in anticipo, il risparmio non comparirà da nessuna "
             "parte."),
            ("E se non riesce a gestire la chiamata?",
             "Passa la mano con i dati e l'intento di chi chiama già allegati, "
             "così la tua persona riparte da dove si è fermato l'agente e non da "
             "zero."),
        ],

        "cta": {
            "hand": "prima di pubblicare l'annuncio",
            "h2": "Restituisci le ore[br]al lavoro che richiede una persona.",
            "sub": "Lo costruiamo noi, lo gestiamo noi, tu vedi i numeri. Online "
                   "in due settimane.",
        },
    },

    # Gemella di /playbooks/high-value-work. Nessuna statistica esterna: la
    # pagina regge interamente sulla struttura. Vedi la nota nel file inglese.
    "attivita-di-valore": {
        "en": "high-value-work",
        "nav": "Libera il tuo team",
        "chip": "Playbook",
        "title": "Lancia il B2B e il servizio VIP senza assumere | Sabato AI",
        "description": "Il tuo team assistenza conosce catalogo e clienti meglio "
                       "di chiunque assumerai. Togligli le chiamate ripetitive e "
                       "mettilo a generare fatturato.",
        "h1": "Il telefono ti ruba[br]le persone migliori.",
        "sub": "Le persone che conoscono meglio il tuo catalogo e i tuoi clienti "
               "passano la giornata a leggere numeri di tracking. Toglilo dal "
               "loro tavolo e lo stesso team può seguire l'ingrosso e un servizio "
               "VIP: online in due settimane.",
        "hero_visual": HIVAL_HERO_SVG_IT,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "LA PERSONA CHE STAVI PER ASSUMERE",
                "h2": "Lavora già per te.",
                "body": [
                    "Il tuo team assistenza conosce il catalogo, le obiezioni e i "
                    "clienti difficili meglio di qualsiasi neoassunto per almeno "
                    "un anno.",
                    "Ed è l'unico gruppo in azienda che parla con chi compra "
                    "tutti i giorni - e lo passa a confermare date di consegna.",
                ],
            },
            {
                "tone": "light",
                "h2_in_col": True,
                "eyebrow": "E IL LAVORO STA GIÀ ARRIVANDO",
                "h2": "Stai chiudendo ticket[br]che erano clienti.",
                "body": [
                    "La richiesta all'ingrosso, il buyer che sta specificando un "
                    "ordine grosso, il cliente al suo undicesimo acquisto: ti "
                    "chiamano già tutti.",
                    "Se risponde una coda diventano ticket, e si chiudono. Se "
                    "risponde qualcuno che ha tempo diventano clienti, e si "
                    "richiamano.",
                ],
                "viz": HIVAL_SPLIT_IT,
            },
            {
                "tone": "dark",
                "eyebrow": "PERCHÉ \u00abCI TROVIAMO IL TEMPO\u00bb NON FUNZIONA MAI",
                "h2": "Il lavoro strategico[br]non si mette in coda.",
                "body": [
                    "\u00abIl venerdì lo dedichiamo ai clienti VIP\u00bb non "
                    "sopravvive a un martedì pieno, perché il telefono sta "
                    "squillando adesso e il richiamo no.",
                    "La capacità va tolta per davvero, non chiesta gentilmente. "
                    "Altrimenti l'urgente batte l'importante ogni settimana, per "
                    "sempre.",
                ],
            },
        ],

        "workflows": {
            "h2": "Cosa Sabato può togliere al tuo team",
            "lede": "Tre di questi liberano la giornata. Il primo è la giornata "
                    "che ti torna indietro.",
            "go": "Vedi il flusso",
            "items": [
                ("Preventivi automatici", "/it/casi-duso/preventivi-automatici",
                 "La richiesta all'ingrosso, raccolta come si deve invece di "
                 "finire nella coda dei ticket.", "quote"),
                ("Dov'è il mio ordine", "/it/casi-duso/dove-e-il-mio-ordine",
                 "Il blocco più grosso della settimana, sparito.", "wismo"),
                ("Gestione resi", "/it/casi-duso/gestione-resi",
                 "Prenotato al telefono senza una persona in mezzo.", "returns"),
                ("Notifica ritorno in stock",
                 "/it/casi-duso/notifica-ritorno-in-stock",
                 "Oggi è pura burocrazia. Gestita senza che nessuno tenga una "
                 "lista.", "restock"),
            ],
        },

        "faq_h2": "Le domande che fanno gli operatori",
        "faq": [
            ("Le nostre persone dell'assistenza non sono venditori.",
             "Non devono esserlo. Sono le persone di cui chi compra si fida già, "
             "e una richiesta all'ingrosso o un richiamo a un cliente VIP è una "
             "conversazione di servizio con un ordine più grande attaccato, non "
             "una chiamata a freddo."),
            ("Da cosa dovrebbero partire?",
             "Dalle richieste che oggi trasformi in ticket. L'ingrosso è la "
             "risposta più frequente: sono pochi contatti, con ordini grandi, e "
             "in questo momento non sono di nessuno."),
            ("Come capiamo se ha funzionato?",
             "Scegli il numero prima di partire: preventivi emessi, tasso di "
             "riacquisto sui clienti migliori, fatturato dai richiami. Se non lo "
             "definisci prima, il guadagno resterà invisibile anche se c'è "
             "stato."),
            ("Il servizio peggiora mentre fanno questo?",
             "No, perché il volume viene tolto, non spostato. Le chiamate "
             "ripetitive le prende l'agente: non restano a squillare mentre il "
             "team fa altro."),
        ],

        "cta": {
            "hand": "prima di assumere un commerciale B2B",
            "h2": "Il team che conosce il tuo prodotto[br]potrebbe venderlo.",
            "sub": "Lo costruiamo noi, lo gestiamo noi, tu vedi i numeri. Online "
                   "in due settimane.",
        },
    },

    # Gemella di /playbooks/multilingual-support. NON è la pagina
    # dell'espansione: là non vendi ancora in quel Paese, qui ci vendi già.
    # Vedi la nota nel file inglese.
    "assistenza-multilingue": {
        "en": "multilingual-support",
        "nav": "Assisti in ogni lingua",
        "chip": "Playbook",
        "title": "Assistenza multilingue senza assumere madrelingua | Sabato AI",
        "description": "Vendi già in sei Paesi e rispondi al telefono in una "
                       "lingua sola. Un agente vocale prende la chiamata in "
                       "quella con cui il cliente apre.",
        "h1": "Localizzato tutto[br]tranne chi risponde.",
        "sub": "Gli annunci, il checkout, la valuta e la promessa di consegna "
               "parlano la loro lingua. Poi risponde una persona, ed è inglese. "
               "Un agente vocale risponde nella lingua con cui aprono: online in "
               "due settimane.",
        "hero_visual": MULTI_HERO_SVG_IT,

        "blocks": [
            {
                "tone": "dark",
                "eyebrow": "L'UNICO PASSAGGIO CHE NON HAI TRADOTTO",
                "h2": "È tutto localizzato finché non risponde una persona.",
                "body": [
                    "Paghi già per raggiungere questi clienti nella loro lingua: "
                    "la campagna, la scheda prodotto, il checkout, le condizioni "
                    "di reso.",
                    "L'unico passaggio ancora in inglese è quello con dentro una "
                    "persona, ed è il passaggio che decide se ricomprano.",
                ],
            },
            {
                "tone": "light",
                "h2_in_col": True,
                "eyebrow": "E LA CASELLA EMAIL TI INGANNA",
                "h2": "Scrivere in inglese[br]non è parlarlo.",
                "body": [
                    "Il tuo helpdesk è pieno di inglese pulito scritto da clienti "
                    "di tutta Europa, e tutti concludono che la questione lingua "
                    "è risolta.",
                    "Scrivere gli dà un dizionario, una scheda col traduttore e "
                    "tutto il tempo che vuole. Una telefonata non gli dà niente "
                    "di tutto questo: così chi avrebbe chiamato semplicemente non "
                    "chiama.",
                ],
                "viz": MULTI_FORK_IT,
            },
            {
                "tone": "dark",
                "eyebrow": "ED È PER QUESTO CHE NESSUNO LO SEGNALA",
                "h2": "Nessuna dashboard dice \u00ablingua sbagliata\u00bb.",
                "body": [
                    "Non esiste una categoria di ticket né una domanda di "
                    "sondaggio, perché il cliente che non se la sentiva di "
                    "chiamare non è mai diventato un contatto.",
                    "Quello che vedi è un mercato che scrive più di quanto "
                    "telefoni e un tasso di riacquisto un filo sotto casa - e "
                    "nessuno dei due sembra un problema di lingua.",
                ],
            },
        ],

        "workflows": {
            "h2": "Cosa Sabato può togliere al tuo team",
            "lede": "Le chiamate che i tuoi clienti già fanno, gestite nella "
                    "lingua in cui le hanno fatte.",
            "go": "Vedi il flusso",
            "items": [
                ("Dov'è il mio ordine", "/it/casi-duso/dove-e-il-mio-ordine",
                 "La chiamata più frequente in ogni mercato in cui vendi. "
                 "Risposta nella sua lingua, confermata per iscritto.", "wismo"),
                ("Gestione resi", "/it/casi-duso/gestione-resi",
                 "La conversazione che meno si vuole fare in una seconda lingua. "
                 "Chiusa durante la chiamata.", "returns"),
                ("Consulenza pre-vendita", "/it/casi-duso/consulenza-pre-vendita",
                 "La domanda che decide l'ordine, senza che nessuno dei due tiri "
                 "a indovinare sul vocabolario.", "presales"),
                ("Feedback post-consegna", "/it/casi-duso/feedback-post-consegna",
                 "Chiedi com'è andata nella sua lingua e ottieni una risposta. "
                 "Chiedilo in inglese e ottieni silenzio.", "feedback"),
            ],
        },

        "faq_h2": "Le domande che fanno gli operatori",
        "faq": [
            ("Come facciamo a sapere quanto ci sta costando?",
             "Confronta il tasso di riacquisto per Paese con quello del mercato "
             "di casa, poi il rapporto tra email e chiamate. Un mercato che "
             "scrive molto più di quanto telefoni di solito è un mercato che non "
             "riesce a telefonarti."),
            ("Serve un numero diverso per ogni Paese?",
             "No. Una sola linea riconosce la lingua dalla prima frase e ci "
             "resta: un numero locale vale come segnale di fiducia, ma è una "
             "decisione separata dalla lingua."),
            ("E le lingue in cui vendiamo pochissimo?",
             "Sono quelle su cui conviene di più. Un mercato troppo piccolo per "
             "giustificare una persona è esattamente il mercato che non ha mai "
             "avuto copertura, e all'agente non importa quante chiamate faccia "
             "una lingua."),
            ("Passa la mano al nostro team?",
             "Sì, con la trascrizione e l'intento del chiamante allegati. Se "
             "arriva a qualcuno che non parla quella lingua, il riepilogo che "
             "riceve è nella tua."),
        ],

        "cta": {
            "hand": "per i clienti che hai già",
            "h2": "Comprano già da te.[br]Rispondi nella loro lingua.",
            "sub": "Lo costruiamo noi, lo gestiamo noi, tu vedi i numeri. Online "
                   "in due settimane.",
        },
    },
}