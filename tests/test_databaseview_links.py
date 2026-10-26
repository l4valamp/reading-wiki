import contextlib
import io
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from mkdocs.commands.build import build
from mkdocs.config import load_config


ROOT = Path(__file__).resolve().parents[1]


class TableLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.in_cell = True
        if tag == "a" and self.in_cell:
            self.links.append(dict(attrs)["href"])

    def handle_endtag(self, tag):
        if tag == "td":
            self.in_cell = False


class DatabaseViewLinksTest(unittest.TestCase):
    def test_built_links_resolve_under_project_prefix(self):
        for directory_urls in (True, False):
            for site_url in ("", "https://l4valamp.github.io/reading-wiki/"):
                with self.subTest(directory_urls=directory_urls, site_url=site_url):
                    with tempfile.TemporaryDirectory() as tmp:
                        tmp = Path(tmp)
                        docs = tmp / "docs"
                        shutil.copytree(ROOT / "docs", docs)
                        # Exercise nested paths, URL punctuation, and property links.
                        nested = docs / "books" / "nested"
                        nested.mkdir()
                        (nested / "A book (draft) #1.md").write_text(
                            '---\ntags: [book]\nstatus: "[[intrasexual-competition]]"\n---\n# Book\n',
                            encoding="utf-8",
                        )
                        config = load_config(
                            config_file=str(ROOT / "mkdocs.yml"),
                            docs_dir=str(docs),
                            site_dir=str(tmp / "site"),
                            site_url=site_url,
                            use_directory_urls=directory_urls,
                            strict=True,
                        )
                        with contextlib.redirect_stdout(io.StringIO()):
                            build(config)
                        for section, count in (("books", 3), ("topics", 1)):
                            parser = TableLinks()
                            parser.feed((tmp / "site" / section / "index.html").read_text(encoding="utf-8"))
                            self.assertEqual(len(parser.links), count)
                            for href in parser.links:
                                if site_url:
                                    self.assertTrue(href.startswith("/reading-wiki/"), href)
                                resolved = urlsplit(urljoin(
                                    f"https://l4valamp.github.io/reading-wiki/{section}/", href
                                ))
                                self.assertTrue(resolved.path.startswith("/reading-wiki/"), href)
                                relative = unquote(resolved.path[len("/reading-wiki/"):])
                                target = tmp / "site" / relative
                                if resolved.path.endswith("/"):
                                    target /= "index.html"
                                self.assertTrue(target.is_file(), f"{href} -> {target}")


if __name__ == "__main__":
    unittest.main()
