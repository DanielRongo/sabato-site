---
title: "La conversazione umana viaggia su un orologio da 208 millisecondi. Il tuo voice agent no."
seo_title: "Come misurare la latenza del tuo voice agent | Sabato AI"
slug: measure-your-voice-agent-latency
description: "Il gap umano tra un turno e l'altro è di +208 ms su 10 lingue. Non esiste un benchmark verificato per i voice agent commerciali: ecco il protocollo per misurare p50 e p90 sulla tua linea, in un pomeriggio."
category: Operations
date: 2026-08-08
cover_style: offwhite
---

Su 10 lingue e 101 conversazioni naturali, il gap medio tra chi smette di parlare e chi comincia è di +208 millisecondi, e il gap più frequente in assoluto è zero ([Stivers et al., PNAS, 2009](https://www.pnas.org/doi/full/10.1073/pnas.0903616106)). Quasi nessuno, valutando un voice agent, ha mai messo un cronometro su quel gap sulla propria linea.

Chi compra testa due cose. Capisce i miei codici articolo, i miei accenti, i miei clienti. Sembra una persona. Domande legittime, entrambe, ed entrambe hanno risposta dentro una demo da cinque minuti.

Il gap non trova risposta, e il gap è ciò a cui il tuo cliente reagisce.

Il protocollo è in fondo a questo post: p50 e p90, misurati dalla fine del parlato del chiamante all'inizio del parlato dell'agente, sul tuo percorso di rete, con i tuoi clienti dall'altra parte. Un pomeriggio.

:::keystat
+208 ms
gap medio tra due parlanti su 10 lingue
Fonte: Stivers et al., PNAS, 2009

0 ms
il gap più frequente in assoluto
Fonte: Stivers et al., PNAS, 2009
:::

## Qual è il gap normale tra due parlanti in una conversazione umana?

Su 10 lingue, campionando 350 domande consecutive per lingua da 101 conversazioni naturali, il gap medio tra chi finisce di parlare e chi comincia è di +208 ms, con una mediana complessiva di +100 ms e un gap modale complessivo pari a zero (Stivers et al., PNAS, 2009). Le medie per lingua vanno da +7 ms del giapponese fino a circa +468 ms all'estremo lento. Si tratta di conversazione naturale, non di telefonate commerciali.

Il dato è vecchio. 2009, e lo dico prima che lo dica qualcun altro.

Ecco perché regge ancora, e la distinzione conta più della data. Stivers et al. è linguistica descrittiva fondativa, replicata ampiamente. Non è una statistica di mercato. Le statistiche di mercato si deteriorano perché i mercati si muovono: un dato del 2009 sulle preferenze di canale o sui volumi di contatto oggi non vale nulla. Una misura di come gli esseri umani sincronizzano i propri turni non si deteriora allo stesso modo, perché ciò che viene misurato è la meccanica del parlato umano, non il comportamento di un mercato. È il test che applicherei a qualsiasi dato datato prima di ripubblicarlo, e questo lo supera.

È la dispersione a rendere il risultato difficile da contestare. Le medie per lingua vanno da +7 ms del giapponese a circa +468 ms all'altro estremo. Persino la lingua più lenta dello studio sta sotto il mezzo secondo. Tutte e dieci rientrano entro circa 250 ms dalla media cross-linguistica: una differenza che il paper descrive come all'incirca il tempo necessario a pronunciare una singola sillaba inglese.

Quindi la finestra non è una preferenza culturale su cui puoi progettare mercato per mercato. È quasi una costante.

Due limiti, detti chiaramente.

Si tratta di conversazione naturale, registrata tra persone che si conoscono, non di chiamate in ingresso a un fornitore per una data di consegna. Nessuno ha misurato i tempi di turno sulle telefonate commerciali. Considera +208 ms come la linea di base umana su cui è stato addestrato l'orecchio di chi ti chiama, non come una specifica per la tua linea.

E la linea di base umana è misurata in modo più generoso rispetto al metro che questo post ti mette in mano. Stivers et al. hanno codificato l'inizio della risposta da video, contando come inizio anche le risposte visive precoci - un cenno del capo - e le inspirazioni udibili che precedono l'enunciato. Il protocollo qui sotto misura da parlato a parlato, perché una linea telefonica non trasporta altro. Quindi il numero umano è semmai leggermente favorito rispetto alla tua misurazione. Non leggere l'intero scarto tra il tuo p50 e i +208 ms come colpa tua.

Se un fornitore ti dice che il suo agente raggiunge il numero umano, sta citando un paper di linguistica sulla conversazione informale faccia a faccia, e dovrebbe dirlo.

## 400 ms è un buon obiettivo per un voice agent?

La Raccomandazione ITU-T G.114 (2003) fissa a 150 ms il ritardo unidirezionale bocca-orecchio sotto il quale l'interattività è sostanzialmente trasparente, e afferma che ritardi superiori a 400 ms "are unacceptable for general network planning purposes" (sono inaccettabili ai fini della pianificazione di rete). Quel budget copre il trasporto dell'audio da una bocca a un orecchio: trasmissione di rete più il codec e il buffering che la rete stessa aggiunge. Non contiene alcun riconoscimento vocale, nessuna inferenza del modello, nessuna interrogazione a database, nessuna sintesi. Per un voice agent è un pavimento, non un obiettivo.

È il numero che il settore ricorda a metà, e viene citato ai buyer con la parola "benchmark" attaccata.

La Raccomandazione ITU-T G.114 (05/2003, tuttora in vigore) è una raccomandazione di pianificazione di rete. Misura il ritardo unidirezionale bocca-orecchio: portare l'audio da una bocca a un orecchio, incluso il codec, la pacchettizzazione e il buffering anti-jitter che la rete stessa aggiunge. Non contiene nulla del lavoro che fa un voice agent. Nessuna attesa di endpointing. Nessun riconoscimento vocale. Nessuna inferenza del modello. Nessuna interrogazione al catalogo o all'ERP. Nessuna sintesi vocale.

Quindi 400 ms non è un obiettivo a cui il tuo agente debba puntare: è la soglia che il settore telecomunicazioni si è data per consegnare l'audio e nient'altro, un pavimento che sta sotto il tuo budget. La rete ha già speso una parte del tuo tempo di risposta prima ancora che il tuo agente inizi a pensare.

Ragionamento nostro, non un risultato di nessuna delle due fonti: se consegnare il solo audio è inaccettabile oltre i 400 ms, allora una risposta totale bocca-orecchio che comprende endpointing, riconoscimento, inferenza, una verifica di giacenza e la sintesi si colloca ben oltre i 208 ms umani. Non a volte. Sempre. Il che significa che la domanda utile smette di essere "possiamo raggiungere il numero umano" e diventa "dove sta finendo esattamente il nostro tempo, e su quale stadio interveniamo".

Chiunque, in prima pagina su Google, afferma una soglia: 300 ms, 200-500 ms, scegline una. Sono andato a cercare lo studio dietro il dato dei 300 ms. Non l'ho trovato: ogni pista che ho seguito finiva su un altro articolo che affermava lo stesso numero, oppure su nulla. Questo non prova che tale studio non esista. Dice che nessuno di quelli che citano il numero ne cita uno. Entrambi i numeri di questo post risalgono a una fonte primaria, e nessuno dei due è un benchmark per la voice AI.

## Perché una demo non può mostrartelo

Comprensione e naturalezza sono le cose giuste da testare. Sono anche le uniche due che una demo può testare, e questo è strutturale, non un complotto.

Le demo sono brevi e a turno singolo. La latenza si accumula lungo una vera chiamata da quindici turni, e il turno che ti uccide è l'undicesimo, non il primo.

Le demo girano sul percorso di rete del fornitore, di solito dal paese del fornitore, di solito a metà mattina di un giorno feriale. I tuoi clienti sono su un altro operatore, in un altro paese, alle 16:50 di venerdì. E le domande da demo non attivano quasi mai una verifica live di giacenza, prezzo o data di consegna: esattamente i turni in cui il numero esplode, e i turni che decidono se la chiamata converte.

In una demo, il silenzio lo riempi tu. Dirai "mm" o "certo" dentro un vuoto di due secondi senza accorgertene, perché sei una persona educata al telefono con un venditore. Un cliente che oggi è già stato in attesa una volta non lo fa. Dice "pronto?" e poi parla sopra all'agente.

La naturalezza si valuta in secondi. La latenza vive nei millisecondi. Il formato è cieco a tutto questo.

## Perché il numero di latenza che ti hanno dato non è quello che sente chi ti chiama

Misura la latenza dall'ultima parola del chiamante, non dal momento in cui il tuo sistema decide che il chiamante ha smesso. Tra questi due punti c'è l'attesa di endpointing - la soglia di silenzio che un voice agent usa per rilevare la fine del turno - ed è spesso il singolo blocco di ritardo più grande. I dati dei fornitori che partono dopo l'endpointing possono sottostimare l'esperienza del chiamante di centinaia di millisecondi.

Un voice agent non sa che il chiamante ha finito di parlare. Aspetta che il silenzio duri abbastanza a lungo da concludere che il turno è chiuso. Questo è l'endpointing, guidato dalla voice activity detection, e solo quando scatta comincia tutto il resto: riconoscimento, inferenza, lookup, sintesi.

L'orologio del chiamante parte dalla sua ultima parola. Molti dati di latenza citati partono dopo che è scattato l'endpointing. La differenza tra i due è la soglia di silenzio, ed è spesso il blocco più grande della catena. Due sistemi che dichiarano entrambi "500 ms" possono distare un secondo dal posto di chi chiama.

:::quote
Il vostro dato di latenza parte dall'ultima parola del chiamante o da quando scatta il vostro endpointing?
:::

Non è una domanda trabocchetto, e non va posta come tale, perché sotto c'è un compromesso reale. Accorci la soglia di silenzio per sembrare più veloce e aumenti le false interruzioni: l'agente che parla sopra a un chiamante che stava ancora pensando. È un fallimento peggiore dell'attesa, perché costringe il cliente a ripetersi e fa sembrare che l'agente non stia ascoltando.

La prova che questo compromesso è inevitabile arriva dalla ricerca sui turni conversazionali, e va accompagnata dai suoi avvertimenti. Su tre corpora europei, il 40,0-41,7% delle transizioni tra parlanti erano sovrapposizioni anziché gap puliti, e solo lo 0,4-0,7% erano passaggi netti senza gap e senza sovrapposizione ([Heldner & Edlund, Journal of Phonetics, 2010](https://staff.fnwi.uva.nl/r.fernandezrovira/teaching/cosp/cosp2016/docs/HeldnerEdlund2010.pdf)). Fonte singola: quella percentuale poggia solo su questo paper. È del 2010. Due dei tre corpora sono dialoghi task-oriented su mappe anziché telefonate commerciali, quindi il corpus portante è lo Spoken Dutch Corpus (321 parlanti, 234 coppie); il sotto-corpus svedese conta appena 8 parlanti. Stivers et al. conferma il quadro generale - gap modale zero, sistematica evitazione dei silenzi lunghi - ma non quella percentuale.

Leggilo per quello che è. I parlanti umani si sovrappongono circa quattro volte su dieci transizioni. Un sistema tarato per attendere un silenzio sicuro sta combattendo contro il modo in cui le persone parlano davvero, e uno tarato per intervenire presto taglierà la parola. Non esiste una taratura che vinca su entrambi i fronti. Il lavoro è sapere da che parte è tarato il tuo, e averlo scelto deliberatamente.

## Come misurare la latenza del tuo voice agent sulla tua linea

Per misurare la latenza di un voice agent: registra chiamate reali in stereo, aprile in un editor di forme d'onda e, per ogni turno, prendi T1 come ultimo campione audio dell'ultima parola del chiamante e T2 come primo campione della risposta dell'agente. La latenza è T2 - T1. Registra almeno 60 turni, suddivisi per tipo, e riporta p50 e p90 separatamente.

Un pomeriggio. Un telefono, un editor di forme d'onda gratuito, un foglio di calcolo. Nessuno sviluppatore.

### Cosa ti serve (circa 20 minuti di preparazione)

Registrazioni delle chiamate con l'audio intatto. Quelle del tuo operatore telefonico di solito vanno bene: verifica che non siano state ridotte a un unico canale mono in modo da sfumare il confine tra chiamante e agente. La registrazione stereo o dual-channel rende tutto molto più semplice: il chiamante finisce su una traccia, l'agente sull'altra, e il passaggio di turno si vede.

Un editor di forme d'onda gratuito che mostri i timestamp in millisecondi. Audacity è la scelta ovvia: imposta la barra di selezione su hh:mm:ss + millisecondi prima di cominciare, altrimenti leggerai secondi con due decimali e discuterai di arrotondamenti. E un foglio di calcolo.

Se non riesci a ottenere registrazioni pulite dal tuo operatore, metti un secondo telefono in vivavoce accanto al primo e registra quello. È abbastanza preciso. Stai cercando differenze di centinaia di millisecondi, non di decine.

### Definisci i due timestamp una volta sola, poi smetti di discuterne

**T1** = l'ultimo campione audio dell'ultima parola del chiamante. Non la fine della finestra di silenzio. Non il punto in cui la trascrizione sostiene che il turno sia finito. La forma d'onda.

**T2** = il primo campione audio della risposta dell'agente. Riempitivi inclusi. Se l'agente dice "verifico subito", quella è la risposta che inizia: segnala, e annota nel log che il turno si è aperto con una frase di attesa, perché servirà più avanti.

**Latenza = T2 - T1.** Un turno, un numero.

Incolla queste tre righe in un tuo documento. Ogni discussione sulla latenza che avrai mai con un fornitore si riduce a quale definizione stia usando ciascuna parte.

### Quanti turni servono prima che p50 e p90 significhino qualcosa

Misura i turni, non le chiamate. Dieci chiamate reali da sei turni fanno 60 turni.

Sii onesto su cosa ti comprano 60 turni, perché nessun altro che scrive di questo lo è: il p50 è ragionevolmente stabile intorno ai 30 turni. Un p90 su 60 turni è il sesto turno più lento che ti è capitato di registrare. È indicativo, non una metrica. Per un p90 da mettere davanti a un fornitore e difendere, punta a 100+ turni.

Non usare la media per niente. Il senso di tutto l'esercizio è la coda.

### Suddividi i turni in quattro tipi prima di fare qualsiasi media

Un unico numero aggregato nasconde il fallimento. Registra ogni turno come uno di questi:

* **conferma** - conferme, sì/no, "ok"
* **recupero dati** - tutto ciò che richiede un lookup live: giacenza, prezzo, stato ordine, data di consegna, compatibilità o applicabilità ([i lookup su stato ordine e resi](/it/blog/reduce-bracketing-returns) sono lo stesso tipo di turno)
* **dopo un enunciato lungo** - il chiamante ha parlato per 15+ secondi prima di fermarsi
* **dopo un'interruzione** - il chiamante ha tagliato la parola all'agente

I turni di recupero dati sono quelli in cui il numero esplode, e sono in modo sproporzionato quelli che decidono se la chiamata converte. Riporta p50 e p90 per tipo.

### Misura sul percorso che i tuoi clienti usano davvero

Non sulla linea demo del fornitore. Non sul wifi dell'ufficio alle 08:30 di martedì.

Da un telefono sulla rete su cui stanno i tuoi clienti, nel paese da cui chiamano, all'ora in cui chiamano. Fai una serie nel tuo picco reale - l'ora in cui il volume di chiamate è più alto - e una fuori picco, e confronta.

Se servi più di un paese, esegui la serie separatamente per mercato e per lingua - [falla per ogni lingua](/it/blog/multilingual-phone-support-eu-expansion). L'operatore è diverso, il percorso è diverso, e il modello che gestisce quella lingua è diverso. Un unico numero europeo aggregato non ti dice nulla sulla linea danese.

### Il risultato: una tabellina

| Tipo di turno | n | p50 | p90 | Turno più lento | Cosa è successo nel turno più lento |
| --- | --- | --- | --- | --- | --- |
| conferma | 22 | 610 ms | 940 ms | 1,1 s | il chiamante si è spento a metà parola, l'endpointer ha atteso |
| recupero dati | 19 | 1.450 ms | 3.900 ms | 5,2 s | verifica giacenza su un codice articolo, due lookup concatenati |
| dopo enunciato lungo | 11 | 780 ms | 1.600 ms | 1,9 s | descrizione del guasto da 40 secondi |
| dopo interruzione | 8 | 1.900 ms | 3.100 ms | 3,4 s | il chiamante interrompe, l'agente ricomincia la frase |
| tutti i turni | 60 | 900 ms | 3.200 ms | 5,2 s | - |

Solo formato illustrativo. I numeri qui sopra sono inventati per mostrare la forma della tabella, non risultati misurati.

L'ultima colonna è dove sta la diagnosi. Tutto il resto è contabilità.

## Cosa ti stanno dicendo il tuo p50 e il tuo p90

Leggi la tabella come se/allora, non come un voto.

**p50 accettabile, p90 diverse volte più alto, e i turni lenti sono tutti di recupero dati** - non è un problema di parlato. È un problema di accesso ai dati. La soluzione sta nel percorso verso il catalogo o l'ERP, e cambiare fornitore non lo tocca. C'è chi cambia piattaforma per questo e si ritrova lo stesso p90.

**Tutti i tipi di turno uniformemente lenti** - architettura o percorso di rete. Chiedi dove sono ospitati i componenti rispetto a chi chiama, e se la risposta è "una region statunitense".

**Il p90 peggiora solo nell'ora di punta** - capacità. Sta peggiorando esattamente quando le chiamate valgono di più.

**I turni dopo interruzione sono i peggiori di gran lunga** - endpointing e gestione del barge-in. Vedi la sezione sopra, e fai la domanda testuale.

Poi la parte che ti dà una seconda leva.

Nemmeno gli esseri umani stanno a +208 ms sulle domande difficili. Tengono il turno. "Verifico subito." "Un secondo." Una tastiera che si sente. Il gap resta breve anche quando la risposta è lenta, perché ciò che rompe una conversazione è il silenzio, non l'attesa. Questo è un nostro ragionamento costruito sul risultato di Stivers, non un risultato in sé: il paper misura i gap tra i turni, non verifica il mantenimento del turno nelle telefonate commerciali.

Ma cambia cosa fare con un turno di recupero dati che non riesci a rendere veloce. La soluzione spesso non è più velocità. È far dire qualcosa all'agente dentro la finestra umana e poi prendersi i quattro secondi che gli servono. È una modifica al prompt e un giorno di lavoro, contro una ri-architettura della tua integrazione di magazzino.

Due leve. Una delle due costa poco.

:::takeaway
La linea di base umana è +208 ms e il tuo agente non la raggiungerà. Smetti di cercare un benchmark che non esiste e misura il tuo p50 e p90, suddivisi per tipo di turno.
Fai a ogni fornitore una domanda: il vostro dato di latenza parte dall'ultima parola del chiamante o da quando scatta l'endpointing?
Dove un turno di recupero dati non può essere reso veloce, fai parlare l'agente dentro la finestra umana e poi lascialo prendere il tempo che serve. Una modifica al prompt batte una ri-architettura del magazzino.
:::

## Cosa questo protocollo non ti dirà

Nulla su quanto la risposta fosse corretta. Una risposta sbagliata e veloce su giacenza o compatibilità ti costa più di una giusta e lenta, e latenza e accuratezza si scambiano l'una con l'altra in diversi punti della catena: finestre di endpointing più corte tagliano le parole, modelli più piccoli rispondono prima e peggio. Misura entrambe, o ti ottimizzerai fino a diventare un bugiardo sicuro di sé e rapidissimo.

Non ti dà una soglia di conversione, e voglio essere preciso sul perché. Non è stato trovato alcun dataset che colleghi la latenza misurata di un voice agent all'abbandono della chiamata o alla conversione su telefonate commerciali europee. Né europeo, né americano. Se ne hai uno, mandamelo e lo pubblico.

Quindi il numero da battere è la tua linea di base, rimisurata dopo ogni modifica.

Noi eseguiamo questo protocollo sulle nostre linee, in Sabato. Il motivo per cui è scritto è che abbiamo dovuto costruircelo prima di poter discutere di latenza con chiunque, noi compresi.

:::action
Cosa fare questa settimana
Registra dieci chiamate reali sulla rete e nell'ora che i tuoi clienti usano davvero. Non la linea demo, non il wifi dell'ufficio di martedì mattina.
Segna T1 e T2 in un editor di forme d'onda per 60 turni, etichettando ciascuno come conferma, recupero dati, dopo enunciato lungo o dopo interruzione.
Riporta p50 e p90 per tipo di turno, e scrivi cosa è successo nel singolo turno più lento. Quella frase è la diagnosi.
Chiedi al tuo fornitore se il dato dichiarato parte dall'ultima parola del chiamante o da quando scatta l'endpointing, e metti per iscritto la risposta.
Rifallo dopo ogni cambio di modello, prompt, telefonia o integrazione di catalogo, e come minimo una volta a trimestre.
:::

Cosa possiedi adesso, inclusa la parte che nessuno mette a budget: non è un esercizio una tantum. Un'ora di analisi delle forme d'onda a trimestre, per sempre. È questo il costo reale, ed è comunque più economico che scoprirlo da un cliente.

## FAQ

**Qual è una buona latenza per un voice agent AI?** Non esiste un benchmark verificato in modo indipendente per le telefonate commerciali. I due riferimenti difendibili sono la norma conversazionale umana - un gap medio di +208 ms su 10 lingue (Stivers et al., PNAS, 2009) - e il tetto di 400 ms della ITU-T G.114 sul ritardo unidirezionale bocca-orecchio, che copre la sola consegna dell'audio. Misura il tuo p50 e p90 e migliora rispetto a quella base.

**Come si misura la latenza di risposta di un voice agent?** Registra le chiamate in stereo, aprile in un editor di forme d'onda e per ogni turno misura dall'ultimo campione audio dell'ultima parola del chiamante al primo campione della risposta dell'agente. Registra almeno 60 turni, suddivisi in conferma, recupero dati, dopo enunciato lungo e dopo interruzione, poi riporta p50 e p90 per ciascun tipo separatamente.

**400 ms è lo standard per la latenza della voice AI?** No. Il dato dei 400 ms viene dalla Raccomandazione ITU-T G.114 (2003) e descrive il ritardo unidirezionale bocca-orecchio per la pianificazione di rete: trasmissione più codec e buffering aggiunti dalla rete. Esclude endpointing, riconoscimento vocale, inferenza del modello, interrogazioni a database e sintesi vocale. Per un voice agent è un pavimento sotto il tempo di risposta totale, non un obiettivo di prestazione.

**Perché il mio voice agent sembra lento se il fornitore ha dichiarato un numero basso?** Molto probabilmente le finestre di misurazione sono diverse. Molti dati dichiarati partono dopo l'endpointing, cioè dal momento in cui il sistema decide che il chiamante ha smesso di parlare. L'esperienza del chiamante parte dalla sua ultima parola. La soglia di silenzio tra questi due punti è spesso il singolo blocco di ritardo più grande della catena.

**Un voice agent più veloce è sempre meglio?** No. Ridurre la soglia di endpointing per accorciare il gap aumenta le false interruzioni, in cui l'agente parla sopra al chiamante a metà pensiero e lo costringe a ripetersi. La conversazione umana si sovrappone continuamente: il 40,0-41,7% delle transizioni su tre corpora europei erano sovrapposizioni (Heldner & Edlund, 2010, fonte singola). Entrambi i fallimenti costano chiamate.

**Il dato dei +208 ms vale per le telefonate?** Non direttamente. Stivers et al. hanno misurato conversazione naturale, in gran parte faccia a faccia, tra persone che si conoscono, e hanno contato come inizio di risposta anche i cenni del capo e le inspirazioni udibili. Nessuno ha pubblicato tempi equivalenti per le chiamate commerciali in ingresso. Consideralo la base su cui è stato addestrato l'orecchio di chi ti chiama, non una specifica per la tua linea.

## Fonti

* Stivers, T. et al., *Universals and cultural variation in turn-taking in conversation*, Proceedings of the National Academy of Sciences, 2009 - [pnas.org](https://www.pnas.org/doi/full/10.1073/pnas.0903616106)
* ITU-T Recommendation G.114 (05/2003), *One-way transmission time* - [itu.int](https://www.itu.int/rec/T-REC-G.114-200305-I/en)
* Heldner, M. & Edlund, J., *Pauses, gaps and overlaps in conversations*, Journal of Phonetics, 2010 - [staff.fnwi.uva.nl](https://staff.fnwi.uva.nl/r.fernandezrovira/teaching/cosp/cosp2016/docs/HeldnerEdlund2010.pdf)
