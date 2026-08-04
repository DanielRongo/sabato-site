/* Sabato site enhancements: blog nav link, Use Cases + Industries dropdowns,
   use-case and industry page wiring.
   Config-driven: add new use-case pages to USECASES and everything updates. */
(function () {
  var IT = location.pathname === "/it" || location.pathname.indexOf("/it/") === 0;
  var BLOG_HREF = IT ? "/it/blog" : "/blog";
  var NAV_ANCHORS = IT ? ["Contatti", "Prezzi"] : ["Contact", "Pricing"];
  var USECASES_LABEL = IT ? "Casi d'uso" : "Use Cases";

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
     Italian list holds only the pages actually built — unbuilt ones keep their
     original anchor so nothing links to a 404. */
  var USECASES_EN = [
    { label: "Pre-Sales Consultation", href: "/use-cases/pre-sales-consultation" },
    { label: "Cart Abandonment Recovery", href: "/use-cases/cart-abandonment-recovery" },
    { label: "Where Is My Order", href: "/use-cases/where-is-my-order" },
    { label: "Qualify & Collect for Quote", href: "/use-cases/qualify-and-collect-for-quote" },
    { label: "Open a Complaint", href: "/use-cases/open-a-complaint" },
    { label: "Checkout Summary via Text", href: "/use-cases/checkout-summary-via-text" },
    { label: "Managing Returns", href: "/use-cases/managing-returns" },
    { label: "Post-Delivery Feedback", href: "/use-cases/post-delivery-feedback" },
    { label: "Back-in-Stock Notification", href: "/use-cases/back-in-stock-notification" }
  ];
  var USECASES_IT = [
    { label: "Consulenza Pre-Vendita", href: "/it/casi-duso/consulenza-pre-vendita" },
    { label: "Recupero Carrelli Abbandonati", href: "/it/casi-duso/recupero-carrelli-abbandonati" },
    { label: "Dov'è il Mio Ordine", href: "/it/casi-duso/dove-e-il-mio-ordine" },
    { label: "Preventivi Automatici", href: "/it/casi-duso/preventivi-automatici" },
    { label: "Apertura Reclamo", href: "/it/casi-duso/apertura-reclamo" },
    { label: "Riepilogo Checkout via Messaggio", href: "/it/casi-duso/riepilogo-checkout-via-messaggio",
      aliases: ["Riepilogo Acquisto via SMS"] },
    { label: "Gestione Resi", href: "/it/casi-duso/gestione-resi" },
    { label: "Feedback Post-Consegna", href: "/it/casi-duso/feedback-post-consegna" },
    { label: "Notifica Ritorno in Stock", href: "/it/casi-duso/notifica-ritorno-in-stock" }
  ];
  var USECASES = IT ? USECASES_IT : USECASES_EN;
  var ALL_LABEL = IT ? "Tutti i casi d'uso" : "All use cases";
  var ALL_HREF = IT ? "/it#casiduso" : "/#usecases";

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
  var IND_LABEL = IT ? "Settori" : "Industries";
  var IND_ALL_LABEL = IT ? "Tutti i settori" : "All industries";
  var IND_ALL_HREF = IT ? "/it/settori" : "/industries";

  /* ---------- 1. Extra links in the FOOTER, right after "Book a Demo" ----------
     (Deliberately not in the top nav — the header stays as designed.)
     Each is a clone of the demo button, so it inherits the footer's styling
     whatever Framer decides that is this week. Order here is the order on the
     page.

     /roi-calculator is deliberately NOT in this list. It is hosted but
     unlisted — reachable only by someone given the URL directly. Adding it
     here puts it in the footer of all 74 pages, which is the opposite of
     unlisted. */
  var DEMO_LABEL = IT ? "Prenota una Demo" : "Book a Demo";
  var FOOTER_LINKS = [
    { label: "Blog", href: BLOG_HREF, attr: "data-blog-link" }
  ];

  function injectFooterLinks() {
    /* "Book a Demo" appears several times (mid-page CTAs + footer). The footer
       one is always the lowest on the page — pick that, never a hero CTA. */
    var links = document.querySelectorAll("a");
    var target = null, targetY = -1;
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (normLabel(a.textContent) !== normLabel(DEMO_LABEL)) continue;
      var r = a.getBoundingClientRect();
      if (r.height === 0) continue;
      var y = r.top + window.scrollY;
      if (y > targetY) { targetY = y; target = a; }
    }
    if (!target) return;
    var box = target.parentElement;
    if (!box || !box.parentElement) return;
    var wrapper = box.querySelectorAll("a").length === 1 ? box : target;

    /* Insert in reverse: each clone goes immediately after the demo button, so
       pushing them in back-to-front leaves FOOTER_LINKS order on screen. */
    for (var j = FOOTER_LINKS.length - 1; j >= 0; j--) {
      var spec = FOOTER_LINKS[j];
      if (document.querySelector("a[" + spec.attr + "]")) continue;
      var clone = wrapper.cloneNode(true);
      var ca = clone.tagName === "A" ? clone : clone.querySelector("a");
      if (!ca) continue;
      var tw = (clone.querySelector && clone.querySelector("p, span, h1, h2, h3, h4, h5, h6")) || ca;
      tw.textContent = spec.label;
      ca.href = spec.href;
      ca.setAttribute(spec.attr, "1");
      ca.removeAttribute("data-uc-wired");
      /* the demo button opens cal.com in a new tab — these are internal */
      ca.removeAttribute("target");
      ca.removeAttribute("rel");
      wrapper.parentElement.insertBefore(clone, wrapper.nextSibling);
    }
  }

  /* ---------- 2. Use Cases dropdown ----------
     Two structural problems this solves:
     (a) nav markup differs between Framer pages (one wrapper per link) and our
         own templates (one shared <nav>), so parent-relative centring drifts —
         we position fixed against the LINK's own bounding box instead;
     (b) Framer re-renders the nav after hydration, orphaning listeners bound to
         a specific element — so we delegate off document and resolve the link
         fresh on every hover. */
  /* A nav link in the top 200px whose label matches — the trigger for a menu. */
  function currentNavLink(node, label) {
    var a = node && node.closest ? node.closest("a") : null;
    if (!a) return null;
    if (normLabel(a.textContent) !== normLabel(label)) return null;
    var r = a.getBoundingClientRect();
    if (r.top < 0 || r.top > 200 || r.height === 0) return null;
    return a;
  }

  /* One dropdown implementation, two menus. Keeping them identical matters more
     than it looks: a second menu built separately drifts in padding, radius and
     hover colour within a release or two. */
  function makeDropdown(opts) {
    var USECASES = opts.items, USECASES_LABEL = opts.trigger;
    var ALL_LABEL = opts.allLabel, ALL_HREF = opts.allHref;
    function currentNavUseCasesLink(n) { return currentNavLink(n, USECASES_LABEL); }

    if (!USECASES.length) return;
    if (document.querySelector("[" + opts.attr + "]")) return;

    var dd = document.createElement("div");
    dd.setAttribute(opts.attr, "1");
    dd.style.cssText = "position:fixed;display:none;z-index:2147483000;padding-top:14px;";
    var card = document.createElement("div");
    card.style.cssText =
      "background:#fff;border:1px solid rgb(227,226,226);border-radius:16px;padding:8px;min-width:250px;box-shadow:0 12px 32px rgba(0,0,0,.10);";
    function item(label, href, bold) {
      var el = document.createElement("a");
      el.href = href;
      el.textContent = label;
      el.style.cssText =
        "display:block;padding:10px 14px;border-radius:10px;font-family:'Satoshi','Inter',sans-serif;font-size:15px;font-weight:" +
        (bold ? "700" : "500") +
        ";color:rgb(18,10,11);text-decoration:none;white-space:nowrap;";
      el.onmouseenter = function () { el.style.background = "rgb(204,255,0)"; };
      el.onmouseleave = function () { el.style.background = "transparent"; };
      return el;
    }
    for (var j = 0; j < USECASES.length; j++) card.appendChild(item(USECASES[j].label, USECASES[j].href, false));
    var sep = document.createElement("div");
    sep.style.cssText = "height:1px;background:rgb(227,226,226);margin:6px 8px;";
    card.appendChild(sep);
    card.appendChild(item(ALL_LABEL, ALL_HREF, true));
    dd.appendChild(card);
    document.body.appendChild(dd);

    var anchorEl = null, hideTimer = null;

    function place() {
      if (!anchorEl || !anchorEl.isConnected) return;
      var r = anchorEl.getBoundingClientRect();
      dd.style.top = r.bottom + "px";
      dd.style.left = "0px";
      var w = dd.offsetWidth || 250;
      var margin = 12;
      var left = r.left + r.width / 2 - w / 2;
      left = Math.max(margin, Math.min(left, window.innerWidth - w - margin));
      dd.style.left = Math.round(left) + "px";
    }
    function show(el) { anchorEl = el; clearTimeout(hideTimer); dd.style.display = "block"; place(); }
    function hide() { hideTimer = setTimeout(function () { dd.style.display = "none"; }, 200); }

    document.addEventListener("mouseover", function (e) {
      var link = currentNavUseCasesLink(e.target);
      if (link) { show(link); return; }
      if (dd.contains(e.target)) { clearTimeout(hideTimer); return; }
      if (dd.style.display === "block") hide();
    }, true);

    dd.addEventListener("mouseenter", function () { clearTimeout(hideTimer); });
    dd.addEventListener("mouseleave", hide);
    window.addEventListener("scroll", function () { if (dd.style.display === "block") place(); }, { passive: true });
    window.addEventListener("resize", function () { if (dd.style.display === "block") place(); });
  }

  function injectDropdown() {
    makeDropdown({ items: USECASES, trigger: USECASES_LABEL, allLabel: ALL_LABEL,
                   allHref: ALL_HREF, attr: "data-uc-dropdown" });
    makeDropdown({ items: INDUSTRIES, trigger: IND_LABEL, allLabel: IND_ALL_LABEL,
                   allHref: IND_ALL_HREF, attr: "data-ind-dropdown" });
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

  /* ---------- 4. Beat Framer's client-side router to the click ----------
     Framer hydrates its own router, which intercepts link clicks, calls
     preventDefault() and navigates via an internal route table — so rewriting
     an anchor's href is not enough on Framer-rendered pages: the click still
     goes to the original destination. We listen on `window` in the CAPTURE
     phase (the earliest point in the event path, before any document-level
     handler Framer registers) and perform the navigation ourselves. */
  /* ---------- Industries nav item ----------
     The header has no Industries link, so clone the Use Cases one to inherit its
     exact styling and insert it alongside. Clone the ANCHOR, never a wrapper:
     cloning a wrapper once duplicated the whole shared <nav> on every use-case
     page. Guard on the label so the MutationObserver can't add a second. */
  function injectIndustriesNav() {
    if (!INDUSTRIES.length) return;
    var links = document.querySelectorAll("a");
    var src = null, already = false;
    for (var i = 0; i < links.length; i++) {
      var a = links[i], r = a.getBoundingClientRect();
      if (r.top < 0 || r.top > 200 || r.height === 0) continue;
      var n = normLabel(a.textContent);
      if (n === normLabel(IND_LABEL)) { already = true; break; }
      if (n === normLabel(USECASES_LABEL) && !src) src = a;
    }
    if (already || !src) return;

    /* Framer wraps each nav link in its own container div; our templates put the
       anchors straight into <nav>. Cloning the anchor on a Framer page drops a
       second link INSIDE that 75px wrapper, which stacks it onto a second row.
       So clone the wrapper when it holds exactly one anchor — and only then,
       because cloning a wrapper that holds the whole nav duplicates the header. */
    var wrap = src.parentElement;
    var cloneWrapper = wrap && wrap !== document.body &&
                       wrap.querySelectorAll("a").length === 1 &&
                       wrap.children.length === 1;
    var node = cloneWrapper ? wrap : src;

    var el = node.cloneNode(true);
    var anchor = cloneWrapper ? el.querySelector("a") : el;
    if (!anchor) return;
    anchor.setAttribute("data-ind-link", "1");
    anchor.removeAttribute("target");
    anchor.removeAttribute("rel");
    anchor.setAttribute("href", IND_ALL_HREF);
    anchor.style.whiteSpace = "nowrap";
    /* Framer nests the label in a <p>; our templates put it in the <a>. */
    var leaf = anchor.querySelector("p, span");
    if (leaf && !leaf.children.length) leaf.textContent = IND_LABEL;
    else anchor.textContent = IND_LABEL;

    node.parentNode.insertBefore(el, node.nextSibling);

    /* A sixth item can push a fixed-gap nav onto two rows. Only shrink the gap
       if that actually happened — measured, not assumed. */
    var row = el.parentElement;
    if (row && getComputedStyle(row).display.indexOf("flex") === 0) {
      var tops = {}, kids = row.children, count = 0;
      for (var k = 0; k < kids.length; k++) {
        var top = Math.round(kids[k].getBoundingClientRect().top);
        if (!tops[top]) { tops[top] = 1; count++; }
      }
      if (count > 1) row.style.gap = "28px";
    }
  }

  /* ---------- Footer industry links ----------
     On Framer pages these labels sit inside <a> elements that have no href at
     all, so they need one setting rather than retargeting — a different repair
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
      if (!a) return;
      var href = a.getAttribute("href") || "";
      var ours = href.indexOf("/use-cases/") === 0 || href.indexOf("/it/casi-duso/") === 0 ||
                 href.indexOf("/industries/") === 0 || href === "/industries" ||
                 href.indexOf("/it/settori/") === 0 || href === "/it/settori" ||
                 a.hasAttribute("data-blog-link") || href === "/blog" || href === "/it/blog" ||
                 a.hasAttribute("data-roi-link") || href === "/roi-calculator" ||
                 href.indexOf("/customers/") === 0;
      if (!ours) return;
      if (a.target === "_blank") return;
      e.preventDefault();
      e.stopImmediatePropagation();
      window.location.assign(href);
    }, true);
  }

  /* ---------- 6. Customer stories band on the homepage ----------
     DRAFT. Placeholders render as loud orange TBC chips and the band is only
     injected on staging hosts — see BAND_ENABLED below.

     Why this is injected rather than written into index.html: Framer pages are
     React-hydrated, so markup added to the HTML is thrown away the moment React
     takes over. (That is exactly how an earlier copy fix appeared to ship while
     staying visibly broken.) Injecting after hydration, and re-asserting on the
     MutationObserver pass that already drives this file, is the only placement
     that survives.

     Position: directly after the workflows section. That is the moment the
     visitor has understood what the product does and is silently asking whether
     it works for someone like them — and it puts evidence immediately before
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
      label: IT ? "delle chiamate gestite in autonomia \u2014 9 agenti live in 3 lingue"
                : "of calls handled autonomously \u2014 9 agents live across 3 languages",
      person: "Alessio Perrucci", role: "CEO" },
    { slug: "creative-cables", name: "Creative Cables", initials: "CC",
      metric: "00%", ph: true,
      label: IT ? "[metrica da approvare]" : "[metric to be approved]",
      person: "Marco Logreco", role: "Head of E-Commerce" }
  ];

  /* Staging only: these pages name real customers and carry unapproved figures.
     Production gets the band the day Daniel has sign-off, by flipping this. */
  var BAND_ENABLED = /netlify\.app$/.test(location.hostname) ||
                     location.hostname === "localhost" ||
                     location.hostname === "127.0.0.1";

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
        '<a class="sb-card" href="/customers/' + c.slug + '">' +
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

  function run() {
    injectFooterLinks(); injectIndustriesNav(); injectDropdown();
    wireUseCaseTargets(); wireIndustryTargets(); installClickInterceptor();
    injectCustomerBand();
  }
  if (document.readyState !== "loading") run();
  else document.addEventListener("DOMContentLoaded", run);
  new MutationObserver(run).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("load", function () { setTimeout(run, 800); });
})();
