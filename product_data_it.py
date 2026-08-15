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
             "gestionale ordini. Sui tuoi sviluppatori non cade niente, perché "
             "non c'è niente da fare.", False),
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
            h2="Un riassunto non serve. I campi sì.",
            h2_in_col=True,
            viz="SIGNALS_VIZ",
            body=[
                "Un paragrafo del tipo «ecco com'è andata la chiamata» non si "
                "filtra, non si conta e non ci fai niente. Quindi la chiamata "
                "viene letta dentro campi con un nome: cosa ha chiesto davvero, "
                "com'è finita, quanto ne siamo sicuri, com'era il tono, se è "
                "servito coinvolgere qualcuno.",
                "Su quei campi si dirama tutto quello che viene dopo. E sono "
                "gli stessi campi che a fine mese diventano i tuoi numeri.",
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
                "lo stesso seguito. Decidono le condizioni: il riepilogo parte "
                "solo verso chi ha detto di sì, un reclamo finisce davanti a "
                "una persona con la trascrizione allegata, e sul CRM si scrive "
                "in ogni caso.",
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
            ("build", "Lo colleghiamo ai tuoi sistemi",
             "CRM, helpdesk, messaggistica, gestionale ordini. Con quello che "
             "espongono: API, webhook, un export. Ai tuoi sviluppatori non "
             "chiediamo niente.", False),
            ("hear", "Lo provi su una chiamata vera",
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
         "consenso, che tono avevano - e ogni ramo fa una cosa diversa."),
        ("Dobbiamo costruirceli noi questi workflow?",
         "No. Tu ci dici cosa deve succedere dopo una chiamata e lo costruiamo "
         "noi. Hai un accesso e puoi guardare ogni esecuzione, ma non c'è "
         "niente che devi configurare."),
        ("Quanto ci mette a partire?",
         "Pochi secondi dalla fine della chiamata. Chi ha accettato il "
         "riepilogo di solito ce l'ha prima di aver riposato il telefono."),
        ("Che fine fanno registrazione e trascrizione?",
         "Restano legate alla conversazione e sono a tua disposizione. La "
         "conservazione la imposta la tua policy, non la nostra."),
    ],

    cta=dict(
        hand="online in due settimane",
        h2="Cosa fa il tuo team dopo una chiamata?",
        sub="Qualunque sia la risposta, è probabilmente una lista. Mandacela e "
            "ti diciamo quali pezzi smettono di essere il compito di qualcuno.",
    ),
)

PRODUCTS_IT = {p["slug"]: p for p in [VOICE_AGENT_BUILDER_IT, WORKFLOW_BUILDER_IT]}
ORDER_IT = ["voice-agent-builder", "workflow-builder"]
