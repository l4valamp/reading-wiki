"""Install the local Obsidian exporter; no npm dependencies or build tools required."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def install():
    import yaml
    config = yaml.safe_load((ROOT / 'mkdocs.yml').read_text(encoding='utf-8-sig'))
    vault = (ROOT / config.get('docs_dir', 'docs')).resolve()
    source = ROOT / 'plugins/obsidian-reading-wiki-exporter'
    target = vault / '.obsidian/plugins/reading-wiki-exporter'
    target.mkdir(parents=True, exist_ok=True)
    core = (source / 'exporter.js').read_text(encoding='utf-8')
    main = (source / 'main.js').read_text(encoding='utf-8')
    # Obsidian supplies its own require function; local relative modules must
    # be bundled into main.js rather than resolved from the app directory.
    bundled = '(function () { const module = { exports: {} };\n' + core + '\nreturn module.exports; })()'
    main = main.replace("require('./exporter')", bundled)
    (target / 'main.js').write_text(main, encoding='utf-8')
    shutil.copyfile(source / 'manifest.json', target / 'manifest.json')
    return target


if __name__ == '__main__':
    print(f'Installed {install()}')
