#!/usr/bin/env python3
"""Pixel-compare the built site against a baseline render of origin/main.

    python3 tools/visual_diff.py --baseline     # capture, from origin/main
    python3 tools/visual_diff.py                # compare the working tree to it
    python3 tools/visual_diff.py --only /       # one page
    python3 tools/visual_diff.py --accept       # bless the current output

WHY THIS EXISTS
---------------
Two things shipped in one day that no gate here could see.

  * The hero's wave video was deleted, because <video preload="none"> with no
    poster paints black, this container's Chromium has no H.264 decoder, and
    black-on-black looks exactly like empty padding. Every link still worked;
    every existing check passed.
  * The hero card was given a fixed 40px inset when Framer uses 30px plus a
    1360px cap. Correct at 1440 and wrong at every other width, so it passed a
    sweep that only ever looked at 1440.

Both are invisible to link audits, contrast audits and footer tests, and both
are one screenshot apart from obvious. The remaining Framer sections get
rebuilt one at a time; without this, each rebuild is another coin flip.

HOW IT AVOIDS CRYING WOLF
-------------------------
A naive pixel diff on this site fails on the first run, forever, for reasons
that are not bugs:

  * The hero wave is a playing video. Two runs never agree on a frame. Media is
    aborted at the network layer, so a video is a flat box in both renders.
  * Framer animates on scroll and on load. Renders settle at slightly different
    times, so the tool waits for two consecutive identical frames of its own
    before it captures, up to a cap.
  * Anti-aliasing puts 1-2 units of noise on text edges. A pixel only counts as
    changed when a channel moves more than CHANNEL_TOL.

What is left after that is real. The threshold is per-page and deliberately
tight: this is a "tell me what moved" tool, not a "roughly similar" one.

The baseline lives in .visual-baseline/ and is gitignored - it is a local
artefact, regenerated from origin/main whenever you want a new reference.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(ROOT, ".visual-baseline")
PORT_A, PORT_B = 8931, 8932

WIDTHS = [("phone", 390), ("desktop", 1440)]

# The pages worth watching. Every distinct template plus both languages of the
# two homepages - not all 74, because a diff nobody reads is a diff nobody acts
# on, and the generated pages differ from each other only by content.
PAGES = [
    "/", "/it",
    "/pricing", "/about", "/contact",
    "/it/prezzi", "/it/chi-siamo", "/it/contatti",
    "/use-cases/", "/industries/", "/blog",
    "/use-cases/where-is-my-order", "/industries/fashion-apparel",
    "/customers/creative-cables", "/blog/reduce-bracketing-returns",
    "/it/casi-duso/", "/it/settori/", "/it/blog",
    "/roi-calculator", "/terms", "/privacy-policy",
    "/it/termini-e-condizioni", "/it/privacy-e-cookie",
]

# A pixel counts as changed only if some channel moves more than this. Text
# anti-aliasing and gradient banding sit at 1-2; anything real clears it easily.
CHANNEL_TOL = 8

# TWO thresholds, because this site is two sites.
#
# Our generated pages are static HTML with no runtime: two renders are identical
# to the pixel. Measured across 25 shots of blog, use-cases, industries,
# customers and legal - every one 0.000%. They get a threshold just off zero.
#
# The Framer-exported pages still run React + `motion`. Even with CSS animation
# frozen, every Web Animations entry finish()ed, and a full scroll pass to fire
# every IntersectionObserver, two renders of the SAME commit still disagree by
# 0.3-1.8%. That is the floor, measured, not guessed. Chasing it further is not
# worth the hours - anything this tool needs to catch is an order of magnitude
# above it (the hero rebuild reads 18-28%).
#
# The good part: this list shrinks as the migration proceeds. Every section that
# stops being Framer's takes some of that noise with it, and when the runtime
# finally goes, every page drops to the tight threshold.
THRESHOLD = 0.0005          # 0.05% - our own pages
THRESHOLD_FRAMER = 0.025    # 2.5%  - pages still running Framer's runtime

FRAMER_PAGES = {"home", "it", "pricing", "about", "contact",
                "it_prezzi", "it_chi-siamo", "it_contatti"}


def threshold_for(name):
    return THRESHOLD_FRAMER if name.split(".")[0] in FRAMER_PAGES else THRESHOLD


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True,
                          text=True, **kw)


def serve(root, port):
    """Serve `root`'s site/ - using THAT tree's copy of the server script.

    serve_like_netlify.py resolves site/ relative to its own file, not to cwd.
    Launching this repo's copy with cwd=<extracted baseline> therefore served
    the working tree on both ports, so the first baseline captured was of the
    code under test and every real change read as 0.000%. A diff tool that
    cannot fail is worse than none: it certifies whatever you did.
    """
    script = os.path.join(root, "tools", "serve_like_netlify.py")
    if not os.path.exists(script):
        raise SystemExit(f"visual_diff: no server script in {root}")
    return subprocess.Popen([sys.executable, script, str(port)], cwd=root,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def capture(base_url, outdir, pages):
    """Screenshot every page x width into outdir. Returns [(name, path)]."""
    from playwright.sync_api import sync_playwright
    os.makedirs(outdir, exist_ok=True)
    made = []
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                               args=["--no-sandbox"])
        for wname, w in WIDTHS:
            ctx = br.new_context(viewport={"width": w, "height": 1000})
            # Video and audio never render deterministically - a playing wave is
            # a different frame every run. Blocking them at the network layer
            # makes both sides a flat box, which is comparable.
            ctx.route("**/*.{mp4,webm,mov,mp3,m4a,ogg}", lambda r: r.abort())
            for path in pages:
                page = ctx.new_page()
                try:
                    page.goto(base_url + path, wait_until="load", timeout=45000)
                except Exception as e:
                    print(f"  !! {path} @{wname}: {type(e).__name__}")
                    page.close()
                    continue
                settle(page)
                name = f"{path.strip('/').replace('/', '_') or 'home'}.{wname}.png"
                out = os.path.join(outdir, name)
                page.screenshot(path=out, full_page=True)
                made.append((name, out))
                page.close()
            ctx.close()
        br.close()
    return made


FREEZE = """
  *, *::before, *::after {
    animation-duration: 0s !important;
    animation-delay: 0s !important;
    transition-duration: 0s !important;
    transition-delay: 0s !important;
  }
  html { scroll-behavior: auto !important; }
"""


def settle(page, tries=10, gap=300):
    """Make the page deterministic, then wait for it to stop moving.

    Three separate sources of noise, all of which produced half-percent diffs
    between two renders of the SAME commit:

      * CSS animations and transitions mid-flight. Frozen by FREEZE.
      * Framer reveals content on IntersectionObserver. A full-page screenshot
        scrolls, so whether a section had been revealed depended on timing. The
        page is scrolled to the bottom once to fire every observer, then back to
        the top, so both renders capture the same, fully-revealed state.
      * Lazy images. The scroll pass loads them too; then we wait for the height
        to stop changing.
    """
    page.add_style_tag(content=FREEZE)
    page.evaluate("""async () => {
        const step = Math.round(window.innerHeight * 0.8);
        for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 60));
        }
        window.scrollTo(0, document.documentElement.scrollHeight);
        await new Promise(r => setTimeout(r, 250));
        window.scrollTo(0, 0);
        await new Promise(r => setTimeout(r, 250));
        // Framer animates with the Web Animations API through `motion`, not CSS
        // transitions, so the FREEZE stylesheet does not touch it. finish()
        // jumps every one of them to its end state. Run twice: finishing an
        // animation can start the next in a sequence.
        for (let i = 0; i < 2; i++) {
            document.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} });
            await new Promise(r => setTimeout(r, 120));
        }
    }""")
    page.wait_for_timeout(500)
    last = -1
    for _ in range(tries):
        h = page.evaluate("() => document.documentElement.scrollHeight")
        if h == last:
            break
        last = h
        page.wait_for_timeout(gap)
    page.wait_for_timeout(300)


def compare(a_path, b_path):
    """(changed_fraction, note). Size mismatch is itself a finding."""
    from PIL import Image, ImageChops
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    if a.size != b.size:
        # Padded to the union so a height change does not hide a content change
        # somewhere above it.
        w = max(a.size[0], b.size[0])
        h = max(a.size[1], b.size[1])
        note = f"size {a.size[0]}x{a.size[1]} -> {b.size[0]}x{b.size[1]}"
        pa = Image.new("RGB", (w, h), (255, 0, 255)); pa.paste(a, (0, 0))
        pb = Image.new("RGB", (w, h), (255, 0, 255)); pb.paste(b, (0, 0))
        a, b = pa, pb
    else:
        note = ""
    diff = ImageChops.difference(a, b)
    # Any channel over tolerance marks the pixel.
    mask = diff.point(lambda v: 255 if v > CHANNEL_TOL else 0).convert("L")
    changed = sum(mask.histogram()[1:])   # every non-zero bucket
    return changed / float(a.size[0] * a.size[1]), note


def write_side_by_side(a_path, b_path, out):
    from PIL import Image, ImageChops
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    h = max(a.size[1], b.size[1])
    w = max(a.size[0], b.size[0])
    canvas = Image.new("RGB", (w * 3 + 40, h), (240, 240, 240))
    canvas.paste(a, (0, 0))
    canvas.paste(b, (w + 20, 0))
    pa = Image.new("RGB", (w, h)); pa.paste(a, (0, 0))
    pb = Image.new("RGB", (w, h)); pb.paste(b, (0, 0))
    canvas.paste(ImageChops.difference(pa, pb), (w * 2 + 40, 0))
    canvas.save(out)


def baseline():
    """Render origin/main into .visual-baseline/."""
    r = sh("git rev-parse origin/main")
    if r.returncode != 0:
        print("cannot resolve origin/main - run git fetch origin", file=sys.stderr)
        return 1
    ref = r.stdout.strip()
    tmp = tempfile.mkdtemp(prefix="visbase-")
    sh(f"git archive {ref} | tar -x -C {tmp}")
    srv = serve(tmp, PORT_A)
    try:
        import time
        time.sleep(4)
        if os.path.isdir(BASE_DIR):
            sh(f"rm -rf {BASE_DIR}")
        made = capture(f"http://127.0.0.1:{PORT_A}", BASE_DIR, PAGES)
        with open(os.path.join(BASE_DIR, "meta.json"), "w") as f:
            json.dump({"ref": ref, "pages": len(PAGES), "shots": len(made)}, f, indent=1)
    finally:
        srv.terminate()
    print(f"baseline: {len(made)} shot(s) from origin/main {ref[:8]} -> .visual-baseline/")
    return 0


def run(only, accept):
    if not os.path.isdir(BASE_DIR):
        print("no baseline - run: python3 tools/visual_diff.py --baseline", file=sys.stderr)
        return 1
    meta = json.load(open(os.path.join(BASE_DIR, "meta.json")))
    pages = [p for p in PAGES if (only is None or p == only)]
    outdir = os.path.join(ROOT, ".visual-current")
    sh(f"rm -rf {outdir}")
    srv = serve(ROOT, PORT_B)
    try:
        import time
        time.sleep(4)
        capture(f"http://127.0.0.1:{PORT_B}", outdir, pages)
    finally:
        srv.terminate()

    reportdir = os.path.join(ROOT, ".visual-report")
    sh(f"rm -rf {reportdir}")
    os.makedirs(reportdir, exist_ok=True)

    rows, failed = [], 0
    for name in sorted(os.listdir(outdir)):
        if not name.endswith(".png"):
            continue
        cur = os.path.join(outdir, name)
        base = os.path.join(BASE_DIR, name)
        if not os.path.exists(base):
            rows.append((name, None, "NEW - not in baseline"))
            continue
        frac, note = compare(base, cur)
        flag = frac > threshold_for(name)
        if flag:
            failed += 1
            write_side_by_side(base, cur, os.path.join(reportdir, name))
        rows.append((name, frac, note))

    print(f"\nbaseline origin/main {meta['ref'][:8]}   tolerance {CHANNEL_TOL}/255   "
          f"threshold {THRESHOLD*100:.2f}% ours / {THRESHOLD_FRAMER*100:.1f}% Framer\n")
    for name, frac, note in sorted(rows, key=lambda r: -(r[1] or 0)):
        if frac is None:
            print(f"  ????  {name}  {note}")
        else:
            mark = "CHANGED" if frac > threshold_for(name) else "ok     "
            print(f"  {mark}  {frac*100:6.3f}%  {name}  {note}")

    if accept:
        sh(f"rm -rf {BASE_DIR} && cp -a {outdir} {BASE_DIR}")
        json.dump(meta, open(os.path.join(BASE_DIR, "meta.json"), "w"))
        print("\naccepted: current output is the new baseline")
        return 0

    if failed:
        print(f"\n{failed} page(s) changed. Side-by-side + diff written to "
              f".visual-report/ - LOOK AT THEM before deciding.")
        print("If every change is intended: python3 tools/visual_diff.py --accept")
        return 1
    print("\nVISUAL DIFF CLEAN")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--accept", action="store_true")
    a = ap.parse_args()
    return baseline() if a.baseline else run(a.only, a.accept)


if __name__ == "__main__":
    sys.exit(main())
