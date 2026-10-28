# Reading Wiki

An MkDocs site built from Obsidian notes. An Obsidian companion plugin automatically exports Bases query results; MkDocs publishes those snapshots without reimplementing Obsidian's filtering or formulas.

## Daily workflow

Keep this project's `docs` vault open in Obsidian. Add or edit notes normally. Database exports and their manifest update automatically, including new embedded views.

```powershell
.\.venv\Scripts\python.exe -m mkdocs serve
.\.venv\Scripts\python.exe -m mkdocs gh-deploy --strict
```

Builds and deployment wait for a fresh Obsidian export. No copying tables or editing mappings is required. Publishing remains an explicit command.

## Setup on another computer

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/install_obsidian_exporter.py
```

Open `docs` as an Obsidian vault and enable Bases and **Reading Wiki Exporter** in Community plugins. The exporter is already installed and enabled in this project's current vault. See [automatic export details](database-snapshots/README.md) for configuration and troubleshooting.

## Validation

```powershell
node --test plugins/obsidian-reading-wiki-exporter/exporter.test.js
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

Output is written to `site/`; GitHub Pages serves https://l4valamp.github.io/reading-wiki/.

## Library styling

The published site uses `docs/stylesheets/library.css`, loaded after the stock MkDocs theme. Edit its `--rw-*` variables to adjust colors, font stacks, spacing, reading width, borders, and transitions. The `[data-bs-theme="dark"]` block supplies the dark palette; the theme's existing color-mode configuration remains unchanged. Obsidian's editor and vault settings are unaffected.

Fraunces (regular and medium) and IBM Plex Mono (regular) are bundled as Latin WOFF2 subsets in `docs/assets/fonts/`, with their SIL Open Font Licenses. These assets come from Fontsource packages Fraunces 5.2.8 and IBM Plex Mono 5.2.7; fonts load locally with system fallbacks and `font-display: swap`. Body text uses the system sans-serif stack.

`docs/javascripts/library.js` only wraps published tables in labeled, keyboard-focusable scroll regions. It leaves the table structure, row order, links, search, and database export pipeline intact. With JavaScript disabled, native tables remain readable. Print styles remove navigation and the margin grid; reduced-motion preferences disable the theme's transitions.

To preview, keep this vault open in Obsidian and run `.\.venv\Scripts\python.exe -m mkdocs serve`, then visit the local URL it prints. Changes are not deployed until the separate `gh-deploy` command runs.

The website renders the Books collection as cover cards; Obsidian's native view remains a table. Add a **Text** property named `cover image` to a book note and paste a direct HTTP/HTTPS image URL, for example:

```yaml
cover image: "https://example.com/my-book-cover.jpg"
```

The book template includes this empty field for new notes. Existing notes are not modified automatically. Covers are cropped centrally to a 2:3 portrait frame; titles and authors remain visible beneath them. Missing, invalid, or failed URLs show a muted placeholder. Images load directly from their external hosts and are not downloaded or cached by the build.

The `databaseview.book_card_views` list in `mkdocs.yml` opts in exact embed identifiers (`Books.base` and `Books.base#View`). Related-books views such as `Books.base#OnTopicPage` remain tables. Cards preserve the exported year groups, membership, and row order; cover metadata is read from the linked note during publishing. Rebuild the site after updating a cover URL.
