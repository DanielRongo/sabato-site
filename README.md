# sabato.ai - static site + blog

Static clone of the Sabato Framer site, self-hosted on Netlify (git-connected: push to main = deploy).

- `site/` - the deployed site (publish dir). Never hand-edit `site/blog/*` - generated.
- `posts/en/*.md`, `posts/it/*.md` - blog posts (frontmatter: title, slug, description, category, date, cover_style).
- `templates/` - blog page templates matching the site design.
- `publish.py` - renders posts → site/blog + indexes + sitemap. Run: `python3 publish.py` (needs `pip install markdown`).
- `dummy-posts.txt` - design dummies to remove when the first real post ships.

Publishing flow: Trello board "Sabato Blog Pipeline" → Approved column → daily publisher task renders, commits, pushes.

## Deploying

Read `DEPLOY.md`. Claude verifies in its cloud container (`bash tools/verify.sh`,
needs Playwright); Daniel pushes from his Mac (`./tools/ship.sh staging "msg"`,
then `./tools/ship.sh live`). `staging` branch → noindexed Netlify preview;
`main` → production, fast-forwarded from staging only.

Do NOT run `tools/rehash_edited_assets.py` with no argument - it defaults to the
repo's first commit and will rename hundreds of assets. Pass a ref
(`origin/main`), or just let `tools/verify.sh` handle it.

## Editing files under site/fuc/

Those files are served with `Cache-Control: immutable, max-age=1y` (Framer names
them by content hash). If you edit one in place, returning visitors keep the old
copy for up to a year. After ANY edit under `site/fuc/`, run:

    python3 tools/rehash_edited_assets.py

It renames each edited file with a fresh content hash and rewrites every
reference, then reports dangling references. Deploy only after it reports clean.
