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
            "note": "Ogni coda risposta in ogni mercato, da un unico team italiano - "
                    "nessun mercato che aspetta un'assunzione prima di avere una linea.",
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
        "description": "Come ClimaConvenienza ha scalato il supporto telefonico su Italia, Francia e Germania senza assumere: 53,1% delle chiamate gestite in autonomia.",
        "h1": "Cresce su tre mercati più in fretta di quanto si possa [nb]assumere.[/nb]",
        "sub": ("ClimaConvenienza vende climatizzazione in Italia, Francia e Germania. La domanda "
                "saliva in tutti e tre - poi un'ondata di caldo l'ha portata a un record otto giorni "
                "dopo il go-live. La linea telefonica è cresciuta con l'azienda invece di frenarla."),

        "situation_eyebrow": "Il contesto",
        "situation_h2": "L'espansione corre più veloce delle assunzioni",
        "situation_body": [
            "ClimaConvenienza vende pompe di calore, caldaie e climatizzatori su Shopify, e da tempo "
            "cresce ben oltre l'Italia. Un mercato nuovo genera telefonate molto prima di generare i "
            "volumi che giustificano una persona madrelingua: una linea francese e una tedesca "
            "costano uno stipendio pieno ciascuna dal primo giorno, su una frazione del traffico. "
            "La crescita arriva prima; il business case per l'organico arriva dopo.",
            "Poi ci si è messo il meteo. La climatizzazione ha una sola curva di domanda ed è la "
            "temperatura. Pochi giorni dopo il go-live l'agente gestiva la "
            "giornata più intensa di sempre - alla seconda settimana di operatività, assorbita senza "
            "una sola assunzione in più.",
        ],
        "situation_points": [
            ("I mercati nuovi squillano prima di ripagarsi",
             "Francia e Germania generavano chiamate da clienti già abbastanza avanti nel funnel da "
             "alzare la cornetta, molto prima che il volume giustificasse personale dedicato."),
            ("La domanda la decide il meteo, non il piano",
             "Un'ondata di caldo non avvisa. Il volume che conta di più arriva nei giorni per cui non "
             "avresti potuto organizzare i turni, e arriva da persone pronte a comprare oggi."),
            ("Metà del traffico telefonico è una sola domanda",
             "Dov'è il mio ordine vale il 48% delle chiamate. Risponderci bene non è una cortesia "
             "del supporto: è la voce più pesante nella giornata del team."),
        ],

        "stack_h2": "Cosa è andato live",
        "stack": [
            ("languages", "Pre-vendita e supporto multilingua",
             "L'agente prende chiamate in italiano, francese e tedesco su tutte e tre le code - "
             "informazioni generali, tracking ordini e configuratore - sullo stesso catalogo e con "
             "le stesse regole."),
            ("wismo", "Dov'è il mio ordine",
             "La coda più grande, di gran lunga. Stato dell'ordine letto in tempo reale da Shopify e "
             "confermato al cliente, con il dettaglio inviato via messaggio così nulla dipende da "
             "cosa si ricorda chi ha chiamato."),
            ("configurator", "Configuratore",
             "Il configuratore, al telefono. L'agente porta chi chiama da dimensionamento e "
             "compatibilità a un modello preciso per il suo spazio e il suo impianto. È la coda con "
             "l'autonomia più alta della linea, al 57,8%."),
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
                           "giusto è 12000. Abbiamo un dual-split Hisense da 12000 con Wi-Fi "
                           "integrato disponibile, e un Mitsubishi della stessa classe se preferisce "
                           "quel marchio."),
                 ("caller", "Che differenza c'è di prezzo?"),
                 ("agent", "L'Hisense è 313,95 euro IVA inclusa, il Mitsubishi parte da 525. "
                           "Entrambi A++ in raffrescamento. Glieli mando via messaggio così li "
                           "confronta?"),
                 ("caller", "Sì, me li mandi."),
             ]},
            {"label": "WISMO", "icon": "wismo",
             "caption": "Dov'è il mio ordine",
             "duration": "00:51",
             "lines": [
                 ("caller", "Buongiorno, ho ordinato una pompa di calore la settimana scorsa e non "
                            "ho più saputo nulla."),
                 ("agent", "Controllo subito. Mi può dare il numero d'ordine?"),
                 ("caller", "Un attimo - 48120."),
                 ("agent", "Grazie. Il suo ordine è partito dal magazzino ieri ed è previsto per "
                           "giovedì. Le mando adesso il link di tracking via messaggio."),
                 ("caller", "E se non c'è nessuno in casa alla consegna?"),
                 ("agent", "Il corriere lascia l'avviso e riprova il giorno dopo. Se preferisce "
                           "fissare una fascia precisa, segnalo e il team gliela conferma."),
             ]},
        ],
        "call_note": ("I dettagli di prodotto e ordine qui sono indicativi. In chiamata reale "
                      "l'agente legge catalogo, disponibilità e ordini veri di ClimaConvenienza - e "
                      "gestisce le stesse due chiamate in francese e tedesco."),

        "results_eyebrow": "Risultati · il primo mese live",
        "results_h2": "Il primo mese",
        "results": [
            ("53,1%", "Chiamate gestite in autonomia",
             "Risolte dall'agente senza alcun operatore, nel primo mese live."),
            ("435", "Ore di supporto restituite",
             "Tempo al telefono assorbito dall'agente invece che da un operatore, reimpiegato sulle "
             "vendite B2B."),
            ("1.535", "Chiamate nel giorno di picco",
             "Assorbite durante un'ondata di caldo, senza una sola assunzione in più."),
        ],
        "results_foot": "Misurato sul primo mese dal go-live.",

        "quote": ("Abbiamo affrontato un picco di domanda enorme senza assumere nessuno - e abbiamo "
                  "spostato una buona parte del team di customer support sulle vendite B2B, così "
                  "fanno crescere l'azienda invece di ripetere la stessa cosa al telefono tutto il "
                  "giorno."),

        "cta_h2": "Vuoi lo stesso per il tuo e-commerce?",
        "cta_sub": ("Un pilota gira sulle tue chiamate vere e misura cosa cambia rispetto alla tua "
                    "baseline. Niente slide."),
    },
    "creative-cables": {
        "en": "creative-cables",
        "name": "Creative Cables",
        "initials": "CC",
        "logo": "/customers/assets/creative-cables-logo.png",
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
