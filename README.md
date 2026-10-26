# Reading Wiki Starter

This is a separate MkDocs project. The databaseview plugin source is copied from SuckitUpDocs; the original project is unchanged.

## Windows PowerShell

Open a terminal in this folder, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m mkdocs serve
```

Open http://127.0.0.1:8000 in a browser. Stop the server with Ctrl+C.

To build the static site:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build
```

The output is in `site/`. A GitHub repository and GitHub Pages deployment can be configured separately.

## Limitations

The copied plugin currently renders Markdown tables, not interactive Obsidian Bases or card galleries. This starter has not been executed in the build environment, so validate the local build before deployment.
