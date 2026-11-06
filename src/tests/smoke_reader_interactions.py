#!/usr/bin/env python3
"""Phase B browser regression: one drawer owner, search, stable reading place, touch.

Run with Playwright Chromium: python src/tests/smoke_reader_interactions.py
"""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from pathlib import Path
import json
import os

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


class QuietServer(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def main() -> None:
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietServer, directory=str(ROOT))
    )
    Thread(target=server.serve_forever, daemon=True).start()
    errors = []
    try:
        with sync_playwright() as playwright:
            options = {"headless": True, "args": ["--no-sandbox"]}
            if os.environ.get("CHROMIUM_BIN"):
                options["executable_path"] = os.environ["CHROMIUM_BIN"]
            browser = playwright.chromium.launch(**options)
            context = browser.new_context(
                viewport={"width": 1360, "height": 850}, reduced_motion="reduce"
            )
            page = context.new_page()
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="load")
            page.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")

            # Main landmark and keyboard-only skip control.
            assert page.locator("main#screenView").count() == 1
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.classList.contains('skip-to-content')")
            page.keyboard.press("Enter")
            assert page.evaluate("document.activeElement.id") == "screenView"

            # Single modal implementation: predictable opener and focus wrapping.
            page.locator("#navTab").click()
            assert page.locator("#navPanel").get_attribute("aria-hidden") == "false"
            assert page.evaluate("document.activeElement.id") == "navClose"
            page.keyboard.press("Shift+Tab")
            assert page.evaluate(
                "document.getElementById('navPanel').contains(document.activeElement)"
            ), "Shift+Tab escaped open modal"
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.id") == "navClose"

            # Search has semantic counts, safe highlights, a true empty state,
            # and an Escape-to-clear-then-Escape-to-close keyboard sequence.
            page.locator('.nav-chapter[data-chapter="1"] .nav-chapter-toggle').click()
            assert page.locator('.nav-chapter[data-chapter="1"] .nav-chapter-toggle').get_attribute("aria-expanded") == "true"
            page.locator("#tocSearch").fill("globalization")
            assert page.locator("#navToc .nav-search-match").count() > 0
            assert "matching chapter" in page.locator("#tocSearchStatus").inner_text()
            assert "section" in page.locator("#tocSearchStatus").inner_text()
            assert page.locator("#tocExpandAll").is_disabled()
            assert page.locator("#tocCollapseAll").is_disabled()
            assert page.locator("#tocClearSearch").is_visible()
            page.locator("#tocSearch").fill("zzzzzyyy-nothing")
            assert page.locator("#tocNoResults").is_visible()
            assert page.locator('.nav-chapter:not([hidden])').count() == 0
            page.locator("#tocSearch").focus()
            page.keyboard.press("Escape")
            assert page.locator("#tocSearch").input_value() == ""
            assert page.locator("#navPanel").get_attribute("aria-hidden") == "false"
            assert page.locator("#tocNoResults").is_hidden()
            assert page.locator("#tocExpandAll").is_enabled()
            assert page.locator('.nav-chapter[data-chapter="1"] .nav-chapter-toggle').get_attribute("aria-expanded") == "true"
            page.keyboard.press("Escape")
            assert page.locator("#navPanel").get_attribute("aria-hidden") == "true"
            assert page.evaluate("document.activeElement.id") == "navTab"

            # Export closes through the same modal handler; body never remains
            # scroll-locked and keyboard focus returns to the Contents control.
            page.locator("#navTab").click()
            page.locator('#navToolsTab').click()
            page.locator("#navExportPanel summary").click()
            page.locator('#navToolsTab').click()
            if not page.locator('#navExportPanel').evaluate('(e)=>e.open'):
                page.locator('#navExportPanel summary').click()
            page.locator("#rangeInput").fill("4,3")
            page.evaluate("window.print=()=>{}")
            page.locator("#printBtn").click()
            assert page.locator("#navPanel").get_attribute("aria-hidden") == "true"
            assert not page.evaluate("document.body.classList.contains('drawer-open')")
            assert page.evaluate("document.activeElement.id") == "navTab"
            assert page.locator("#printView .page.type-hero").count() == 2

            # Toggle revision visibility while reading near the back of the
            # book. Absolute scrollY MUST change as prior revision pages are
            # removed; the same section must stay at the same viewport position.
            page.locator("#navTab").click()
            entry = page.locator('.nav-chapter[data-chapter="29"]')
            entry.locator(".nav-chapter-toggle").click()
            heading_link = entry.locator(".nav-section-link").nth(2)
            target = heading_link.get_attribute("data-target")
            heading_link.click()
            page.wait_for_timeout(130)
            before = page.evaluate("""id => ({
                top:document.getElementById(id).getBoundingClientRect().top,
                scroll:window.scrollY
            })""", target)
            assert before["scroll"] > 10000, before
            page.locator("#navTab").click()
            assert page.locator("#navExportPanel").evaluate("(e)=>e.open")
            page.locator('#navToolsTab').click()
            page.locator("#includeRevisionChk").uncheck()
            page.wait_for_timeout(130)
            without = page.evaluate("""id => ({
                top:document.getElementById(id).getBoundingClientRect().top,
                scroll:window.scrollY,
                drawer:document.body.classList.contains('drawer-open'),
                focus:document.activeElement.id
            })""", target)
            assert abs(without["top"] - before["top"]) < 90, (before, without)
            assert abs(without["scroll"] - before["scroll"]) > 1000, (
                "Expected document height to change after removing preceding revisions",
                before, without,
            )
            assert without["drawer"] and without["focus"] == "includeRevisionChk"
            assert page.locator(".nav-shortcut", has_text="Revision").count() == 0
            page.locator('#navToolsTab').click()
            page.locator("#includeRevisionChk").check()
            page.wait_for_timeout(130)
            restored = page.evaluate("""id => ({
                top:document.getElementById(id).getBoundingClientRect().top,
                scroll:window.scrollY
            })""", target)
            assert abs(restored["top"] - before["top"]) < 90, (before, restored)
            assert page.locator(".nav-shortcut", has_text="Revision").count() == 33
            page.keyboard.press("Escape")
            assert not page.evaluate("document.body.classList.contains('drawer-open')")

            # Touch-mode test: tappable controls, full-height drawer, readable
            # chapter context and no horizontal overflow at narrow widths.
            mobile_context = browser.new_context(
                viewport={"width": 390, "height": 844},
                is_mobile=True, has_touch=True, device_scale_factor=1,
                reduced_motion="reduce",
            )
            mobile = mobile_context.new_page()
            mobile.on("pageerror", lambda exc: errors.append(str(exc)))
            mobile.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="load")
            mobile.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")
            mobile.locator("#navTab").tap()
            assert mobile.locator("#navPanel").bounding_box()["width"] >= 385
            for selector in ("#navClose", ".nav-chapter-toggle", "#tocExpandAll"):
                control = mobile.locator(selector).first.bounding_box()
                assert control and control["height"] >= 43 and control["width"] >= 43, (
                    selector, control
                )
            mobile.locator('.nav-chapter[data-chapter="24"] .nav-chapter-link').tap()
            mobile.wait_for_timeout(120)
            assert mobile.locator("#currentChapterLabel").is_visible()
            assert "Ch.24" in mobile.locator("#currentChapterLabel").inner_text()
            assert mobile.evaluate("document.documentElement.scrollWidth <= innerWidth")
            mobile.set_viewport_size({"width": 320, "height": 720})
            assert mobile.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert mobile.locator("#currentChapterLabel").is_visible()
            mobile.locator("#navTab").tap()
            assert mobile.locator("#navPanel").bounding_box()["width"] >= 315
            mobile.keyboard.press("Escape")
            assert mobile.evaluate("document.activeElement.id") == "navTab"
            assert not errors, errors
            browser.close()
            print(json.dumps({
                "chapters": 33,
                "searchHighlight": True,
                "searchZeroState": True,
                "keyboardEscapeSequence": True,
                "modalFocus": True,
                "readingViewportPreserved": True,
                "before": before,
                "afterHidingRevision": without,
                "afterRestoringRevision": restored,
                "mobileWidths": [390, 320],
                "javascriptErrors": errors
            }, indent=2))
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
