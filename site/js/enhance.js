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

  /* Industry pages. English only for now: the Italian footer carries the same
     English category labels, and pointing an Italian visitor at an English page
     is worse than leaving the label unlinked. Add INDUSTRIES_IT when /it/settori
     exists and this whole block starts working there too. */
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
  var INDUSTRIES = IT ? [] : INDUSTRIES_EN;
  var IND_LABEL = "Industries";
  var IND_ALL_LABEL = "All industries";
  var IND_ALL_HREF = "/industries";

  /* ---------- 1. Blog link in the FOOTER, right after "Book a Demo" ----------
     (Deliberately not in the top nav — the header stays as designed.) */
  var DEMO_LABEL = IT ? "Prenota una Demo" : "Book a Demo";
  function injectBlogLink() {
    if (document.querySelector("a[data-blog-link]")) return;
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
    var clone = wrapper.cloneNode(true);
    var ca = clone.tagName === "A" ? clone : clone.querySelector("a");
    if (!ca) return;
    var tw = (clone.querySelector && clone.querySelector("p, span, h1, h2, h3, h4, h5, h6")) || ca;
    tw.textContent = "Blog";
    ca.href = BLOG_HREF;
    ca.setAttribute("data-blog-link", "1");
    ca.removeAttribute("data-uc-wired");
    /* the demo button opens cal.com in a new tab — Blog is internal, so drop that */
    ca.removeAttribute("target");
    ca.removeAttribute("rel");
    wrapper.parentElement.insertBefore(clone, wrapper.nextSibling);
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
          var txt = a.textContent || "";
          if (normLabel(txt) !== normLabel(ind.label)) continue;
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
                 a.hasAttribute("data-blog-link") || href === "/blog" || href === "/it/blog";
      if (!ours) return;
      if (a.target === "_blank") return;
      e.preventDefault();
      e.stopImmediatePropagation();
      window.location.assign(href);
    }, true);
  }

  function run() {
    injectBlogLink(); injectIndustriesNav(); injectDropdown();
    wireUseCaseTargets(); wireIndustryTargets(); installClickInterceptor();
  }
  if (document.readyState !== "loading") run();
  else document.addEventListener("DOMContentLoaded", run);
  new MutationObserver(run).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("load", function () { setTimeout(run, 800); });
})();
