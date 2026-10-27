#!/usr/bin/env python3
"""Italian customer stories.

Same schema as customer_data.py. `en` maps each Italian slug back to its English
counterpart so the two builds can cross-link with hreflang without a second
lookup table drifting out of step.

Translation notes worth keeping:
  - "Where is my order" stays WISMO in the tile and the transcript label. It is
    the term the trade uses in Italian too, and it is what the report calls the
    queue.
  - The transcripts are re-voiced, not translated word for word. A caller asking
    about a heat pump in Italian does not phrase it the way an English caller
    does, and a transcript that reads as translated undoes the point of showing
    a real call.
"""

CUSTOMERS_IT = {
    "clima-convenienza": {
        "en": "clima-convenienza",
        "name": "ClimaConvenienza",
        "initials": "CC",
        "logo": "/customers/assets/climaconvenienza-logo.png",
        "person": "Alessio Perrucci",
        "person_initials": "AP",
        "role": "CEO",
        "photo": "/customers/assets/alessio-perrucci.jpg",
        "coverage": {
            "title": "Un agente · ogni coda · ogni mercato",
            "languages": ["Italiano", "Français", "Deutsch"],
            "queues": ["Informazioni generali", "Dov'è il mio ordine", "Configuratore"],
            "note": "Ogni coda risponde in ogni mercato con lo stesso agente, attivo in "
                    "ogni lingua dal primo giorno.",
        },
        "storefront": None,
        "storefront_url": "",
        "platform": "Shopify",
        "platform_logo": "/customers/assets/shopify.png",
        "industry": "Clima e Riscaldamento",
        "industry_href": "/it/settori/clima-e-riscaldamento",
        "chip": "Storia cliente",
        "approved": True,
        "promotable": False,
        "title": "ClimaConvenienza: case study agenti vocali | Sabato AI",
        "description": "Come ClimaConvenienza gestisce l'assistenza telefonica in Italia, Francia e Germania: 12.127 chiamate nel primo mese, il 44,5% concluse senza operatore.",
        "h1": "Tre mercati, tre lingue, una linea che cresce con [nb]l'azienda.[/nb]",
        "sub": ("ClimaConvenienza propone soluzioni per il comfort domestico in Italia, Francia e "
                "Germania. La domanda cresceva in tutti e tre i mercati, e sei giorni dopo il go-live "
                "un'ondata di caldo l'ha portata al record. La linea telefonica ha retto il picco e ha "
                "seguito la crescita."),

        "situation_eyebrow": "Il contesto",
        "situation_h2": "Un'assistenza multilingua a supporto della crescita internazionale",
        "situation_body": [
            "ClimaConvenienza porta il comfort domestico in tre Paesi e da anni cresce oltre i "
            "confini italiani. Ogni nuovo mercato porta subito clienti che vogliono parlare con "
            "qualcuno nella propria lingua, spesso prima ancora di acquistare. Serviva un'assistenza "
            "capace di seguire l'espansione in modo flessibile e di reggere i picchi di richieste, "
            "senza incidere pesantemente sui costi di gestione.",
            "Poi è arrivato il caldo. Nella climatizzazione la domanda ha forti picchi stagionali "
            "legati al meteo. Sei giorni dopo il go-live l'agente ha gestito la giornata più intensa "
            "di sempre: 973 chiamate.",
        ],
        "situation_points": [
            ("Ogni nuovo mercato chiama dal primo giorno",
             "In Francia e Germania i clienti telefonavano già nelle prime settimane, spesso a un "
             "passo dall'acquisto. L'assistenza doveva rispondere in francese e in tedesco subito, "
             "con la stessa qualità offerta in Italia."),
            ("I picchi seguono il meteo",
             "Un'ondata di caldo non si annuncia con settimane di anticipo. Le chiamate più preziose "
             "arrivano proprio in quei giorni, da persone pronte a comprare."),
            ("Più di quattro chiamate su dieci fanno la stessa domanda",
             "Dov'è il mio ordine vale il 42,4% delle 12.127 chiamate ricevute dall'agente nel primo "
             "mese. È la richiesta più frequente della giornata."),
        ],

        "stack_h2": "Cosa è andato live",
        "stack": [
            ("languages", "Pre-vendita e supporto multilingua",
             "L'agente prende chiamate in italiano, francese e tedesco su tutte e tre le code "
             "(informazioni generali, tracking ordini e configuratore), sullo stesso catalogo e con "
             "le stesse regole."),
            ("wismo", "Dov'è il mio ordine",
             "La domanda più frequente della linea. Stato dell'ordine letto in tempo reale da Shopify "
             "e confermato al cliente, con il dettaglio inviato via messaggio, così nulla dipende da "
             "cosa ricorda chi ha chiamato."),
            ("configurator", "Configuratore",
             "Il configuratore, al telefono. L'agente porta chi chiama da dimensionamento e "
             "compatibilità a un modello preciso per il suo spazio e il suo impianto. È la coda con "
             "la quota più alta di chiamate concluse senza operatore: il 56,7%."),
        ],
        "stack_note": ("Collegato a Shopify: l'agente legge lo stesso catalogo, gli stessi prezzi e "
                       "gli stessi ordini dello store."),

        "call_h2": "Com'è una chiamata ClimaConvenienza",
        "calls": [
            {"label": "Configuratore", "icon": "configurator",
             "caption": "Scegliere il modello giusto per la stanza",
             "duration": "01:24",
             "lines": [
                 ("caller", "Mi serve un condizionatore per una camera, saranno 30 metri quadri. "
                            "Non ho idea di che potenza prendere."),
                 ("agent", "Lo vediamo insieme. La stanza è all'ultimo piano? E prende molto sole nel "
                           "pomeriggio?"),
                 ("caller", "Ultimo piano sì, e sole tutto il pomeriggio."),
                 ("agent", "Allora 9000 BTU sarebbero sottodimensionati per quella stanza: il taglio "
                           "giusto è 12000. Abbiamo un monosplit Hisense da 12000 con Wi-Fi "
                           "integrato disponibile, e un Mitsubishi della stessa classe se preferisce "
                           "quel marchio."),
                 ("caller", "Che differenza c'è di prezzo?"),
                 ("agent", "L'Hisense è intorno ai 300 euro IVA inclusa, il Mitsubishi parte da circa "
                           "500. Glieli mando via messaggio così li confronta con calma?"),
                 ("caller", "Sì, me li mandi."),
             ]},
            {"label": "WISMO", "icon": "wismo",
             "caption": "Dov'è il mio ordine",
             "duration": "00:51",
             "lines": [
                 ("caller", "Buongiorno, ho ordinato una pompa di calore la settimana scorsa e non "
                            "ho più saputo nulla."),
                 ("agent", "Controllo subito. Mi può dare il numero d'ordine?"),
                 ("caller", "Un attimo... 48120."),
                 ("agent", "Grazie. Il suo ordine è partito dal magazzino ieri ed è previsto per "
                           "giovedì. Le mando adesso il link di tracking via messaggio."),
                 ("caller", "E se non c'è nessuno in casa alla consegna?"),
                 ("agent", "Segnalo la sua richiesta e il team la ricontatta per concordare la "
                           "consegna."),
             ]},
        ],
        "call_note": ("I dettagli di prodotto e ordine qui sono indicativi. In chiamata reale "
                      "l'agente legge catalogo, disponibilità e ordini veri di ClimaConvenienza, e "
                      "gestisce le stesse chiamate anche in francese e tedesco."),

        "results_eyebrow": "Risultati · dal 24 giugno al 24 luglio 2026",
        "results_h2": "Il primo mese",
        "results": [
            ("44,5%", "Chiamate concluse senza operatore",
             "Chiamate in cui l'agente non ha avviato alcun trasferimento a una persona del team. "
             "Base: 12.127 chiamate ricevute dall'agente."),
            ("12.127", "Chiamate gestite dall'agente",
             "In 30 giorni, per un totale di 264 ore di conversazione."),
            ("973", "Chiamate nel giorno di picco",
             "Ricevute dall'agente martedì 30 giugno 2026, sei giorni dopo il go-live, durante "
             "un'ondata di caldo."),
        ],
        "results_foot": ("Dati misurati sulla piattaforma Sabato dal 24 giugno al 24 luglio 2026, "
                         "chiamate di test escluse."),

        "quote": ("Sara ci ha aiutato a gestire un forte picco di richieste e a dedicare una parte "
                  "del team di assistenza alla gestione delle richieste più complesse e allo "
                  "sviluppo delle vendite B2B. Automatizzando le richieste più ricorrenti, possiamo "
                  "valorizzare le competenze delle nostre persone e dedicare più tempo alla "
                  "relazione con i clienti e alla crescita commerciale."),

        "cta_h2": "Vuoi lo stesso per il tuo e-commerce?",
        "cta_sub": ("Un pilota gira sulle tue chiamate vere e misura cosa cambia rispetto alla tua "
                    "baseline. Niente slide."),
    },
    "creative-cables": {
        "en": "creative-cables",
        "name": "Creative Cables",
        "initials": "CC",
        "logo": "/customers/assets/creative-cables-logo.png",
        # White knockout for use on the black proof card. The stock logo is
        # dark ink on an OPAQUE near-white plate, so it lands as a grey
        # rectangle on anything dark. Generated once, not filtered in CSS.
        "logo_white": "/customers/assets/creative-cables-logo-white.png",
        "person": "Marco Logreco",
        "person_initials": "ML",
        "role": "Head of E-Commerce",
        "photo": "/customers/assets/marco-logreco.jpg",
        "coverage": None,
        "kb": {
            "title": "Cosa sa Elena",
            "number": "~50.000 parole",
            "topics": ["Spedizioni", "Resi e garanzia", "Garanzia per paese", "Dogana",
                       "Pagamenti", "Servizi in negozio", "Certificazioni",
                       "Tracking ordini", "Formazione prodotto"],
            "note": "Un'unica base di conoscenza dietro entrambi gli agenti: la risposta su un reso "
                    "è la stessa lunedì alle 9 e venerdì alle 19.",
        },
        "storefront": None,
        "storefront_url": "",
        "platform": "",
        "platform_logo": None,
        "industry": "Arredamento e Casa",
        "industry_href": "/it/settori/arredamento",
        "chip": "Storia cliente",
        "approved": True,
        "promotable": True,
        "title": "Creative Cables: case study agenti vocali | Sabato AI",
        "description": "Come Creative Cables ha portato la voice AI sulla linea clienti italiana: 39% delle chiamate risolte dall'inizio alla fine nel primo mese.",
        "h1": "Elena risponde alle chiamate che si ripetono, in [nb]55 secondi.[/nb]",
        "sub": ("Creative Cables vende illuminazione decorativa, cavi tessili e componenti da Torino "
                "- sette negozi in Italia, uno a Parigi, spedizioni in tutto il mondo. Quasi tutto "
                "quello che chiede il telefono ha una risposta nota. Ora le risposte note arrivano "
                "subito, e al team restano le altre."),

        "situation_eyebrow": "Il contesto",
        "situation_h2": "Quasi tutte le chiamate hanno una risposta nota",
        "situation_body": [
            "Tempi di spedizione. Finestre di reso. Termini di garanzia, che cambiano da paese a "
            "paese. Dogana. Metodi di pagamento. Orari dei negozi. Nessuna di queste è una domanda "
            "difficile: sono le stesse domande, tutto il giorno, e ognuna occupa una persona che "
            "potrebbe seguire un caso che ha davvero bisogno di giudizio.",
            "Sotto a tutte c'è la richiesta più ripetitiva di tutte: dov'è il mio ordine. Era "
            "gestita interamente da persone, ed è la chiamata più prevedibile che un retailer "
            "riceva. La risposta esiste già nel sistema ordini: serviva solo qualcuno, o qualcosa, "
            "che la leggesse.",
        ],
        "situation_points": [
            ("Le stesse domande, tutto il giorno",
             "Spedizioni, resi, garanzia e pagamenti si ripetono all'infinito. Il costo non è la "
             "difficoltà, è il volume contro un team finito."),
            ("Dov'è il mio ordine era tutto manuale",
             "Il motivo di chiamata più ripetitivo della linea, gestito da una persona ogni singola "
             "volta, su dati che una macchina può leggere direttamente."),
            ("La vera esigenza è la coerenza",
             "Finestre di reso, regole doganali e termini di garanzia cambiano per paese. Devono "
             "essere corretti, e identici, a ogni chiamata - non giusti all'incirca a seconda di "
             "chi ha risposto."),
        ],

        "stack_h2": "Cosa è andato live",
        "stack": [
            ("languages", "Elena, sulla linea generale",
             "Un agente madrelingua italiano che gestisce azienda, spedizioni, resi, garanzia, "
             "pagamenti e domande sui negozi da un'unica base di conoscenza - così la risposta non "
             "dipende da chi ha alzato la cornetta."),
            ("wismo", "Dov'è il mio ordine, con dati live",
             "Un agente dedicato allo stato ordine, con lookup in tempo reale sul sistema ordini. "
             "Chi chiama riceve lo stato reale del proprio ordine, senza nessuno in mezzo."),
            ("configurator", "Un triage che protegge il team",
             "Prodotti danneggiati, cambi indirizzo e annullamenti vengono riconosciuti come veri "
             "casi post-vendita e passati a una persona con il contesto già raccolto."),
        ],
        "stack_note": "Due agenti, live sulla linea clienti italiana.",

        "call_h2": "Com'è una chiamata Creative Cables",
        "calls": [
            {"label": "WISMO", "icon": "wismo",
             "caption": "Stato ordine, letto dal sistema in tempo reale",
             "duration": "00:48",
             "lines": [
                 ("caller", "Buongiorno, ho ordinato una sospensione e del cavo la settimana scorsa "
                            "e vorrei sapere a che punto è."),
                 ("agent", "Certo. Sono Elena di Creative Cables. Mi può dare il numero d'ordine?"),
                 ("caller", "È 30294."),
                 ("agent", "Grazie. Vedo l'ordine: è partito martedì e il corriere ce l'ha in "
                           "consegna oggi. Le mando adesso il link di tracking via messaggio."),
                 ("caller", "Perfetto. E il cavo era nello stesso ordine?"),
                 ("agent", "Sì, sono entrambi nello stesso pacco."),
             ]},
            {"label": "Informazioni generali", "icon": "languages",
             "caption": "Una domanda sui resi, con la stessa risposta ogni volta",
             "duration": "01:02",
             "lines": [
                 ("caller", "Se ordino una lampada e non va bene per la stanza, quanto tempo ho per "
                            "restituirla?"),
                 ("agent", "Ha trenta giorni dalla consegna per richiedere il reso, e l'articolo "
                           "deve essere non utilizzato e nella confezione originale."),
                 ("caller", "Ordino dall'estero: cambia qualcosa?"),
                 ("agent", "La finestra è la stessa. Cambiano la spedizione di reso e gli eventuali "
                           "oneri doganali, che dipendono dal paese. Se mi dice da dove ordina le "
                           "do i termini esatti."),
                 ("caller", "Svizzera."),
                 ("agent", "Allora la dogana si applica in entrata e viene rimborsata separatamente "
                           "dal valore dell'ordine. Le mando i termini completi via messaggio così "
                           "li ha per iscritto."),
             ]},
        ],
        "call_note": ("I dettagli di ordine e policy qui sono indicativi. In chiamata reale Elena "
                      "legge il sistema ordini vero e la base policy vera."),

        "results_eyebrow": "Risultati · il primo mese live",
        "results_h2": "Il primo mese",
        "results": [
            ("39%", "Chiamate risolte dall'inizio alla fine",
             "Chiuse dall'agente senza alcun intervento umano, su entrambe le linee, nelle prime "
             "quattro settimane live."),
            ("57%", "Delle richieste stato ordine automatizzate",
             "La domanda più frequente e più ripetitiva della linea, risposta su dati ordine live."),
            ("55s", "Durata media della chiamata",
             "Il tempo che serve all'agente per rispondere e chiudere una chiamata."),
        ],
        "results_foot": "Misurato sulle prime quattro settimane dal go-live.",

        "quote": ("Elena gestisce le nostre chiamate più ripetitive - stato ordine, spedizioni, "
                  "resi - in linea con il brand e all'istante. Il nostro team ora si concentra sui "
                  "casi che hanno davvero bisogno di una persona."),

        "cta_h2": "Vuoi lo stesso per il tuo e-commerce?",
        "cta_sub": ("Un pilota gira sulle tue chiamate vere e misura cosa cambia rispetto alla tua "
                    "baseline. Niente slide."),
    },
}

ORDER_IT = ["clima-convenienza", "creative-cables"]
