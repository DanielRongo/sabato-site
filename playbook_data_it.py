#!/usr/bin/env python3
"""Playbook content, Italian. Mirrors the English landing rules exactly:
one-sentence paragraphs, three CTAs, global framing - nothing
jurisdiction-specific. See playbook_data.py for the full brief.

SVGs are imported and relabelled, never copied: the coordinates are identical
in both languages and a translator has no business editing path data.
"""
from playbook_data import HERO_SVG, BAND_SVG

ORDER_IT = ["picchi-stagionali"]


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

_EVRI = "https://www.evri.com/press/return-to-sender-four-million-gifts-to-be-sent-back-in-january-2025"

PLAYBOOKS_IT = {
    "picchi-stagionali": {
        "en": "peak-season",
        "nav": "Picchi stagionali",
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
            "h2": "Cosa toglie al tuo team",
            "lede": "Il picco è quattro problemi ordinari che arrivano insieme. "
                    "Ognuno è un flusso che l'agente già gestisce.",
            "go": "Vedi il flusso",
            "items": [
                ("Dov'è il mio ordine", "/it/casi-duso/dove-e-il-mio-ordine",
                 "La chiamata che definisce la settimana. Stato letto in tempo "
                 "reale, confermato via messaggio."),
                ("Gestione resi", "/it/casi-duso/gestione-resi",
                 "Il picco di gennaio. Prenotato al telefono nel momento in cui "
                 "il portale dice no."),
                ("Notifica ritorno in stock", "/it/casi-duso/notifica-ritorno-in-stock",
                 "L'altra faccia del picco è finire le scorte. Chi chiama viene "
                 "avvisato appena torna."),
                ("Recupero carrelli abbandonati", "/it/casi-duso/recupero-carrelli-abbandonati",
                 "In picco i carrelli si bloccano su date e disponibilità. Una "
                 "chiamata da un minuto risolve entrambe."),
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
}
