/* What is LEFT of the Sabato enhancements layer.

   This file used to build the footer's extra links, the nav dropdowns and the
   industries nav, and repair the Italian header. It no longer does any of that:
   header.py and footer.py render those at build time, from these same arrays.
   The four passes that became redundant were removed on 7 Aug 2026 after
   measuring - each was wrapped in a MutationObserver and 21 pages were loaded at
   1440 and 390; all four made zero DOM changes everywhere. 44KB -> 32KB.

   What remains exists because Framer's BODY content still needs it:
     * repairMistypedHrefs   the `https://it/prezzi` hrefs Framer stored
     * enforceItalianLinks   Italian body links pointing into the English site
     * wireUseCaseTargets    body tiles still ship the "/#usecases" hook
     * wireIndustryTargets   ...and inert <span>s where links belong
     * installClickInterceptor  resolves a destination from the label AT CLICK
       TIME, so a link works whether or not the wiring above has run or survived
       hydration. This is the one that must never be removed.
     * injectCustomerBand    staging-only draft, gated behind BAND_ENABLED

   Everything here writes to the DOM, which is why boot order matters - see the
   comment at the bottom of the file before changing when this runs.
   Config-driven: add a use-case page to USECASES and nav, footer and hub all
   pick it up. */
(function () {
  var IT = location.pathname === "/it" || location.pathname.indexOf("/it/") === 0;

  /* Typographic vs straight apostrophes differ between Framer pages and ours,
     so all label comparisons go through this. */
  function normLabel(x) {
    return (x || "").replace(/[\u2018\u2019\u02BC]/g, "'").replace(/\s+/g, " ").trim();
  }

  /* True if `text` is this use case's label or any known alias (the homepage
     tiles and the footer sometimes name the same workflow differently). */
  function matchesUC(text, uc) {
    var n = normLabel(text);
    if (n === normLabel(uc.label)) return true;
    var al = uc.aliases || [];
    for (var i = 0; i < al.length; i++) if (n === normLabel(al[i])) return true;
    return false;
  }

  /* Use-case pages that exist. label = exact text on the site; href = live page.
     Italian list holds only the pages actually built - unbuilt ones keep their
     original anchor so nothing links to a 404. */
  /* The `aliases` that read like abbreviations are footer.py's SHORT map: the
     footer column is a 210px track, so five entries per language are shortened
     there and the visible text is NOT the label below. resolveByLabel is the
     fallback the click interceptor uses when hydration has reverted the href,
     so a short label missing from this list means a DEAD footer link on a cold
     first load - caught by tools/test_footer_clicks.py on 17 Aug 2026, where
     "Checkout su WhatsApp" resolved to Framer's /#usecases hook.
     KEEP IN SYNC WITH footer.py's SHORT map. */
  var USECASES_EN = [
    { label: "Pre-Sales Consultation", href: "/use-cases/pre-sales-consultation" },
    { label: "Cart Abandonment Recovery", href: "/use-cases/cart-abandonment-recovery",
      aliases: ["Cart Recovery"] },
    { label: "Where Is My Order", href: "/use-cases/where-is-my-order" },
    { label: "Qualify & Collect for Quote", href: "/use-cases/qualify-and-collect-for-quote",
      aliases: ["B2B Quote Collection"] },
    { label: "Open a Complaint", href: "/use-cases/open-a-complaint" },
    { label: "Checkout Summary via Text", href: "/use-cases/checkout-summary-via-text",
      aliases: ["WhatsApp Checkout"] },
    { label: "Managing Returns", href: "/use-cases/managing-returns" },
    { label: "Post-Delivery Feedback", href: "/use-cases/post-delivery-feedback" },
    { label: "Back-in-Stock Notification", href: "/use-cases/back-in-stock-notification",
      aliases: ["Back-in-Stock Alerts"] }
  ];
  var USECASES_IT = [
    { label: "Consulenza Pre-Vendita", href: "/it/casi-duso/consulenza-pre-vendita" },
    { label: "Recupero Carrelli Abbandonati", href: "/it/casi-duso/recupero-carrelli-abbandonati",
      aliases: ["Recupero Carrelli"] },
    { label: "Dov'è il Mio Ordine", href: "/it/casi-duso/dove-e-il-mio-ordine" },
    { label: "Preventivi Automatici", href: "/it/casi-duso/preventivi-automatici" },
    { label: "Apertura Reclamo", href: "/it/casi-duso/apertura-reclamo" },
    { label: "Riepilogo Checkout via Messaggio", href: "/it/casi-duso/riepilogo-checkout-via-messaggio",
      aliases: ["Riepilogo Acquisto via SMS", "Checkout su WhatsApp"] },
    { label: "Gestione Resi", href: "/it/casi-duso/gestione-resi" },
    { label: "Feedback Post-Consegna", href: "/it/casi-duso/feedback-post-consegna",
      aliases: ["Feedback Consegna"] },
    { label: "Notifica Ritorno in Stock", href: "/it/casi-duso/notifica-ritorno-in-stock" }
  ];
  /* /it/chi-siamo renders an entire ENGLISH footer above the Italian one (the
     page was duplicated from /about in Framer and the footer component was never
     swapped). At phone width the two stack, so an Italian visitor scrolls into a
     use-case column labelled in English whose links are all still the unwired
     "../#usecases" hook - nine dead links, exactly as reported.

     Rather than special-case that page, teach the Italian entries their English
     names. Everything downstream - wireUseCaseTargets, resolveByLabel, the click
     interceptor - already matches on aliases, so this one loop fixes the labels
     wherever they appear, including any page duplicated the same way later.

     Guarded on equal length because this pairs BY INDEX: the two arrays are
     written in the same order on purpose. If someone adds a use case to one and
     not the other, do nothing rather than link Italian visitors to the wrong
     page. (The INDUSTRIES arrays are deliberately NOT paired this way - their
     order does differ, which is why those entries carry hand-written aliases.) */
  if (USECASES_EN.length === USECASES_IT.length) {
    for (var uci = 0; uci < USECASES_IT.length; uci++) {
      USECASES_IT[uci].aliases =
        (USECASES_IT[uci].aliases || []).concat([USECASES_EN[uci].label]);
    }
  }

  var USECASES = IT ? USECASES_IT : USECASES_EN;

  /* Industry pages, both languages. The Italian footer names some categories
     differently between the Framer build and our own templates (and left
     "Home Improvement" untranslated), so aliases carry the variants. */
  var INDUSTRIES_EN = [
    { label: "Home Improvement", href: "/industries/home-improvement" },
    { label: "Automotive & Parts", href: "/industries/automotive-parts" },
    { label: "Electronics & Tech", href: "/industries/electronics-tech" },
    { label: "Furniture & Home", href: "/industries/furniture-home" },
    { label: "Outdoor & Garden", href: "/industries/outdoor-garden" },
    { label: "Fashion & Apparel", href: "/industries/fashion-apparel" },
    { label: "Health & Wellness", href: "/industries/health-wellness" },
    { label: "Sports & Fitness", href: "/industries/sports-fitness" },
    { label: "Industrial & B2B", href: "/industries/industrial-b2b" }
  ];
  var INDUSTRIES_IT = [
    { label: "Clima e Riscaldamento", href: "/it/settori/clima-e-riscaldamento", aliases: ["Home Improvement", "Miglioramento Casa"] },
    { label: "Automotive e Ricambi", href: "/it/settori/ricambi-auto", aliases: ["Automotive & Parts"] },
    { label: "Elettronica e Tech", href: "/it/settori/elettronica", aliases: ["Electronics & Tech"] },
    { label: "Arredamento e Casa", href: "/it/settori/arredamento", aliases: ["Furniture & Home"] },
    { label: "Industria e B2B", href: "/it/settori/industria-b2b", aliases: ["Industrial & B2B"] },
    { label: "Outdoor e Giardino", href: "/it/settori/giardino-outdoor", aliases: ["Outdoor & Garden"] },
    { label: "Fashion e Abbigliamento", href: "/it/settori/moda-abbigliamento", aliases: ["Fashion & Apparel"] },
    { label: "Salute e Benessere", href: "/it/settori/salute-benessere", aliases: ["Health & Wellness"] },
    { label: "Sport e Fitness", href: "/it/settori/sport-fitness", aliases: ["Sports & Fitness"] }
  ];
  var INDUSTRIES = IT ? INDUSTRIES_IT : INDUSTRIES_EN;


  /* ---------- 0. Repair malformed hrefs authored in Framer ----------
     Four Italian pages ship footer links written as `it/prezzi` in Framer's URL
     field, which Framer stored as `https://it/prezzi` - an absolute URL whose
     HOSTNAME is "it". Clicking them leaves the site and fails to resolve. They
     also carry target="_blank".

     Fixing the static HTML is not enough: Framer's client runtime re-hydrates
     these anchors from its own bundle and puts the bad href back. Verified 6 Aug
     2026 - the served HTML contained 0 occurrences while the live DOM had 3. So
     the repair has to run here, after hydration.

     Generic on purpose: any http(s) URL whose host contains no dot cannot be a
     real domain, so it is a mistyped path. Rewriting it root-relative fixes this
     class of Framer authoring error, not just the three we found. */
  /* ---------- OUR FOOTER IS OFF LIMITS ----------
     site/css/footer.css hides Framer's footer and footer.py renders ours, with
     real absolute hrefs, correct per language, generated at build time from the
     same arrays this file uses. Nothing in here needs to repair it, and every
     function that tried would do damage:

       * enforceItalianLinks would rewrite the language switcher (an anchor
         pointing at the other language ON PURPOSE) straight back to this one.
       * injectFooterLinks would clone the lowest "Book a Demo" - which is now
         inside our footer - and inject a duplicate Blog link next to the real
         one already in the Company column.
       * wireUseCaseTargets / wireIndustryTargets look for "/#usecases" hooks and
         inert <span>s. Ours has neither.

     So every rewriting pass skips it. This is the whole point of the rebuild:
     the footer stops being something that gets patched at runtime. */
  /* ours() survives on its own: repairMistypedHrefs and enforceItalianLinks
     still run, and both must keep their hands off the header and footer that
     header.py and footer.py now own. The haveOurFooter/haveOurHeader guards are
     gone with the passes that used them. */
  function ours(el) {
    return !!(el && el.closest && el.closest(".sb-footer, .sb-header"));
  }



  function repairMistypedHrefs() {
    var as = document.querySelectorAll('a[href^="http://"], a[href^="https://"]');
    for (var i = 0; i < as.length; i++) {
      var a = as[i], h = a.getAttribute("href") || "";
      if (ours(a)) continue;
      var m = h.match(/^https?:\/\/([^\/?#]+)(\/[^?#]*)?/);
      if (!m) continue;
      var host = m[1];
      if (host.indexOf(".") !== -1 || host.indexOf(":") !== -1) continue; /* real domain */
      a.setAttribute("href", "/" + host + (m[2] || ""));
      a.removeAttribute("target");
      a.removeAttribute("rel");
    }
  }

  /* ---------- 0b. Keep Italian pages inside the Italian site ----------
     Audited 6 Aug 2026 at 390px and 1440px: /it/chi-siamo renders TWO footers
     stacked - an English one (logo and Home -> "/", Pricing -> "/pricing",
     About -> "/about", Contact -> "/contact") sitting directly above the
     Italian one. The Italian page was built by duplicating the English one in
     Framer and that footer component was never swapped, so an Italian visitor
     who scrolls down is one tap from the English site, with English labels.
     Reported as "the Italian footer is all over the place", worst on mobile
     because the two footers stack instead of sitting side by side.

     Fixed here rather than in the HTML because Framer re-hydrates these anchors
     from its own bundle and puts the English hrefs back - the same reason
     repairMistypedHrefs() lives here.

     Deliberately NOT rewritten:
       * the language switcher (the flag anchors) - pointing at the English site
         is its entire job. Detected by the regional-indicator characters that
         make up a flag emoji.
       * /terms and /privacy-policy - those pages exist in English only, so the
         link is correct even on an Italian page. Their LABELS are still English
         in the Italian footer; that is a copy decision, not a bug, and is left
         alone on purpose. */
  var IT_PATH = {
    "/": "/it",
    "/pricing": "/it/prezzi",
    "/about": "/it/chi-siamo",
    "/contact": "/it/contatti",
    "/blog": "/it/blog",
    "/use-cases": "/it/casi-duso",
    "/industries": "/it/settori"
  };
  var IT_LABEL = {
    "Home": "Home", "Pricing": "Prezzi", "About": "Chi Siamo",
    "Contact": "Contatti", "Contact us": "Contattaci", "Blog": "Blog",
    "Book a Demo": "Prenota una Demo"
  };
  /* U+1F1E6-U+1F1FF are the regional indicators a flag emoji is built from. */
  var FLAG = /[\uD83C][\uDDE6-\uDDFF]/;

  function enforceItalianLinks() {
    if (!IT) return;
    var as = document.querySelectorAll("a[href]");
    for (var i = 0; i < as.length; i++) {
      var a = as[i];
      if (ours(a)) continue;                                  /* footer.py owns it */
      if (a.hasAttribute("data-lang-switch")) continue;       /* deliberate */
      if (FLAG.test(a.textContent || "")) continue;           /* language switcher */
      var raw = a.getAttribute("href") || "";
      if (raw.indexOf("http") === 0) continue;
      /* ANY fragment, not just a leading "#". The nav's use-case and industry
         hooks are written "/#usecases" and "/#casiduso" - their pathname is "/",
         so an earlier version of this mapped them to "/it" and destroyed the
         hook wireUseCaseTargets() retargets. Caught by the footer click test:
         "Gestione Resi" started landing on /it. Those anchors have an owner
         already; this function is not it. */
      if (raw.indexOf("#") !== -1) continue;
      /* Resolve ./ and ../ the browser's own way before deciding. */
      var path;
      try { path = new URL(a.href).pathname; } catch (e) { continue; }
      if (path.length > 1) path = path.replace(/\/$/, "");
      var want = IT_PATH[path];
      if (!want) continue;
      if (raw !== want) a.setAttribute("href", want);
      var holder = a.querySelector("p, span, h1, h2, h3, h4, h5, h6") || a;
      if (holder.children.length) continue;                   /* not a plain label */
      var it = IT_LABEL[normLabel(holder.textContent)];
      if (it && normLabel(holder.textContent) !== it) holder.textContent = it;
    }
  }

  /* ---------- 3. Retarget footer links + make matching tiles clickable ----------
     Two DOM shapes exist: Framer pages nest the label in a <p>/<span> inside the
     <a>; our own templates put the text directly in the <a>. Handle both. */
  function wireUseCaseTargets() {
    for (var i = 0; i < USECASES.length; i++) {
      (function (uc) {
        /* 3a. anchors whose own text is the label (our templates) */
        var anchors = document.querySelectorAll('a[href*="#usecases"], a[href*="#casiduso"]');
        for (var m = 0; m < anchors.length; m++) {
          var an = anchors[m];
          if (!matchesUC(an.textContent, uc)) continue;
          if (an.getAttribute("data-uc-wired") === "1") continue;
          an.href = uc.href;
          an.setAttribute("data-uc-wired", "1");
        }

        /* 3b. label nested in a text element (Framer pages) */
        var nodes = document.querySelectorAll("p, span, h1, h2, h3, h4, h5, h6");
        for (var k = 0; k < nodes.length; k++) {
          var el = nodes[k];
          if (el.children.length !== 0) continue;
          if (!matchesUC(el.textContent, uc)) continue;
          var anchor = el.closest("a");
          if (anchor) {
            var href = anchor.getAttribute("href") || "";
            if ((href.indexOf("#usecases") !== -1 || href.indexOf("#casiduso") !== -1) && anchor.getAttribute("data-uc-wired") !== "1") {
              anchor.href = uc.href;
              anchor.setAttribute("data-uc-wired", "1");
            }
          } else {
            /* homepage tile: climb to the card container and make it clickable */
            var card = el;
            for (var d = 0; d < 5 && card.parentElement; d++) {
              card = card.parentElement;
              if (card.clientHeight > 120 && card.clientWidth > 180) break;
            }
            if (card.getAttribute("data-uc-wired") === "1") continue;
            card.setAttribute("data-uc-wired", "1");
            card.style.cursor = "pointer";
            card.addEventListener("click", function (e) {
              if (e.target.closest("a")) return; /* don't hijack real links inside */
              window.location.href = uc.href;
            });
          }
        }
      })(USECASES[i]);
    }
  }

  /* ---------- Footer industry links ----------
     On Framer pages these labels sit inside <a> elements that have no href at
     all, so they need one setting rather than retargeting - a different repair
     from the use-case links, which had a wrong href. */
  function wireIndustryTargets() {
    for (var i = 0; i < INDUSTRIES.length; i++) {
      (function (ind) {
        var all = document.querySelectorAll("a");
        for (var j = 0; j < all.length; j++) {
          var a = all[j];
          if (a.hasAttribute("data-ind-link")) continue;
          if (!matchesUC(a.textContent || "", ind)) continue;
          if (a.getAttribute("href") === ind.href) continue;
          a.setAttribute("href", ind.href);
          a.removeAttribute("target");
          a.removeAttribute("rel");
        }
      })(INDUSTRIES[i]);
    }
  }

  /* Resolve a destination from an element's own label, for when the DOM has not
     been wired yet. Leaf nodes only, short text only, so a click on a container
     cannot match half the page. */
  function resolveByLabel(node) {
    if (!node || (node.children && node.children.length)) return null;
    var t = normLabel(node.textContent || "");
    if (!t || t.length > 40) return null;
    var i;
    for (i = 0; i < USECASES.length; i++) if (matchesUC(t, USECASES[i])) return USECASES[i].href;
    for (i = 0; i < INDUSTRIES.length; i++) if (matchesUC(t, INDUSTRIES[i])) return INDUSTRIES[i].href;
    return null;
  }

  function installClickInterceptor() {
    if (window.__ucClickInterceptor) return;
    window.__ucClickInterceptor = true;
    window.addEventListener("click", function (e) {
      /* deliberately NOT checking e.defaultPrevented: Framer's router may already
         have cancelled the event (it registers on the same target/phase before us),
         and for our own pages we want to override that and navigate anyway. */
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var node = e.target;
      var a = node && node.closest ? node.closest("a") : null;
      var href = a ? (a.getAttribute("href") || "") : "";
      var ours = href.indexOf("/use-cases/") === 0 || href.indexOf("/it/casi-duso/") === 0 ||
                 href.indexOf("/industries/") === 0 || href === "/industries" ||
                 href.indexOf("/it/settori/") === 0 || href === "/it/settori" ||
                 /* `a &&` is load-bearing. Framer renders the homepage tiles with
                    NO anchor at all, so `a` is null there - and an unguarded
                    a.hasAttribute() threw a TypeError that killed this handler
                    before the label fallback below could run. The one case the
                    fallback exists for was the one case it never reached.
                    Found 7 Aug 2026 by clicking "Gestione Resi" on live /it. */
                 (a && a.hasAttribute("data-blog-link")) || href === "/blog" || href === "/it/blog" ||
                 (a && a.hasAttribute("data-roi-link")) || href === "/roi-calculator" ||
                 href.indexOf("/customers/") === 0 ||
                 href.indexOf("/it/clienti/") === 0;
      /* TIMING-PROOF FALLBACK.
         Everything above assumes wireUseCaseTargets()/wireIndustryTargets() has
         already rewritten this anchor. On a cold first load that is not
         guaranteed: enhance.js is a separate request while Framer's bundles
         hydrate, and hydration is known to revert our DOM edits (proved 6 Aug
         2026 - the served HTML had 0 malformed hrefs while the live DOM had 3).
         Reported symptom: footer links do nothing on the first visit, then work
         after a reload.

         So if the anchor still carries the /#usecases hook - or there is no
         anchor at all, because Framer renders the footer entry as a <span> -
         resolve the destination from the label instead. Then the click works
         whether or not any wiring has run. */
      if (!ours) {
        var hooked = !a || href === "" || href === "#" ||
                     href.indexOf("#usecases") !== -1 || href.indexOf("#casiduso") !== -1;
        if (hooked) {
          var alt = resolveByLabel(node);
          if (!alt && a) alt = resolveByLabel(a.querySelector("p, span, h3, h4") || a);
          if (alt) { href = alt; ours = true; }
        }
      }
      if (!ours) return;
      if (a && a.target === "_blank") return;
      e.preventDefault();
      e.stopImmediatePropagation();
      window.location.assign(href);
    }, true);
  }

  /* ---------- 6. Customer stories band on the homepage ----------
     DRAFT. Placeholders render as loud orange TBC chips and the band is only
     injected on staging hosts - see BAND_ENABLED below.

     Why this is injected rather than written into index.html: Framer pages are
     React-hydrated, so markup added to the HTML is thrown away the moment React
     takes over. (That is exactly how an earlier copy fix appeared to ship while
     staying visibly broken.) Injecting after hydration, and re-asserting on the
     MutationObserver pass that already drives this file, is the only placement
     that survives.

     Position: directly after the workflows section. That is the moment the
     visitor has understood what the product does and is silently asking whether
     it works for someone like them - and it puts evidence immediately before
     the 9 / 24-7 / 2-weeks stat block, so those read as track record rather
     than claim. */
  var BAND_ANCHOR = IT ? "Scegli i workflow. Al resto pensiamo noi."
                       : "Pick the workflows that move your numbers";
  var BAND_COPY = IT
    ? { eyebrow: "Storie dei clienti", h2: "Cataloghi veri, chiamate vere",
        sub: "Due e-commerce dove il telefono era il collo di bottiglia.",
        cta: "Leggi la storia" }
    : { eyebrow: "Customer stories", h2: "Real catalogues, real calls",
        sub: "Two stores where the phone was the bottleneck.",
        cta: "Read the full story" };

  var BAND_ITEMS = [
    { slug: "clima-convenienza", name: "ClimaConvenienza", initials: "CC",
      metric: "53.1%", ph: false,
      label: IT ? "delle chiamate gestite in autonomia - 9 agenti live in 3 lingue"
                : "of calls handled autonomously - 9 agents live across 3 languages",
      person: "Alessio Perrucci", role: "CEO" },
    { slug: "creative-cables", name: "Creative Cables", initials: "CC",
      metric: "39%", ph: false,
      label: IT ? "delle chiamate risolte dall'inizio alla fine nel primo mese"
                : "of calls resolved end to end in the first month",
      person: "Marco Logreco", role: "Head of E-Commerce" }
  ];

  /* OFF EVERYWHERE, including staging. Daniel's call, 5 Aug 2026: the two
     customers have not signed off on their stories being used as homepage
     marketing, and what belongs on the homepage is a design decision he has
     not made yet - it may not be this band at all.

     Do NOT flip this back on to "just show him what it looks like". Named
     customers and their metrics do not go in front of visitors before the
     customers have approved it, and that approval is Daniel's to obtain, not
     something a session can infer from the figures being confirmed. The
     /customers/ pages themselves stay built, noindex and unlinked.

     The band below is kept as reference for whatever replaces it. */
  var BAND_ENABLED = false;

  var BAND_CSS =
    ".sb-cust{max-width:1200px;width:calc(100% - 80px);margin:0 auto;background:#000;" +
    "border-radius:24px;padding:76px 48px;font-family:'Satoshi',Inter,-apple-system,sans-serif}" +
    ".sb-cust .sb-eyebrow{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;" +
    "color:rgb(204,255,0);text-align:center;margin:0 0 14px}" +
    ".sb-cust h2{font-size:42px;font-weight:700;letter-spacing:-1.2px;line-height:1.15;color:#fff;" +
    "text-align:center;margin:0 0 12px}" +
    ".sb-cust .sb-sub{font-size:18px;line-height:1.7;color:rgba(255,255,255,.66);text-align:center;" +
    "max-width:620px;margin:0 auto 46px}" +
    ".sb-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:1000px;margin:0 auto}" +
    ".sb-card,.sb-card *{text-decoration:none!important}" +
    ".sb-card{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:18px;" +
    "padding:34px 30px;display:flex;flex-direction:column;gap:6px;transition:border-color .2s,background .2s}" +
    ".sb-card:hover{background:rgba(255,255,255,.09);border-color:rgba(204,255,0,.45)}" +
    ".sb-brand{display:flex;align-items:center;gap:10px;margin-bottom:18px}" +
    ".sb-mono{width:32px;height:32px;border-radius:9px;background:rgb(204,255,0);color:#000;display:grid;" +
    "place-items:center;font-size:12px;font-weight:900}" +
    ".sb-brand b{font-size:13px;font-weight:800;color:rgba(255,255,255,.75);letter-spacing:.13em;text-transform:uppercase}" +
    ".sb-num{font-size:58px;font-weight:900;letter-spacing:-2px;line-height:1;color:rgb(204,255,0)}" +
    ".sb-lab{font-size:15px;line-height:1.6;color:#fff;margin-top:10px}" +
    ".sb-who{font-size:14px;line-height:1.6;color:rgba(255,255,255,.55);margin-top:20px}" +
    ".sb-more{font-size:15px;font-weight:700;color:rgb(204,255,0);margin-top:22px}" +
    ".sb-ph{display:inline-block;border:2px dashed rgb(255,138,0);background:rgba(255,138,0,.16);" +
    "border-radius:8px;padding:0 10px;color:rgb(255,176,92)}" +
    "@media(max-width:809px){.sb-cust{width:calc(100% - 32px);padding:56px 24px}" +
    ".sb-cust h2{font-size:30px}.sb-grid{grid-template-columns:1fr}.sb-num{font-size:46px}}";

  function injectCustomerBand() {
    if (!BAND_ENABLED) return;
    if (document.querySelector("[data-sb-cust]")) return;

    var anchor = null;
    var hs = document.querySelectorAll("h1, h2");
    for (var i = 0; i < hs.length; i++) {
      if (normLabel(hs[i].textContent) === normLabel(BAND_ANCHOR)) {
        anchor = hs[i].closest("section"); break;
      }
    }
    if (!anchor || !anchor.parentElement) return;

    if (!document.getElementById("sb-cust-css")) {
      var st = document.createElement("style");
      st.id = "sb-cust-css"; st.textContent = BAND_CSS;
      (document.head || document.documentElement).appendChild(st);
    }

    var cards = "";
    for (var j = 0; j < BAND_ITEMS.length; j++) {
      var c = BAND_ITEMS[j];
      var num = c.ph ? '<span class="sb-ph">' + c.metric + "</span>" : c.metric;
      var lab = c.ph ? '<span class="sb-ph">' + c.label + "</span>" : c.label;
      cards +=
        '<a class="sb-card" href="' + (IT ? "/it/clienti/" : "/customers/") + c.slug + '">' +
          '<span class="sb-brand"><b>' + c.name + "</b></span>" +
          '<span class="sb-num">' + num + "</span>" +
          '<span class="sb-lab">' + lab + "</span>" +
          '<span class="sb-who">' + c.person + " · " + c.role + ", " + c.name + "</span>" +
          '<span class="sb-more">' + BAND_COPY.cta + " &rarr;</span>" +
        "</a>";
    }

    var wrap = document.createElement("div");
    wrap.setAttribute("data-sb-cust", "1");
    wrap.style.cssText = "margin:96px 0 0";
    wrap.innerHTML =
      '<section class="sb-cust">' +
        '<p class="sb-eyebrow">' + BAND_COPY.eyebrow + "</p>" +
        "<h2>" + BAND_COPY.h2 + "</h2>" +
        '<p class="sb-sub">' + BAND_COPY.sub + "</p>" +
        '<div class="sb-grid">' + cards + "</div>" +
      "</section>";
    anchor.parentElement.insertBefore(wrap, anchor.nextSibling);
  }

  /* THE PRODUCT SHOWCASE - replaces Framer's "Pick the workflows" section.

     Same reasoning as injectCustomerBand: this section is Framer BODY content,
     React-hydrated, so editing index.html does nothing that survives. We find
     the section by its own heading text, keep its eyebrow pill / h2 / sub
     ELEMENTS (so the typography stays Framer's, not ours) and swap only their
     text, then replace the card rows with five tabs over the product
     screenshots.

     Idempotence matters more here than in the band, because this pass runs on
     every observer tick: setText() writes only when the string actually
     differs, so a steady state produces zero mutations and the observer
     settles. The tab markup is guarded on data-sb-prod.

     The screenshots are the real product exports at /product/assets/*.webp -
     the same files the five product pages use, so there is nothing new to ship
     and nothing to keep in sync. */
  var PROD_ANCHOR = IT ? "Scegli i workflow. Al resto pensiamo noi."
                       : "Pick the workflows that move your numbers";

  var PROD_COPY = IT
    ? { pill: "Prodotto",
        h2: "Un agente al telefono. <br>Dietro, un'intera operazione.",
        sub: "Cinque schermate, un prodotto. È quello che gira mentre i tuoi " +
             "clienti parlano, e puoi leggerlo tutto.",
        explore: "Scopri" }
    : { pill: "Product",
        h2: "One agent on the line. <br>A whole operation behind it.",
        sub: "Five screens, one product. This is what runs while your customers " +
             "talk, and everything in it is readable by you.",
        explore: "Explore" };

  var PROD_ICONS = {
    build: '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/><path d="M10 6.5h5a2 2 0 0 1 2 2V14"/>',
    automate: '<path d="M13 2 4.5 13H11l-1 9 9.5-12H13z"/>',
    understand: '<path d="M4 20V10M9.5 20V4M15 20v-7M20.5 20v-4"/>',
    improve: '<path d="M21 12a9 9 0 1 1-3.2-6.9"/><path d="M8.5 11.8 11.4 15 21 5.4"/>',
    connect: '<path d="M10.5 13.5a4 4 0 0 0 5.7 0l2.9-2.9a4 4 0 0 0-5.7-5.7l-1.4 1.4"/>' +
             '<path d="M13.5 10.5a4 4 0 0 0-5.7 0l-2.9 2.9a4 4 0 0 0 5.7 5.7l1.4-1.4"/>'
  };

  var PROD_TABS = IT
    ? [{ k: "build", tab: "Costruisci", shot: "voice-agent-builder", name: "Voice Agent Builder",
         tag: "Il tuo agente, le sue regole, i suoi strumenti, su una tela che sai leggere.",
         href: "/it/prodotto/voice-agent-builder" },
       { k: "automate", tab: "Automatizza", shot: "workflow-builder", name: "Workflow Builder",
         tag: "Cosa succede dopo la chiamata: il tag, il ticket, il follow-up, senza nessuno.",
         href: "/it/prodotto/workflow-builder" },
       { k: "understand", tab: "Capisci", shot: "call-data-intelligence", name: "Call Data Intelligence",
         tag: "Ogni chiamata trascritta e cercabile. Cosa chiedono, cosa non hai, cosa non funziona.",
         href: "/it/prodotto/call-data-intelligence" },
       { k: "improve", tab: "Migliora", shot: "agent-evaluation", name: "Agent Evaluation",
         tag: "Rivediamo le chiamate, troviamo le lacune, pubblichiamo la correzione. Tu guardi.",
         href: "/it/prodotto/agent-evaluation" },
       { k: "connect", tab: "Collega", shot: "integrations-webhooks", name: "Integrazioni &amp; Webhook",
         tag: "Nativo con Shopify, 8.500+ app via Zapier, un webhook per tutto il resto.",
         href: "/it/prodotto/integrations-webhooks" }]
    : [{ k: "build", tab: "Build", shot: "voice-agent-builder", name: "Voice Agent Builder",
         tag: "Your agent, its rules, its tools, designed with you on a canvas you can read.",
         href: "/product/voice-agent-builder" },
       { k: "automate", tab: "Automate", shot: "workflow-builder", name: "Workflow Builder",
         tag: "What happens after the call: the tag, the ticket, the follow-up, without a person.",
         href: "/product/workflow-builder" },
       { k: "understand", tab: "Understand", shot: "call-data-intelligence", name: "Call Data Intelligence",
         tag: "Every call, transcribed and searchable. What they asked, what you don't stock, what broke.",
         href: "/product/call-data-intelligence" },
       { k: "improve", tab: "Improve", shot: "agent-evaluation", name: "Agent Evaluation",
         tag: "We review the calls, find the gaps, publish the fix. You watch it happen.",
         href: "/product/agent-evaluation" },
       { k: "connect", tab: "Connect", shot: "integrations-webhooks", name: "Integrations &amp; Webhooks",
         tag: "Native with Shopify, 8,500+ apps via Zapier, a webhook for everything else.",
         href: "/product/integrations-webhooks" }];

  /* Pills borrow the Book-a-Call lime for the active state and the site's
     #F9FAFD card grey for the rest, so nothing new enters the palette. The
     screenshot frame is the ink used on the product pages. */
  var PROD_CSS =
    ".sb-prod-pills{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:0 0 26px}" +
    ".sb-prod-pill{display:inline-flex;align-items:center;gap:9px;background:#F9FAFD;" +
    "border:1px solid #e3e2e2;border-radius:999px;padding:13px 24px;cursor:pointer;" +
    "font-family:Satoshi,Inter,sans-serif;font-weight:700;font-size:16px;line-height:1;" +
    "color:rgb(11,11,12);transition:background .18s,border-color .18s}" +
    ".sb-prod-pill svg{width:18px;height:18px;flex:none}" +
    ".sb-prod-pill[aria-selected=true]{background:rgb(204,255,0);border-color:rgb(204,255,0)}" +
    ".sb-prod-panel{display:none}.sb-prod-panel.is-on{display:block;animation:sbProdIn .22s ease-out}" +
    "@keyframes sbProdIn{from{opacity:0}to{opacity:1}}" +
    "@media(prefers-reduced-motion:reduce){.sb-prod-panel.is-on{animation:none}}" +
    ".sb-prod-shot{background:rgb(11,11,12);border-radius:24px;padding:12px}" +
    ".sb-prod-shot img{display:block;width:100%;height:auto;border-radius:14px}" +
    ".sb-prod-cap{display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;margin:20px 6px 0}" +
    ".sb-prod-cap b{font-weight:700;font-size:20px;color:rgb(11,11,12)}" +
    ".sb-prod-cap span{font-size:16px;color:rgb(111,106,102);flex:1;min-width:280px}" +
    ".sb-prod-cap a{font-weight:700;font-size:16px;color:rgb(11,11,12);text-decoration:none;" +
    "white-space:nowrap;border-bottom:2px solid rgb(204,255,0);padding-bottom:2px}" +
    "@media(max-width:809px){.sb-prod-pills{gap:8px;margin-bottom:20px}" +
    ".sb-prod-pill{padding:10px 16px;font-size:14px}.sb-prod-pill svg{width:15px;height:15px}" +
    ".sb-prod-shot{border-radius:16px;padding:7px}.sb-prod-shot img{border-radius:9px}" +
    ".sb-prod-cap{gap:8px;margin-top:16px}.sb-prod-cap b{font-size:17px}" +
    ".sb-prod-cap span{font-size:14.5px;min-width:0;flex:1 1 100%}}";

  /* Writes only when the value actually changes. Without this the pass feeds
     the MutationObserver on every tick. */
  function setText(el, txt) {
    if (el && el.textContent !== txt) el.textContent = txt;
  }
  function setHTML(el, htm) {
    if (el && el.innerHTML !== htm) el.innerHTML = htm;
  }

  function replaceWorkflowsWithProduct() {
    var sec = null;
    var hs = document.querySelectorAll("h2");
    for (var i = 0; i < hs.length; i++) {
      var t = normLabel(hs[i].textContent);
      if (t === normLabel(PROD_ANCHOR) || t === normLabel(stripTags(PROD_COPY.h2))) {
        sec = hs[i].closest("section"); break;
      }
    }
    if (!sec) return;

    var h2 = sec.querySelector("h2");
    if (!h2) return;

    /* Framer's shape here is section > column > [heading block, card row,
       card row, card row]. Find the column and the heading block by
       containment rather than by class - the hashed class names change every
       time the Framer project is republished. */
    var inner = sec.firstElementChild;
    if (!inner || !inner.contains(h2)) return;
    var head = null, kids = inner.children;
    for (var k = 0; k < kids.length; k++) if (kids[k].contains(h2)) head = kids[k];
    if (!head) return;

    /* The eyebrow pill and the sub are the section's own elements - only their
       text changes, so Framer keeps owning the type. Both are scoped to the
       heading block, so a card title can never be mistaken for the sub. */
    var pill = head.querySelector("a p, a span");
    if (pill && normLabel(pill.textContent).length < 40) setText(pill, PROD_COPY.pill);
    setHTML(h2, PROD_COPY.h2);
    /* Framer splits the sub into two paragraphs on /it and one on / - take the
       first for the new copy and fold the rest away. Hidden rather than
       removed: React owns these nodes and puts back anything we delete. */
    var ps = head.querySelectorAll("p"), got = false;
    for (var j = 0; j < ps.length; j++) {
      if (ps[j] === pill || pill_contains(pill, ps[j])) continue;
      if (!got) { setText(ps[j], PROD_COPY.sub); got = true; }
      else if (ps[j].style.display !== "none") ps[j].style.display = "none";
    }

    if (sec.querySelector("[data-sb-prod]")) return;

    if (!document.getElementById("sb-prod-css")) {
      var st = document.createElement("style");
      st.id = "sb-prod-css"; st.textContent = PROD_CSS;
      (document.head || document.documentElement).appendChild(st);
    }

    var rows = [];
    for (var q = 0; q < kids.length; q++) if (kids[q] !== head) rows.push(kids[q]);

    var pills = "", panels = "";
    for (var n = 0; n < PROD_TABS.length; n++) {
      var tb = PROD_TABS[n], on = n === 0;
      pills +=
        '<button class="sb-prod-pill" type="button" role="tab" data-i="' + n + '" ' +
        'aria-selected="' + (on ? "true" : "false") + '">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        PROD_ICONS[tb.k] + "</svg><span>" + tb.tab + "</span></button>";
      panels +=
        '<div class="sb-prod-panel' + (on ? " is-on" : "") + '" data-p="' + n + '">' +
          '<div class="sb-prod-shot"><picture>' +
            '<source media="(max-width: 810px)" srcset="/product/assets/' + tb.shot + '-phone.webp">' +
            '<img src="/product/assets/' + tb.shot + '.webp" width="1560" height="796" ' +
            'loading="lazy" decoding="async" alt="' + tb.name + '">' +
          "</picture></div>" +
          '<div class="sb-prod-cap"><b>' + tb.name + "</b><span>" + tb.tag + "</span>" +
          '<a href="' + tb.href + '">' + PROD_COPY.explore + " &rarr;</a></div>" +
        "</div>";
    }

    var wrap = document.createElement("div");
    wrap.setAttribute("data-sb-prod", "1");
    wrap.innerHTML = '<div class="sb-prod-pills" role="tablist">' + pills + "</div>" + panels;
    inner.appendChild(wrap);
    for (var r = 0; r < rows.length; r++) rows[r].remove();

    /* PRELOAD THE OTHER FOUR SCREENSHOTS.

       The inactive panels are display:none, so the browser has no reason to
       fetch their images until the moment they are shown - which is exactly
       when the visitor is looking at them. The first click on each tab
       therefore rendered an empty frame that filled in a beat later.

       Warming them eagerly at page load would be the wrong trade: five product
       exports is ~1MB of WebP on a page most visitors never scroll this far
       down. So fetch them when the browser says it is idle, and again on the
       first hover or keyboard focus over the pill row, whichever comes first -
       a mouse arriving at the pills is the earliest honest signal that a click
       is coming, and it beats the click by enough to matter.

       Only the variant the current viewport would actually use is warmed, so a
       phone does not pull four 3120px exports over mobile data. */
    var warmed = false;
    function warmShots() {
      if (warmed) return;
      warmed = true;
      var phone = window.matchMedia && window.matchMedia("(max-width: 810px)").matches;
      for (var w = 0; w < PROD_TABS.length; w++) {
        var im = new Image();
        im.decoding = "async";
        im.src = "/product/assets/" + PROD_TABS[w].shot + (phone ? "-phone" : "") + ".webp";
      }
    }
    if (window.requestIdleCallback) window.requestIdleCallback(warmShots, { timeout: 3000 });
    else setTimeout(warmShots, 1800);
    wrap.addEventListener("pointerenter", warmShots, true);
    wrap.addEventListener("focusin", warmShots);

    wrap.addEventListener("click", function (e) {
      var btn = e.target && e.target.closest ? e.target.closest(".sb-prod-pill") : null;
      if (!btn) return;
      var bs = wrap.querySelectorAll(".sb-prod-pill");
      for (var a = 0; a < bs.length; a++) bs[a].setAttribute("aria-selected", "false");
      btn.setAttribute("aria-selected", "true");
      var pn = wrap.querySelectorAll(".sb-prod-panel");
      for (var c = 0; c < pn.length; c++) pn[c].classList.remove("is-on");
      var want = wrap.querySelector('.sb-prod-panel[data-p="' + btn.getAttribute("data-i") + '"]');
      if (want) want.classList.add("is-on");
    });
  }

  function stripTags(s) { return (s || "").replace(/<[^>]*>/g, " "); }

  /* True when `el` sits inside the eyebrow pill's own anchor - the pill's text
     node is a <p> too, so it has to be excluded from the sub hunt. */
  function pill_contains(pill, el) {
    if (!pill) return false;
    var a = pill.closest ? pill.closest("a") : null;
    return !!(a && a.contains(el));
  }

  /* Measured 7 Aug 2026 by wrapping every pass in a MutationObserver and
     loading 21 pages at 1440 and 390: restoreChiSiamo, injectFooterLinks,
     injectIndustriesNav and injectDropdown made ZERO DOM changes on every page
     at both widths, because header.py and footer.py now render what they used
     to graft on. They are gone.

     What survives, and why - same measurement:
       wireUseCaseTargets   360 writes  Framer's BODY tiles still ship the
       wireIndustryTargets  162 writes  "/#usecases" hook and inert <span>s
       enforceItalianLinks   19 writes  Italian body links into the English site
       repairMistypedHrefs   10 writes  the https://it/prezzi hrefs, phone only
     installClickInterceptor shows 0 because it only adds a listener - it is the
     timing-proof click path and must stay. injectCustomerBand is a staging-only
     draft behind BAND_ENABLED. */
  function run() {
    repairMistypedHrefs();
    enforceItalianLinks();
    wireUseCaseTargets(); wireIndustryTargets(); installClickInterceptor();
    injectCustomerBand();
    replaceWorkflowsWithProduct();
  }
  /* SELF-FEEDING OBSERVER - fixed 6 Aug 2026.

     This used to be `new MutationObserver(run)`. run() writes to the DOM, so
     every write we made re-triggered the observer, which called run() again,
     which wrote again. Measured on the local build: ~5,200 mutation records in
     the first 300ms and a steady ~180/second afterwards that NEVER settles.

     That is not just wasted CPU. A browser only fires `click` when mousedown and
     mouseup land on the same node - so if React replaces a footer node between
     the two, no click event is generated at all and no click handler, ours
     included, can rescue it. That is the reported symptom: footer links that do
     nothing, intermittently, worse right after a page appears.

     So: coalesce to at most one pass per animation frame, and deafen the
     observer while that pass runs so our own edits cannot feed back into it. */
  var __mo = null, __pending = false, __busy = false;

  /* NOTE: an earlier version of this also disconnected the observer for the
     duration of the pass. That lost every mutation Framer made while we were
     running - and Framer hydrates exactly then. Caught by tools/audit_links.py:
     the footer logo on /it/prezzi and /it/contatti at 390px stayed pointed at
     the English home because the pass that would have fixed it never fired.
     Coalescing alone is enough: run() is idempotent, so a pass triggered by our
     own writes finds nothing to change and the loop dies after one frame. */
  function runGuarded() {
    if (__busy) return;
    __busy = true;
    try { run(); } finally { __busy = false; }
  }

  function schedule() {
    if (__pending) return;
    __pending = true;
    var fire = function () { __pending = false; runGuarded(); };
    if (window.requestAnimationFrame) window.requestAnimationFrame(fire);
    else setTimeout(fire, 16);
  }

  /* ---------- BOOT ORDER: THIS IS THE IMPORTANT PART ----------

     Measured 6 Aug 2026 on /it/prezzi at 390px, by loading the page twice and
     counting React's "Caught a recoverable error" warnings:

         enhance.js BLOCKED :  2 recoverable errors
         enhance.js LOADED  : 16 recoverable errors

     Those 14 extra errors are ours. We used to start rewriting hrefs at
     DOMContentLoaded - i.e. while React was still hydrating. React compares the
     server HTML against what it expects, finds our edits, treats the tree as
     corrupt, and re-renders the whole subtree from its own bundle. Our edits are
     wiped, and the links revert to whatever Framer authored: the /#usecases
     hook, the English footer on Italian pages, the lot.

     That single mechanism explains every symptom reported: links that do nothing
     on a first visit but work after a reload (cache changes the timing), Italian
     pages linking into the English site, and why it was always worse on mobile
     (slower hydration = a wider window for us to collide with it).

     So the file is split in two by whether a thing WRITES to the DOM:

       * installClickInterceptor() only listens. It cannot trigger a hydration
         mismatch, so it goes on immediately and every link is clickable from the
         first paint, wired or not - that is what resolveByLabel() is for.

       * everything else writes, so it waits for `load`, by which point React has
         hydrated and our edits stick instead of being reverted.

     Do not move DOM writes back to DOMContentLoaded to make them "apply sooner".
     They will apply sooner and then be thrown away. */
  installClickInterceptor();

  /* `load` is necessary but not always sufficient: on the heavier pages at phone
     width React is still reconciling when it fires. Measured on /it at 390px -
     booting exactly at load still produced 16 recoverable errors against a
     baseline of 2. One frame plus a short pause puts our first write after the
     reconciliation instead of inside it. */
  function boot() {
    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(function () { setTimeout(bootNow, 400); });
    } else {
      setTimeout(bootNow, 400);
    }
  }

  function bootNow() {
    runGuarded();
    __mo = new MutationObserver(schedule);
    /* attributeFilter:["href"] matters. The observer used to watch childList
       only, so when Framer rewrote an EXISTING anchor's href in place - no node
       added or removed - we never heard about it and never corrected it. That is
       why the footer logo on /it/prezzi and /it/contatti at 390px sat on "../"
       (the English home): at our last pass it still read "../it", and Framer
       changed it afterwards. Safe to watch, because run() is idempotent and
       schedule() coalesces to one pass per frame. */
    __mo.observe(document.documentElement, {
      childList: true, subtree: true, attributes: true, attributeFilter: ["href"]
    });
    /* Framer finishes some work after load; one late pass catches it. */
    setTimeout(runGuarded, 800);
  }
  if (document.readyState === "complete") boot();
  else window.addEventListener("load", boot);
})();
