# -*- coding: utf-8 -*-
FONTS = open('/tmp/satoshi.css', encoding='utf-8').read()

NUMBERS = [
    ("gb", "\U0001F1EC\U0001F1E7", "United Kingdom", "+44 20 3893 2636",  "+442038932636"),
    ("us", "\U0001F1FA\U0001F1F8", "United States",  "+1 754 208 0610",   "+17542080610"),
    ("it", "\U0001F1EE\U0001F1F9", "Italia",         "+39 081 1818 1316", "+3908118181316"),
    ("es", "\U0001F1EA\U0001F1F8", "España",    "+34 871 073 084",   "+34871073084"),
]
PHONE = ('<svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
 '<path d="M6.6 2.8h3.1l1.6 4-2 1.2a11.3 11.3 0 0 0 4.7 4.7l1.2-2 4 1.6v3.1'
 'a1.6 1.6 0 0 1-1.7 1.6A15.8 15.8 0 0 1 5 6.1a1.6 1.6 0 0 1 1.6-1.7Z" '
 'stroke="currentColor" stroke-width="2.1" stroke-linejoin="round"/></svg>')

INCLUDED = ["the build", "the integrations", "every workflow",
            "every language you sell in", "proactive human management",
            "agent evaluation and optimization"]
NOTCHARGED = ["platform fee", "setup fee", "per seat license", "per workflow charge",
              "language surcharge", "minimum contract"]
GRID6 = "".join(f'<div class="gi"><span class="tick">&#10003;</span>{c}</div>' for c in INCLUDED)
NOTS  = "".join(f'<span class="nochip">{c}</span>' for c in NOTCHARGED)

# D1: one line, numbers visible
D1 = '<div class="diallab">or call the agent right now, it picks up</div><div class="dialrow">' + "".join(
  f'<a class="dial" href="tel:{tel}"><span class="fl">{flag}</span>'
  f'<span class="dnum">{disp}</span>{PHONE}</a>' for c, flag, lab, disp, tel in NUMBERS) + '</div>'

# D2: homepage component, masked until click
D2 = '<div class="diallab">or call the agent right now, it picks up</div><div class="dialrow cards">' + "".join(
  f'<a class="dcard" href="tel:{tel}"><span class="fl">{flag}</span>'
  f'<span class="dlab">{lab}</span><span class="dmask">Show number</span></a>'
  for c, flag, lab, disp, tel in NUMBERS) + '</div>'

def hero(dial):
    return f'''<div class="hero">
  <span class="eyebrow">PRICING</span>
  <h1>You only pay when<br>the line is talking.</h1>
  <div class="box">
    <div class="boxtop">
      <div class="bignum"><span class="cur">$</span>0.65<span class="per">per minute of talk</span></div>
      <div class="allinwrap"><span class="allin">ALL IN <em>managed service included</em></span></div>
      <div class="boxsub">billed by the second, so a 40 second call costs 40 seconds. Volume brings the rate down to $0.55.</div>
    </div>
    <div class="boxbot"><div class="boxbot-h">everything below is already in that number</div>
      <div class="grid6">{GRID6}</div></div>
  </div>
  <div class="nots">{NOTS}<span class="notlab">not charged, ever</span></div>
  <div class="ctas"><span class="btn">Book a call</span></div>
  {dial}
</div>'''

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Satoshi,sans-serif;background:#EEEBE7;color:rgb(11,11,12);-webkit-font-smoothing:antialiased;padding:44px 20px 80px}
.doc{max-width:1180px;margin:0 auto}
.dochead h1{font-size:30px;letter-spacing:-.9px;font-weight:900}
.dochead p{font-size:15px;color:#5F5A55;margin:8px 0 38px;max-width:780px;line-height:1.55}
.wf{margin:0 0 34px}
.wfhead{display:flex;align-items:center;gap:12px;margin-bottom:9px}
.num{font-size:11px;font-weight:900;letter-spacing:.14em;background:rgb(11,11,12);color:#fff;padding:4px 9px;border-radius:5px}
.tag{font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#6F6A65}
.frame{background:#fff;border:1px solid #DED9D3;border-radius:16px;padding:50px 46px 54px}
.why{display:flex;gap:12px;margin-top:9px;padding:12px 15px;background:#E4E0DA;border-radius:10px;font-size:13.5px;line-height:1.6;color:#413D39}
.why b{font-size:10px;font-weight:900;letter-spacing:.15em;text-transform:uppercase;color:#8A847E;flex:none;padding-top:3px}
.hero{text-align:center}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.18em;color:#6F6A65}
.hero h1{font-size:52px;line-height:1.05;letter-spacing:-2px;font-weight:900;margin-top:14px}
.box{max-width:840px;margin:30px auto 0;border:2px solid rgb(11,11,12);border-radius:20px;overflow:hidden}
.boxtop{padding:36px 30px 28px}
.bignum{display:flex;align-items:baseline;justify-content:center;gap:9px;font-size:74px;font-weight:900;letter-spacing:-3px;line-height:1}
.bignum .cur{font-size:38px;letter-spacing:-1px}
.bignum .per{font-size:17px;font-weight:700;color:#6F6A65;letter-spacing:0;margin-left:4px}
.allinwrap{margin-top:16px}
.allin{background:rgb(204,255,0);color:rgb(11,11,12);border-radius:999px;padding:9px 17px;font-size:12.5px;
 font-weight:900;letter-spacing:.14em;display:inline-flex;align-items:center;gap:8px;border:1.5px solid rgb(11,11,12)}
.allin em{font-style:normal;font-size:11px;font-weight:700;letter-spacing:.02em;text-transform:none;border-left:1px solid rgba(11,11,12,.35);padding-left:8px}
.boxsub{margin-top:14px;font-size:14.5px;color:#5F5A55}
.boxbot{background:rgb(204,255,0);padding:20px 30px 26px}
.boxbot-h{font-size:11px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;color:rgba(11,11,12,.62);margin-bottom:14px}
.grid6{display:grid;grid-template-columns:repeat(3,1fr);gap:12px 22px;text-align:left}
.gi{display:flex;align-items:flex-start;gap:9px;font-size:14.5px;font-weight:700;line-height:1.3}
.tick{font-size:13px;font-weight:900;line-height:1.45;flex:none}
.nots{margin:18px auto 0;max-width:840px;display:flex;flex-wrap:wrap;gap:7px;justify-content:center;align-items:center}
.nochip{font-size:12.5px;color:#A8A29C;text-decoration:line-through}
.nochip:not(:last-of-type)::after{content:"·";margin-left:7px;display:inline-block;text-decoration:none;color:#C9C3BD}
.notlab{font-size:11px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:#6F6A65}
.ctas{display:flex;gap:12px;justify-content:center;margin-top:30px}
.btn{background:rgb(11,11,12);color:#fff;border-radius:999px;padding:14px 30px;font-size:14.5px;font-weight:700}
.diallab{margin-top:20px;font-size:13px;color:#6F6A65}
.dialrow{display:flex;flex-wrap:wrap;gap:9px;justify-content:center;margin-top:12px}
.dial{display:inline-flex;align-items:center;gap:9px;text-decoration:none;color:rgb(11,11,12);
 border:1px solid #DED9D3;border-radius:999px;padding:9px 15px;background:#fff;transition:border-color .15s,background .15s}
.dial:hover{border-color:rgb(11,11,12);background:#FBFCFE}
.dial .fl{font-size:15px;line-height:1}
.dnum{font-size:13.5px;font-weight:700;letter-spacing:-.1px;font-variant-numeric:tabular-nums}
.dial svg{color:#A29C96}
.dial:hover svg{color:rgb(11,11,12)}
.dcard{display:inline-flex;align-items:center;gap:10px;text-decoration:none;color:rgb(11,11,12);
 border:1px solid #DED9D3;border-radius:12px;padding:11px 16px;background:#fff}
.dlab{font-size:13.5px;font-weight:700}
.dmask{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#8A847E;
 border-left:1px solid #E7E4E0;padding-left:10px}
"""
def sec(n,tag,body,why):
    return f'''<section class="wf"><div class="wfhead"><span class="num">{n}</span><span class="tag">{tag}</span></div>
<div class="frame">{body}</div><div class="why"><b>note</b>{why}</div></section>'''

HTML=f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Pricing hero, dial options</title>
<style>{FONTS}</style><style>{CSS}</style></head><body><div class="doc">
<div class="dochead"><h1>The dial row, two ways</h1>
<p>"Talk to the agent right now" is gone as a button. In both versions the four lines sit under Book a call, so the primary action stays single and the secondary one is a choice of country rather than a second button competing with the first.</p></div>
{sec("D1","numbers visible, one line",hero(D1),
 "Numbers in the clear. A visitor this deep is deciding whether we are real, and a number they can read and dial in one motion answers that faster than a button that asks them to click first. Tabular figures so the four line up. This deviates from the homepage, where the numbers are masked behind Show number.")}
{sec("D2","the homepage component, reused as is",hero(D2),
 "Identical behaviour to the homepage: masked, first click reveals, second click dials, and with JS off all four numbers render readable rather than as dead buttons. Zero new code, since hero.py already emits this. Costs one extra click at the exact moment somebody wants to test us.")}
</div></body></html>"""
open('/home/claude/mock/pricing-dial.html','w',encoding='utf-8').write(HTML)
print("ok")
