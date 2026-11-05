#!/usr/bin/env python3
"""Release coverage for strict custom chapter ranges and live revision options."""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import os

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def main():
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    errors = []
    report = []
    try:
        with sync_playwright() as playwright:
            options = {"headless": True, "args":["--no-sandbox"]}
            if os.environ.get("CHROMIUM_BIN"):
                options["executable_path"] = os.environ["CHROMIUM_BIN"]
            browser = playwright.chromium.launch(**options)
            page = browser.new_page(viewport={"width":1280,"height":850},
                                    reduced_motion="reduce")
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.goto(f"http://127.0.0.1:{server.server_port}/",wait_until="load")
            page.locator("#navToc .nav-chapter-link").first.wait_for()
            all_names = page.evaluate("""() => Object.fromEntries(
              [...document.querySelectorAll('#chapterData .chapter-source')]
              .map(x=>[Number(x.getAttribute('data-chapter')),
                       x.getAttribute('data-title')]))""")
            page.evaluate("window.print=()=>{}")
            page.locator("#navTab").click()
            page.locator("#navExportPanel summary").click()

            invalid = ("1,,2","1x,2","999,1","0-99","1-2,,5",
                       "-1","1-","1-2000","1 2","1-2,abc")
            for val in invalid:
                page.locator("#rangeInput").fill(val)
                assert page.locator("#printBtn").is_disabled(), val
                assert page.locator("#rangeInput").get_attribute("aria-invalid") == "true", val
                assert page.locator("#rangeHint").get_attribute("class").find("error") >= 0

            # Explicit user order, reverse ranges, and intentional duplication.
            cases = [
                ("6-5,1,6", [6,5,1,6]),
                ("5-6,1,3,20-24", [5,6,1,3,20,21,22,23,24]),
                ("0-2", [0,1,2]),
            ]
            for selector, expected in cases:
                if page.locator("#navPanel").get_attribute("aria-hidden") == "true":
                    page.locator("#navTab").click()
                page.locator("#rangeInput").fill(selector)
                assert page.locator("#printBtn").is_enabled(),selector
                page.locator("#printBtn").click()
                rendered = page.locator("#printView .hero-title").all_text_contents()
                wanted = [all_names[str(n)] if str(n) in all_names
                          else all_names[n] for n in expected]
                assert rendered == wanted, (selector,rendered,wanted)
                assert page.locator("#navPanel").get_attribute("aria-hidden") == "true"
                assert not page.evaluate("document.body.classList.contains('drawer-open')")
                report.append({"range":selector,"chapterSequence":expected,
                               "heroPages":len(rendered)})

            # The summaries toggle changes BOTH screen and print composition,
            # with a fresh print signature even when ordered selection stays put.
            page.locator("#navTab").click()
            page.locator("#rangeInput").fill("0,1")
            page.locator("#includeRevisionChk").uncheck()
            assert page.locator(".nav-shortcut",has_text="Revision").count() == 0
            page.locator("#printBtn").click()
            assert page.locator("#printView .page.is-revision").count() == 0
            without = page.locator("#printView .page-slot").count()

            page.locator("#navTab").click()
            page.locator("#includeRevisionChk").check()
            assert page.locator(".nav-shortcut",has_text="Revision").count() == 33
            page.locator("#printBtn").click()
            with_revisions = page.locator("#printView .page-slot").count()
            assert page.locator("#printView .page.is-revision").count() > 0
            assert with_revisions > without, (without,with_revisions)

            # Beforeprint (Ctrl+P/menu) must not destroy/recreate an identical
            # tree, but a changed ordered range must do so.
            stable = page.evaluate("""() => {
              const root=document.getElementById('printView');
              root.dataset.testIdentity='retained';
              return root.firstElementChild;
            }""")
            page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
            assert page.evaluate("""() =>
              document.getElementById('printView').dataset.testIdentity === 'retained'
              && document.querySelector('#printView .page-slot') !== null""")
            assert not errors, errors
            report.append({"summariesExcludedPages":without,
                           "summariesIncludedPages":with_revisions,
                           "printReuse":True,"pageErrors":errors})
            browser.close()
            print(json.dumps(report,indent=2))
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
