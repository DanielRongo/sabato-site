# sabato.ai — static site + blog

Static clone of the Sabato Framer site, self-hosted on Netlify (git-connected: push to main = deploy).

- `site/` — the deployed site (publish dir). Never hand-edit `site/blog/*` — generated.
- `posts/en/*.md`, `posts/it/*.md` — blog posts (frontmatter: title, slug, description, category, date, cover_style).
- `templates/` — blog page templates matching the site design.
- `publish.py` — renders posts → site/blog + indexes + sitemap. Run: `python3 publish.py` (needs `pip install markdown`).
- `dummy-posts.txt` — design dummies to remove when the first real post ships.

Publishing flow: Trello board "Sabato Blog Pipeline" → Approved column → daily publisher task renders, commits, pushes.
