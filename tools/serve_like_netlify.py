#!/usr/bin/env python3
"""Static server that mimics Netlify's pretty-URL routing, so the post-deploy
sweep can run offline against the built site.

Netlify serves /blog/foo from /blog/foo.html and /it from /it.html. python's
http.server does not, so a local run of postdeploy_check.py against a plain
static server 404s on every extensionless path. Use this instead:

    python3 tools/serve_like_netlify.py 8909 &
    python3 tools/postdeploy_check.py http://127.0.0.1:8909
"""
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")


class NetlifyLike(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        full = super().translate_path(path)
        if os.path.isdir(full):
            for cand in ("index.html",):
                if os.path.exists(os.path.join(full, cand)):
                    return os.path.join(full, cand)
            # /it -> /it.html when /it/ has no index
            if os.path.exists(full.rstrip(os.sep) + ".html"):
                return full.rstrip(os.sep) + ".html"
        if not os.path.exists(full) and not os.path.splitext(full)[1]:
            if os.path.exists(full + ".html"):
                return full + ".html"
        return full

    def guess_type(self, path):
        # Mirror the site/_headers rule for Framer's hash-suffixed icon modules
        # (e.g. plus.js@0.0.29). Must override guess_type, not add a header in
        # end_headers: SimpleHTTPRequestHandler already sent one Content-Type by
        # then, and the browser honours the first — which rejects ES modules.
        if ".js@" in path or path.endswith((".js", ".mjs")):
            return "text/javascript"
        return super().guess_type(path)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8909
    os.chdir(ROOT)
    ThreadingHTTPServer(("127.0.0.1", port), partial(NetlifyLike, directory=ROOT)).serve_forever()
