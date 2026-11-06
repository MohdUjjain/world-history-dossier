#!/usr/bin/env python3
"""Validate the self-contained GitHub Pages publication and PWA assets."""
from __future__ import annotations

import json
import re
import struct
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
URL = "https://mohdujjain.github.io/world-history-dossier/"
ASSETS = [
    "index.html", "manifest.webmanifest",
    "icons/icon-192.png", "icons/icon-512.png",
    "og-image.jpg", "404.html", "sitemap.xml", "robots.txt",
    "service-worker.js",
]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.chapters = []
        self.links = []
        self.metas = []
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == "title":
            self.in_title = True
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "div" and "chapter-source" in a.get("class", "").split():
            self.chapters.append(a.get("data-chapter"))
        if tag == "meta":
            self.metas.append(a)
        if tag == "link":
            self.links.append(a)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, content):
        if self.in_title:
            self.title += content


def metadata(page, kind, name):
    vals = [m.get("content") for m in page.metas if m.get(kind) == name]
    assert len(vals) == 1, (kind, name, vals)
    return vals[0]


def verify():
    for asset in ASSETS + [".nojekyll", "src/offline-reader.js", "src/service-worker.template.js"]:
        assert (ROOT / asset).is_file(), f"Missing published or source file: {asset}"
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(html)
    assert page.title == "World History Dossier — 20th-Century International History"
    assert len(page.chapters) == 33, page.chapters
    assert [int(n) for n in page.chapters] == list(range(33)), page.chapters
    assert metadata(page, "name", "description")
    assert metadata(page, "name", "twitter:card") == "summary_large_image"
    for key, value in {
        "og:title": page.title,
        "og:url": URL,
        "og:image": URL + "og-image.jpg",
        "og:image:width": "1200",
        "og:image:height": "630",
    }.items():
        assert metadata(page, "property", key) == value, key
    canonical = [x.get("href") for x in page.links if x.get("rel") == "canonical"]
    assert canonical == [URL]
    assert [x.get("href") for x in page.links if x.get("rel") == "manifest"] == ["./manifest.webmanifest"]
    assert len(page.ids) == len(set(page.ids)), "HTML contains duplicate IDs"
    assert 'id="editionUpdateNotice"' in html
    assert 'id="offlineStatus"' in html
    assert 'id="offlineKeep"' in html
    assert "controllerchange" in html and "PREPARE_FONTS" in html
    assert "serviceWorker.register" in html

    manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert manifest["id"] == "/world-history-dossier/"
    assert manifest["scope"] == manifest["start_url"] == "./"
    assert manifest["display"] == "standalone"
    assert manifest["name"] == "World History Dossier"
    sizes = set()
    for item in manifest["icons"]:
        filename = ROOT / item["src"]
        assert filename.is_file()
        data = filename.read_bytes()
        assert data[:8] == bytes.fromhex("89504e470d0a1a0a"), filename
        width, height = struct.unpack(">II", data[16:24])
        assert (width, height) == tuple(map(int, item["sizes"].split("x"))), filename
        sizes.add(item["sizes"])
    assert {"192x192", "512x512"} <= sizes
    assert (ROOT / "og-image.jpg").read_bytes().startswith(b"\xff\xd8")
    assert (ROOT / "20th-Century International History.pdf").read_bytes()[:4] == b"%PDF"

    content404 = (ROOT / "404.html").read_text(encoding="utf-8").lower()
    assert 'name="robots"' in content404 and "noindex" in content404
    assert "/world-history-dossier/" in content404
    xml = ET.parse(ROOT / "sitemap.xml")
    locs = [node.text for node in xml.getroot().iter() if node.tag.endswith("loc")]
    assert locs == [URL], locs
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "Sitemap: " + URL + "sitemap.xml" in robots

    worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
    assert "__REVISION__" not in worker and "whd-edition-" in worker
    for path in ["./index.html", "./manifest.webmanifest", "./404.html",
                 "./sitemap.xml", "./robots.txt", "./og-image.jpg",
                 "./icons/icon-192.png", "./icons/icon-512.png"]:
        assert path in worker, f"Not in offline cache: {path}"
    assert "fonts.googleapis.com" in worker and "fonts.gstatic.com" in worker
    assert ".pdf" in worker and "name.startsWith(CACHE_PREFIX)" in worker
    assert "cache.addAll(CORE_ASSETS)" in worker and "self.skipWaiting()" in worker
    assert "OPTIONAL_ASSETS" in worker and "Promise.allSettled" in worker
    assert (ROOT / "src/shell.html").read_text(encoding="utf-8").count("/*__OFFLINE_READER__*/") == 1
    assert re.search(r"CACHE_NAME\s*=\s*CACHE_PREFIX\s*\+\s*'[0-9a-f]{12}'", worker), "Worker revision not content hashed"

    print("PASS: 33 chapters, source and web assets, PDF, meta tags, PWA icons, 404, sitemap, cache and update UX")


if __name__ == "__main__":
    verify()
