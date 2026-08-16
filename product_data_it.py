# -*- coding: utf-8 -*-
"""Copy italiana per le pagine Prodotto.

NON È UNA TRADUZIONE. Daniel, 14 ago: "non tradurre l'italiano letteralmente
ma localizza davvero", e poi, sulla prima versione: "sotto il cofano non
esiste - si dice dietro le quinte". Quindi qui si scrive in italiano e si
controlla ogni frase contro il calco, non contro l'inglese.

I calchi trovati e corretti nella prima stesura, come promemoria:

    "sotto il cofano"        -> "dietro le quinte"
    "e' il posto dove..."    -> costruzione italiana, non "is where"
    "agente di ingresso"     -> "il primo agente" / "quello che risponde".
                                "Entry agent" resta inglese DENTRO il prodotto,
                                ma in una pagina di vendita si dice altrimenti.
    "di un negozio"          -> "di uno store": chi vende online in Italia dice
                                store o shop, non negozio.

ACCENTI VERI, NON APOSTROFI. La prima stesura scriveva "e'", "piu'", "cosi'",
"disponibilita'". Ogni altro file italiano di questo repo usa è, più, così,
disponibilità - 159 accenti in playbook_data_it.py, 421 in industry_data_it.py,
zero apostrofi di ripiego. Una pagina che scrive "c'e'" invece di "c'è" si
riconosce a colpo d'occhio come tradotta male, che è esattamente l'impressione
che questa pagina non può permettersi.

Il nome del prodotto resta in inglese - "Voice Agent Builder" - come tutti i
prodotti software venduti in Italia. "Costruttore di Agenti Vocali" suonerebbe
come un manuale tradotto col traduttore automatico.
"""

VOICE_AGENT_BUILDER_IT = dict(
    slug="voice-agent-builder",
    en="voice-agent-builder",
    chip="Voice Agent Builder",

    title="Voice Agent Builder | Sabato AI",
    description="Qui l'agente al telefono riceve istruzioni, strumenti e "
                "limiti. Le regole le detti tu, noi lo costruiamo e lo teniamo "
                "aggiornato. Online in due settimane.",

    # 22 e 22 caratteri. "Al resto pensiamo noi" è già la formula della homepage
    # italiana ("Scegli i workflow. Al resto pensiamo noi."): riusarla qui fa
    # suonare il sito come una voce sola invece che come sei pagine scritte da
    # sei persone diverse.
    h1="Le regole le detti tu.[br]Al resto pensiamo noi.",
    sub="Nel Voice Agent Builder un agente telefonico prende le sue istruzioni, "
        "i suoi strumenti e i suoi limiti. Tu racconti come deve andare una "
        "chiamata. Costruirlo, e poi tenerlo aggiornato, è compito nostro.",

    hero_visual="",

    shot=dict(
        src="/product/assets/voice-agent-builder",
        alt="Il designer degli agenti di Sabato: l'agente che risponde alle "
            "chiamate collegato a tre agenti specializzati, con la "
            "configurazione dell'agente selezionato aperta di fianco.",
        caption="L'agente pre-vendita di uno store. Risponde il primo agente; "
                "le chiamate che non deve gestire da solo passano a tre "
                "specialisti.",
    ),

    # Lo statement e i due pannelli che seguono lo screenshot grande.
    pair=dict(
        eyebrow="GLI STRUMENTI",
        h2="Non parla soltanto.[br]Fa le cose.",
        lede="Un chatbot con un numero di telefono sa solo parlare. Un agente "
             "con gli strumenti giusti tira fuori l'ordine dal tuo gestionale "
             "mentre il cliente è ancora al telefono - stato, corriere, la data "
             "che gli avevi promesso - e prima di riagganciare ci scrive com'è "
             "andata.",
    ),

    # I due capitoli qui sotto stanno in un'unica fascia scura, sotto un titolo.
    group=dict(
        eyebrow="DIETRO LE QUINTE",
        h2="Come si costruisce.[br]E come si cambia.",
    ),

    blocks=[
        dict(
            eyebrow="01 · LE ISTRUZIONI",
            h2="Un agente vale quanto le istruzioni che ha.",
            h2_in_col=True,
            viz="BRIEF_VIZ",
            body=[
                "Dietro ogni agente c'è un documento scritto: chi è, a cosa "
                "serve, come deve parlare e le cose che non deve dire mai. Non "
                "codice: frasi. Quello che daresti a una persona nuova il primo "
                "giorno, con la differenza che questa se lo rilegge prima di "
                "ogni singola chiamata.",
                "Il tuo puoi leggerlo quando vuoi. Ogni modifica resta "
                "registrata con la sua data, così «da quando dice questa "
                "cosa?» diventa una domanda che ha una risposta.",
            ],
        ),
        dict(
            eyebrow="02 · NIENTE VA ONLINE PER SBAGLIO",
            h2="Prima in bozza. Poi la senti. Poi pubblichi.",
            h2_in_col=True,
            flip=True,
            viz="RELEASE_FLOW",
            body=[
                "Le modifiche restano in bozza finché qualcuno non le pubblica. "
                "Prima puoi chiamare la bozza e sentirtela gestire proprio il "
                "caso che ti preoccupa: è una prova molto più seria che "
                "rileggere le istruzioni e sperare.",
                "Quello che sta per uscire è elencato prima di uscire, e ogni "
                "versione resta. Se un cambiamento peggiora le cose, quella di "
                "prima è ancora lì.",
            ],
        ),
    ],

    # Non un elenco di funzionalità: la sequenza che il cliente attraversa
    # davvero, con l'unico passo che tocca a lui messo in evidenza. Tre su
    # quattro sono nostri, e quella proporzione È l'argomento.
    hands=dict(
        eyebrow="SERVIZIO COMPLETO",
        h2="Da te ci serve solo[br]quello che già sai.",
        lede="Quattro passaggi dalla prima chiacchierata a un agente che "
             "risponde a chiamate vere. Tre sono nostri. Lo strumento non devi "
             "aprirlo mai.",
        step_word="PASSO",
        steps=[
            ("talk", "Ci racconti come deve andare",
             "Una sessione. Come vuoi che si parli ai tuoi clienti, cosa non si "
             "promette mai, e le risposte che stanno solo nella testa del tuo "
             "team.", True),
            ("build", "Lo costruiamo noi, tutto",
             "Le istruzioni, gli strumenti, il collegamento al catalogo e al "
             "gestionale ordini. Il tuo team tecnico può guardare ogni pezzo: "
             "solo, non gli chiediamo uno sprint.", False),
            ("hear", "Lo senti tu, prima di tutti",
             "Ti chiamiamo con la bozza e te la senti gestire i casi che ti "
             "preoccupano. Online ci va quando lo dici tu.", False),
            ("run", "Lo teniamo acceso e aggiornato",
             "Prodotti nuovi, prezzi nuovi, casi nuovi. Resta giusto mentre il "
             "catalogo si muove - e ogni chiamata te la trovi trascritta.",
             False),
        ],
    ),

    faq_h2="Le domande che ci fanno davvero",
    faq=[
        ("Dobbiamo costruircelo noi l'agente?",
         "No. Questo è lo strumento con cui lo costruiamo noi. Tu hai un "
         "accesso e puoi leggere tutto - istruzioni, strumenti, trascrizioni - "
         "ma dalla tua parte non deve configurare niente nessuno. Se poi ti va "
         "di mettere mano a qualche modifica leggera, puoi: è una possibilità, "
         "non un compito."),
        ("Possiamo vedere esattamente cosa gli avete detto di dire?",
         "Sì, tutto, e nella lingua in cui lavora l'agente: non siamo "
         "legati a un elenco di lingue. Sono istruzioni scritte, non una "
         "scatola nera, e ogni modifica resta registrata con la sua data."),
        ("E quando non sa rispondere?",
         "Lo dice e passa la chiamata a una persona del tuo team, con quello "
         "che il cliente ha già raccontato. È fatto per passare la mano invece "
         "di inventare: una risposta sbagliata detta con sicurezza costa molto "
         "più di un trasferimento."),
        ("Può fare qualcosa o sa solo parlare?",
         "Cerca ordini e disponibilità, manda un riepilogo, apre un ticket, "
         "trasferisce la chiamata e scrive com'è andata nei tuoi sistemi "
         "tramite webhook. Cosa può raggiungere lo decidiamo insieme quando lo "
         "costruiamo."),
        ("Il nostro catalogo cambia in continuazione. L'agente resta indietro?",
         "Legge il tuo catalogo, non una copia: prodotti nuovi e cambi di "
         "prezzo ci sono appena vanno online nel tuo store. Le istruzioni le "
         "manteniamo noi, fa parte del servizio."),
        ("Quanto ci vuole prima che risponda a chiamate vere?",
         "Due settimane dalla prima call, sul tuo numero, con il catalogo vero "
         "dietro."),
    ],

    cta=dict(
        hand="online in due settimane",
        h2="Portaci una chiamata che ricevete di continuo.",
        sub="Dicci qual è la chiamata che il tuo team non ne può più di "
            "prendere, e ti facciamo vedere l'agente che la prende al posto "
            "suo. Senza slide.",
    ),
)


# ---------------------------------------------------------------------------
# 2. WORKFLOW BUILDER
#
# La linea netta fra questa pagina e il Voice Agent Builder: quella è cosa fa
# l'agente MENTRE il cliente è al telefono, questa è cosa succede DOPO che ha
# riagganciato. Tenere separate le due cose è il motivo per cui esistono due
# pagine invece di una lunghissima.
#
# Attenzione ai calchi, come sempre: "post-call" non si traduce "post-chiamata"
# in una frase parlata - si dice "dopo la chiamata". E "gestionale" è la parola
# italiana per il sistema ordini, non "sistema di gestione ordini".
# ---------------------------------------------------------------------------
WORKFLOW_BUILDER_IT = dict(
    slug="workflow-builder",
    en="workflow-builder",
    chip="Workflow Builder",

    title="Workflow Builder | Sabato AI",
    description="Cosa succede dopo che il cliente ha riagganciato: la chiamata "
                "viene letta, i dati estratti, i tuoi sistemi aggiornati. "
                "Nessuno scrive niente a mano. Online in due settimane.",

    h1="La chiamata finisce.[br]Il lavoro comincia.",
    sub="Quasi tutti i centralini si fermano quando cade la linea. È lì che "
        "comincia il lavoro vero: la nota, il messaggio, il ticket, il campo "
        "che qualcuno deve aggiornare. Nel Workflow Builder quel lavoro smette "
        "di essere il compito di qualcuno.",

    hero_visual="",

    shot=dict(
        src="/product/assets/workflow-builder",
        alt="Il canvas dei workflow dopo la chiamata: un trigger a fine "
            "chiamata che si dirama in lettura della chiamata, verifica del "
            "consenso, invio del riepilogo WhatsApp, scrittura sul CRM e "
            "segnalazione di un problema.",
        caption="Il workflow di uno store dopo la chiamata. Tutto quello che "
                "vedi qui parte nei secondi dopo che il cliente ha "
                "riagganciato.",
    ),

    pair_kind="workflow",
    pair=dict(
        eyebrow="DOPO LA CHIAMATA",
        h2="Non lo scrive nessuno.[br]È già fatto.",
        lede="Appena la chiamata finisce, l'agente la passa a un workflow. La "
             "chiamata viene letta, le condizioni verificate, e ogni sistema "
             "che deve saperlo lo sa - prima che il tuo team avesse finito di "
             "scrivere la prima nota.",
    ),

    group=dict(
        eyebrow="COM'È FATTO UN WORKFLOW",
        h2="Legge la chiamata.[br]Poi agisce.",
    ),

    blocks=[
        dict(
            eyebrow="01 · COSA LEGGE",
            h2="Un riassunto non serve.[br]Le etichette sì.",
            h2_in_col=True,
            viz="LABELS_VIZ",
            body=[
                "Un paragrafo del tipo «ecco com'è andata la chiamata» non si "
                "filtra, non si conta e non ci fai niente. Quindi ogni "
                "conversazione viene etichettata: la categoria di prodotto, "
                "cosa ha chiesto davvero, se ha già comprato, quanto vale, da "
                "che paese sta chiamando.",
                "Su quelle etichette si dirama tutto quello che viene dopo. E "
                "sono quelle che a fine mese ti fanno chiedere quale categoria "
                "ha generato più chiamate e quante hanno venduto.",
            ],
        ),
        dict(
            eyebrow="02 · COSA FA",
            h2="Chiamate diverse meritano finali diversi.",
            h2_in_col=True,
            flip=True,
            viz="BRANCH_VIZ",
            body=[
                "Una chiamata andata bene e una andata male non possono avere "
                "lo stesso seguito. Decidono le etichette. Un cliente VIP che "
                "chiede una fornitura fa arrivare un SMS all'account manager "
                "prima ancora che abbia riposato il telefono; un'escalation "
                "finisce riassunta al responsabile assistenza con la "
                "trascrizione allegata; ticket e CRM si aggiornano comunque.",
                "Aggiungere un ramo è una modifica come le altre: resta in "
                "bozza, la provi su una chiamata vera, e va online quando "
                "pubblichi.",
            ],
        ),
    ],

    hands=dict(
        eyebrow="SERVIZIO COMPLETO",
        h2="Tu dici cosa deve succedere.[br]Lo colleghiamo noi.",
        lede="Quattro passaggi dalla prima chiacchierata a un workflow che gira "
             "dopo ogni chiamata. Tre sono nostri. Lo strumento non devi "
             "aprirlo mai.",
        step_word="PASSO",
        steps=[
            ("talk", "Ci dici cosa deve succedere",
             "Cosa fa oggi il tuo team dopo una chiamata, e quali di quelle "
             "cose devono smettere di essere il compito di qualcuno. Quella "
             "lista è tutto il briefing.", True),
            ("wire", "Lo colleghiamo ai tuoi sistemi",
             "CRM, helpdesk, messaggistica, gestionale ordini. Con quello che "
             "espongono: API, webhook, un export. I tuoi sviluppatori "
             "autorizzano gli accessi, il resto lo facciamo noi.", False),
            ("trial", "Lo provi su una chiamata vera",
             "Facciamo girare il workflow su una chiamata già avvenuta e ti "
             "facciamo vedere esattamente cosa ha scritto e dove. Online ci va "
             "quando pubblichi tu.", False),
            ("run", "Poi gira su ogni chiamata",
             "In silenzio, in pochi secondi, e ogni esecuzione resta "
             "registrata: se qualcosa non torna, vedi quale passaggio l'ha "
             "fatto.", False),
        ],
    ),

    faq_h2="Le domande che ci fanno davvero",
    faq=[
        ("A cosa si collega, in concreto?",
         "A qualsiasi cosa abbia un'API o un webhook, che è quasi tutto: "
         "Shopify, il tuo helpdesk, il CRM, WhatsApp, un foglio Google se il "
         "lavoro vive davvero lì. Se un sistema non ha un'API te lo diciamo, "
         "invece di far finta di niente."),
        ("E se il workflow fa la cosa sbagliata?",
         "Ogni esecuzione resta registrata passaggio per passaggio, quindi vedi "
         "cosa è partito e cosa ha scritto. Le modifiche seguono la stessa "
         "strada dell'agente - bozza, prova, pubblicazione - così una modifica "
         "sbagliata si becca prima che arrivi a un cliente, non dopo."),
        ("Può comportarsi diversamente a seconda della chiamata?",
         "È esattamente il punto. Le condizioni leggono i campi estratti dalla "
         "conversazione - cosa hanno chiesto, com'è finita, se hanno dato il "
         "consenso, quanto valgono - e ogni ramo fa una cosa diversa."),
        ("Dobbiamo costruirceli noi questi workflow?",
         "No. Tu ci dici cosa deve succedere dopo una chiamata e lo costruiamo "
         "noi. Hai un accesso e puoi guardare ogni esecuzione, ma non c'è "
         "niente che devi configurare."),
        ("Quanto ci mette a partire?",
         "Pochi secondi dalla fine della chiamata. Chi ha accettato il "
         "riepilogo di solito ce l'ha prima di aver riposato il telefono."),
        ("Che fine fanno registrazione e trascrizione?",
         "Restano legate alla conversazione: le apri, le leggi o le esporti "
         "quando vuoi."),
    ],

    cta=dict(
        hand="online in due settimane",
        h2="Cosa fa il tuo team dopo una chiamata?",
        sub="Qualunque sia la risposta, è probabilmente una lista. Mandacela e "
            "ti diciamo quali pezzi smettono di essere il compito di qualcuno.",
    ),
)


# ---------------------------------------------------------------------------
# 3. CALL DATA INTELLIGENCE
#
# L'angolo: il telefono è l'unico posto dove un cliente ti dice, con parole sue,
# cosa voleva e non ha trovato. La barra di ricerca mostra cosa ha scritto; il
# telefono mostra cosa intendeva.
#
# Calchi evitati: "research panel" non si dice "pannello di ricerca" (è una
# ricerca di mercato); "insight" resta inglese solo se serve, ma qui non serve.
# ---------------------------------------------------------------------------
CALL_DATA_INTELLIGENCE_IT = dict(
    slug="call-data-intelligence",
    en="call-data-intelligence",
    chip="Call Data Intelligence",
    pair_kind="insight",

    title="Call Data Intelligence | Sabato AI",
    description="Ogni chiamata letta, etichettata e contata. Scopri quali "
                "domande tornano sempre, quali prodotti confondono e cosa manca "
                "al catalogo. Online in due settimane.",

    h1="I clienti te l'hanno[br]già detto.",
    sub="La barra di ricerca ti dice cosa hanno scritto. Il telefono ti dice "
        "cosa intendevano - ed è l'unico posto dove te lo dicono in frasi "
        "intere. Call Data Intelligence è dove mille di quelle conversazioni "
        "diventano qualcosa su cui puoi agire.",

    hero_visual="",

    shot=dict(
        src="/product/assets/call-data-intelligence",
        alt="La vista conversazioni di Sabato: i filtri per etichetta in alto, "
            "una riga di numeri chiave e la classifica di quello per cui i "
            "clienti hanno chiamato, con dietro le singole chiamate.",
        caption="Filtrato su una categoria e un livello di cliente. La "
                "classifica è quello che quei 412 hanno chiesto davvero.",
    ),

    pair=dict(
        eyebrow="COM'È FATTO",
        h2="Ogni chiamata contata.[br]Ogni conto verificabile.",
        lede="Filtri per categoria, per cosa hanno chiesto, per chi ha già "
             "comprato, per paese. La classifica si aggiorna. E qualsiasi "
             "numero si apre sulle chiamate da cui viene, così nessuno deve "
             "crederti sulla parola.",
    ),

    group=dict(
        eyebrow="QUELLO CHE IL TELEFONO SA",
        h2="Chiedigli quello che vuoi.[br]Ha ascoltato tutto.",
    ),

    blocks=[
        dict(
            eyebrow="01 · LE DOMANDE",
            h2="Non ti è mai servita una ricerca di mercato.",
            h2_in_col=True,
            viz="QUESTIONS_VIZ",
            body=[
                "Ci sono aziende che pagano agenzie per chiedere ai clienti "
                "cosa non gli è chiaro. Tu hai centinaia di clienti al mese che "
                "te lo raccontano al telefono, spontaneamente, con parole loro - "
                "e fino a ieri non finiva scritto da nessuna parte dove potessi "
                "contarlo.",
                "Adesso sì. Non come una pila di registrazioni che non aprirà "
                "nessuno, ma come etichette che filtri e totali che ordini.",
            ],
        ),
        dict(
            eyebrow="02 · COSA CI FAI",
            h2="Un numero su cui non agisci è una curiosità.",
            h2_in_col=True,
            flip=True,
            viz="ACTIONS_VIZ",
            body=[
                "Centotrentaquattro persone che chiamano per sapere che modello "
                "serve per la loro stanza non sono una statistica interessante. "
                "Sono un paragrafo che manca su una scheda prodotto, una taglia "
                "che finisce sempre, e una domanda che il tuo agente dovrebbe "
                "già gestire prima che qualcuno alzi la cornetta.",
                "Misurare il telefono non serve per avere una dashboard. Serve "
                "per le quattro o cinque cose che ogni mese cambi grazie a "
                "quello che leggi lì.",
            ],
        ),
    ],

    hands=dict(
        eyebrow="SERVIZIO COMPLETO",
        h2="Nessun analista.[br]Nessun export. Nessuna attesa.",
        lede="Quattro passaggi dalla prima chiacchierata a numeri di cui ti "
             "fidi. Tre sono nostri. Lo strumento non devi aprirlo mai.",
        step_word="PASSO",
        steps=[
            ("talk", "Ci dici cosa vuoi sapere",
             "Le domande che faresti se una persona ascoltasse tutte le "
             "chiamate. Quelle diventano le etichette.", True),
            ("label", "Le etichette le impostiamo noi",
             "Categorie che rispecchiano il tuo catalogo, livelli che "
             "rispecchiano i tuoi clienti, e tutto il resto che vuoi contare. "
             "Non una tassonomia generica appiccicata sopra.", False),
            ("verify", "Le verifichi su chiamate vere",
             "Ti facciamo vedere le etichette su chiamate già avvenute, così "
             "controlli che siano giuste prima che qualcuno ci costruisca un "
             "report sopra.", False),
            ("count", "Poi conta tutto, per sempre",
             "Ogni chiamata da quel giorno in poi, etichettata allo stesso "
             "modo: così il confronto mese su mese vuol dire qualcosa.", False),
        ],
    ),

    faq_h2="Le domande che ci fanno davvero",
    faq=[
        ("È solo registrazione delle chiamate con una ricerca sopra?",
         "No. Le registrazioni sono un pagliaio: cento ore che non ascolterà "
         "mai nessuno. Qui ogni chiamata viene letta dentro etichette che "
         "filtri e conti, e da qualsiasi numero apri le chiamate che ci stanno "
         "dietro. La registrazione è la prova, non il prodotto."),
        ("Analizzate come si sentiva il cliente?",
         "No, ed è una scelta. Indovinare l’umore di una persona dalla voce "
         "non è una cosa su cui vorremmo far prendere decisioni a "
         "un’azienda. Tutto quello che etichettiamo è un fatto della "
         "chiamata: cosa è stato chiesto, di che categoria era, se è stata "
         "risolta."),
        ("I dati possiamo portarceli via?",
         "Sì. Li esporti, oppure te li mandiamo nel tuo data warehouse o nel "
         "tuo sistema di reportistica via webhook. Sono dati tuoi sui tuoi "
         "clienti: tenerli in ostaggio sarebbe un modo strano di farsi "
         "rinnovare."),
        ("Da quanto indietro parte?",
         "Dal giorno in cui l'agente va online. Non c'è modo di etichettare "
         "chiamate che nessuno ha mai registrato, quindi prima parte e prima "
         "esiste un confronto mese su mese."),
        ("Chi può vedere le trascrizioni?",
         "Chi dici tu. Gli accessi sono per persona, e puoi tenere le "
         "trascrizioni aperte a un responsabile lasciando chiuse le "
         "registrazioni."),
        ("Funziona anche se la maggior parte delle chiamate le prendiamo noi?",
         "Sì: l'agente etichetta quelle che gestisce, e anche quelle che passa "
         "al tuo team restano etichettate fino al momento del trasferimento. "
         "Non serve automatizzare tutto per misurare tutto."),
    ],

    cta=dict(
        hand="online in due settimane",
        h2="Qual è la domanda a cui non sai rispondere?",
        sub="Quasi tutti ne hanno una: perché abbandonano, cosa chiedono prima "
            "di comprare, quale prodotto confonde chiunque. Probabilmente la "
            "risposta è già sul tuo telefono.",
    ),
)

AGENT_EVALUATION_IT = dict(
    slug="agent-evaluation",
    en="agent-evaluation",
    chip="Agent Evaluation",
    pair_kind="review",

    title="Agent Evaluation | Sabato AI",
    description="Ogni chiamata rivista, ogni lacuna scritta, ogni modifica al "
                "prompt versionata. La parte che nessuno mostra in demo, e che "
                "è quasi tutto il lavoro. Online in due settimane.",

    h1="La demo è il 5%.[br]Noi facciamo il 95.",
    sub="Qualsiasi fornitore di voice AI ti fa vedere un agente che parla. "
        "Quella parte si fa in un weekend. Il novantacinque per cento restante "
        "è sapere che alla diecimillesima chiamata dice ancora la cosa "
        "giusta, accorgersene il giorno in cui smette, e poterlo dimostrare. "
        "Quella metà non te la vende quasi nessuno, perché in demo non si "
        "vede.",

    hero_visual="",

    shot=dict(
        src="/product/assets/agent-evaluation",
        alt="La bacheca dei problemi di Sabato: le lacune trovate in revisione "
            "- una regola che nessuno ha scritto, dati prodotto che si "
            "contraddicono, una policy che esiste in due versioni - ognuna con "
            "il numero di chiamate da cui è saltata fuori.",
        caption="Una settimana normale. Quasi tutto quello che la revisione "
                "trova è conoscenza che manca, non un agente rotto.",
    ),

    pair=dict(
        eyebrow="LA PARTE CHE NESSUNO TI MOSTRA",
        h2="Una lacuna, e la correzione[br]che l’ha chiusa.",
        lede="Ecco com’è fatto davvero il lavoro. Dodici clienti hanno "
             "descritto una stanza più grande di qualsiasi cosa ci fosse nei "
             "dati prodotto: abbiamo chiesto la tabella di copertura, scritto la "
             "regola su quella, provata su quelle dodici chiamate e pubblicata "
             "entro l’ora. La versione precedente è ancora lì.",
    ),

    group=dict(
        eyebrow="COME LO TENIAMO ONESTO",
        h2="Rivisto ogni giorno.[br]Riscritto ogni settimana.",
    ),

    blocks=[
        dict(
            eyebrow="01 · RIVEDIAMO OGNI CHIAMATA",
            h2="Due su cento era un budget, non uno standard.",
            h2_in_col=True,
            viz="REVIEW_VIZ",
            body=[
                "Il controllo qualità su un team al telefono vuol dire che "
                "qualcuno ascolta due chiamate su cento e spera fossero "
                "rappresentative. Quel numero non l’ha scelto nessuno perché "
                "fosse rigoroso: l’hanno scelto perché ascoltare costa un’ora "
                "di una persona.",
                "Adesso non più. Ogni chiamata viene letta contro quello che "
                "per te è una chiamata fatta bene, e quello che ne esce non è "
                "un punteggio in un foglio: è un elenco di lacune precise - "
                "una regola che nessuno ha scritto, un prodotto che nessuno ha "
                "descritto, una policy che esiste in due versioni - ognuna con "
                "quante volte è saltata fuori.",
            ],
        ),
        dict(
            eyebrow="02 · IL PROMPT È VIVO",
            h2="Non è un file scritto una volta e basta.",
            h2_in_col=True,
            viz="LIVING_VIZ",
            flip=True,
            body=[
                "Le istruzioni dietro al tuo agente cambiano quasi ogni "
                "settimana, perché le chiamate vere continuano a tirare fuori "
                "cose che nessuno aveva previsto. Uno chiede di parlare con una "
                "persona in un modo che le regole non contemplavano. Una frase "
                "cade male su una linea disturbata.",
                "Ognuna di quelle modifiche è scritta, versionata e "
                "riconducibile alla chiamata che l’ha causata, e qualsiasi "
                "versione si può rimettere. Un agente che al sesto mese è "
                "identico al primo giorno vuol dire che non se n’è occupato "
                "nessuno.",
            ],
        ),
    ],

    hands=dict(
        eyebrow="COMPLETAMENTE GESTITO",
        h2="Questo è il lavoro[br]che stai comprando.",
        lede="Non una dashboard da guardare. Un ciclo che portiamo avanti noi, "
             "sul tuo agente, ogni settimana - e puoi leggerlo tutto.",
        step_word="PASSO",
        steps=[
            ("standard", "Definisci tu cos’è una chiamata fatta bene",
             "Cosa deve succedere sempre, cosa non si dice mai, quando deve "
             "subentrare una persona. Quello diventa lo standard su cui si "
             "rivede tutto.", True),
            ("review", "Rivediamo, tutti i giorni",
             "Non a campione. Gli errori li scriviamo come cose precise e "
             "contabili, non come un punteggio di qualità su cui non ci fai "
             "niente.", False),
            ("fix", "Correggiamo e pubblichiamo",
             "Scritto sulla regola esatta che ha fallito, provato su chiamate "
             "già avvenute e pubblicato: di solito lo stesso giorno.", False),
            ("read", "E puoi leggere tutto",
             "Ogni problema, ogni correzione, ogni versione del prompt e cosa è "
             "cambiato in mezzo. Comprese quelle che abbiamo aperto su di "
             "noi.", False),
        ],
    ),

    faq_h2="Le domande che fanno davvero",
    faq=[
        ("Chi decide cos’è una chiamata fatta bene?",
         "Lo decidi tu, e noi lo mettiamo per iscritto così si può anche "
         "contestare. È la tua policy - cosa si deve dire, cosa non si "
         "promette mai, quando subentra una persona - non un modello di "
         "qualità generico con dentro le nostre opinioni."),
        ("Non è che vi date i voti da soli?",
         "In parte sì, e far finta di no sarebbe offensivo. Quello che lo "
         "rende verificabile è che lo standard è tuo, che ogni problema e "
         "ogni correzione li vedi con la trascrizione allegata, e che lo "
         "storico mostra esattamente cosa è cambiato e quando. Puoi non "
         "essere d’accordo su una chiamata che abbiamo dato per buona."),
        ("Quanto ci mette una cosa a essere corretta davvero?",
         "Di solito lo stesso giorno in cui salta fuori. L’esempio in questa "
         "pagina è passato dal momento in cui uno ha visto lo schema alla "
         "pubblicazione in quaranta minuti, e quasi tutto quel tempo è "
         "servito a provare la modifica sulle chiamate da cui veniva."),
        ("Cosa impedisce che una correzione ne rompa un’altra?",
         "Le modifiche si provano su chiamate già avvenute prima di "
         "avvicinarsi a un cliente, e restano in bozza finché non le "
         "pubblichi. Se una peggiora le cose, la versione precedente è "
         "ancora lì e torna dentro con un clic."),
        ("Dobbiamo farlo noi qualcosa di tutto questo?",
         "No. Puoi leggere ogni problema e ogni correzione, e c’è chi vuole "
         "farci sopra un giro ogni settimana. Altri non lo aprono mai. Vanno "
         "bene entrambe: il lavoro succede comunque."),
        ("Costa a parte?",
         "No. È il modo in cui la cosa resta funzionante. Fartelo pagare a "
         "parte vorrebbe dire farti pagare il nostro controllo qualità."),
    ],

    cta=dict(
        hand="online in due settimane",
        h2="Chiedici cosa succede alla diecimillesima chiamata.",
        sub="È la domanda che vorremmo ci facessero se fossimo noi a comprare. "
            "Falla a noi, e falla a chiunque altro stai sentendo.",
    ),
)

# ---------------------------------------------------------------------------
# Italiano localizzato, non tradotto. Due trappole già cadute una volta su
# questo sito: i calchi ("sotto il cofano" non esiste, si dice "dietro le
# quinte") e gli accenti scritti con l’apostrofo.
# ---------------------------------------------------------------------------
INTEGRATIONS_WEBHOOKS_IT = dict(
    slug="integrations-webhooks",
    en="integrations-webhooks",
    chip="Integrazioni & Webhook",
    pair_kind="connect",

    title="Integrazioni & Webhook | Sabato AI",
    description="L’agente legge il tuo gestionale, il catalogo e il CRM "
                "mentre il cliente è ancora in linea, e scrive dopo. Nativo con "
                "Shopify, 8.500+ app via Zapier. Online in due settimane.",

    h1="Il tuo agente si collega[br]a tutto quello che già usi.",
    sub="Un agente vocale da solo sa solo dire con gentilezza che non lo sa. Il "
        "nostro non lavora da solo: legge il gestionale, il catalogo e la "
        "scheda del cliente mentre la persona è ancora al telefono, e quando la "
        "chiamata finisce scrive nel tuo CRM, nel tuo helpdesk e nel tuo store. "
        "Nativo con Shopify, e 8.500+ app via Zapier.",

    hero_visual="",

    shot=dict(
        src="/product/assets/integrations-webhooks",
        alt="Il flusso post-chiamata di Sabato: finisce una chiamata e partono "
            "quattro passaggi - il lead nel CRM, l’ordine aggiornato in modo "
            "nativo su Shopify, 8.500+ app via Zapier e un webhook firmato "
            "verso i tuoi sistemi - con sotto il registro delle esecuzioni.",
        caption="Finisce una chiamata. Succedono quattro cose, in quattro "
                "strumenti diversi, prima che qualcuno apra il computer.",
    ),

    pair=dict(
        eyebrow="COSA VUOL DIRE DAVVERO “INTEGRATO”",
        h2="Legge durante la chiamata.[br]Scrive dopo.",
        lede="Quasi sempre “integrato” vuol dire un export notturno e una "
             "dashboard. Va benissimo per un report ed è inutile al telefono, "
             "perché il cliente sta chiedendo dell’ordine che ha fatto "
             "quaranta minuti fa. Tutto quello che l’agente dice viene letto "
             "nel momento in cui lo dice, e tutto quello che fa dopo succede "
             "nei sistemi dove il tuo team lavora già.",
    ),

    group=dict(
        eyebrow="COSA TOCCA",
        h2="Legge quello che serve.[br]Scrive dove lavori tu.",
    ),

    blocks=[
        dict(
            eyebrow="01 · COSA PUÒ LEGGERE",
            h2="La risposta è già in un tuo sistema.",
            h2_in_col=True,
            viz="READS_VIZ",
            body=[
                "Quasi tutte le domande per cui un cliente chiama hanno una "
                "risposta dentro un software che paghi già. Dov’è il mio "
                "ordine. C’è la mia taglia. È arrivato il reso. Cosa avevo "
                "preso l’altra volta. Quanto costa con il mio sconto "
                "rivenditore. Non sono domande difficili: sono difficili solo "
                "perché chi potrebbe guardare è già al telefono con "
                "qualcun altro.",
                "L’agente ha accesso in lettura ai campi che gli servono e a "
                "nient’altro, e li legge nel momento in cui risponde. Quindi "
                "quello che dice è vero quando lo dice, non vero alle tre di "
                "notte quando è girato l’export.",
            ],
        ),
        dict(
            eyebrow="02 · COSA CI FA",
            h2="Poi fa il lavoro, dove il lavoro si fa.",
            h2_in_col=True,
            viz="WRITES_VIZ",
            flip=True,
            body=[
                "Leggere è metà. L’altra metà è che dopo nessuno deve "
                "ribattere la chiamata a mano. Il lead arriva nel CRM con "
                "quello che si sono detti davvero. Il ticket si apre "
                "nell’helpdesk con il numero d’ordine già dentro. Il "
                "cliente riceve il link di tracking via SMS prima di "
                "riattaccare. E l’account manager scopre che ha appena "
                "chiamato un’opportunità da quattordicimila euro.",
                "Lavoriamo con quello che riesci a esporre: un’API, un "
                "webhook, un file notturno, o un portale in cui entriamo come "
                "farebbe una persona.",
            ],
        ),
        dict(
            eyebrow="03 · A COSA SI COLLEGA",
            h2="Nativo con Shopify.[br]Tutto il resto via Zapier.",
            h2_in_col=True,
            viz="CONNECT_VIZ",
            body=[
                "Con Shopify è nativo. L’agente legge l’ordine, la "
                "disponibilità e cosa aveva comprato l’altra volta "
                "direttamente dal tuo store, e ci riscrive dentro la nota, il "
                "tag e l’ordine in bozza. Nessuno strato in mezzo e niente da "
                "mantenere per te.",
                "Tutto il resto che già usi - helpdesk, CRM, email, fogli, "
                "agenda, WhatsApp - si collega via Zapier, che sono 8.500+ app. "
                "Se non c’è, è un webhook: un pomeriggio di lavoro, non un "
                "progetto.",
            ],
        ),
    ],

    hands=dict(
        eyebrow="COMPLETAMENTE GESTITO",
        h2="La parte tecnica la facciamo noi.[br]La tua roadmap resta tua.",
        lede="Quattro passi dalla prima chiamata a un agente che legge i tuoi "
             "dati veri. Tre sono nostri, e a nessuno serve uno sprint del tuo "
             "team.",
        step_word="PASSO",
        steps=[
            ("standard", "Ci dici cosa deve vedere",
             "Quali sistemi hanno le risposte e chi li tiene in mano. Una "
             "chiamata con chi lo sa, o una login.", True),
            ("wire", "Lo colleghiamo noi",
             "API, webhook, file notturno, o un portale in cui entriamo. "
             "Credenziali, mappatura e casi strani li gestiamo noi.", False),
            ("trial", "Lo guardi leggere una scheda vera",
             "Lo facciamo girare su un ordine vero e ti mostriamo cosa ha visto "
             "e cosa no. Online ci va quando lo dici tu.", False),
            ("run", "Lo teniamo collegato",
             "I sistemi cambiano, i token scadono, i campi si rinominano. "
             "Quando si rompe qualcosa lo vediamo noi e lo sistemiamo prima che "
             "ti costi una chiamata.", False),
        ],
    ),

    faq_h2="Le domande che fanno davvero",
    faq=[
        ("E se il nostro gestionale non ha API?",
         "Allora usiamo quello che ha: un export notturno, una vista sul "
         "database, o un portale in cui entriamo come ci entra il tuo team. Ci "
         "vuole più tempo e funziona. Due delle connessioni dietro la "
         "schermata qui sopra sono esattamente questo."),
        ("Quanto ci mette l’integrazione?",
         "Giorni, non un trimestre, perché il lavoro è nostro. La parte "
         "lunga non è quasi mai il software: è farsi dare le credenziali "
         "da chi tiene in mano il sistema."),
        ("Legge i dati veri o una copia?",
         "I dati veri. L’agente interroga il tuo sistema nel momento in cui "
         "risponde, quindi quello che dice al cliente è vero quando lo dice, "
         "non vero alle tre di notte quando è girato un export. Ogni lettura "
         "e ogni scrittura restano elencate sulla chiamata a cui "
         "appartenevano."),
        ("Cosa succede se una scrittura fallisce?",
         "Riprova. Se continua a fallire diventa un problema aperto con la "
         "chiamata allegata invece di sparire, e vedi ogni tentativo - anche "
         "quelli che ce ne hanno messi due."),
        ("Possiamo mandare i dati delle chiamate nei nostri sistemi?",
         "Sì. call.completed arriva al tuo endpoint con trascrizione, "
         "etichette ed esito, firmato e versionato. Qualcuno lo manda dritto "
         "nella propria reportistica e la nostra interfaccia non la apre mai."),
        ("Quali sistemi supportate?",
         "Con Shopify siamo nativi. Tutto il resto passa da Zapier, che sono "
         "8.500+ app - Zendesk, Salesforce, HubSpot, Klaviyo, Slack, Fogli "
         "Google, WhatsApp e il resto della directory. Quello che non c’è è "
         "un webhook. L’elenco non è davvero il punto: se una persona del "
         "tuo team riesce a tirare fuori la risposta da lì, ci riusciamo "
         "anche noi."),
    ],

    cta=dict(
        hand="online in due settimane",
        h2="Chiedici di leggere un tuo ordine.",
        sub="Non una slide sulle integrazioni: una scheda vera dal tuo sistema, "
            "letta ad alta voce in chiamata, nelle prime due settimane.",
    ),
)

PRODUCTS_IT = {p["slug"]: p for p in [VOICE_AGENT_BUILDER_IT, WORKFLOW_BUILDER_IT,
                                      CALL_DATA_INTELLIGENCE_IT, AGENT_EVALUATION_IT,
                                      INTEGRATIONS_WEBHOOKS_IT]}
ORDER_IT = ["voice-agent-builder", "workflow-builder", "call-data-intelligence",
            "agent-evaluation", "integrations-webhooks"]
