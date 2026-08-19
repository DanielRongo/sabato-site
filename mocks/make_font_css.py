#!/usr/bin/env python3
"""Inline the four upright Satoshi weights as base64 into /tmp/satoshi.css.

Mocks are opened as file:// with no server, so a mock that links the site's
woff2 files renders in Times New Roman and every judgement made from it is
wrong. Read the weights out of the built homepage rather than hard-coding the
hashed paths, which change whenever Framer re-exports.
"""
import base64, os, re, sys

SRC = "site/index.html"
OUT = "/tmp/satoshi.css"

def main():
    if not os.path.exists(SRC):
        sys.exit("run me from the repo root")
    h = open(SRC, encoding="utf-8").read()
    want = {400: None, 500: None, 700: None, 900: None}
    for m in re.finditer(r"@font-face\s*\{[^}]*\}", h):
        b = m.group(0)
        if not re.search(r'font-family:\s*"?Satoshi"?', b):
            continue
        st = re.search(r"font-style:\s*(\w+)", b)
        if st and st.group(1) != "normal":
            continue
        w = re.search(r"font-weight:\s*(\d+)", b)
        u = re.search(r'url\("?([^")]+)"?\)', b)
        if not (w and u):
            continue
        wt = int(w.group(1))
        if wt in want and want[wt] is None:
            want[wt] = u.group(1)
    css = []
    for wt, url in want.items():
        if not url:
            print("missing weight", wt); continue
        p = os.path.join("site", url.lstrip("/"))
        if not os.path.exists(p):
            print("missing file for", wt, p); continue
        data = base64.b64encode(open(p, "rb").read()).decode()
        css.append("@font-face{font-family:Satoshi;font-style:normal;font-weight:%d;"
                   "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}" % (wt, data))
    open(OUT, "w").write("\n".join(css))
    print("wrote", OUT, sum(map(len, css)), "bytes,", len(css), "weights")

if __name__ == "__main__":
    main()
