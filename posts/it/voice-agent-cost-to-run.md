---
title: "Quanto costa far girare un voice agent, non costruirlo"
seo_title: "Quanto costa far girare un voice agent | Sabato AI"
slug: voice-agent-cost-to-run
description: "Il prezzo al minuto è la voce più piccola del foglio. Le sette che ricorrono davvero, e perché il costo di gestione cresce con la varietà, non col volume."
category: Voice AI fai-da-te
date: 2026-08-18
cover_style: black
---

*The Build File, numero 03. Una stagione su come gestire un progetto voice senza essere un tecnico.*

Tutti citano il costo al minuto.

È il numero sulla pagina prezzi, è quello che il tuo responsabile tecnico porta in riunione, ed
è la voce più piccola del foglio. Non una delle più piccole. La più piccola.

La cosa conta perché quasi ogni business case interno per un voice agent è costruito sul costo
di *costruirlo*. Una tantum, quotata in settimane di sviluppo, di cui entro un anno non si
ricorderà più nessuno. Il costo di *farlo girare* è per sempre, e di solito nel documento non
c'è proprio.

Il costo di gestione si divide in sette voci. Qui non trovi i tuoi numeri: trovi quali domande
girare al tuo direttore finanziario, e cosa succede se una delle voci manca.

---

## Le sette voci

**1. L'elaborazione, al minuto di conversazione.** Voce in ingresso, un modello che decide cosa
dire, voce in uscita, contati al minuto. È quella famosa, è davvero a consumo, e scende in modo
costante da due anni. È la voce che tutti citano perché è l'unica con un prezzo pubblicato, che
è una pessima ragione.

**2. La linea.** Un numero di telefono in ogni paese in cui vendi, a canone mensile, più i minuti
in entrata a tariffa operatore. Poco, per mercato. La cosa da notare è *per mercato*. Quattro
paesi sono quattro contratti, quattro fatture e quattro pratiche, non una voce sola con un numero
più grande.

**3. Qualcuno che ascolta.** Ogni settimana una persona estrae un campione di chiamate, le
ascolta e sistema quello che è andato storto. Non durante il progetto. Per sempre.

È la voce ricorrente più grande nella maggior parte delle operation voice, e manca da quasi tutti
i business case, perché non sembra infrastruttura. Sembra il pomeriggio di qualcuno. Resta la
differenza tra un agente che migliora e un agente che si degrada.

**4. Qualcuno che risponde alle 20.** Quando si rompe fuori orario, o paghi una persona per
essere reperibile, o la linea resta zoppa fino a lunedì. Sono due scelte entrambe legittime. Di
solito ne viene messa a budget una sola, e raramente è quella che poi si adotta.

**5. Il testing che non finisce mai.** Mantenere un set di prova, farlo girare ogni mese, e
rifarlo dopo ogni modifica alle istruzioni o al catalogo. È poco, è noioso, ed è sempre la prima
voce a saltare. È il motivo per cui tanti agenti che a marzo funzionavano a settembre non
funzionano più. [Le venti chiamate](/it/blog/voice-agent-acceptance-test) sono la versione
economica di questa voce.

**6. Ogni lingua in più.** Non è un moltiplicatore della voce 1. È una ripetizione delle voci
dalla 2 alla 5: altri numeri, un altro set di prova, un'altra sessione di ascolto settimanale. E
la parte che sorprende: un'altra persona in grado di giudicare davvero se quelle chiamate sono
andate bene. Le chiamate in olandese non le puoi rivedere con un team italiano.

**7. La ricostruzione.** Ogni diciotto mesi circa il terreno si muove sotto: i modelli cambiano,
un fornitore cambia il formato dei dati, la cosa su cui avevi costruito viene dismessa. Mettila a
budget come voce ricorrente e non come sorpresa annuale, perché è esattamente quello.

---

## La voce che ribalta tutto

Questa è la parte da portare al direttore finanziario, perché contraddice l'istinto con cui tutti
guardano alla spesa in software.

Nel software normale costruisci una volta e ogni utente in più ti costa quasi zero. È la forma
stessa del settore, ed è il motivo per cui le software company valgono tanto.

Il voice non si comporta così, perché la maggior parte del costo ricorrente è **attenzione
umana**: le voci 3, 4, 5 e metà della 6. L'attenzione umana non cresce col volume. Cresce con la
**varietà**.

Diecimila chiamate al mese su tre argomenti costano poco da gestire. Duemila chiamate al mese su
quaranta argomenti costano care, e possono facilmente costare di più in totale pur essendo un
quinto del volume. Ogni tipo di chiamata diverso vuole le sue istruzioni, i suoi casi di prova,
la sua revisione e i suoi modi di fallire, che qualcuno deve accorgersi di notare.

Quindi la domanda su cui è costruito il tuo business case è probabilmente quella sbagliata. Quasi
sempre è *quante chiamate riceviamo?* La domanda che determina davvero il costo di gestione è
**quanti tipi diversi di chiamata riceviamo**. La risposta decide se la cosa è economica o
rovinosa. Non è un dettaglio di budget: è tutto l'argomento a favore di definire il primo agente
in modo stretto.
<!-- FORWARD LINK - numero 05. Il giorno in cui esce /blog/scoping-a-voice-agent, ripristina:
     [definire il primo agente in modo stretto](/it/blog/scoping-a-voice-agent) -->

---

## Il moltiplicatore europeo

Ognuna di quelle voci umane è prezzata sul costo del lavoro locale, ed è il motivo per cui questo
business case non si trasferisce da un paese all'altro.

Nel 2025 il costo orario del lavoro nell'UE andava da 12,0 &euro; in Bulgaria a 56,8 &euro; in
Lussemburgo, contro una media UE di 34,9 &euro; e una media dell'area euro di 38,2 &euro;,
secondo Eurostat. I Paesi Bassi erano a 47,9 &euro;, la Danimarca a 51,7 &euro;, la Romania a
13,6 &euro;.

Una precisazione, perché conta: sono dati sull'intera economia, per imprese con dieci o più
dipendenti, e comprendono retribuzioni più contributi a carico del datore di lavoro. Sono un buon
riferimento per capire come varia il costo del lavoro *tra* i mercati. Non sono un preventivo per
quanto ti costa un addetto all'assistenza, e chi li usa così sta facendo un lavoro sciatto.

Usati bene, però, dicono una cosa netta. Lo stesso identico agente, sullo stesso identico volume,
ha un business case che cambia di circa quattro volte a seconda di dove si trova il tuo team di
assistenza.

E c'è una conseguenza scomoda. Gli operatori con il caso economico più forte per automatizzare
stanno nei mercati a costo più alto. Quelli più tentati di costruirselo in casa, perché lì gli
sviluppatori bravi costano poco, stanno in quelli a costo più basso. L'istinto di costruire è più
forte proprio dove il ritorno è più debole, e conviene sapere quale dei due sei prima che qualcuno
scriva una riga di codice.
<!-- FORWARD LINK - numero 07. Il giorno in cui esce /blog/voice-ai-europe-markets, ripristina:
     Ne parliamo in [perché un playbook olandese non funziona in Italia](/it/blog/voice-ai-europe-markets). -->

---

## Il modello in una pagina

Portalo a chi tiene i numeri. La colonna di destra è il lavoro da fare.

| Voce | Ricorre | Come ottenere un numero vero |
|---|---|---|
| Elaborazione al minuto | Mensile, col volume | Chiedi un preventivo sui tuoi minuti reali, non il prezzo di listino |
| Numeri e minuti operatore | Mensile, per paese | Un preventivo per ogni mercato in cui vendi |
| Ascolto e correzioni settimanali | Per sempre | Ore a settimana x il tuo costo orario pieno. Fai il nome della persona |
| Reperibilità fuori orario | Per sempre, o mai | Decidi esplicitamente. "Vedremo" costa quanto l'opzione cara |
| Testing mensile | Per sempre | Mezza giornata al mese. Mettila in agenda a qualcuno o non succede |
| Ogni lingua in più | Per mercato | Rifai le righe da 2 a 5 per quel mercato, revisore madrelingua incluso |
| Ricostruzione | Ogni 18-24 mesi | Una frazione della build iniziale, spalmata sull'anno |

Se una proposta di build copre la prima riga e nessuna delle altre, non è un preventivo di costo.
È il prezzo del componente più economico, e sbaglierà di un multiplo, non di una percentuale.

Niente di tutto questo significa che costruire in casa sia la risposta sbagliata. Per alcune
aziende è chiaramente quella giusta. Significa che la decisione va presa sul costo di gestione e
non sul costo di costruzione, perché il costo di costruzione è la parte che finisce.
<!-- FORWARD LINK - numero 04. Il giorno in cui esce /blog/build-vs-buy-voice-ai, ripristina:
     ...quella giusta, e i criteri onesti stanno in
     [quando conviene costruirselo in casa](/it/blog/build-vs-buy-voice-ai). Significa... -->

---

*The Build File è una serie per chi i progetti vocali li approva, non per chi li scrive.*

<!--
NON PUBBLICARE. Nota di verifica. publish.py rimuove i commenti HTML, quindi
questo non arriva mai in pagina: resta qui come registro delle fonti.

Ogni cifra in euro di questo post viene dai dati 2025 sul costo orario del lavoro, verificati su
due fonti indipendenti prima della stesura:
  1. Eurostat, "EU hourly labour costs ranged from EUR 12 to EUR 57 in 2025" (31 mar 2026)
     https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260331-2
  2. Plataforma Media, che riporta lo stesso comunicato Eurostat in modo indipendente
     https://www.plataformamedia.com/en/2026/03/31/eu-labour-costs-2025-portugal-19-4-euro/
  Riscontro su Eurostat Statistics Explained, "Hourly labour costs"
     https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Hourly_labour_costs

Cifre usate: UE 34,9 - area euro 38,2 - Bulgaria 12,0 - Romania 13,6 - Paesi Bassi 47,9 -
Danimarca 51,7 - Lussemburgo 56,8.

Deliberatamente NON usate: Italia, Germania, Spagna, Francia, Polonia. Il comunicato non riporta
i valori assoluti 2025 per questi paesi, solo le variazioni anno su anno. Non aggiungerli senza
andare al dataset di origine.

La precisazione sul perimetro sta nel corpo del testo e deve restarci: intera economia, imprese
con 10+ dipendenti, retribuzioni più contributi a carico del datore. Non è un dato specifico dei
contact centre.

In questo post non è citato nessun prezzo al minuto, di telefonia o di fornitore. È una scelta:
sono dati a fonte singola, si muovono ogni trimestre, e citarli data la pagina. Il post dà il
modello e dice al lettore di farsi fare i preventivi.
-->
