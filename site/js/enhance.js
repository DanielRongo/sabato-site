/* Sabato site enhancements: blog nav link, Use Cases dropdown, use-case page wiring.
   Config-driven: add new use-case pages to USECASES and everything updates. */
(function () {
  var IT = location.pathname === "/it" || location.pathname.indexOf("/it/") === 0;
  var BLOG_HREF = IT ? "/it/blog" : "/blog";
  var NAV_ANCHORS = IT ? ["Contatti", "Prezzi"] : ["Contact", "Pricing"];
  var USECASES_LABEL = IT ? "Casi d'uso" : "Use Cases";

  /* Use-case pages that exist. label = exact text on site; href = live page. */
  var USECASES = [
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

  /* ---------- 1. Blog link in top nav (cloned from a sibling for identical styling) ---------- */
  function injectBlogLink() {
    if (document.querySelector("a[data-blog-link]")) return;
    var links = document.querySelectorAll("a");
    /* if the top nav already has a Blog link (static pages), do nothing */
    for (var i = 0; i < links.length; i++) {
      var a0 = links[i];
      var r0 = a0.getBoundingClientRect();
      if ((a0.textContent || "").trim() === "Blog" && r0.top >= 0 && r0.top < 200 && r0.height > 0) return;
    }
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var t = (a.textContent || "").trim();
      if (t !== NAV_ANCHORS[0] && t !== NAV_ANCHORS[1]) continue;
      var r = a.getBoundingClientRect();
      if (r.top < 0 || r.top > 200 || r.height === 0) continue;
      var box = a.parentElement;
      /* only clone single-item wrappers — never a shared container */
      if (box.querySelectorAll("a").length !== 1) continue;
      var clone = box.cloneNode(true);
      var ca = clone.querySelector("a");
      if (!ca) continue;
      var tw = clone.querySelector("p, span, h1, h2, h3, h4, h5, h6") || ca;
      tw.textContent = "Blog";
      ca.href = BLOG_HREF;
      ca.setAttribute("data-blog-link", "1");
      box.parentElement.insertBefore(clone, box.nextSibling);
      return;
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
  function currentNavUseCasesLink(node) {
    var a = node && node.closest ? node.closest("a") : null;
    if (!a) return null;
    if ((a.textContent || "").trim() !== USECASES_LABEL) return null;
    var r = a.getBoundingClientRect();
    if (r.top < 0 || r.top > 200 || r.height === 0) return null;
    return a;
  }

  function injectDropdown() {
    if (IT) return;
    if (document.querySelector("[data-uc-dropdown]")) return;

    var dd = document.createElement("div");
    dd.setAttribute("data-uc-dropdown", "1");
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
    card.appendChild(item("All use cases", "/#usecases", true));
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

  /* ---------- 3. Retarget footer links + make matching tiles clickable ---------- */
  function wireUseCaseTargets() {
    for (var i = 0; i < USECASES.length; i++) {
      (function (uc) {
        var nodes = document.querySelectorAll("p, span, h1, h2, h3, h4, h5, h6");
        for (var k = 0; k < nodes.length; k++) {
          var el = nodes[k];
          if (el.children.length !== 0) continue;
          if ((el.textContent || "").trim() !== uc.label) continue;
          var anchor = el.closest("a");
          if (anchor) {
            /* footer link (or any anchor) still pointing at the old #usecases target */
            var href = anchor.getAttribute("href") || "";
            if (href.indexOf("#usecases") !== -1 && anchor.getAttribute("data-uc-wired") !== "1") {
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

  function run() { injectBlogLink(); injectDropdown(); wireUseCaseTargets(); }
  if (document.readyState !== "loading") run();
  else document.addEventListener("DOMContentLoaded", run);
  new MutationObserver(run).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("load", function () { setTimeout(run, 800); });
})();
