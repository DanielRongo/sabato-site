#!/usr/bin/env python3
"""The cookie consent banner, EN and IT.

    from consent import consent_html
    consent_html("en")   # markup + the manager script, for the end of <body>

DESIGN CONSTRAINTS, and where they come from
--------------------------------------------
This is a hand-built banner rather than a hosted CMP - Daniel's call, 12 Aug
2026, on the reasoning that a subscription for ~150 lines is the wrong trade for
a bootstrapped static site with exactly two non-essential scripts. The cost of
that choice is that the consent record lives in the visitor's own browser: we
can show our code and our policy, but there is no server-side log to produce if
anyone ever asks us to prove a specific visitor said yes.

The rules this has to satisfy - GDPR art. 7 plus the Italian Garante's cookie
guidelines (8 July 2021), which is the regime that actually applies to us:

  * PRIOR consent. Nothing non-essential may run before the visitor chooses.
    That is enforced upstream, not here: tools/inject_ga.py sets Google Consent
    Mode to denied before any config call, and tools/inject_reb2b.py only
    defines its loader rather than calling it. A banner that appears while the
    trackers already fired is worse than no banner - it is written evidence
    that we knew.
  * REJECT AS EASY AS ACCEPT. Both are one click, first layer, same row, same
    size. No "reject" buried behind a preferences panel.
  * NO COOKIE WALL, and scrolling is not consent. The bar does not block the
    page, has no overlay, and no dismiss-by-scroll.
  * NO BARE X. A close button that silently means "accept" is the single most
    commonly enforced violation. There isn't one - you choose or the bar stays.
  * GRANULAR. Analytics and marketing are separate switches, because they are
    separate purposes.
  * LAYERED WORDING. The strip stays generic - "to understand how this site is
    used" - and the specifics live one layer down, on the switches, and in full
    in the privacy policy. Daniel, 12 Aug: naming visitor identification on the
    first line "freaks people out". That is a real conversion cost for no legal
    gain: what the law requires is that consent be informed at the point it is
    GIVEN, which is the switch, not that the strip recite every vendor. Do not
    let this drift the other way either - softening it past the point where a
    reader can tell WHAT they are agreeing to is where generic stops being
    layered and starts being misleading.

    The switches name the purpose and the category, not the vendor: "company-
    level tracking" rather than "RB2B", and no geography. Naming the processor
    is a privacy-policy job, and it is done there in full - including the
    US-only scope - because that is the document the law points at and the one
    a regulator reads. Do NOT strip it from the policy to match the banner.
  * WITHDRAWABLE. A footer link reopens this at any time, which is the half
    most implementations forget.
  * RE-ASK. A stored choice expires after 180 days, so consent stays current
    rather than being collected once in 2026 and relied on forever.

WHY IT LIVES AT THE END OF <BODY>
The Framer pages hydrate a React tree into #main, and anything we insert inside
that tree is silently deleted at hydration - that cost a day on the proof
widget. This is a fixed-position sibling AFTER the root, never inside it, so
React never sees it.
"""

STORAGE_KEY = "sb-consent"
VERSION = 1
MAX_AGE_DAYS = 180

COPY = {
    "en": dict(
        title="Cookies",
        # ONE LINE. At 13.5px the strip leaves roughly 90 characters beside
        # the buttons on a 1200px card; past that it wraps and stops being a
        # slim bar. Keep any edit under that, and check it at 1280px.
        body="We use cookies to understand how this site is used. Nothing "
             "runs until you choose.",
        policy="Privacy and Cookies", policy_href="/privacy-policy",
        accept="Accept all", reject="Reject all",
        prefs="Preferences", save="Save choices",
        cats=[
            ("necessary", "Strictly necessary",
             "Page delivery, security, and remembering this choice. Always on."),
            ("analytics", "Analytics",
             "Google Analytics 4. Which pages get read and how people arrive, "
             "in aggregate."),
            ("marketing", "Marketing",
             "Company-level tracking, so we can follow up with businesses that "
             "show interest."),
        ],
    ),
    "it": dict(
        title="Cookie",
        # Italian runs ~15% longer than English; trimmed to match.
        body="Usiamo cookie per capire come viene usato il sito. Niente parte "
             "senza il tuo consenso.",
        policy="Privacy e Cookie", policy_href="/it/privacy-e-cookie",
        accept="Accetta tutti", reject="Rifiuta tutti",
        prefs="Preferenze", save="Salva le scelte",
        cats=[
            ("necessary", "Tecnici necessari",
             "Consegna delle pagine, sicurezza e memoria di questa scelta. "
             "Sempre attivi."),
            ("analytics", "Analisi",
             "Google Analytics 4. Quali pagine vengono lette e come arrivano le "
             "persone, in forma aggregata."),
            ("marketing", "Marketing",
             "Tracciamento a livello aziendale, per dare seguito alle aziende "
             "che mostrano interesse."),
        ],
    ),
}


def _rows(c):
    out = []
    for key, label, desc in c["cats"]:
        locked = ' checked disabled' if key == "necessary" else ''
        attr = '' if key == "necessary" else ' data-sb-cat="%s"' % key
        out.append(
            '<label class="sb-c-row">'
            '<span class="sb-c-rt"><b>%s</b><i>%s</i></span>'
            '<input type="checkbox"%s%s></label>' % (label, desc, attr, locked))
    return "".join(out)


def consent_html(lang="en"):
    c = COPY[lang]
    return (
        # A strip, not a panel. The headline is gone and the dialog takes its
        # accessible name from aria-label instead - a visible <h2> on a one-line
        # bar is just a second line.
        # The preferences panel comes AFTER the row, so opening it grows the bar
        # downward instead of shoving the buttons around.
        '<div class="sb-consent" id="sb-consent" role="dialog" '
        'aria-label="%s" aria-describedby="sb-consent-body" '
        'data-lang="%s" hidden>'
        '<div class="sb-c-card">'
        '<div class="sb-c-bar">'
        '<p id="sb-consent-body">%s <a href="%s">%s</a></p>'
        '<div class="sb-c-btns">'
        # Accept and reject are adjacent, identical in size, first layer.
        '<button type="button" class="sb-c-btn sb-c-primary" data-sb-c="accept">%s</button>'
        '<button type="button" class="sb-c-btn sb-c-ghost" data-sb-c="reject">%s</button>'
        '<button type="button" class="sb-c-btn sb-c-text" data-sb-c="prefs">%s</button>'
        '<button type="button" class="sb-c-btn sb-c-primary" data-sb-c="save" hidden>%s</button>'
        '</div></div>'
        '<div class="sb-c-prefs" hidden>%s</div>'
        '</div></div>%s'
        % (c["title"], lang, c["body"], c["policy_href"], c["policy"],
           c["accept"], c["reject"], c["prefs"], c["save"], _rows(c), SCRIPT)
    )


# ES5 on purpose: this runs before anything else on every page, including for
# whatever browser a prospect's IT department has standardised on.
SCRIPT = """<script data-sb-consent>(function(){
var K="%s",V=%d,MAXMS=%d*864e5;
function read(){try{var o=JSON.parse(localStorage.getItem(K)||"null");
if(!o||o.v!==V)return null;
if(o.ts&&(Date.now()-Date.parse(o.ts))>MAXMS)return null;return o;}catch(e){return null;}}
function write(a,m){try{localStorage.setItem(K,JSON.stringify(
{v:V,ts:new Date().toISOString(),analytics:!!a,marketing:!!m}));}catch(e){}}
function apply(a,m){
// Consent Mode v2. inject_ga.py has already defaulted these to denied, so this
// only ever loosens - and only on an explicit click.
if(window.gtag)window.gtag("consent","update",{
ad_storage:m?"granted":"denied",ad_user_data:m?"granted":"denied",
ad_personalization:m?"granted":"denied",analytics_storage:a?"granted":"denied"});
// The marketing loader is defined but never called until this point.
if(m&&window.sbReb2b)window.sbReb2b();}
var el=null;
function box(){return el||(el=document.getElementById("sb-consent"));}
function show(pre){var b=box();if(!b)return;
var c=pre||read()||{};
var t=b.querySelectorAll("[data-sb-cat]"),i;
for(i=0;i<t.length;i++)t[i].checked=!!c[t[i].getAttribute("data-sb-cat")];
b.hidden=false;}
function hide(){var b=box();if(b)b.hidden=true;}
function close_(a,m){write(a,m);apply(a,m);hide();}
function wire(){var b=box();if(!b)return;
b.addEventListener("click",function(e){
var t=e.target.closest?e.target.closest("[data-sb-c]"):null;if(!t)return;
var act=t.getAttribute("data-sb-c");
if(act==="accept")return close_(true,true);
if(act==="reject")return close_(false,false);
if(act==="prefs"){b.querySelector(".sb-c-prefs").hidden=false;
t.hidden=true;b.querySelector('[data-sb-c="save"]').hidden=false;
b.className+=" sb-c-open";return;}
if(act==="save"){var g={},n=b.querySelectorAll("[data-sb-cat]"),i;
for(i=0;i<n.length;i++)g[n[i].getAttribute("data-sb-cat")]=n[i].checked;
return close_(g.analytics,g.marketing);}});
// Withdrawal, from the footer link on every page.
document.addEventListener("click",function(e){
var o=e.target.closest?e.target.closest("[data-sb-consent-open]"):null;
if(!o)return;e.preventDefault();
b.querySelector(".sb-c-prefs").hidden=false;
b.querySelector('[data-sb-c="prefs"]').hidden=true;
b.querySelector('[data-sb-c="save"]').hidden=false;
b.className+=" sb-c-open";
show(read()||{});});
var saved=read();
if(saved)apply(saved.analytics,saved.marketing);else show({});}
window.sbConsent={open:function(){show(read()||{});},get:read};
if(document.readyState==="loading")
document.addEventListener("DOMContentLoaded",wire);else wire();
})();</script>""" % (STORAGE_KEY, VERSION, MAX_AGE_DAYS)
