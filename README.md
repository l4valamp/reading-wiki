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
