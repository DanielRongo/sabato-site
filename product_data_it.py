# -*- coding: utf-8 -*-
"""Copy italiana per le pagine Prodotto.

NON E' UNA TRADUZIONE. Daniel, 14 Aug: "non tradurre l'italiano letteralmente
ma localizza davvero". Quindi questa pagina e' scritta in italiano, non
ricalcata sull'inglese: le frasi sono diverse, non solo le parole. Dove
l'inglese usa "brief" l'italiano usa "istruzioni", perche' "brief" in un
e-commerce italiano suona da agenzia pubblicitaria. Dove l'inglese fa una
battuta sul chatbot, l'italiano fa la stessa battuta ma con il ritmo giusto.

Il nome del prodotto resta in inglese - "Voice Agent Builder" - come fanno
tutti i prodotti software venduti in Italia. Tradurlo ("Costruttore di Agenti
Vocali") suonerebbe come un manuale tradotto male, ed e' esattamente
l'impressione che questa pagina non puo' permettersi.
"""

VOICE_AGENT_BUILDER_IT = dict(
    slug="voice-agent-builder",
    en="voice-agent-builder",
    chip="Voice Agent Builder",

    title="Voice Agent Builder | Sabato AI",
    description="Qui l'agente al telefono riceve istruzioni, strumenti e "
                "limiti. Le regole le detti tu, noi lo costruiamo e lo teniamo "
                "aggiornato. Online in due settimane.",

    # 22 e 22 caratteri. "Al resto pensiamo noi" e' gia' la formula che usa la
    # homepage italiana ("Scegli i workflow. Al resto pensiamo noi."): riusarla
    # qui fa suonare il sito come una voce sola invece che come sei pagine
    # scritte da sei persone.
    h1="Le regole le detti tu.[br]Al resto pensiamo noi.",
    sub="Il Voice Agent Builder e' il posto dove un agente telefonico riceve "
        "le sue istruzioni, i suoi strumenti e i suoi limiti. Tu spieghi come "
        "deve andare una chiamata. Al resto - costruirlo e tenerlo aggiornato "
        "- pensiamo noi.",

    hero_visual="",

    shot=dict(
        src="/product/assets/voice-agent-builder",
        alt="Il designer degli agenti di Sabato: un agente di ingresso "
            "collegato a tre agenti specializzati, con la configurazione "
            "dell'agente selezionato aperta di fianco.",
        caption="L'agente pre-vendita di un negozio. L'agente di ingresso "
                "risponde; tre specialisti prendono le chiamate che non deve "
                "gestire da solo.",
    ),

    blocks=[
        dict(
            tone="dark",
            eyebrow="LE ISTRUZIONI",
            h2="Un agente vale quanto le istruzioni che ha.",
            body=[
                "Sotto ogni agente c'e' un documento scritto: chi e', a cosa "
                "serve, come deve parlare e le cose che non deve dire mai. "
                "Non codice - frasi. Quello che daresti a una persona nuova il "
                "primo giorno, con la differenza che questa se lo rilegge "
                "prima di ogni singola chiamata.",
                "Il tuo puoi leggerlo quando vuoi. Ogni modifica resta "
                "registrata con la data, cosi' \"da quando dice questa cosa?\" "
                "e' una domanda che ha una risposta.",
            ],
        ),
        dict(
            tone="light",
            eyebrow="GLI STRUMENTI",
            h2="Non parla soltanto. Fa le cose.",
            h2_in_col=True,
            body=[
                "Un chatbot con un numero di telefono sa solo parlare. Un "
                "agente con gli strumenti giusti cerca l'ordine del cliente, "
                "controlla se quello che vuole c'e' davvero, passa la chiamata "
                "a una persona e scrive com'e' andata nei tuoi sistemi prima "
                "di riagganciare.",
                "Ogni strumento ha la sua regola su quando usarlo. E, cosa che "
                "conta uguale, su quando non usarlo.",
            ],
            viz="TOOLS_VIZ",
        ),
        dict(
            tone="dark",
            eyebrow="NIENTE VA ONLINE PER SBAGLIO",
            h2="Prima in bozza. Poi lo ascolti. Poi pubblichi.",
            h2_in_col=True,
            viz="RELEASE_FLOW",
            body=[
                "Le modifiche restano in bozza finche' qualcuno non le "
                "pubblica. Prima puoi chiamare la bozza e sentirtela gestire "
                "proprio il caso che ti preoccupa: e' un test piu' serio che "
                "rileggere le istruzioni e sperare.",
                "Le modifiche in attesa sono elencate prima di uscire, e ogni "
                "versione resta. Se un cambiamento peggiora le cose, quella "
                "precedente e' ancora li'.",
            ],
        ),
    ],

    hands=dict(
        h2="Chi ci mette le mani, in concreto",
        lede="Quello che vedi e' il nostro strumento di lavoro, non un lavoro "
             "in piu' per te. La divisione onesta e' questa.",
        cards=[
            ("Le regole le porti tu",
             "Come vuoi che si parli ai tuoi clienti. Cosa non si promette "
             "mai. Quali chiamate devono sempre arrivare a una persona. Queste "
             "le sai tu, non noi."),
            ("Il lavoro lo facciamo noi",
             "Scrivere le istruzioni, collegare gli strumenti al catalogo e "
             "agli ordini, testare, e rimetterci mano quando la gamma cambia."),
            ("Tu vedi tutto",
             "Ogni chiamata trascritta, ogni strumento che l'agente ha usato, "
             "ogni modifica con la sua data. In sola lettura, se preferisci "
             "cosi'."),
        ],
    ),

    faq_h2="Le domande che ci fanno davvero",
    faq=[
        ("Dobbiamo costruircelo noi l'agente?",
         "No. Questo e' lo strumento con cui lo costruiamo noi. Tu hai un "
         "accesso e puoi leggere tutto - istruzioni, strumenti, trascrizioni - "
         "ma nessuno da parte tua deve configurare niente. Se poi preferisci "
         "fare da solo qualche modifica leggera, puoi: e' una possibilita', "
         "non un compito."),
        ("Possiamo vedere esattamente cosa gli avete detto di dire?",
         "Si', tutto, in italiano. Sono istruzioni scritte, non una scatola "
         "nera, e ogni modifica resta registrata con la data."),
        ("E quando non sa rispondere?",
         "Lo dice e passa la chiamata a una persona del tuo team, con quello "
         "che il cliente ha gia' raccontato. E' impostato per passare la mano "
         "invece di inventare: una risposta sbagliata detta con sicurezza "
         "costa molto piu' di un trasferimento."),
        ("Puo' fare qualcosa o sa solo parlare?",
         "Cerca ordini e disponibilita', manda un messaggio di riepilogo, apre "
         "un ticket, trasferisce la chiamata e scrive com'e' andata nei tuoi "
         "sistemi tramite webhook. Cosa puo' raggiungere lo decidiamo insieme "
         "quando lo costruiamo."),
        ("Il nostro catalogo cambia in continuazione. L'agente resta indietro?",
         "Legge il tuo catalogo, non una copia: prodotti nuovi e cambi di "
         "prezzo ci sono appena sono online nel tuo store. Le istruzioni le "
         "manteniamo noi, fa parte del servizio."),
        ("Quanto ci vuole prima che risponda a chiamate vere?",
         "Due settimane dalla prima call, sul tuo numero, con il catalogo "
         "vero dietro."),
    ],

    cta=dict(
        hand="online in due settimane",
        h2="Portaci una chiamata che ricevete sempre.",
        sub="Dicci qual e' la chiamata che il tuo team non ne puo' piu' di "
            "prendere, e ti facciamo vedere l'agente che la prende al posto "
            "suo. Senza slide.",
    ),
)

PRODUCTS_IT = {p["slug"]: p for p in [VOICE_AGENT_BUILDER_IT]}
ORDER_IT = ["voice-agent-builder"]
