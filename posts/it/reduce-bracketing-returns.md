---
title: "Come ridurre i resi da bracketing senza perdere la vendita"
slug: reduce-bracketing-returns
description: "Come ridurre i resi da bracketing senza perdere la vendita: la query SQL per misurarlo, il costo reale per ordine e il break-even che quasi nessun brand calcola."
category: Resi
date: 2026-07-30
cover_style: lime
---

Una cliente vuole la taglia 44. Non è sicura che la tua 44 sia davvero una 44, quindi compra la 44 e la 46, ne tiene una e rispedisce l'altra. Secondo l'*Annual Returns Benchmark 2024* di ZigZag e Retail Economics, il 27,4% degli acquirenti UK di abbigliamento e calzature lo fa di proposito. Ognuno di loro ha pagato un secondo capo perché la tua scheda prodotto non rispondeva a una domanda.

:::keystat
27,4%
degli acquirenti UK di moda ordina deliberatamente più taglie per poi renderne una parte
Fonte: ZigZag / Retail Economics, Annual Returns Benchmark 2024
:::

## Perché il bracketing è un problema di informazione e non di logistica?

Il bracketing è l'acquisto deliberato dello stesso articolo in due o più taglie, con l'intenzione di rendere tutte tranne una. Finisce nel report della logistica inversa, quindi viene trattato come un problema di logistica inversa. Non lo è.

Sahoo, Dellarocas e Srinivasan hanno documentato il meccanismo su *Information Systems Research* nel 2018, su due anni di dati transazionali di un retailer specializzato nordamericano. Dove le recensioni erano scarse, gli acquirenti compravano prodotti sostitutivi accanto all'acquisto principale per coprirsi, e i resi salivano di conseguenza. Più recensioni, meno resi. Recensioni votate utili dagli altri acquirenti, ancora meno.

:::quote
La seconda taglia non è un comportamento da reprimere. È un acquisto che la cliente fa al posto di una risposta che non le hai dato.
:::

Trattieni la risposta, e lei compra la copertura. Il che sposta il problema a monte: fuori dal magazzino, dentro il merchandising.

## Step 1: contalo. La regola di rilevamento a tre livelli sui tuoi dati

Nessuno può dirti il tuo tasso di bracketing. Va calcolato.

**Livello 1 — stesso ordine.** Un ordine contiene due o più varianti dello stesso prodotto padre che differiscono solo per taglia.

```
WITH size_groups AS (
  SELECT
    ol.order_id,
    o.customer_id,
    v.product_id,
    v.option_colour,
    COUNT(DISTINCT v.option_size)   AS distinct_sizes,
    SUM(ol.qty)                     AS units,
    SUM(ol.qty * ol.unit_price)     AS gross_value
  FROM order_lines ol
  JOIN variants v ON v.variant_id = ol.variant_id
  JOIN orders   o ON o.order_id   = ol.order_id
  GROUP BY 1,2,3,4
)
SELECT * FROM size_groups
WHERE distinct_sizes >= 2;         -- il flag di bracketing
```

Raggruppa per product_id **e colore**. Due colori dello stesso modello sono una copertura di *stile*: una domanda diversa, con una risposta diversa. Se li unisci, sbagli diagnosi e sbagli rimedio.

**Livello 2 — la finestra breve.** Alcuni clienti ordinano, si fanno prendere dal dubbio e comprano la taglia sopra dieci minuti dopo. Self-join sullo stesso cliente, stesso product_id e colore, taglia diversa, dentro una finestra:

```
SELECT a.customer_id, a.product_id, a.option_colour,
       a.order_id AS order_a, b.order_id AS order_b,
       ABS(EXTRACT(EPOCH FROM (b.created_at - a.created_at)))/3600 AS hours_apart
FROM order_variant_flat a
JOIN order_variant_flat b
  ON  a.customer_id   = b.customer_id
  AND a.product_id    = b.product_id
  AND a.option_colour = b.option_colour
  AND a.option_size  <> b.option_size
  AND a.order_id      < b.order_id
WHERE ABS(EXTRACT(EPOCH FROM (b.created_at - a.created_at))) <= 48*3600;
```

Non ereditare le 48 ore da me. Traccia la distribuzione delle ore tra ordini stesso-prodotto-taglia-diversa. Vedrai un picco nelle prime ore (la copertura) e una lunga coda piatta (il riacquisto genuino dopo la prova). Taglia al gomito della curva, documenta il taglio, non cambiarlo mai a esperimento in corso.

**Livello 3 — bracketing confermato.** L'unico livello con dentro il conto economico: flag di bracketing E reso parziale del gruppo taglie.

```
bracket_confirmed = (distinct_sizes >= 2)
                AND (returned_units_in_group >= 1)
                AND (returned_units_in_group <  units_in_group)
```

| Esito | Regola | Cosa significa | Cosa fare |
| --- | --- | --- | --- |
| Bracketing confermato | reso parziale del gruppo taglie | La copertura ha funzionato. L'hai pagata tu. | Intervieni con una risposta pre-acquisto |
| Reso dell'intero gruppo | ogni unità resa | Ha fallito il prodotto, non la taglia | Passa a merchandising / QA |
| Gruppo tenuto per intero | nessun reso | Regalo, famiglia, multi-acquisto genuino | Escludi — è il tuo tasso di falsi positivi |

:::takeaway Come si misura il bracketing
Segnala gli ordini con due o più varianti dello stesso prodotto padre e colore che differiscono solo per taglia (Livello 1).
Aggiungi gli ordini stesso-cliente, stesso-prodotto piazzati dentro una finestra breve (Livello 2).
Conferma il bracketing dove una parte, ma non tutto, del gruppo taglie torna indietro (Livello 3).
Raggruppa per prodotto padre più colore, mai per prodotto da solo. Non esiste un benchmark pubblico: il tuo baseline sei tu.
:::

Due cose ti morderanno prima ancora dell'analisi.

**Il blocco della prima settimana sono i dati, non l'SQL.** Se option_size non è un'opzione variante strutturata — frequente sui cataloghi Shopify e Magento migrati — hai un lavoro di pulizia prima di avere una query. Poi fissa le esclusioni: regali (salto di taglia oltre due misure, o reparto diverso), SKU da bundle promozionali, buchi di identità del guest checkout (dichiara onestamente il tuo tasso di ricongiungimento, o il numero del Livello 2 è un pavimento), cambi registrati come resi, canale marketplace, e sistemi taglie non ordinali che richiedono prima una lookup di size_rank.

**Non esiste alcun benchmark pubblico degli ordini bracketed come quota degli ordini. Nessuno.** Ogni cifra in circolazione è quota-sui-*resi* e pubblicata da vendor. Calcola il tuo mensilmente su 24 mesi e segmenta per modello, categoria, nuovi contro abituali, canale e profondità sconto. Il segnale non è la media. È la varianza tra modelli. Qualunque modello sopra 1,5× la mediana di categoria su 200+ ordini in 90 giorni ha una domanda senza risposta sulla sua scheda prodotto. Quella lista è la tua coda di interventi.

## Step 2: dagli un prezzo. Quanto costa davvero un ordine bracketed

La maggior parte degli operatori conta due voci: il trasporto del reso e un po' di manodopera di magazzino. Ecco il modello completo su un tariffario fashion UK di fascia media. Ogni [IPOTESI] è un segnaposto da sostituire con i tuoi numeri.

| Voce | Valore | Fonte |
| --- | --- | --- |
| Prezzo medio per unità | £40,00 | [IPOTESI] |
| Margine lordo 60% → utile lordo | £24,00 | [IPOTESI] |
| Spedizione in uscita incrementale (seconda taglia, stesso pacco) | £0,50 | [IPOTESI] |
| Pick & pack incrementale | £0,35 | [IPOTESI] |
| Trasporto del reso in entrata | £3,50 | [IPOTESI] |
| Ricezione, ispezione, stiratura, ri-etichettatura, ri-imbustamento, restock | £2,50 | [IPOTESI], ancorata al processing fashion bevh |
| Commissione di pagamento non restituita sul rimborso | £0,80 | Tariffa UK pubblicata da Stripe + policy rimborsi Stripe |
| Deprezzamento / markdown, 13,1% del valore merce | £5,24 | bevh-Retourenkompendium, che cita l'Università di Bamberg |
| Contatto CS: 20% dei resi × £4,00 di costo gestione | £0,80 | [IPOTESI] |

Due di quelle voci sono silenziose, e quasi nessuno le mette a libro. La documentazione di supporto di Stripe dichiara che le commissioni della transazione originale non vengono restituite al rimborso; alla tariffa standard UK pubblicata di 1,5% + 20p, un articolo da £40 rimborsato ti costa per sempre £0,80, sepolti tra le commissioni di pagamento dove nessuno li attribuisce ai resi. Il deprezzamento è l'altra — ed è la voce più grossa del modello.

:::chart bar
Dove finiscono le £13,69 di costo di un'unità resa
Deprezzamento / markdown | £5,24 | 38% — la voce che nessuno mette a libro
Trasporto del reso | £3,50 | l'unica voce che l'industria ottimizza
Ricezione, ricondizionamento, restock | £2,50
Commissione di pagamento persa | £0,80
Contatto CS (allocato) | £0,80
Spedizione in uscita incrementale | £0,50
Pick & pack incrementale | £0,35
Fonte: modello di cui sopra — bevh-Retourenkompendium; prezzi e policy rimborsi Stripe UK
:::

Ora l'ordine bracketed. Due unità a £40. Ne tiene una, ne rende una.

:::compare Un ordine, due esiti
Ordine bracketed | Taglia giusta al primo colpo
Unità acquistate | 2 | 1
Utile lordo sull'unità tenuta | £24,00 | £24,00
Costo dell'unità resa | −£13,69 | £0,00
Contribuzione netta | £10,31 | £24,00
:::

La domanda sulla vestibilità a cui non hai risposto costa il 57% dell'utile lordo di quell'ordine.

£13,69 sta dentro la forchetta £10–£20 per reso pubblicata da ZigZag e Retail Economics per il non-food UK nel 2024 — ma la loro forchetta include anche il costo opportunità della vendita persa, la mia no. Trattala come una verifica dell'ordine di grandezza, non come una conferma.

Guarda quale voce domina. Il trasporto del reso, la cosa che l'intera industria ottimizza, è £3,50 su £13,69: il 26%. Il deprezzamento è il 38%. Rinegozia la logistica inversa fino letteralmente a zero e ti restano comunque £10,19 di costo su ogni ordine bracketed.

Un avvertimento, perché è l'errore più comune nei contenuti sui resi: £10–£20 (ZigZag 2024, include il costo opportunità della vendita persa) e €2,85 (Bamberg/EUROM, 2020–21, solo trasporto e handling) non sono due stime della stessa cosa. Sono due perimetri di costo diversi. Scegline uno, dichiaralo, e non cambiarlo più.

## Step 3: fai il break-even prima di scoraggiare chiunque

Il tasso di reso lo puoi sempre abbassare rendendo più difficile comprare. La domanda è quanta deterrenza ti puoi permettere.

Sia G = utile lordo per unità tenuta, C = costo netto di un'unità resa, s = quota dei bracketer potenziali che compra comunque dopo il tuo intervento, k = il loro tasso di tenuta successivo.

```
Tasso di sopravvivenza di pareggio:  s* = (G − C) / ( k·G − (1−k)·C )
```

**Caso A — informazione perfetta, k = 1.**

```
s* = (24,00 − 13,69) / 24,00 = 10,31 / 24,00 = 43%
```

Un intervento che elimina il bracketing paga solo se almeno 43 bracketer potenziali su 100 comprano comunque. Se ne scappano più di 57, ti sei impoverito mentre la dashboard dei resi diventava verde.

**Caso B — una fee sui resi da £3,95, la tariffa ASOS.** La fee recupera £3,95, quindi C netto = £9,74. Assumi k = 0,9:

```
s* = 10,31 / (0,9 × 24,00 − 0,1 × 9,74) = 10,31 / 20,626 = 50%
```

:::keystat
43%
dei bracketer potenziali deve comprare comunque perché un intervento a informazione perfetta vada in pari
Fonte: esempio svolto — prezzo £40, margine 60%, £13,69 di costo per reso

50%
deve comprare comunque se invece applichi una fee sui resi da £3,95
Fonte: stesso modello, fee recuperata contro il costo del reso
:::

Una fee sui resi ha bisogno che metà dei tuoi bracketer potenziali continui a comprare. L'unico sondaggio disponibile sulla deterrenza (Trustpilot/OnePoll, 2023, USA, intenzione dichiarata e non comportamento osservato) ha il 49% degli acquirenti che afferma che non comprerebbe da retailer che fanno pagare i resi. Ti stanno chiedendo di scommettere il conto economico su un lancio di moneta.

**Caso C — rispondi alla domanda invece di scoraggiarla.** Prendi 100 bracketer. Poniamo che 70 ora comprino una sola taglia (tenendola nel 90% dei casi), 25 continuino a fare bracketing, 5 non comprino nulla.

```
70 comprano →  63 tenuti × £24,00   = £1.512,00
            →   7 resi × £13,69     =   − £95,83
25 ancora bracketing × £10,31       =  + £257,75
 5 non comprano                     =       £0,00
                            Totale  =  £1.673,92

Baseline: 100 × £10,31              =  £1.031,00
Uplift                              =  + £642,92  (+62,4%)
```

Rispondere alla domanda vale +62% di contribuzione su quella coorte. Reprimere il comportamento vale, nel migliore dei casi, il pareggio.

Addebito le £13,69 piene anche ai 7 resi a taglia singola, benché £0,85 — la spedizione in uscita e il pick & pack della seconda unità — non siano mai stati sostenuti. Questo sottostima l'uplift. Preferisco arrotondare contro il mio stesso argomento.

:::takeaway Prima di applicare una fee sui resi
Su un articolo da £40 al 60% di margine con £13,69 di costo per unità resa, eliminare il bracketing paga solo se circa il 43% dei bracketer potenziali compra comunque.
Una fee da £3,95 ne richiede circa il 50% — e un sondaggio ha il 49% degli acquirenti che dichiara che le fee lo fermano.
43% e 50% escono da questo esempio, non da una legge di natura. Ricostruisci le soglie sul tuo tariffario prima di scoraggiare chiunque.
:::

E annota il contrappeso: Balaram, Perdikaki e Galbreth hanno mostrato su *Naval Research Logistics* nel 2022 che il bracketing taglia in entrambe le direzioni — alza i costi di logistica inversa ma riduce l'esitazione sulla vestibilità e spinge i volumi. Ecco perché la soglia te la calcoli da solo invece di prendere in prestito la mia.

## Step 4: ordina i reason code tra ciò a cui puoi rispondere e ciò a cui non puoi

Prima di spendere un centesimo in strumenti, ri-mappa i reason code esistenti in questi sei secchi.

| Secchio | Codici di esempio | Rispondibile pre-acquisto? | Owner |
| --- | --- | --- | --- |
| **A. Vestibilità dimensionale** | troppo piccolo, maniche corte, vita larga | Del tutto, con le misure del capo | Dati prodotto |
| **B. Carattere della vestibilità / caduta** | "boxy", "veste piccolo", "non fedele alla taglia" | Sì — ma solo da chi l'ha indossato | UGC, clienteling, conversazione |
| **C. Specifiche / materiale** | peso, opacità, elasticità, calore | Sì. Puro gap informativo | Copy della scheda e Q&A |
| **D. Aspettativa disattesa** | colore diverso dalla foto, sembrava più economico | In parte, e più media possono peggiorare | Merchandising |
| **E. Gusto / occasione** | "non mi piaceva", ho cambiato idea | No. Smetti di provarci | Nessuno |
| **F. Difetto di prodotto o operations** | difettoso, articolo sbagliato | No. Problema del tutto diverso | QA / magazzino |

Sul secchio D, resisti al riflesso di aggiungere contenuto. Lo studio econometrico del 2013 di De, Hu e Rahman su un retailer di abbigliamento femminile ha trovato che l'uso dello zoom riduceva i resi mentre *le foto alternative li aumentavano*. Più media non è monotonicamente meglio.

Due regole.

**Solo A, B e C sono in scope per un intervento pre-acquisto.** Se la tua tassonomia ha un solo secchio chiamato "taglia/vestibilità", non puoi separare A da B, e una size chart strutturalmente non può risolvere B. Se il campo libero "altro" supera il 15% del volume, quello è il primo lavoro; B e C di solito si nascondono lì dentro.

**Quasi nessun portale resi offre un codice che dica "ho ordinato due taglie di proposito".** Così i resi da bracketing vengono registrati come "troppo piccolo", inquinano il segnale dei difetti di vestibilità e puntano i tuoi interventi sulla scheda dei modelli sbagliati. Aggiungi il codice. Il 27,4% di ZigZag esiste perché qualcuno ha fatto la domanda direttamente. Il tuo portale non la fa mai.

## Step 5: classifica gli interventi per evidenza e velocità di rilascio

| Intervento | Costo | Rilascio | Secchio | Evidenza (grado) |
| --- | --- | --- | --- | --- |
| Misure della modella + "la modella indossa la taglia X" | ~£0 | giorni | A | Baymard #10 (UX indipendente) |
| Misure del capo + guida taglie accanto al selettore | manodopera | 2–6 sett. | A | Baymard #3–#7; NN/g 2022 (UX indipendente) |
| Sub-punteggio di vestibilità + recensioni "veste piccolo" strutturate | SaaS basso | 2–6 sett. | **B** | Sahoo et al. 2018 (**peer-reviewed — la più solida**) |
| Nudge anti-bracketing al checkout | uno sprint | 1–3 sett. | A/B | SAIZ, True Fit (solo vendor, non quantificata) |
| Fit finder / raccomandatore di taglia | SaaS | 4–12 sett. | A | Zalando −10%; A/B di Fit Analytics (first-party + vendor) |
| Allungare la finestra resi | £0 + circolante | giorni | dotazione | Janakiraman et al. 2016 (meta-analisi peer-reviewed) |
| Fee sui resi | £0 | giorni | repressione | Contraddittoria; break-even al 50% (debole) |
| Prova virtuale | SaaS alto | 8–16 sett. | A/D | Nessuna credibile (scarsa) |
| Spostare il mix pagamenti via dal BNPL | rischio ricavi | trimestri | strutturale | 30,15% resi prepagato vs 55,65% fattura — Bamberg (correlazionale) |
| [Conversazione pre-acquisto (Sabato)](/it/casi-duso/consulenza-pre-vendita) | SaaS | settimane | A/B/C | Baymard #9; EHI 48% (**ipotesi — nessuna evidenza di terzi**) |

Le forchette dei tempi di rilascio sono una mia stima da esperienza di implementazione, non numeri pubblicati dai vendor.

Le righe 1 e 2 sono gratis o quasi, e tutto il resto ne dipende: fit tool, chatbot e agenti sono garbage-in, garbage-out sulle misure del capo. I test Baymard del 2022 hanno trovato che l'83% dei siti apparel desktop dà informazioni di taglia insufficienti — quindi assumi di essere uno di loro finché non hai verificato. La riga 3 è la voce meglio evidenziata della lista, e porta con sé un avvertimento dallo stesso paper: mostrare valutazioni medie *più alte* di quelle reali aumentava i resi. Sopprimere le recensioni negative sulla vestibilità è attivamente dannoso.

Il nudge al checkout è la regola del Livello 1 dello Step 1 eseguita sull'oggetto carrello: una ventina di righe di JS più una lookup variante-padre, rilasciabile in uno sprint. **Regola di design: il nudge deve rispondere alla domanda, mai bloccare o colpevolizzare.** Togliere la seconda taglia toglie la copertura. Rispondere toglie il *bisogno* della copertura. I vendor lo vendono; nessuno pubblica numeri.

Sii onesto sull'evidenza dei fit finder. La cifra credibile è la dichiarazione di Zalando di luglio 2023: −10% di resi legati alla taglia dove il suo size advice è disponibile. La *metodologia* credibile è l'A/B di Fit Analytics con THE ICONIC: 250.000 acquirenti, tre mesi, misurato come ricavo al netto dei resi. I "+150% di conversione" e "−50% di bracketing" che circolano altrove sono marketing vendor non verificato.

Due righe meritano un secondo sguardo. Allungare la finestra resi è gratis e controintuitivo: la meta-analisi 2016 di Janakiraman, Syrdal e Freling su 21 paper ha trovato che la clemenza sul *tempo* riduce i resi via effetto dotazione, mentre la clemenza sul perimetro li aumenta. Gli operatori sotto pressione resi accorciano la finestra. È il contrario.

E se proprio vuoi far pagare, ruba il meccanismo di ASOS, non il titolo. ASOS calcola un tasso di reso personale per cliente su 12 mesi mobili e addebita £3,95 sopra il 70% con tre o più ordini — **a meno che tu non tenga più di £40 dell'ordine.** Quella soglia significa che ASOS non punisce i resi: punisce la bassa retention del carrello. Fare bracketing su un vestito da £60 e tenerlo è gratis. Poi torna indietro e calcola il tuo s*.

La prova virtuale è il divario più grande tra hype ed evidenza della lista, e non una prima mossa. L'unico datapoint con fonte è negativo: nel sondaggio EHI sui retailer tedeschi (~2019), gli strumenti di prova virtuale erano giudicati efficaci dal 34%, sotto la consulenza personale al 48%.

Sulla riga pagamenti: prima di toccare la scheda prodotto, segmenta il tuo tasso di bracketing per metodo di pagamento. Se il BNPL è il 40% dei tuoi ordini fashion, quello è un driver strutturale più grosso della tua size chart. Dati tedeschi, correlazionali, e l'auto-selezione è ovvia — chi pianifica di rendere sceglie la fattura. Non leggerlo come causale.

**Sulla riga Sabato.** La nostra tesi: una conversazione pre-acquisto toglie il bisogno della copertura. Il vanity sizing mette un tetto a qualunque algoritmo deterministico. La domanda residua è un giudizio: la 44 di questo brand veste come la tua solita 44? Nessuno ha pubblicato evidenza che una conversazione riduca il bracketing, noi compresi. I supporti onesti sono Baymard, che elenca un link al customer service dentro la guida taglie come best practice *di sizing*, e i retailer che classificano la consulenza personale sopra la prova virtuale. Trattala come un'ipotesi. Falsificala col design qui sotto: potenza sul tasso di bracketing confermato, guardrail sul tasso ordini dei nuovi clienti.

## Step 6: testalo come si deve, o rilascerai la cosa sbagliata

**Mai rilasciare sul solo tasso di reso.** Il tasso di reso lo porti a zero anche non spedendo niente. Non può distinguere un percorso che sopprime la domanda da uno neutrale — che è l'intera questione.

**Scegli l'OEC.** Kohavi, Tang e Xu, *Trustworthy Online Controlled Experiments* (2020): un solo Overall Evaluation Criterion, più guardrail che non devono degradare. Usa la contribuzione netta per sessione — (unità tenute × utile lordo − unità rese × C) ÷ sessioni. Primario: unità tenute per sessione. Diagnostico: tasso di bracketing confermato. Guardrail: tasso ordini, **tasso ordini dei nuovi clienti** (i nuovi fanno più bracketing e sono quelli che una fee spaventa), AOV, tasso di contatti CS. Le unità per ordine possono legittimamente scendere. È il punto.

**Randomizza per utente, sticky, mai per sessione.** Lo stesso acquirente deve vedere una sola esperienza tra navigazione, carrello e reso, o il tuo rilevamento di bracketing finisce a cavallo dei due bracci. Mai testare a livello prodotto: gli acquirenti attraversano più modelli in una sessione e contaminano entrambi.

**Il problema di potenza, detto onestamente.** Rilevare un calo di 1 punto percentuale del bracketing confermato da una base ipotizzata dell'8% — mettici la tua — richiede circa 11.800 ordini per braccio: raggiungibile in un trimestre per la maggior parte dei brand di fascia media. Rilevare un +3% di ricavo per sessione, su una media di £2,00 con deviazione standard di £12,00, richiede 640.000 sessioni per braccio. La metrica dei soldi non la puoi alimentare. Quindi doppia lettura: potenza del test sul diagnostico, ricavo come guardrail direzionale con intervallo largo, e mai lasciare che un "ricavi +4%" sottodimensionato diventi il business case.

**La trappola del ritardo.** Le metriche sui resi non si leggono finché la finestra non si è chiusa. Congela la coorte di esposizione, poi aspetta finestra_resi + 21 giorni. Riporta i risultati intermedi solo su metriche lato ordine, e etichettali come intermedi.

**Pre-registra i confondenti.** Stagionalità (mai a cavallo di un confine saldi), profondità promo, mix nuovi-contro-abituali, rotazione del catalogo (l'assortimento fashion gira in sei-otto settimane), decadimento della novità (scarta la settimana uno), e confronti multipli — cinque metriche su otto segmenti sono quaranta test, e la "significatività" la troverai.

## Vale anche fuori dal fashion?

Il meccanismo generalizza: quando una domanda pre-acquisto decisiva resta senza risposta, l'acquirente compra una copertura oppure non compra affatto. Nel fashion la copertura è una seconda taglia. A prezzi medi più alti la copertura diventa troppo costosa da comprare, quindi il modo di fallimento passa dal *reso* al *non-acquisto* — invisibile nei dati resi, visibile solo nel tasso di uscita dalla scheda e nel volume di contatti pre-acquisto.

| Categoria | La domanda senza risposta | La copertura | Come rilevarlo |
| --- | --- | --- | --- |
| Arredamento | Passa dalla porta, su per le scale, nella nicchia? | Prima il campione, due finiture, o abbandono | Multi-variante stesso-padre in un ordine |
| Elettrodomestici | Apertura, reversibilità porta, attacchi idraulici | Raro — chiama o abbandona | Tasso di contatti pre-acquisto per SKU |
| Bici | Taglia telaio, e sono tra due | Due taglie di telaio dove i resi sono gratis | Stesso modello, due taglie, ≤7 giorni |
| Ricambi auto | Va bene per *la mia* macchina? | Due varianti, o compra da chi garantisce il fit | Due varianti di una famiglia di ricambi, un ordine |
| B2B a specifica | Tolleranza, certificazione, interoperabilità | Campioni di due o tre specifiche | Ordini campione, carrelli multi-specifica |

La prova sta nei ricambi. A febbraio 2023 eBay Motors ha lanciato Guaranteed Fit: inserisci il veicolo, ottieni la spunta verde "Fits", e se il ricambio non va bene eBay copre la spedizione del reso e ti rimborsa. Poi eBay ha comprato il gruppo myFitment per tenere corretti i dati di compatibilità. Un business che eBay descrive come oltre 10 miliardi di dollari di GMV annuo ha garantito la risposta sulla compatibilità col proprio bilancio. Nessuno lo fa per un problema di logistica. Lo si fa per un problema di conversione.

Non esiste un benchmark credibile di tasso di bracketing in nessuna di queste categorie. L'argomento qui è strutturale, non statistico.

:::action I tuoi prossimi 30 giorni
Giorni 1–3: verifica se option_size è un'opzione variante strutturata. Se non lo è, quella è tutta la tua prima settimana.
Giorni 3–7: esegui la query di Livello 1 su 24 mesi. Segmenta per modello. Costruisci la coda di interventi >1,5× la mediana.
Giorni 3–7, in parallelo, costo zero: estrai gli ultimi 500 contatti CS pre-acquisto, tagga ognuno con la domanda posta, ordina per frequenza. Ogni domanda della top 10 senza risposta sulla scheda è una copertura o un abbandono che stai pagando.
Settimana 2: ricostruisci il modello di costo sul tuo tariffario. Calcola il tuo s*.
Settimana 2: ri-mappa i reason code su A–F. Aggiungi il codice "ho ordinato due taglie di proposito".
Settimane 3–4: rilascia le cose gratis — misure della modella, taglia indossata, guida taglie accanto al selettore, link al CS dentro la guida taglie.
Settimana 4: pre-registra un test sul primo modello della coda. Scegli l'OEC prima di costruire qualsiasi cosa.
:::

Il bracketing non è un problema di resi da processare. È una domanda a cui non hai risposto — e puoi scoprire esattamente quale entro venerdì.

## FAQ

**Cos'è il bracketing nell'ecommerce?** Il bracketing è quando un acquirente ordina deliberatamente lo stesso articolo in due o più taglie o varianti, con l'intenzione di tenerne una e rendere il resto. Lo fa come copertura contro una domanda a cui la scheda prodotto non ha risposto. L'*Annual Returns Benchmark 2024* di ZigZag e Retail Economics ha trovato che il 27,4% degli acquirenti UK di abbigliamento e calzature lo ammette.

**Come si calcola il proprio tasso di bracketing?** Tre livelli. Livello 1: ordini con due o più varianti dello stesso prodotto padre e colore che differiscono solo per taglia — raggruppa per prodotto padre *e* colore, mai per prodotto da solo. Livello 2: la stessa coppia su due ordini dentro una finestra breve. Livello 3, l'unico con il conto economico: flag di bracketing più reso parziale di quel gruppo taglie.

**Far pagare i resi ferma il bracketing?** Riduce il comportamento. Se ti faccia guadagnare è un'altra domanda. Su un articolo da £40 al 60% di margine, una fee da £3,95 ha bisogno che circa metà dei bracketer potenziali continui a comprare solo per andare in pari, e l'unico sondaggio disponibile ha il 49% che dichiara che le fee lo fermano. Prima fai l'aritmetica.

**Qual è il costo medio di un articolo reso?** Sul modello svolto qui (trasporto, pick & pack, ricezione, ricondizionamento, commissioni di pagamento non recuperate, deprezzamento e un contatto CS) un'unità resa costa £13,69. Sta dentro la forchetta UK £10–£20 di ZigZag, che usa un perimetro ancora più ampio — include anche il costo opportunità della vendita persa. I costi per reso pubblicati usano perimetri incompatibili: mai confrontarli senza controllare cosa c'è dentro.

**Conviene accorciare la finestra resi per ridurre i resi?** No. La meta-analisi 2016 di Janakiraman, Syrdal e Freling su 21 paper ha trovato che la clemenza sul *tempo* riduce i tassi di reso, attribuendolo all'effetto dotazione: più a lungo qualcuno tiene un articolo, più ci si affeziona. La clemenza sul perimetro aumenta i resi; quella sul tempo no. Allungare la finestra è la leva gratuita e supportata dall'evidenza che quasi nessuno usa.

## Fonti

- Sahoo, Dellarocas & Srinivasan (2018), *The Impact of Online Product Reviews on Product Returns*, Information Systems Research — [ideas.repec.org](https://ideas.repec.org/a/inm/orisre/v29y2018i3p723-738.html)
- De, Hu & Rahman (2013), *Product-Oriented Web Technologies and Product Returns*, Information Systems Research — [econpapers.repec.org](https://econpapers.repec.org/article/inmorisre/v_3a24_3ay_3a2013_3ai_3a4_3ap_3a998-1010.htm)
- Balaram, Perdikaki & Galbreth (2022), *Bracketing of purchases to manage size uncertainty*, Naval Research Logistics — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3823892)
- Janakiraman, Syrdal & Freling (2016), *The Effect of Return Policy Leniency on Consumer Purchase and Return Decisions*, Journal of Retailing — [UT Dallas](https://news.utdallas.edu/business-management/researchers-examine-effect-of-return-policies-on-c)
- ZigZag / Retail Economics, *Annual Returns Benchmark 2024* — [PDF](https://info.zigzag.global/hubfs/Annual-Returns-Benchmark-Report-2024-ZigZag.pdf)
- bevh-Retourenkompendium, 2. Auflage (cita la ricerca sui resi dell'Università di Bamberg e il sondaggio retailer EHI, ~2019) — [PDF](https://bevh.org/fileadmin/user_upload/Studien/Retourenkompendium/Final_2._Auflage_Retourenkompendium_41_.pdf)
- Università di Bamberg, progetto EUROM (n=411 retailer europei, 2020–21) — [retourenforschung.de](https://www.retourenforschung.de/forschungsprojekt-eurom-2122.html)
- Baymard Institute (2022), *Apparel: 10 Best Practices on Sizing* — [baymard.com](https://baymard.com/blog/apparel-size-information)
- Baymard Institute (2024), *Always Provide an Aggregate Fit Subscore* — [baymard.com](https://baymard.com/blog/apparel-provide-aggregate-fit-subscore-in-reviews)
- Nielsen Norman Group (2022), *Size Guides and Product Measurements for International Shoppers* — [nngroup.com](https://www.nngroup.com/articles/sizes-measurements-ecommerce/)
- Zalando (2023), *Size recommendations based on customers' own body measurements* — [corporate.zalando.com](https://corporate.zalando.com/en/technology/zalando-launches-size-recommendations-based-customers-own-body-measurements)
- Fit Analytics, case study THE ICONIC (vendor) — [fitanalytics.com](https://fitanalytics.com/case-studies/the-iconic)
- True Fit, case study ASICS (vendor) — [truefit.com](https://info.truefit.com/asics-case-study)
- SAIZ, *Automated checkout nudges to stop bracketing* (vendor) — [saiz.io](https://www.saiz.io/checkout-nudges)
- ASOS, *What is your Fair Use Policy* — [asos.com](https://www.asos.com/customer-care/returns-refunds/what-is-your-fair-use-policy)
- Trustpilot / OnePoll (2023), sondaggio acquirenti online USA — [trustpilot.com](https://corporate.trustpilot.com/press/news/a-quarter-of-americans-admit-to-buying-more-to-save)
- Stripe, *Understanding fees for refunded payments* — [support.stripe.com](https://support.stripe.com/questions/understanding-fees-for-refunded-payments)
- Prezzi Stripe UK — [stripe.com](https://stripe.com/gb/pricing)
- eBay Motors (2023), lancio di *eBay Guaranteed Fit* — [stocktitan.net](https://www.stocktitan.net/news/EBAY/e-bay-motors-launches-new-purchase-protections-for-auto-parts-y44cw5yq6mdz.html)
- eBay acquisisce il gruppo myFitment — [stocktitan.net](https://www.stocktitan.net/news/EBAY/e-bay-acquires-the-my-fitment-group-of-companies-to-enhance-part-and-fj5wzm5b5dan.html)
- Kohavi, Tang & Xu (2020), *Trustworthy Online Controlled Experiments* — [experimentguide.com](https://experimentguide.com/wp-content/uploads/TrustworthyOnlineControlledExperiments_PracticalGuideToABTesting_Chapter1.pdf)
