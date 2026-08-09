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
    # FIRST, and it writes nothing: it only asks whether the last step would
    # refuse. The generators rewrite pages from templates that have no header
    # and no footer, so an abort further down leaves the site half-applied.
    ("tools/apply_footer.py --preflight", "can the footer step run at all?"),
    ("publish.py",   "blog posts + indexes, from posts/*.md"),
    ("customers.py", "case studies, from customer_data*.py - MUST precede industries.py"),
    ("use_cases.py", "use-case hubs, reads the built use-case pages"),
    ("industries.py", "industry pages + indexes, THEN relinks footers site-wide - runs last"),
    ("legal.py",     "terms + privacy, EN and IT, from legal/*.md"),
    ("tools/set_page_meta.py", "metadata for static pages that no generator owns"),
    ("tools/apply_footer.py", "THE footer, from footer.py - must be last, owns every footer"),
]


def main():
    failed = []
    for script, why in STEPS:
        print(f"\n==> {script}   ({why})")
        # split(): a step may carry a flag, e.g. "... --preflight".
        r = subprocess.run([sys.executable] + script.split(), capture_output=True, text=True)
        out = (r.stdout or "").strip().splitlines()
        for line in out[-4:]:
            print(f"    {line}")
        if r.returncode != 0:
            failed.append(script)
            print(f"    FAILED (exit {r.returncode})")
            if r.stderr.strip():
                for line in r.stderr.strip().splitlines()[-4:]:
                    print(f"    {line}")
            # A failed preflight means the LAST step would refuse. Stop here and
            # write nothing: every generator after this point rewrites pages from
            # templates that carry no header and no footer, so carrying on turns
            # a clean refusal into 43 broken pages. Learned the hard way.
            if "--preflight" in script:
                print("\nPreflight failed - nothing was built, nothing was changed.",
                      file=sys.stderr)
                return 1

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
