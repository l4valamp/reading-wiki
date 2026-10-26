# Automatic Obsidian exports

The companion plugin runs **inside Obsidian** and receives the full Bases query result through Obsidian's supported `BasesView` API. Obsidian evaluates the existing global/view filters, formulas, sorting, limits, groups, and summaries. The exporter writes static Markdown tables and a generated manifest; the MkDocs plugin never evaluates Bases expressions.

## Your normal workflow

1. Keep this project's `docs` vault open in Obsidian and edit or add notes normally.
2. Publish with the usual command:

```powershell
.\.venv\Scripts\python.exe -m mkdocs gh-deploy --strict
```

Saving, creating, deleting, or renaming a note or `.base` file automatically refreshes snapshots after a short delay. New embedded views and pages are discovered automatically. **Do not copy tables, edit the manifest, or register new notes.** The publish command requests a fresh export and waits for completion, even if the background export has not finished yet. There is no automatic deployment on every keystroke; the publish command controls when changes become public.

Both local preview and builds use the same mechanism:

```powershell
.\.venv\Scripts\python.exe -m mkdocs serve
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

Obsidian must remain running with this vault open. If it is closed or the companion plugin is disabled, the build stops instead of deploying stale results. No CLI registration is required for normal operation.

## One-time setup on another computer or checkout

This companion is already installed and enabled in the current project's vault. For another installation:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/install_obsidian_exporter.py
```

Open the project's `docs` folder as an Obsidian vault. Enable Bases, then enable **Reading Wiki Exporter** under Settings ? Community plugins. Requires desktop Obsidian 1.10 or newer. The installer bundles the plugin without npm dependencies; rerun it after changing the companion source, then toggle the plugin off/on to reload it.

```yaml
plugins:
  - databaseview:
      auto_export: true
      snapshot_manifest: database-snapshots/manifest.yml
      export_timeout: 90
```

The manifest and snapshots are generated under `database-snapshots/`. They are outside the vault so they cannot become rows in their own databases. `.obsidian` preferences, request/response files, and generated exports are ignored by Git. Plugin source is kept in `plugins/obsidian-reading-wiki-exporter/`.

## How it works

For each real `![[Base.base#View]]` embed, the companion resolves the Base through Obsidian, copies its configuration in memory, and asks Obsidian to render that exact view in the source note's context. The temporary renderer receives the **complete result set**, including rows outside the visible viewport. Original notes and `.base` files are not rewritten. `this` refers to the embedding note, so page-dependent views get separate snapshots.

The first view is used for an embed without `#View`, matching Obsidian's default. Table views are supported; unsupported view types stop the export with an error rather than publish an approximation. File cells are emitted as encoded Markdown links. Other values are serialized from Obsidian's evaluated Values; existing wikilinks become website links during the MkDocs build. References to nonexistent notes remain readable text without a fabricated destination.

Each successful export writes an immutable generation, then atomically switches the manifest. Builds verify the source fingerprint, manifest hash, and snapshot hashes, and check again for note changes before finishing. Files changing during export stop that build; publish again once editing is finished. Background exports exclude hidden folders and templates. Build-triggered exports use the exact set of pages MkDocs will publish.

Snapshots are static website tables, not interactive replicas of Obsidian's table controls. The manual `save_database_snapshot.py` helper remains available for deliberate offline snapshots with `auto_export: false`; it is not used in the automatic workflow.

## Development checks

```powershell
node --test plugins/obsidian-reading-wiki-exporter/exporter.test.js
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

Obsidian API reference: https://github.com/obsidianmd/obsidian-api
