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
    /* The card rows go. buildWorkflowsSection() renders its own tiles further
       down the page - shorter copy, outline icons, left-aligned - so Framer's
       nine centred cards are not reused. Only the HEADING BLOCK is kept, cloned,
       so the red pill and the h2 stay Framer's type. */
    SAVED_HEAD = head;

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
    for (var r = 0; r < rows.length; r++) rows[r].parentNode.removeChild(rows[r]);

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

  /* ---------- THE WORKFLOWS SECTION ----------
     "Start where it hurts." Six tiles in two labelled bands, rendered here
     rather than reusing Framer's nine centred cards: shorter copy, one outline
     icon top-left, text left-aligned, on the site's own #F9FAFD card grey.

     Six, not nine. That drops the homepage's direct links to three use-case
     pages, so the band closes with a link to the /use-cases hub - the crawl
     path to all nine survives, and so does the visitor's way to find them. */
  var SAVED_HEAD = null;

  var WF_COPY = IT
    ? { pill: "Casi d'uso", h2: "Parti da dove fa male.",
        sub: "Ogni workflow \u00e8 preconfigurato per l'e-commerce e collegato al tuo " +
             "catalogo. Accendi quello che ti serve, quando ti serve.",
        g1: "Svuota la coda", g2: "Poi fai rendere il telefono",
        all: "Tutti i workflow", allHref: "/it/casi-duso" }
    : { pill: "Use Cases", h2: "Start where it hurts.",
        sub: "Every workflow is pre-configured for e-commerce and wired to your " +
             "catalog. Turn on the ones you need, when you need them.",
        g1: "Kill the queue", g2: "Then make the line pay",
        all: "All nine workflows", allHref: "/use-cases" };

  function wfIc(d) {
    return '<svg class="sb-wf-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
           'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ' +
           'aria-hidden="true">' + d + "</svg>";
  }
  var WF_ICONS = {
    order:   wfIc('<path d="M3 8.5 12 4l9 4.5v7L12 20l-9-4.5z"/><path d="M3 8.5 12 13l9-4.5M12 13v7"/>'),
    complaint: wfIc('<path d="M20 15a2 2 0 0 1-2 2H8l-4 3V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z"/><path d="M12 8v3.5M12 14h.01"/>'),
    returns: wfIc('<path d="M3 10h11a5 5 0 0 1 0 10H9"/><path d="M7 6 3 10l4 4"/>'),
    stock:   wfIc('<path d="M18 8a6 6 0 1 0-12 0c0 6-2 7-2 7h16s-2-1-2-7"/><path d="M10.5 20a2 2 0 0 0 3 0"/>'),
    presale: wfIc('<path d="M4 12a8 8 0 0 1 16 0v5a3 3 0 0 1-3 3h-2"/><rect x="2" y="12" width="4" height="6" rx="1.6"/><rect x="18" y="12" width="4" height="6" rx="1.6"/>'),
    quote:   wfIc('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M14.5 12.2a2.6 2.6 0 1 0 0 3.6M9.5 13h4M9.5 15h4"/>')
  };

  var WF_TILES = IT
    ? [["order", "Dov'\u00e8 il Mio Ordine", "Legge l'ordine in tempo reale e lo dice al cliente, in pochi secondi, a qualsiasi ora.", "/it/casi-duso/dove-e-il-mio-ordine", 1],
       ["complaint", "Apertura Reclamo", "Raccoglie il problema con tutto il contesto e lo manda alla persona giusta.", "/it/casi-duso/apertura-reclamo", 1],
       ["returns", "Gestione Resi", "Verifica le condizioni contro la tua policy e avvia la pratica.", "/it/casi-duso/gestione-resi", 1],
       ["stock", "Notifica Ritorno in Stock", "Chiama chi lo voleva, invece di un'email che finisce nello spam.", "/it/casi-duso/notifica-ritorno-in-stock", 1],
       ["presale", "Consulenza Pre-Vendita", "Risponde alla domanda sul prodotto e accompagna il cliente al checkout.", "/it/casi-duso/consulenza-pre-vendita", 2],
       ["quote", "Preventivi Automatici", "Qualifica, raccoglie i requisiti e manda il preventivo prima che qualcuno alzi un dito.", "/it/casi-duso/preventivi-automatici", 2]]
    : [["order", "Where Is My Order", "Reads the live order and tells them, in seconds, at any hour.", "/use-cases/where-is-my-order", 1],
       ["complaint", "Open a Complaint", "Captures the issue with full context and routes it to the right person.", "/use-cases/open-a-complaint", 1],
       ["returns", "Managing Returns", "Checks eligibility against your policy and starts the process.", "/use-cases/managing-returns", 1],
       ["stock", "Back-in-Stock Alerts", "Calls the people who wanted it, not an email in a spam folder.", "/use-cases/back-in-stock-notification", 1],
       ["presale", "Pre-Sales Consultation", "Answers the product question and guides the buyer to checkout.", "/use-cases/pre-sales-consultation", 2],
       ["quote", "B2B Quote Collection", "Qualifies, collects requirements, sends the quote before anyone touches it.", "/use-cases/qualify-and-collect-for-quote", 2]];

  var WF_CSS =
    ".sb-wf-band{display:flex;align-items:center;gap:16px;margin:34px 0 16px;" +
    "font-family:Satoshi,Inter,sans-serif;font-weight:700;font-size:11.5px;letter-spacing:.16em;" +
    "text-transform:uppercase;color:rgb(111,106,102)}" +
    ".sb-wf-band:after{content:'';flex:1;height:1px;background:rgba(11,11,12,.10)}" +
    ".sb-wf-grid{display:grid;gap:16px}" +
    ".sb-wf-grid.g4{grid-template-columns:repeat(4,1fr)}" +
    ".sb-wf-grid.g2{grid-template-columns:repeat(2,1fr)}" +
    ".sb-wf-tile{display:block;text-decoration:none;background:#F9FAFD;border-radius:20px;" +
    "padding:26px 26px 30px;transition:background .18s,transform .18s}" +
    ".sb-wf-tile:hover{background:#F1F4FA;transform:translateY(-2px)}" +
    ".sb-wf-ic{width:22px;height:22px;color:rgb(11,11,12);display:block;margin-bottom:14px}" +
    ".sb-wf-tile b{display:block;font-family:Satoshi,Inter,sans-serif;font-weight:700;" +
    "font-size:17px;line-height:1.3;color:rgb(11,11,12)}" +
    ".sb-wf-tile span{display:block;margin-top:9px;font-family:Satoshi,Inter,sans-serif;" +
    "font-size:14.5px;line-height:1.5;color:rgb(111,106,102);text-wrap:pretty}" +
    ".sb-wf-all{display:block;margin:26px 0 0;text-align:center;font-family:Satoshi,Inter,sans-serif;" +
    "font-weight:700;font-size:15.5px;color:rgb(11,11,12);text-decoration:none}" +
    ".sb-wf-all u{text-decoration:none;border-bottom:2px solid rgb(204,255,0);padding-bottom:2px}" +
    "@media(max-width:1024px){.sb-wf-grid.g4{grid-template-columns:repeat(2,1fr)}}" +
    "@media(max-width:640px){.sb-wf-grid.g4,.sb-wf-grid.g2{grid-template-columns:1fr}" +
    ".sb-wf-band{margin:26px 0 12px;font-size:10.5px}.sb-wf-tile{padding:22px 22px 24px}}";

  function wfTiles(group) {
    var out = "";
    for (var i = 0; i < WF_TILES.length; i++) {
      var t = WF_TILES[i];
      if (t[4] !== group) continue;
      out += '<a class="sb-wf-tile" href="' + t[3] + '">' + WF_ICONS[t[0]] +
             "<b>" + t[1] + "</b><span>" + t[2] + "</span></a>";
    }
    return out;
  }

  function buildWorkflowsSection() {
    if (!SAVED_HEAD) return;
    if (document.querySelector("[data-sb-wf]")) return;
    var host = document.querySelector("[data-sb-prod]");
    if (!host) return;
    var prodSec = host.closest("section");
    if (!prodSec || !prodSec.parentElement) return;

    if (!document.getElementById("sb-wf-css")) {
      var st = document.createElement("style");
      st.id = "sb-wf-css"; st.textContent = WF_CSS;
      (document.head || document.documentElement).appendChild(st);
    }

    var sec = document.createElement("section");
    sec.setAttribute("data-sb-wf", "1");
    var col = document.createElement("div");
    col.style.cssText = "max-width:1200px;margin:0 auto;padding:0 20px";
    sec.appendChild(col);

    /* Cloned heading block: the red pill and the h2 keep Framer's exact type. */
    var head = SAVED_HEAD.cloneNode(true);
    col.appendChild(head);
    var pill = head.querySelector("a p, a span");
    if (pill) setText(pill, WF_COPY.pill);
    var h2 = head.querySelector("h2");
    if (h2) setHTML(h2, WF_COPY.h2);
    var ps = head.querySelectorAll("p"), got = false;
    for (var j = 0; j < ps.length; j++) {
      if (ps[j] === pill || pill_contains(pill, ps[j])) continue;
      if (!got) { setText(ps[j], WF_COPY.sub); ps[j].style.display = ""; got = true; }
      else if (ps[j].style.display !== "none") ps[j].style.display = "none";
    }

    var body = document.createElement("div");
    body.innerHTML =
      '<div class="sb-wf-band">' + WF_COPY.g1 + "</div>" +
      '<div class="sb-wf-grid g4">' + wfTiles(1) + "</div>" +
      '<div class="sb-wf-band">' + WF_COPY.g2 + "</div>" +
      '<div class="sb-wf-grid g2">' + wfTiles(2) + "</div>" +
      '<a class="sb-wf-all" href="' + WF_COPY.allHref + '"><u>' + WF_COPY.all +
      " &rarr;</u></a>";
    col.appendChild(body);
    prodSec.parentElement.insertBefore(sec, prodSec.nextSibling);
  }

  /* ---------- THE QUEUE, and THE DEMO IS 5% ----------
     Two bands that replace Framer's "Overview Section" (the "We handle the AI"
     block and the 9 / 24-7 / 2 weeks stats) and "Features Section" ("Live in
     three steps", 2,066px of it).

     Both are found by data-framer-name, not by class or heading text: React
     writes that attribute itself so it survives hydration, the hashes differ per
     page, and the Italian page wraps its heading in ssr-variant nodes that make
     child-walking unreliable. Framer's section is hidden rather than emptied -
     React owns those nodes and puts back anything removed - and ours is inserted
     immediately after it.

     Neither borrows Framer's type. The queue is a dark band and the 95% band is
     strongly designed, so they carry their own scale, and their eyebrow is the
     lime dot introduced on 17 Aug 2026.

     TRADE-OFF, stated so the next person does not have to rediscover it: these
     are JS passes, so a crawler that runs no JavaScript sees none of this copy.
     That was acceptable for the product showcase and the workflows; it is worth
     watching here, because "The demo is 5%. We run the other 95." is the
     positioning line most worth being quoted on. The FAQ carries the
     citation-shaped copy and it IS static - see faq.py. If GEO ever needs these
     two, they move to the faq.py pattern and the CSS places them. */

  var Q_COPY = IT
    ? { eyebrow: "La coda",
        h2: "Il tuo store &egrave; cresciuto. <br>Il telefono no.",
        beats: [
          ["01", "Ogni ordine genera chiamate.",
           "Dov'è, come lo rendo, mi va bene la taglia. Sempre le stesse domande, " +
           "tutto il giorno, da una coda che non si accorcia mai."],
          ["02", "L'alta stagione ti punisce due volte.",
           "La domanda raddoppia: o assumi stagionali che non sanno niente, o lasci i " +
           "clienti in attesa due ore. Entrambe ti costano clienti che hai già pagato."],
          ["03", "Ogni lingua è un'assunzione. Ogni notte è buio.",
           "Un team che copre quattro mercati 24 ore su 24 è un costo del personale, " +
           "non un reparto."]],
        turn: "La coda non è un problema di organico. Ha smesso di esserlo." }
    : { eyebrow: "The queue",
        h2: "Your store scaled. <br>Your phone line didn't.",
        beats: [
          ["01", "Every order creates calls.",
           "Where is it, how do I return it, does it fit. The same handful of questions, " +
           "all day, from a queue that never shortens."],
          ["02", "Peak season punishes you twice.",
           "Demand doubles, so you hire temps who know nothing, or you let customers hold " +
           "for two hours. Both cost you customers you already paid to acquire."],
          ["03", "Every language is a hire. Every night is dark.",
           "A support team that covers four markets around the clock is a payroll, not a " +
           "department."]],
        turn: "The queue is not a headcount problem. It stopped being one." };

  var M_COPY = IT
    ? { eyebrow: "Completamente gestito",
        h2: "La demo &egrave; il 5%. <br>Il restante 95 lo gestiamo noi.",
        lede: "Chiunque può mostrarti un agente che parla. Il lavoro è tenerlo " +
              "preciso alla diecimillesima chiamata, e quel lavoro è nostro, ogni giorno.",
        steps: [
          ["Step 1", "Ci dici come deve andare",
           "Le tue regole, il tuo tono, i tuoi limiti. Una sessione con chi sa."],
          ["Step 2", "Lo costruiamo e lo colleghiamo",
           "Catalogo, ordini, CRM, helpdesk. Nessuno sprint per il tuo team."],
          ["Step 3", "Lo ascolti tu, prima di tutti",
           "Ti chiamiamo con la bozza. Online quando dici tu, non prima."],
          ["Step 4", "Rivediamo ogni chiamata, ogni giorno",
           "Lacune trovate, correzioni pubblicate, tutto leggibile da te."]],
        tiles: [
          ["2.914", "up", "+318 vs settimana scorsa", "Chiamate riviste questa settimana", "blue"],
          ["23", "down", "-6 vs settimana scorsa", "Lacune trovate", "orange"],
          ["9", "up", "+2 vs settimana scorsa", "Correzioni pubblicate", "green"],
          ["56,93%", "up", "+1,45% vs settimana scorsa", "Tasso di autonomia", "yellow"]] }
    : { eyebrow: "Fully managed",
        h2: "The demo is 5%. <br>We run the other 95.",
        lede: "Any vendor can show you an agent that talks. The work is keeping it right " +
              "on the ten-thousandth call, and that work is ours, daily.",
        steps: [
          ["Step 1", "You tell us how it should go",
           "Your rules, your tone, your red lines. One session with whoever knows."],
          ["Step 2", "We build and wire it",
           "Catalog, orders, CRM, helpdesk. No sprint from your team."],
          ["Step 3", "You hear it before anyone else",
           "We call you with the draft. Live when you say so, not before."],
          ["Step 4", "We review every call, every day",
           "Gaps found, fixes published, all of it readable by you."]],
        tiles: [
          ["2,914", "up", "+318 vs last week", "Calls reviewed this week", "blue"],
          ["23", "down", "-6 vs last week", "Gaps found", "orange"],
          ["9", "up", "+2 vs last week", "Fixes published", "green"],
          ["56.93%", "up", "+1.45% vs last week", "Autonomy rate", "yellow"]] };

  /* The four chip colours are the Agent Evaluation screen's own label palette,
     lifted from assets-src/agent-evaluation.html so the section visually rhymes
     with the product it describes.

     THE ARROW CARRIES THE MEANING, NOT THE COLOUR. All four deltas are green,
     because all four are good news - but "good" on Gaps found is DOWN. A naive
     up-arrow on every tile would read as the agent degrading, which is the
     opposite of this section's argument. */
  var SB_CSS =
    ".sb-band{font-family:Satoshi,Inter,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}" +
    ".sb-q{max-width:1200px;margin:0 auto;padding:0 20px}" +
    ".sb-q-card{background:rgb(11,11,12);color:#fff;border-radius:26px;padding:64px 58px}" +
    ".sb-eyeb{display:inline-flex;align-items:center;gap:9px;font-size:12px;line-height:1.2;" +
    "font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:rgb(111,106,102);margin:0}" +
    ".sb-eyeb:before{content:'';width:7px;height:7px;border-radius:50%;background:rgb(204,255,0);flex:none}" +
    ".sb-q-card .sb-eyeb{color:rgba(255,255,255,.62)}" +
    ".sb-band h2{font-size:46px;line-height:1.16;letter-spacing:-1.4px;font-weight:700;margin:16px 0 0;" +
    "color:rgb(11,11,12)}" +
    ".sb-q-card h2{color:#fff}" +
    ".sb-beat{display:grid;grid-template-columns:56px 1fr;gap:8px;border-top:1px solid rgba(255,255,255,.10);padding:26px 0}" +
    ".sb-beat:first-of-type{margin-top:34px}" +
    ".sb-beat i{font-size:12px;line-height:1.6;color:rgb(204,255,0);font-style:normal;font-weight:700}" +
    ".sb-beat b{font-size:21px;line-height:1.3;display:block}" +
    ".sb-beat p{margin:8px 0 0;font-size:15px;line-height:1.55;color:rgba(255,255,255,.66);max-width:780px}" +
    ".sb-turn{margin:24px 0 0;font-size:17px;font-weight:700;color:rgb(204,255,0)}" +
    ".sb-m{max-width:1200px;margin:0 auto;padding:0 20px;text-align:center}" +
    ".sb-m .sb-lede{max-width:680px;margin:16px auto 0;font-size:17px;line-height:1.6;color:rgb(111,106,102)}" +
    ".sb-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:34px 0 0;text-align:left}" +
    ".sb-step{background:#F9FAFD;border-radius:20px;padding:26px}" +
    ".sb-step.on{background:rgb(11,11,12);color:#fff}" +
    ".sb-step small{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgb(111,106,102)}" +
    ".sb-step.on small{color:rgb(204,255,0)}" +
    ".sb-step b{display:block;margin-top:12px;font-size:17px;line-height:1.3}" +
    ".sb-step p{margin:9px 0 0;font-size:14.5px;line-height:1.5;color:rgb(111,106,102);text-wrap:pretty}" +
    ".sb-step.on p{color:rgba(255,255,255,.72)}" +
    ".sb-tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:16px 0 0}" +
    ".sb-tile{border-radius:16px;padding:22px 18px;text-align:center}" +
    ".sb-tile b{display:block;font-size:28px;line-height:1;font-weight:700;color:rgb(11,11,12)}" +
    ".sb-tile u{display:block;margin-top:9px;font-size:12px;font-weight:700;color:rgb(47,107,71);text-decoration:none}" +
    ".sb-tile span{display:inline-block;margin-top:11px;border-radius:999px;padding:5px 11px;" +
    "font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}" +
    ".sb-tile.blue{background:#f2f6fc}   .sb-tile.blue span{background:#e5eefa;color:#28588c}" +
    ".sb-tile.orange{background:#fdf6ef} .sb-tile.orange span{background:#fdeee0;color:#8a4c14}" +
    ".sb-tile.green{background:#f1f8f4}  .sb-tile.green span{background:#e4f1ea;color:#2f6b47}" +
    ".sb-tile.yellow{background:#fdfaef} .sb-tile.yellow span{background:#fbf3d9;color:#7a5c10}" +
    "@media(max-width:1024px){.sb-steps,.sb-tiles{grid-template-columns:repeat(2,1fr)}}" +
    "@media(max-width:809px){.sb-q-card{padding:44px 24px;border-radius:20px}" +
    ".sb-band h2{font-size:30px;letter-spacing:-.8px}" +
    ".sb-beat{grid-template-columns:38px 1fr;padding:20px 0}.sb-beat b{font-size:18px}" +
    ".sb-turn{font-size:15.5px}.sb-m .sb-lede{font-size:16px}" +
    ".sb-steps,.sb-tiles{grid-template-columns:1fr}.sb-step{padding:22px}}";

  function sbCss() {
    if (document.getElementById("sb-band-css")) return;
    var st = document.createElement("style");
    st.id = "sb-band-css"; st.textContent = SB_CSS;
    (document.head || document.documentElement).appendChild(st);
  }

  /* Hide the Framer section of that name and return it, so ours can be placed
     immediately after. Returns null when it is already handled or absent. */
  function takeOver(framerName, ourAttr) {
    if (document.querySelector("[" + ourAttr + "]")) return null;
    var sec = document.querySelector('section[data-framer-name="' + framerName + '" i]');
    if (!sec || !sec.parentElement) return null;
    if (sec.style.display !== "none") sec.style.display = "none";
    return sec;
  }

  function buildQueue() {
    var anchor = takeOver("Overview Section", "data-sb-queue");
    if (!anchor) return;
    sbCss();
    var beats = "";
    for (var i = 0; i < Q_COPY.beats.length; i++) {
      var bt = Q_COPY.beats[i];
      beats += '<div class="sb-beat"><i>' + bt[0] + "</i><div><b>" + bt[1] +
               "</b><p>" + bt[2] + "</p></div></div>";
    }
    var sec = document.createElement("section");
    sec.setAttribute("data-sb-queue", "1");
    sec.className = "sb-band";
    sec.style.cssText = "padding:64px 0";
    sec.innerHTML =
      '<div class="sb-q"><div class="sb-q-card">' +
        '<p class="sb-eyeb">' + Q_COPY.eyebrow + "</p>" +
        "<h2>" + Q_COPY.h2 + "</h2>" + beats +
        '<p class="sb-turn">' + Q_COPY.turn + "</p>" +
      "</div></div>";
    anchor.parentElement.insertBefore(sec, anchor.nextSibling);
  }

  function buildManaged() {
    var anchor = takeOver("Features Section", "data-sb-managed");
    if (!anchor) return;
    sbCss();
    var steps = "";
    for (var i = 0; i < M_COPY.steps.length; i++) {
      var s = M_COPY.steps[i];
      steps += '<div class="sb-step' + (i === 0 ? " on" : "") + '"><small>' + s[0] +
               "</small><b>" + s[1] + "</b><p>" + s[2] + "</p></div>";
    }
    var tiles = "";
    for (var t = 0; t < M_COPY.tiles.length; t++) {
      var m = M_COPY.tiles[t];
      var arrow = m[1] === "down" ? "↓" : "↑";
      tiles += '<div class="sb-tile ' + m[4] + '"><b>' + m[0] + "</b><u>" + arrow + " " +
               m[2] + "</u><span>" + m[3] + "</span></div>";
    }
    var sec = document.createElement("section");
    sec.setAttribute("data-sb-managed", "1");
    sec.className = "sb-band";
    sec.style.cssText = "padding:64px 0";
    sec.innerHTML =
      '<div class="sb-m">' +
        '<p class="sb-eyeb">' + M_COPY.eyebrow + "</p>" +
        "<h2>" + M_COPY.h2 + "</h2>" +
        '<p class="sb-lede">' + M_COPY.lede + "</p>" +
        '<div class="sb-steps">' + steps + "</div>" +
        '<div class="sb-tiles">' + tiles + "</div>" +
      "</div>";
    anchor.parentElement.insertBefore(sec, anchor.nextSibling);
  }

  /* ---------- WHAT CHANGES INSIDE ----------
     The redeployment argument, and the only section on the page written for the
     customer service lead rather than the founder. The hero promises the team
     gets its time back; nothing until now showed what they do with it, which is
     exactly the thing she has to defend internally.

     No Framer section to displace: this is new, and it slots between the 95%
     band and the closing proof. Two columns, because the argument IS the
     comparison - what leaves her desk against what arrives on it. */

  var I_COPY = IT
    ? { eyebrow: "Cosa cambia dentro",
        h2: "La coda va all'agente. <br>Il tuo team va altrove.",
        lede: "Non stai tagliando il team. Lo stai spostando, via dalla coda che si " +
              "ripete, sul lavoro che solo una persona può fare.",
        aHead: "Cosa prende l'agente",
        bHead: "Cosa si riprende il team",
        a: ["Dov'è il mio ordine",
            "Date e fasce di consegna",
            "Condizioni di reso",
            "Orari e disponibilità",
            "La stessa domanda, in quattro lingue, alle 2 di notte"],
        b: ["Il cliente arrabbiato che vuole una persona",
            "L'ordine da 4.000 € che richiede una decisione",
            "Il fornitore che insegue una consegna",
            "Le chiamate di retention che nessuno aveva tempo di fare",
            "Leggere i dati delle chiamate e sistemare lo store"],
        kicker: "Non perdi persone. Smetti di perdere le loro giornate." }
    : { eyebrow: "What changes inside",
        h2: "The queue goes to the agent. <br>Your team goes somewhere better.",
        lede: "You are not cutting the team. You are moving it, off the queue that " +
              "repeats itself, onto the work only a person can do.",
        aHead: "What the agent takes",
        bHead: "What your team takes back",
        a: ["Where is my order",
            "Delivery dates and slots",
            "Return eligibility",
            "Opening hours and stock",
            "The same question, in four languages, at 2am"],
        b: ["The angry customer who needs a human",
            "The €4,000 order that needs a decision",
            "The supplier chasing a delivery",
            "Retention calls nobody had time for",
            "Reading the call data and fixing the store"],
        kicker: "You don't lose people. You stop losing their day." };

  /* THE CLASS NAMES HERE ARE PREFIXED sb-ix- FOR A REASON. The first version
     called the two columns .sb-col, which is the FOOTER's own class (footer.py
     renders the link columns with it, site/css/footer.css styles it). This
     stylesheet is injected after the footer's, so every footer column became a
     white rounded card with ink text on a black background - invisible links,
     on every page, shipped. Reported by Daniel on 18 Aug 2026: "what the hell
     happened to the footer".

     enhance.js styles are GLOBAL. Namespace every class this file adds, and
     diff new class names against site/css/footer.css before shipping. Note that
     tools/test_footer_clicks.py passed throughout: it clicks by label text, and
     the links were present and resolving correctly - just invisible. A test
     that asserts behaviour will not catch a page that cannot be read. */
  var I_CSS =
    ".sb-i{max-width:1200px;margin:0 auto;padding:0 20px;text-align:center}" +
    ".sb-i .sb-lede{max-width:680px;margin:14px auto 0;font-size:17px;line-height:1.6;" +
    "color:rgb(111,106,102)}" +
    ".sb-split{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:34px 0 0;text-align:left}" +
    ".sb-ix-col{background:#F9FAFD;border-radius:20px;padding:30px 32px 32px}" +
    ".sb-ix-col.hi{background:#fff;box-shadow:inset 0 0 0 1.5px rgb(11,11,12)}" +
    ".sb-ix-col small{font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;" +
    "color:rgb(111,106,102)}" +
    ".sb-ix-col.hi small{color:rgb(11,11,12)}" +
    ".sb-ix-col ul{list-style:none;margin:18px 0 0;padding:0}" +
    ".sb-ix-col li{font-size:16px;line-height:1.5;font-weight:500;padding:11px 0 11px 26px;" +
    "border-top:1px solid rgba(11,11,12,.08);position:relative;color:rgb(11,11,12)}" +
    ".sb-ix-col li:first-child{border-top:0}" +
    ".sb-ix-col li:before{content:'';position:absolute;left:2px;top:19px;width:12px;height:1.5px;" +
    "background:#c8c3be}" +
    ".sb-ix-col.hi li:before{left:1px;top:16px;width:0;height:0;background:none;" +
    "border-left:7px solid #8a9e00;border-top:5px solid transparent;border-bottom:5px solid transparent}" +
    ".sb-kick{margin:30px 0 0;font-size:21px;line-height:1.4;font-weight:700;letter-spacing:-.4px;" +
    "color:rgb(11,11,12)}" +
    "@media(max-width:809px){.sb-split{grid-template-columns:1fr;gap:14px;margin-top:26px}" +
    ".sb-ix-col{padding:24px 22px 26px}.sb-ix-col li{font-size:15px}" +
    ".sb-kick{font-size:17px;margin-top:24px}.sb-i .sb-lede{font-size:16px}}";

  function buildInside() {
    if (document.querySelector("[data-sb-inside]")) return;
    /* HOST CHECK BEFORE STYLESHEET. The first version injected I_CSS and only
       then looked for a host, so all 112 pages loaded rules for a section that
       only two of them render - which is how one bad class name reached every
       footer on the site. A page never needs CSS for a section it does not
       have. */
    var probe = document.querySelector("[data-sb-managed]");
    if (!probe || !probe.parentElement) return;
    sbCss();
    if (!document.getElementById("sb-inside-css")) {
      var st = document.createElement("style");
      st.id = "sb-inside-css"; st.textContent = I_CSS;
      (document.head || document.documentElement).appendChild(st);
    }
    /* Anchored to the 95% band rather than to a Framer section, because there
       is no Framer section here to anchor to. If that band is ever removed this
       one goes with it, which is correct: the argument only lands after the
       reader knows we run the thing. */
    var host = document.querySelector("[data-sb-managed]");
    if (!host || !host.parentElement) return;

    var li = function (arr) {
      var out = "";
      for (var i = 0; i < arr.length; i++) out += "<li>" + arr[i] + "</li>";
      return out;
    };
    var sec = document.createElement("section");
    sec.setAttribute("data-sb-inside", "1");
    sec.className = "sb-band";
    sec.style.cssText = "padding:64px 0";
    sec.innerHTML =
      '<div class="sb-i">' +
        '<p class="sb-eyeb">' + I_COPY.eyebrow + "</p>" +
        "<h2>" + I_COPY.h2 + "</h2>" +
        '<p class="sb-lede">' + I_COPY.lede + "</p>" +
        '<div class="sb-split">' +
          '<div class="sb-ix-col"><small>' + I_COPY.aHead + "</small><ul>" + li(I_COPY.a) + "</ul></div>" +
          '<div class="sb-ix-col hi"><small>' + I_COPY.bHead + "</small><ul>" + li(I_COPY.b) + "</ul></div>" +
        "</div>" +
        '<p class="sb-kick">' + I_COPY.kicker + "</p>" +
      "</div>";
    host.parentElement.insertBefore(sec, host.nextSibling);
  }

  /* ---------- INTEGRATIONS, and retiring the transcript band ----------

     RETIRE. Framer's "Conversational Intelligence" band (the "See what your
     customers actually ask" transcript) comes off the homepage. Two reasons,
     and the second is the one that decided it: the Understand tab in the
     product showcase already shows Call Data Intelligence 4,000px further up,
     so the page explained one product twice; and the transcript image is a
     1200x750 JPG from the Framer project, against 3120x1592 for every export we
     have made since, so the one asset whose job was proving the product is real
     was the softest thing on the page. Daniel, 18 Aug: "just retire it".

     INTEGRATIONS. Same thirteen logos, same files, restyled onto our own card:
     the site's #F9FAFD grey instead of Framer's, the lime-dot eyebrow, and two
     changes that are arguments rather than decoration -
       * Shopify carries a NATIVE tag. That is the whole differentiator; without
         it we read as one more Zapier listing.
       * the "8,500+" line moves from a hand-drawn annotation floating over the
         first chip to a pill UNDER the grid, where it reads as the answer to
         "what about my stack" rather than as a caption on Shopify. */

  var INTEG_LOGOS = [
    ["Shopify", "jhdHQKz8nA2pnUVTCJ9a9QfqMuI-6325b5aa.svg"],
    ["Magento", "CJ03BIvLYf5OH3pRPylOcWitl8-02a27367.png"],
    ["WooCommerce", "7zvknPBPAmTBb748bTSrxPbo-20cf3652.webp"],
    ["BigCommerce", "mB0Xo441Jxk0vYkyoAVaOmgFkBY-20cf3652.png"],
    ["Zendesk", "q37WkBUsC8sYmKSnvIx6ydbF8WM-e975e1e8.png"],
    ["Zoho", "YsdiKtj8aYff1o1AvTtF75ZTy4-27741d12.png"],
    ["Cal.com", "SkDREEWQtYeYtwr5sakudMa8L8-12f321eb.jpg"],
    ["Calendly", "stXuR6eP5CTdhhUCviLUDJJy6oY-f1032781.png"],
    ["Zapier", "Sj0aR7FEGpZX1JThxKfTyi2xPI-0718a85f.png"],
    ["WhatsApp", "G1mdQkk8b5uQQj3jV9wkI6HUOgs-d2e8f70d.png"],
    ["Twilio", "rNa3XhIxXIBxpzeNq8MXB8Ba5nI-cfbbeecb.svg"],
    ["Telnyx", "ppwUrPDgob81bqZwHDNupu0Q0U-5be18e7b.png"],
    ["Salesforce", "ZVHfOaoY4tHeeAEzvNLiG3fsBA-a5eb2970.png"]
  ];

  var N_COPY = IT
    ? { eyebrow: "Integrazioni",
        h2: "Si collega al tuo stack e-commerce.",
        lede: "Nativo con Shopify. Tutto il resto passa da Zapier o da un webhook: " +
              "il tuo CRM, il tuo helpdesk, il tuo ERP, il tuo calendario.",
        tag: "Nativo",
        more: "<b>8.500+</b> altre app via Zapier, o qualsiasi endpoint a cui puoi " +
              "puntare un webhook." }
    : { eyebrow: "Integrations",
        h2: "Connects to your e-commerce stack.",
        lede: "Native with Shopify. Everything else through Zapier or a webhook: " +
              "your CRM, your helpdesk, your ERP, your calendar.",
        tag: "Native",
        more: "<b>8,500+</b> more apps via Zapier, or any endpoint you can point a " +
              "webhook at." };

  var N_CSS =
    ".sb-n{max-width:1200px;margin:0 auto;padding:0 20px}" +
    ".sb-n-card{background:#F9FAFD;border-radius:26px;padding:56px 48px 60px;text-align:center}" +
    ".sb-n-card .sb-lede{max-width:660px;margin:14px auto 0;font-size:17px;line-height:1.6;" +
    "color:rgb(111,106,102)}" +
    ".sb-n-rows{margin:34px 0 0;display:flex;flex-direction:column;gap:14px;align-items:center}" +
    ".sb-n-row{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}" +
    ".sb-lg{display:inline-flex;align-items:center;gap:11px;background:#fff;border-radius:14px;" +
    "padding:12px 20px 12px 13px;font-size:17px;font-weight:600;color:rgb(11,11,12);" +
    "box-shadow:0 1px 2px rgba(11,11,12,.05)}" +
    ".sb-lg img{width:28px;height:28px;object-fit:contain;flex:none}" +
    ".sb-lg.native{box-shadow:inset 0 0 0 1.5px rgb(11,11,12)}" +
    ".sb-lg .tagn{font-size:9.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;" +
    "background:rgb(204,255,0);border-radius:5px;padding:4px 6px;margin-left:3px}" +
    ".sb-n-more{margin:26px auto 0;width:max-content;max-width:100%;background:rgb(11,11,12);" +
    "color:#fff;border-radius:999px;padding:13px 24px;font-size:15px;line-height:1.4;text-align:center}" +
    ".sb-n-more b{color:rgb(204,255,0);font-weight:700}" +
    "@media(max-width:809px){.sb-n-card{padding:40px 20px 44px;border-radius:20px}" +
    ".sb-lg{font-size:14.5px;padding:10px 14px 10px 10px;gap:8px}" +
    ".sb-lg img{width:22px;height:22px}.sb-n-row{gap:10px}.sb-n-rows{gap:10px}" +
    ".sb-n-more{font-size:14px;padding:12px 18px}}";

  function retireTranscript() {
    var el = document.querySelector('[data-framer-name="Conversational Intelligence" i]');
    if (el && el.style.display !== "none") el.style.display = "none";
  }

  function buildIntegrations() {
    var anchor = takeOver("Integrations Section", "data-sb-integ");
    if (!anchor) return;
    sbCss();
    if (!document.getElementById("sb-integ-css")) {
      var st = document.createElement("style");
      st.id = "sb-integ-css"; st.textContent = N_CSS;
      (document.head || document.documentElement).appendChild(st);
    }

    var rows = [[0, 4], [4, 9], [9, 13]], html = "";
    for (var r = 0; r < rows.length; r++) {
      html += '<div class="sb-n-row">';
      for (var i = rows[r][0]; i < rows[r][1]; i++) {
        var lg = INTEG_LOGOS[i], native = lg[0] === "Shopify";
        html += '<div class="sb-lg' + (native ? " native" : "") + '">' +
                '<img src="/fuc/images/' + lg[1] + '" alt="" loading="lazy" decoding="async">' +
                lg[0] + (native ? '<span class="tagn">' + N_COPY.tag + "</span>" : "") + "</div>";
      }
      html += "</div>";
    }

    var sec = document.createElement("section");
    sec.setAttribute("data-sb-integ", "1");
    sec.className = "sb-band";
    sec.style.cssText = "padding:64px 0";
    sec.innerHTML =
      '<div class="sb-n"><div class="sb-n-card">' +
        '<p class="sb-eyeb">' + N_COPY.eyebrow + "</p>" +
        "<h2>" + N_COPY.h2 + "</h2>" +
        '<p class="sb-lede">' + N_COPY.lede + "</p>" +
        '<div class="sb-n-rows">' + html + "</div>" +
        '<div class="sb-n-more">' + N_COPY.more + "</div>" +
      "</div></div>";
    anchor.parentElement.insertBefore(sec, anchor.nextSibling);
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
    buildWorkflowsSection();
    buildQueue();
    buildManaged();
    buildInside();
    retireTranscript();
    buildIntegrations();
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
