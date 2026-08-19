# -*- coding: utf-8 -*-
"""D2 on a light page: the two ways to make the homepage dial card work here.

The card component in hero.py is styled for .sb-hero-card, which is #000. Its
country label is rgba(255,255,255,.45) and its fill is rgba(255,255,255,.05),
so dropping it on the white pricing hero renders it white on white. Either the
row gets a dark panel to sit on, or the card gets a light variant.
"""
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

def cards():
    out = []
    for i, (c, flag, lab, disp, tel) in enumerate(NUMBERS):
        # third card shown in its revealed state so both states are visible
        op = " is-open" if i == 2 else ""
        out.append(
          f'<a class="sb-hero-num{op}" href="tel:{tel}">'
          f'<span class="sb-hero-cc">{flag} {lab}</span>'
          f'<span class="sb-hero-slot"><span class="sb-hero-no">{disp}</span>'
          f'<span class="sb-hero-reveal">Show number</span></span>'
          f'<span class="sb-hero-call">{PHONE}Call now</span></a>')
    return '<div class="sb-hero-nums">' + "".join(out) + '</div>'

INCLUDED = ["the build", "the integrations", "every workflow",
            "every language you sell in", "proactive human management",
            "agent evaluation and optimization"]
GRID6 = "".join(f'<div class="gi"><span class="tick">&#10003;</span>{c}</div>' for c in INCLUDED)
NOTCHARGED = ["platform fee", "setup fee", "per seat license", "per workflow charge",
              "language surcharge", "minimum contract"]
NOTS = "".join(f'<span class="nochip">{c}</span>' for c in NOTCHARGED)

def hero(dialwrap):
    return f'''<div class="hero">
  <span class="eyebrow">PRICING</span>
  <h1>You only pay when<br>the line is talking.</h1>
  <div class="box"><div class="boxtop">
      <div class="bignum"><span class="cur">$</span>0.65<span class="per">per minute of talk</span></div>
      <div class="allinwrap"><span class="allin">ALL IN <em>managed service included</em></span></div>
      <div class="boxsub">billed by the second, so a 40 second call costs 40 seconds. Volume brings the rate down to $0.55.</div>
    </div>
    <div class="boxbot"><div class="boxbot-h">everything below is already in that number</div>
      <div class="grid6">{GRID6}</div></div></div>
  <div class="nots">{NOTS}<span class="notlab">not charged, ever</span></div>
  <div class="ctas"><span class="btn">Book a call</span></div>
  {dialwrap}
</div>'''

DARK = ('<div class="dialpanel"><div class="diallab dark">or call the agent right now, it picks up</div>'
        + cards() + '</div>')
LIGHT = ('<div class="dialpanel light"><div class="diallab">or call the agent right now, it picks up</div>'
         + cards() + '</div>')

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Satoshi,sans-serif;background:#EEEBE7;color:rgb(11,11,12);-webkit-font-smoothing:antialiased;padding:44px 20px 80px}
.doc{max-width:1180px;margin:0 auto}
.dochead h1{font-size:30px;letter-spacing:-.9px;font-weight:900}
.dochead p{font-size:15px;color:#5F5A55;margin:8px 0 38px;max-width:800px;line-height:1.55}
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
.allin{background:rgb(204,255,0);color:rgb(11,11,12);border-radius:999px;padding:9px 17px;font-size:12.5px;font-weight:900;
 letter-spacing:.14em;display:inline-flex;align-items:center;gap:8px;border:1.5px solid rgb(11,11,12)}
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

/* the panel that holds the row */
.dialpanel{max-width:880px;margin:26px auto 0;background:#000;border-radius:20px;padding:22px 24px 26px}
.dialpanel.light{background:transparent;padding:8px 0 0}
.diallab{font-size:13px;color:#6F6A65;margin-bottom:4px}
.diallab.dark{color:rgba(255,255,255,.5)}

/* verbatim from footer.css, the component as it exists today */
.sb-hero-nums{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;width:min(880px,100%);margin:18px auto 0}
.sb-hero-num{display:flex;flex-direction:column;align-items:center;gap:5px;text-decoration:none;
 background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.11);border-radius:16px;padding:18px 12px 16px}
.sb-hero-cc{font-size:11px;letter-spacing:1.6px;font-weight:700;text-transform:uppercase;color:rgba(255,255,255,.45)}
.sb-hero-slot{display:grid;justify-items:center}
.sb-hero-slot>*{grid-area:1/1}
.sb-hero-no{font-size:15px;font-weight:700;color:#fff;font-variant-numeric:tabular-nums}
.sb-hero-reveal{font-size:12px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,.55)}
.sb-hero-call{display:inline-flex;align-items:center;justify-content:center;gap:5px;font-size:11px;font-weight:700;
 letter-spacing:1.4px;text-transform:uppercase;color:#CCFF00;border-radius:9px;padding:8px 12px;margin:-5px 0}
.sb-hero-reveal,.sb-hero-call{visibility:hidden}
.sb-hero-num .sb-hero-no{visibility:hidden}
.sb-hero-num .sb-hero-reveal{visibility:visible}
.sb-hero-num.is-open .sb-hero-no{visibility:visible}
.sb-hero-num.is-open .sb-hero-reveal{visibility:hidden}
.sb-hero-num.is-open .sb-hero-call{visibility:visible}
.sb-hero-num.is-open{background:rgba(204,255,0,.1);border-color:rgba(204,255,0,.45)}

/* the light variant: six namespaced overrides, nothing else changes */
.light .sb-hero-num{background:#fff;border:1px solid #DED9D3}
.light .sb-hero-cc{color:#6F6A65}
.light .sb-hero-no{color:rgb(11,11,12)}
.light .sb-hero-reveal{color:#8A847E}
.light .sb-hero-call{color:rgb(11,11,12);background:rgb(204,255,0)}
.light .sb-hero-num.is-open{background:#FBFCFE;border-color:rgb(11,11,12)}
"""
def sec(n,tag,body,why):
    return f'''<section class="wf"><div class="wfhead"><span class="num">{n}</span><span class="tag">{tag}</span></div>
<div class="frame">{body}</div><div class="why"><b>note</b>{why}</div></section>'''

HTML=f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>D2 on a light page</title>
<style>{FONTS}</style><style>{CSS}</style></head><body><div class="doc">
<div class="dochead"><h1>D2 needs a decision I did not flag</h1>
<p>The homepage card is built for a black panel. On the white pricing hero it renders white on white, so reusing it is either a dark strip or a light variant. Third card in each row is shown revealed, so you can see both states at once.</p></div>
{sec("D2a","dark strip, component untouched",hero(DARK),
 "The component ships exactly as it is today, no CSS added, no risk of a collision like the footer one. The strip also does useful work: it separates the price, which is a light object, from the invitation to test it, which is a dark one. It echoes the homepage hero without repeating it.")}
{sec("D2b","light variant, six namespaced overrides",hero(LIGHT),
 "Keeps the hero one continuous light surface. Costs six rules, all scoped under a wrapper class so nothing can leak the way .sb-col did. The reveal loses a little of its punch because the lime CALL NOW is doing the work on white rather than glowing on black.")}
</div></body></html>"""
open('/home/claude/mock/pricing-dial2.html','w',encoding='utf-8').write(HTML)
print("ok")
