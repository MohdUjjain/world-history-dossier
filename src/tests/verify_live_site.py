#!/usr/bin/env python3
"""Check the deployed GitHub Pages site (weekly/manual, not during a push race)."""
from __future__ import annotations
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = "https://mohdujjain.github.io/world-history-dossier/"
paths = {
    "": b"World History Dossier",
    "manifest.webmanifest": b'"start_url": "./"',
    "service-worker.js": b"whd-edition-",
    "sitemap.xml": BASE.encode(),
    "robots.txt": b"Sitemap:",
    "icons/icon-192.png": b"\x89PNG",
    "icons/icon-512.png": b"\x89PNG",
    "og-image.jpg": b"\xff\xd8",
}
for path, needle in paths.items():
    request = Request(BASE + path, headers={"User-Agent": "WHD-PublicationVerifier/1.0"})
    with urlopen(request, timeout=25) as response:
        assert response.status == 200, (path, response.status)
        content = response.read()
    assert needle in content, f"Unexpected live content at {path}"
    print("PASS:", BASE + path, len(content), "bytes")
try:
    urlopen(Request(BASE + "definitely-not-a-page", headers={"User-Agent":"WHD-PublicationVerifier/1.0"}), timeout=25)
    raise AssertionError("Expected a 404 for unknown routes")
except HTTPError as exc:
    assert exc.code == 404, exc.code
    assert b"Page not found" in exc.read(), "Custom 404 wasn't served"
print("PASS: live site, cached assets and custom 404")
