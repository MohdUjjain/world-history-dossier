#!/usr/bin/env python3
"""Real Chromium PWA offline and update regression (in addition to SW mock tests).

Tests atomic precache, offline reader re-opening, no PDF precache and update
notification after a newly installed worker claims an existing controlled tab.
"""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import os
import re

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
WORKER = (ROOT / "service-worker.js").read_text(encoding="utf-8")
MATCH = re.search(r"CACHE_NAME\s*=\s*CACHE_PREFIX\s*\+\s*'([a-f0-9]{12})'", WORKER)
assert MATCH, "Service worker revision does not match release hash convention"
ORIGINAL = MATCH.group(1)
UPDATED = "d0123456789a" if ORIGINAL != "d0123456789a" else "e0123456789a"


class UpdatingHandler(SimpleHTTPRequestHandler):
    revision = ORIGINAL

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/service-worker.js":
            body = WORKER.replace("'" + ORIGINAL + "'", "'" + self.revision + "'")
            data = body.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()


def main():
    UpdatingHandler.revision = ORIGINAL
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(UpdatingHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    failures = []
    try:
        with sync_playwright() as playwright:
            options = {"headless":True,"args":["--no-sandbox"]}
            if os.environ.get("CHROMIUM_BIN"):
                options["executable_path"] = os.environ["CHROMIUM_BIN"]
            browser = playwright.chromium.launch(**options)
            context = browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()
            page.on("pageerror", lambda error: failures.append(str(error)))
            url = f"http://127.0.0.1:{server.server_port}/"
            page.goto(url, wait_until="load")
            page.wait_for_function("""async () => {
              if (!navigator.serviceWorker.controller) return false;
              const names=(await caches.keys()).filter(n=>n.startsWith('whd-edition-'));
              return names.length === 1;
            }""", timeout=20000)
            # The first controller event can happen before screen hydration
            # has completed, so wait for both independently.
            page.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")
            initial = page.evaluate("""async () => ({
              controlled:!!navigator.serviceWorker.controller,
              caches:(await caches.keys()).filter(n=>n.startsWith('whd-edition-')),
              pdfPrecached:!!(await (await caches.open(
                (await caches.keys()).find(x=>x.startsWith('whd-edition-'))
              )).match('./20th-Century%20International%20History.pdf'))
            })""")
            assert initial["controlled"] and len(initial["caches"]) == 1, initial
            assert not initial["pdfPrecached"], initial
            context.set_offline(True)
            page.goto(url, wait_until="load")
            page.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")
            assert page.locator("#screenView .chapter-flow").count() == 33
            # Registration/status refresh is async after the hydrated reader
            # appears; wait for readiness instead of reading the initial text.
            page.wait_for_function("""() => document.querySelector('#offlineStatus')
              ?.textContent.includes('All 33 chapters saved offline')""",
              timeout=15000)
            context.set_offline(False)

            # A newly installed worker must show a non-forced reader update
            # notification and replace only older whd-edition-* cache versions.
            UpdatingHandler.revision = UPDATED
            page.evaluate("""async () => {
              const reg=await navigator.serviceWorker.ready;
              await reg.update();
            }""")
            page.locator("#editionUpdateNotice").wait_for(state="visible", timeout=20000)
            # A previous worker can still complete fetches while its clients
            # hand over. First require the new complete edition to be present;
            # evaluate stale-cache cleanup again after reloading into it.
            page.wait_for_function("""async expected =>
              (await caches.keys()).includes(expected)""",
              arg="whd-edition-" + UPDATED, timeout=20000)
            after = page.evaluate("""async () => ({
              caches:(await caches.keys()).filter(x=>x.startsWith('whd-edition-')),
              chapters:document.querySelectorAll('#screenView .chapter-flow').length,
              notice:!document.getElementById('editionUpdateNotice').hidden
            })""")
            assert after["notice"] and after["chapters"] == 33, after
            assert "whd-edition-" + UPDATED in after["caches"], after
            page.locator("#editionDismissBtn").click()
            assert page.locator("#editionUpdateNotice").is_hidden()
            page.goto(url, wait_until="load")
            assert page.locator("#screenView .chapter-flow").count() == 33
            page.wait_for_function("""async expected => {
              const names=(await caches.keys())
                .filter(name=>name.startsWith('whd-edition-'));
              return names.length===1 && names[0]===expected;
            }""", arg="whd-edition-" + UPDATED, timeout=15000)
            after["postReloadCaches"] = page.evaluate("""async () =>
              (await caches.keys()).filter(x=>x.startsWith('whd-edition-'))""")
            assert not failures, failures
            browser.close()
            print(json.dumps({"initial":initial,"offlineChapters":33,
                              "updateRevision":UPDATED,"after":after,
                              "pageErrors":failures},indent=2))
    finally:
        UpdatingHandler.revision = ORIGINAL
        server.shutdown()


if __name__ == "__main__":
    main()
