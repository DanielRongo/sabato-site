#!/usr/bin/env python3
"""Put the Chaport live-chat launcher on every page, exactly once.

Run after every build, with the other injectors (tools/verify.sh does it):

    python3 tools/inject_chat.py

WHY A CLICK-TO-LOAD BUTTON INSTEAD OF CHAPORT'S OWN SNIPPET
-----------------------------------------------------------
Chaport's installation code loads its script on every page view, before the
visitor does anything. That script identifies the browser and reports which
pages it visits. The consent banner on this site promises "nothing runs until
you choose", so loading it up front would make that line false on every page.

Gating it behind the Analytics or Marketing switch would be legal but wrong:
most visitors never open the preferences, so most visitors would never see the
chat at all.

So the page carries our own button and nothing else. Chaport's script loads
only when someone clicks it. A visitor who clicks "chat" has asked for the
service, and storage needed to deliver a service the user explicitly asked for
does not need cookie consent under the Garante's guidelines. Once they have
opened it, a flag in localStorage loads Chaport silently on their later page
views, so an agent's reply still reaches them as they browse.

Chaport's own launcher is switched off (launcher.show = false). Our button is
the only way in, so there is one bubble on screen, in our palette, everywhere.

Snippet supplied verbatim by Daniel, 27 Oct 2026. The vendor loader is kept
byte for byte inside the wrapper; all we do is stop calling it on page load.

Placement: end of <body>, like the consent banner. The Framer pages hydrate a
React tree into #main and delete anything inserted inside it.
"""
import glob
import os
import sys

APP_ID = "6ae0745c47782f0bbb52fd51"

MARK_OPEN = "<!-- Live chat (Sabato) -->"
MARK_CLOSE = "<!-- /Live chat -->"

CSS = (
    ".sb-chat{position:fixed;right:20px;bottom:20px;z-index:2147483000;"
    "width:56px;height:56px;border-radius:100px;border:0;padding:0;cursor:pointer;"
    "background:rgb(0,0,0);color:rgb(204,255,0);display:flex;align-items:center;"
    "justify-content:center;box-shadow:0 0 0 2px rgb(204,255,0);"
    "transition:transform .15s ease}"
    ".sb-chat:hover{transform:scale(1.06)}"
    ".sb-chat:focus-visible{outline:3px solid rgb(0,153,255);outline-offset:3px}"
    ".sb-chat[hidden]{display:none}"
    ".sb-chat svg{width:26px;height:26px;display:block}"
    "@media (max-width:809px){.sb-chat{right:16px;bottom:16px;width:52px;height:52px}}"
)

# Speech bubble, drawn on a 24-unit grid and centred on (12,12): the body spans
# x 3..21 and y 4..17 plus a 3-unit tail, so its visual centre sits on the grid
# centre rather than being nudged by eye.
ICON = (
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M5 4.5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-4 3.5v-3.5H5a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2z" '
    'fill="currentColor"/></svg>'
)

JS = (
    "(function(){"
    "var IT=location.pathname==='/it'||location.pathname.indexOf('/it/')===0;"
    "var K='sb-chat',b=document.getElementById('sb-chat');if(!b)return;"
    "b.setAttribute('aria-label',IT?'Scrivici in chat':'Chat with us');"
    "b.setAttribute('title',IT?'Scrivici in chat':'Chat with us');"
    "function load(){if(window.chaport)return;"
    # Config first: Chaport reads it when its script boots.
    "window.chaportConfig={appId:'" + APP_ID + "',"
    "language:{use:IT?'it':'en'},launcher:{show:false}};"
    # --- vendor loader, verbatim ---
    "(function(w,d,v3){"
    "if(w.chaport)return;v3=w.chaport={};v3._q=[];v3._l={};"
    "v3.q=function(){v3._q.push(arguments)};"
    "v3.on=function(e,fn){if(!v3._l[e])v3._l[e]=[];v3._l[e].push(fn)};"
    "var s=d.createElement('script');s.type='text/javascript';s.async=true;"
    "s.src='https://app.chaport.com/javascripts/insert.js';"
    "var ss=d.getElementsByTagName('script')[0];ss.parentNode.insertBefore(s,ss)"
    "})(window,document);"
    # --- end vendor loader ---
    "}"
    "b.addEventListener('click',function(){"
    "try{localStorage.setItem(K,'1');}catch(e){}"
    "load();window.chaport.q('open');});"
    # A visitor who already opened the chat keeps it across pages.
    "try{if(localStorage.getItem(K)==='1')load();}catch(e){}"
    # Step aside while the cookie banner is up: on a phone both sit bottom-right.
    # The banner markup comes AFTER this snippet in <body>, so look it up once
    # the document has parsed, not now.
    "function watch(){var c=document.getElementById('sb-consent');"
    "function sync(){b.hidden=!!(c&&!c.hidden);}"
    "if(c&&window.MutationObserver){new MutationObserver(sync)"
    ".observe(c,{attributes:true,attributeFilter:['hidden']});}"
    "sync();}"
    "if(document.readyState==='loading')"
    "document.addEventListener('DOMContentLoaded',watch);else watch();"
    "})();"
)

SNIPPET = (
    MARK_OPEN + "\n"
    "<style>" + CSS + "</style>"
    '<button type="button" class="sb-chat" id="sb-chat" aria-label="Chat with us">'
    + ICON + "</button>"
    "<script>" + JS + "</script>\n"
    + MARK_CLOSE + "\n"
)


def strip(src):
    while MARK_OPEN in src:
        a = src.index(MARK_OPEN)
        z = src.index(MARK_CLOSE, a) + len(MARK_CLOSE)
        if src[z:z + 1] == "\n":
            z += 1
        src = src[:a] + src[z:]
    return src


def process(path):
    src = open(path, encoding="utf-8").read()
    out = strip(src)
    if "</body>" not in out:
        return ("no-body", False)
    # rfind: some Framer pages carry "</body>" inside inline JS strings.
    i = out.rfind("</body>")
    out = out[:i] + SNIPPET + out[i:]
    if out != src:
        open(path, "w", encoding="utf-8").write(out)
        return ("injected", True)
    return ("injected", False)


def main():
    files = sorted(set(glob.glob("site/**/*.html", recursive=True) +
                       glob.glob("templates/*.html")))
    if not files:
        sys.exit("no HTML found - run this from the repo root")

    tally, changed = {}, 0
    for f in files:
        action, did = process(f)
        tally[action] = tally.get(action, 0) + 1
        changed += did
    for k in sorted(tally):
        print("  %s: %d" % (k, tally[k]))
    print("%d file(s) scanned, %d written" % (len(files), changed))

    wrong = []
    for f in files:
        s = open(f, encoding="utf-8").read()
        if "</body>" in s and (s.count(MARK_OPEN) != 1 or s.count(APP_ID) != 1):
            wrong.append((f, s.count(MARK_OPEN), s.count(APP_ID)))
    if wrong:
        print("\nCHAT COUNT WRONG (marker, appId):")
        for w in wrong:
            print("   ", w)
        sys.exit(1)
    print("every page carries the chat launcher exactly once")


if __name__ == "__main__":
    main()
