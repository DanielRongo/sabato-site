# The deploy bridge - Cowork ↔ GitHub ↔ Netlify

Read this before touching a deploy. `SABATO-SITE-HANDBOOK.md` is the permanent
playbook for the site itself; this file is the permanent playbook for **getting
changes out of a Claude session and onto the internet**.

---

## The one fact that shapes everything

A Cowork session and your Mac are **two different computers**, and each is
missing something the other has:

| | Claude's cloud container | Your Mac (via the Cowork bridge) |
|---|---|---|
| Network | yes | **no** |
| Playwright + Chromium | yes (`/opt/pw-browsers/chromium`) | no, and cannot install it |
| Your GitHub credentials | no | yes |
| Survives the session | **no** - wiped | yes |

`tools/postdeploy_check.py` needs Playwright, so **verification can only happen
in the cloud**. Pushing needs credentials and network, so **deploying can only
happen on your Mac**. There is no arrangement where one machine does both.

That is not a limitation to work around. It is the safety model: the machine
that checks the work is not the machine that can ship it.

---

## The flow

```
   ┌─ CLAUDE (cloud container) ──────────────┐
   │  1. git clone (public repo, no creds)   │
   │  2. make the changes                    │
   │  3. bash tools/verify.sh                │
   │       rehash assets → inject GA →       │
   │       serve → Playwright sweep          │
   │  4. writes .deploy-receipt.json         │
   └──────────────┬──────────────────────────┘
                  │  device_commit_files
                  ▼
   ┌─ YOUR MAC (~/Documents/sabato-site) ────┐
   │  5. ./tools/ship.sh staging "message"   │
   │       checks receipt still matches      │
   └──────────────┬──────────────────────────┘
                  │  git push origin staging
                  ▼
      staging--delicate-valkyrie-20e427.netlify.app
                  │   (noindexed - see netlify.toml)
                  │  Claude sweeps this URL too
                  ▼
   ┌─ YOUR MAC ──────────────────────────────┐
   │  6. ./tools/ship.sh live                │
   │       fast-forward main to staging      │
   └──────────────┬──────────────────────────┘
                  ▼
              sabato.ai
```

Claude never holds a credential and never pushes. You are the gate on both hops.

---

## The receipt

`tools/verify.sh` ends by writing `.deploy-receipt.json` (gitignored) containing
a SHA-256 fingerprint of every file under `site/`.

`tools/ship.sh` recomputes that fingerprint before it will push. If a single byte
of `site/` changed after Claude verified it, the digest moves and the push is
**refused**.

This closes the gap the two-computer split creates: without it, "Claude checked
it" and "what you are about to push" are two different claims with nothing
connecting them. Override is `FORCE=1` and should feel uncomfortable.

Both machines compute the digest with `python3 tools/site_digest.py` - written in
Python precisely because macOS has `shasum` and Linux has `sha256sum` and they
disagree.

---

## Commands

**On your Mac, in Terminal** (not through Claude - the bridge has no network):

```bash
./tools/ship.sh status              # what is verified, what is pending
./tools/ship.sh staging "message"   # commit + push to staging → preview deploy
./tools/ship.sh live                # fast-forward main to staging → production
```

**In a Claude session** (Claude runs this itself):

```bash
bash tools/verify.sh                        # gate the local build, write receipt
```

### Claude cannot sweep a deployed URL from the cloud container

Tested 5 Aug 2026: Chromium inside a Cowork container cannot reach `sabato.ai`,
`main--delicate-valkyrie-20e427.netlify.app` or the staging URL. All three fail
with `ERR_TUNNEL_CONNECTION_FAILED` - egress is proxied to package registries
only. `verify.sh <url>` now probes first and says so, rather than reporting a
perfectly healthy site as broken.

So the **local sweep is the real gate**, and it is a good one: it runs the same
40+ page Playwright check against the exact bytes that get deployed, served
through `serve_like_netlify.py`. What it cannot catch is anything introduced
*by Netlify itself* - header rules, redirects, context build commands.

To check a deployed URL, in order of preference:

1. **Claude in Chrome** - drives Daniel's own browser, so it has real network
   access and can read response headers. The only option that can confirm
   Netlify-side behaviour such as `X-Robots-Tag`.
2. **WebFetch** - works, but returns page text only. No headers, one page at a
   time. Fine for "did it deploy and does it look right", useless for header
   rules.
3. **Daniel's eyes**, plus the Netlify deploy log at
   `app.netlify.com/projects/delicate-valkyrie-20e427/deploys`.

---

## Branch model

- `staging` is where work lands. Always.
- `main` is only ever **fast-forwarded** to `staging` - `ship.sh live` uses
  `--ff-only`, so production is byte-identical to whatever staging deployed and
  already passed a sweep. If it refuses, someone committed straight to `main`;
  rebase staging onto main, re-verify, retry.
- Never commit directly to `main`. It breaks the guarantee above.

## Staging must stay invisible

A branch deploy is a complete, public, crawlable copy of the site. Indexed, it
competes with `sabato.ai` for our own terms. `netlify.toml` therefore runs
`tools/mark_noindex.sh` on `branch-deploy` and `deploy-preview` contexts only,
appending a catch-all `X-Robots-Tag: noindex, nofollow`.

`robots.txt` is deliberately left alone - a `Disallow` stops crawlers fetching
the page, which means they never see the `noindex` and the URL can still surface.
Same reasoning already recorded for `/roi-calculator`.

---

## One-time setup still needed on Netlify

Netlify facts confirmed via the connector (5 Aug 2026):

- site `delicate-valkyrie-20e427`, id `68487802-e2a9-46b4-bb09-e26aa077d9ad`
- primary URL is the **apex** `https://sabato.ai`, not `www`
- plan `nf_team_dev`
- production deploy is `ready`, built from `main` @ `4d34f387`, 11 header rules

**Branch deploys must be switched on in the UI** - the MCP connector exposes no
setting for it, so this cannot be automated:

**Site configuration → Build & deploy → Branches and deploy contexts** →
production branch `main`, add `staging` under branch deploys.

Until that is done, `ship.sh staging` pushes successfully but no preview appears.

**Unverified: whether the Netlify site is genuinely git-connected.** The latest
production deploy reports `deploy_source: "api"`, not a git-triggered build, even
though it carries a real `commit_ref` and `committer`. If the repo link was ever
removed and deploys have been going out by API, then pushing to GitHub will
deploy *nothing* and the whole flow above is inert. The cheap test is the first
`ship.sh staging` push: if no deploy appears in Netlify within a minute or two,
the site is not git-connected and the repo link needs restoring under
**Site configuration → Build & deploy → Continuous deployment**.

## Stronger option for staging: password, not just noindex

`noindex` keeps staging out of search results. It does not stop anyone who has
the URL from reading an unreleased pricing page.

Netlify can password-protect **non-production deploys only**, leaving production
open. That is a per-site access control (`appliesTo: non-production-projects`),
and Claude can set it through the Netlify connector on request.

Trade-off before turning it on: a password wall breaks the automated staging
sweep, because `postdeploy_check.py` would hit the login form instead of the
site. Turning it on means either teaching that script to authenticate first, or
accepting that staging gets checked by eye rather than by Playwright. It may also
require a paid plan; the site is currently on `nf_team_dev`.

---

## Bootstrapping a fresh Claude session

Persistent memory is off on this account and the container is thrown away, so
paste this to start:

```
Read DEPLOY.md, SABATO-SITE-HANDBOOK.md and HANDOFF.md in
~/Documents/sabato-site, then <the task>. Verify with tools/verify.sh
before handing anything back.
```

If the folder is not connected to the session, Claude can `git clone
https://github.com/DanielRongo/sabato-site.git` instead - the repo is public, so
no credentials are involved. But then it can only hand files back, not write them
into your working copy.

---

## Claude must never run git through the Cowork bridge

`device_bash` on the Mac side **cannot delete files** - `rm` returns
"Operation not permitted". Git needs to create and then remove `.git/index.lock`
for almost every operation, so any `git status`, `git add` or `git checkout` run
through the bridge leaves a stranded lock behind:

```
warning: unable to unlink '.git/index.lock': Operation not permitted
```

The next real git command Daniel runs then dies with *"Another git process seems
to be running in this repository"* - and Claude cannot clear it, because deleting
is exactly what the bridge forbids. Recovery is manual:

```bash
rm -f ~/Documents/sabato-site/.git/index.lock
```

So: **read files through the bridge, never drive git through it.** For repo
state, use the cloud clone (`git clone https://github.com/DanielRongo/sabato-site.git`)
or ask Daniel to run the command. This happened once, on 5 Aug 2026, from a
`ship.sh status` run used as a test. Do not repeat it.

## device_commit_files strips the executable bit

Every file Claude writes to the Mac through the bridge lands as `100644`. A shell
script delivered that way arrives **non-executable**, and `./tools/ship.sh` then
fails with `permission denied`. It bit `verify.sh` on 5 Aug 2026, which was
committed as `100644` an hour after being created `100755`.

So: **after any `device_commit_files` that touches a script, chmod it back.**

```bash
chmod +x tools/ship.sh tools/verify.sh tools/mark_noindex.sh tools/site_digest.py
```

Claude can run that itself through the bridge - `chmod` is permitted, only
deleting is not. Do it in the same turn as the delivery, not later.

Fallback if the bit is ever missing and Daniel is mid-deploy: `bash
tools/ship.sh staging "msg"` works regardless of the mode.

## Known sharp edges

- **The repo is public.** No secrets, tokens or `.env` files, ever. Reverted ROI
  calculator commits are still readable in the git log.
- `tools/inject_ga.py` must run **last** in any build. It patches `templates/`
  too, otherwise the next `publish.py` run strips the tag off every page it
  regenerates.
- After editing anything under `site/fuc/`, `tools/rehash_edited_assets.py` is
  not optional - those files are served `immutable, max-age=1y`. `verify.sh`
  runs it first so this is hard to get wrong.
