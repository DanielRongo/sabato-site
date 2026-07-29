#!/usr/bin/env python3
"""Re-hash edited Framer bundle files so cached copies can't go stale.

site/fuc/* is served with `Cache-Control: immutable, max-age=1y` because Framer
names those files by content hash. If we EDIT one in place the name stays the
same, so returning visitors keep the old copy for up to a year.

This script gives every edited file a fresh hash in its filename and rewrites
every reference to it across the site. Run it after editing anything under
site/fuc/, before deploying:

    python3 tools/rehash_edited_assets.py            # rehash files changed vs the initial commit
    python3 tools/rehash_edited_assets.py <ref>      # ...changed vs an arbitrary git ref
"""
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
TEXT_EXT = re.compile(r"\.(html|mjs|js|json|xml)$")

# NAME.<hash>.mjs   |   searchIndex-<hash>.json
MJS = re.compile(r"^(?P<stem>.+)\.(?P<hash>[A-Za-z0-9_-]{6,12})\.mjs$")
IDX = re.compile(r"^(?P<stem>searchIndex)-(?P<hash>[A-Za-z0-9_-]{6,16})\.json$")


def short_hash(path):
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    return h[:10]


def changed_files(ref):
    out = subprocess.run(
        ["git", "diff", "--name-only", ref, "HEAD", "--", "site/fuc/"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.split()
    # include uncommitted edits too
    out += subprocess.run(
        ["git", "diff", "--name-only", "--", "site/fuc/"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.split()
    return sorted(set(p for p in out if os.path.exists(os.path.join(ROOT, p))))


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"],
        cwd=ROOT, capture_output=True, text=True).stdout.strip()

    def rewrite_refs(renames):
        touched = 0
        for dirpath, _, files in os.walk(SITE):
            for fn in files:
                if not TEXT_EXT.search(fn):
                    continue
                fp = os.path.join(dirpath, fn)
                try:
                    t = open(fp, encoding="utf-8").read()
                except UnicodeDecodeError:
                    continue
                orig = t
                for old, new in renames.items():
                    if old in t:
                        t = t.replace(old, new)
                if t != orig:
                    open(fp, "w", encoding="utf-8").write(t)
                    touched += 1
        return touched

    # Renaming a file changes its referrers, which are themselves immutable-cached,
    # so they must be rehashed too. Iterate until nothing new needs renaming.
    all_renames = {}
    done = set()
    for round_no in range(1, 11):
        renames = {}
        for rel in changed_files(ref):
            abs_path = os.path.join(ROOT, rel)
            name = os.path.basename(rel)
            if name in done or not os.path.exists(abs_path):
                continue
            m = MJS.match(name) or IDX.match(name)
            if not m:
                continue
            new_hash = short_hash(abs_path)
            if new_hash == m.group("hash"):
                continue
            if name.endswith(".mjs"):
                new_name = f'{m.group("stem")}.{new_hash}.mjs'
            else:
                new_name = f'{m.group("stem")}-{new_hash}.json'
            os.rename(abs_path, os.path.join(os.path.dirname(abs_path), new_name))
            renames[name] = new_name
            done.add(name)
            done.add(new_name)
            print(f"  [round {round_no}] {name}\n              -> {new_name}")
        if not renames:
            break
        rewrite_refs(renames)
        all_renames.update(renames)

    if not all_renames:
        print("nothing to rehash — all edited assets already have fresh names")
        return 0
    print(f"\nrenamed {len(all_renames)} file(s) across {round_no} round(s)")

    dangling = []
    for dirpath, _, files in os.walk(SITE):
        for fn in files:
            if not TEXT_EXT.search(fn):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                t = open(fp, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            for old in all_renames:
                if old in t:
                    dangling.append((os.path.relpath(fp, ROOT), old))
    if dangling:
        print("DANGLING REFERENCES:")
        for f, o in dangling:
            print("  ", f, "->", o)
        return 1
    print("no dangling references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
