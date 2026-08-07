#!/usr/bin/env python3
"""Run every generator in the one order that is correct.

    python3 build.py

BUILD ORDER IS NOT ARBITRARY. Two steps reach outside their own pages:

  * industries.py ends with link_footer_industries(), which rewrites the footer
    industry list on ~24 pages, including blog, use-case and CUSTOMER pages -
    turning inert <span> labels into real links.
  * tools/set_page_meta.py patches metadata on static pages after they exist.

So any generator that rebuilds a page from a template must run BEFORE
industries.py, or it overwrites those footer links with the template's spans.

That is not hypothetical. On 6 Aug 2026 the order was
publish -> industries -> customers, and customers.py silently wiped nine footer
links from every customer page. It shipped to production that way.

inject_ga.py deliberately is NOT here: it must be the last thing to touch any
HTML, and tools/verify.sh already runs it as part of the gate. Running it here
too would only invite someone to run a generator afterwards and strip the tag.
"""
import subprocess
import sys

# (script, why it sits here)
STEPS = [
    ("publish.py",   "blog posts + indexes, from posts/*.md"),
    ("customers.py", "case studies, from customer_data*.py - MUST precede industries.py"),
    ("use_cases.py", "use-case hubs, reads the built use-case pages"),
    ("industries.py", "industry pages + indexes, THEN relinks footers site-wide - runs last"),
    ("tools/set_page_meta.py", "metadata for static pages that no generator owns"),
    ("tools/apply_footer.py", "THE footer, from footer.py - must be last, owns every footer"),
]


def main():
    failed = []
    for script, why in STEPS:
        print(f"\n==> {script}   ({why})")
        r = subprocess.run([sys.executable, script], capture_output=True, text=True)
        out = (r.stdout or "").strip().splitlines()
        for line in out[-4:]:
            print(f"    {line}")
        if r.returncode != 0:
            failed.append(script)
            print(f"    FAILED (exit {r.returncode})")
            if r.stderr.strip():
                print(f"    {r.stderr.strip().splitlines()[-1]}")

    print("\n==> tools/version_enhance.py   (cache-bust enhance.js everywhere)")
    r = subprocess.run([sys.executable, "tools/version_enhance.py"], capture_output=True, text=True)
    print(f"    {(r.stdout or '').strip().splitlines()[-1] if r.stdout.strip() else 'no output'}")

    if failed:
        print(f"\n{len(failed)} step(s) failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("\nBuild complete. Now run:  bash tools/verify.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
