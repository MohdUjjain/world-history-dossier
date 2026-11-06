#!/usr/bin/env python3
"""Playwright regression tests for World History Dossier screen navigation.

Runs against a local HTTP server (needed for localStorage and service workers).
    python src/tests/smoke_reader_ui.py
Requires playwright + installed Chromium. CHROMIUM_BIN=/usr/bin/chromium is optional.
"""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}/'
    errors = []
    try:
        with sync_playwright() as playwright:
            kwargs = {'headless': True, 'args': ['--no-sandbox']}
            system = os.environ.get('CHROMIUM_BIN')
            if system:
                kwargs['executable_path'] = system
            browser = playwright.chromium.launch(**kwargs)
            context = browser.new_context(viewport={'width': 1340, 'height': 850},
                                          reduced_motion='reduce')
            page = context.new_page()
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(url, wait_until='load')
            page.locator('#navToc .nav-chapter-link').first.wait_for(state='attached')

            assert page.locator('#chapterData .chapter-source').count() == 33
            assert page.locator('#navToc .nav-chapter-link').count() == 33
            assert page.locator('#navToc .nav-section-link').count() > 150
            assert page.locator('#chapterProgressRing').is_hidden()
            assert page.locator('#navExportPanel').evaluate('(node)=>!node.open')
            assert page.locator('#navPanel').get_attribute('aria-hidden') == 'true'

            # Narrative paragraphs in HTML have one paragraph break, not
            # stacked <p> margin + block padding + block margin (39px).
            # Keep section headings and other pedagogical blocks distinct.
            gaps = page.evaluate("""() => {
                const next = [...document.querySelectorAll(
                  '#screenView .main-flow > .block[data-kind="p"] + .block[data-kind="p"]'
                )].filter(el => el.querySelector(':scope > p') &&
                    el.previousElementSibling.querySelector(':scope > p'));
                return next.slice(0, 20).map(el =>
                    el.querySelector(':scope > p').getBoundingClientRect().top -
                    el.previousElementSibling.querySelector(':scope > p').getBoundingClientRect().bottom
                );
            }""")
            assert gaps and all(15 <= gap <= 19 for gap in gaps), gaps
            prose_styles = page.locator(
                '#screenView .main-flow > .block[data-kind="p"]').first.evaluate(
                """el => ({
                    padding:getComputedStyle(el).paddingBottom,
                    margin:getComputedStyle(el).marginBottom
                })""")
            assert prose_styles == {'padding': '0px', 'margin': '0px'}, prose_styles
            assert page.locator('#screenView .main-flow h3').first.evaluate(
                "el => getComputedStyle(el).marginTop") == '30px'

            # Header search uses the full authored text, not just Index headings.
            assert page.locator('#readerSearchBox').get_attribute('role') == 'search'
            page.locator('#readerSearchInput').fill('Pan-Turanianism')
            page.locator('#readerSearchHits .reader-search-hit').first.wait_for(state='visible')
            assert page.locator('#readerSearchHits mark').count() >= 1
            assert 'Ch.00' in page.locator('#readerSearchHits .reader-search-context').first.inner_text()
            assert 'matching passages' in page.locator('#readerSearchStatus').inner_text()
            page.locator('#readerSearchHits .reader-search-hit').first.click()
            assert page.locator('#readerSearchResults').is_hidden()
            assert page.locator('#screenView .reader-search-target').count() == 1
            assert page.evaluate("location.hash.startsWith('#whd-hit-')")

            # Search respects the Tools boundary; hidden summaries cannot be
            # retrieved and selecting hits must never silently re-enable them.
            page.locator('#navTab').click()
            page.locator('#navToolsTab').click()
            page.locator('#includeRevisionChk').uncheck()
            page.keyboard.press('Escape')
            assert page.locator('#screenView .revision-flow').count() == 0
            page.locator('#readerSearchInput').fill('Summary of Twentieth-Century Imperial Evolutions')
            page.wait_for_function("document.querySelector('#readerSearchStatus').textContent.includes('No matches')")
            assert page.locator('#readerSearchHits .reader-search-hit').count() == 0
            assert not page.locator('#includeRevisionChk').is_checked()
            assert page.locator('#screenView .revision-flow').count() == 0
            # Ordinary authored paragraphs still return search results.
            page.locator('#readerSearchInput').fill('Pan-Turanianism')
            page.locator('#readerSearchHits .reader-search-hit').first.wait_for(state='visible')
            page.locator('#readerSearchHits .reader-search-hit').first.click()
            assert not page.locator('#includeRevisionChk').is_checked()
            assert page.locator('#screenView .revision-flow').count() == 0
            page.locator('#navTab').click()
            page.locator('#navToolsTab').click()
            page.locator('#includeRevisionChk').check()
            page.keyboard.press('Escape')
            page.locator('#readerSearchInput').fill('Summary of Twentieth-Century Imperial Evolutions')
            page.locator('#readerSearchHits .reader-search-hit').first.wait_for(state='visible')
            assert page.locator('#readerSearchHits .reader-search-hit').count() > 0

            # Slash shortcut and Escape remain independent of the Contents
            # modal and leave the typed full-book query intact.
            page.locator('#readerSearchInput').fill('')
            page.locator('#screenView').focus()
            page.keyboard.press('/')
            assert page.evaluate("document.activeElement.id") == 'readerSearchInput'
            page.locator('#readerSearchInput').fill('unlikelyxxxxxxphrase')
            page.wait_for_function("document.querySelector('#readerSearchStatus').textContent.includes('No matches')")
            page.keyboard.press('Escape')
            assert page.locator('#readerSearchResults').is_hidden()

            # A floating button opens a modal drawer with correct keyboard focus.
            page.locator('#navTab').click()
            assert page.locator('#navPanel').get_attribute('aria-hidden') == 'false'
            assert page.locator('#navTab').get_attribute('aria-expanded') == 'true'
            assert page.evaluate("document.activeElement.id") == 'navClose'
            assert page.locator('#navIndexTab').get_attribute('aria-selected') == 'true'
            assert page.locator('#navToolsPanel').is_hidden()
            page.locator('#navIndexTab').focus()
            page.keyboard.press('ArrowRight')
            assert page.locator('#navToolsTab').get_attribute('aria-selected') == 'true'
            assert page.locator('#navIndexPanel').is_hidden()
            assert page.evaluate("document.activeElement.id") == 'navToolsTab'
            page.keyboard.press('Home')
            assert page.locator('#navIndexTab').get_attribute('aria-selected') == 'true'
            page.keyboard.press('End')
            assert page.locator('#navToolsTab').get_attribute('aria-selected') == 'true'
            page.keyboard.press('ArrowLeft')
            assert page.locator('#navIndexPanel').is_visible()
            assert page.locator('#navToolsPanel').is_hidden()
            page.keyboard.press('Escape')
            assert page.locator('#navPanel').get_attribute('aria-hidden') == 'true'
            assert page.evaluate("document.activeElement.id") == 'navTab'

            page.locator('#navTab').click()
            page.locator('#tocExpandAll').click()
            assert page.locator('.nav-chapter-toggle[aria-expanded="true"]').count() == 33
            page.locator('#tocCollapseAll').click()
            assert page.locator('.nav-chapter-toggle[aria-expanded="false"]').count() == 33

            # Index is a navigation tree only; full-book search belongs in the header.
            assert page.locator('#tocSearch, #tocClearSearch, #tocSearchStatus').count() == 0
            assert page.locator('#navIndexPanel .nav-tree-controls button').count() == 2
            assert page.locator('#navToc .nav-chapter:not([hidden])').count() == 33
            assert page.locator('#readerSearchInput').count() == 1
            assert page.locator('.nav-chapter-toggle[aria-expanded="false"]').count() == 33

            # Chevron is independent of the chapter link and keyboard-operable.
            first_toggle = page.locator('.nav-chapter-toggle').first
            first_toggle.focus()
            page.keyboard.press('Enter')
            assert first_toggle.get_attribute('aria-expanded') == 'true'
            first_toggle.focus()
            page.keyboard.press('Space')
            assert first_toggle.get_attribute('aria-expanded') == 'false'

            # Dedicated revision and study-aid shortcuts exist.
            assert page.locator('.nav-shortcut', has_text='Revision').count() == 33
            assert page.locator('.nav-shortcut', has_text='Definitions').count() > 20
            assert page.locator('.nav-shortcut', has_text='Memory aids').count() > 20
            assert page.locator('.nav-shortcut', has_text='Questions').count() > 0

            # Expand, follow section link, highlight current section without
            # automatically expanding every manually collapsed branch.
            page.locator('#tocExpandAll').click()
            link = page.locator('#navToc .nav-chapter[data-chapter="16"] .nav-section-link').first
            target = link.get_attribute('data-target')
            link.click()
            page.wait_for_timeout(150)
            assert page.locator('#navPanel').get_attribute('aria-hidden') == 'true'
            assert page.evaluate('window.scrollY') > 200
            assert page.locator('#chapterProgressRing').is_visible()
            assert int(page.locator('#chapterProgressRing').get_attribute('aria-valuenow')) >= 0
            assert page.locator('.nav-chapter[data-chapter="16"]').get_attribute('class').find('current-chapter') >= 0
            assert page.locator(f'#{target}').get_attribute('id') == target
            assert page.locator('.nav-section-link[aria-current="location"]').count() == 1

            # Invalid print ranges cannot generate a partial PDF; ordered
            # reversed ranges and repeated chapters remain supported.
            page.locator('#navTab').click()
            page.locator('#navToolsTab').click()
            page.locator('#navExportPanel summary').click()
            page.locator('#navToolsTab').click()
            if not page.locator('#navExportPanel').evaluate('(e)=>e.open'):
                page.locator('#navExportPanel summary').click()
            page.locator('#rangeInput').fill('999,1')
            assert page.locator('#printBtn').is_disabled()
            page.locator('#navToolsTab').click()
            if not page.locator('#navExportPanel').evaluate('(e)=>e.open'):
                page.locator('#navExportPanel summary').click()
            page.locator('#rangeInput').fill('1,,2')
            assert page.locator('#printBtn').is_disabled()
            page.locator('#navToolsTab').click()
            if not page.locator('#navExportPanel').evaluate('(e)=>e.open'):
                page.locator('#navExportPanel summary').click()
            page.locator('#rangeInput').fill('1x,2')
            assert page.locator('#printBtn').is_disabled()
            page.locator('#navToolsTab').click()
            if not page.locator('#navExportPanel').evaluate('(e)=>e.open'):
                page.locator('#navExportPanel summary').click()
            page.locator('#rangeInput').fill('6-5,1,6')
            assert page.locator('#printBtn').is_enabled()
            page.evaluate('window.print=()=>{}')
            page.locator('#printBtn').click()
            assert not page.evaluate("document.body.classList.contains('drawer-open')"), (
                'Export must restore normal page scrolling')
            printed = page.locator('#printView .hero-title').all_text_contents()
            assert printed == [
                page.locator('#chapterData .chapter-source[data-chapter="6"]').get_attribute('data-title'),
                page.locator('#chapterData .chapter-source[data-chapter="5"]').get_attribute('data-title'),
                page.locator('#chapterData .chapter-source[data-chapter="1"]').get_attribute('data-title'),
                page.locator('#chapterData .chapter-source[data-chapter="6"]').get_attribute('data-title')
            ], printed

            # Resume is optional, local to the browser, and never an auto-jump.
            page.evaluate('window.scrollBy(0,180)')
            page.mouse.wheel(0, 220)
            page.wait_for_timeout(1900)
            stored = page.evaluate("localStorage.getItem('whd-reading-place-v1')")
            assert stored is not None, "Reading position must be saved after real movement"
            other = context.new_page()
            other.goto(url,wait_until='load')
            other.locator('#navToc .nav-chapter-link').first.wait_for(state='attached')
            other.locator('#resumeReaderPrompt').wait_for(state='visible',timeout=5000)
            assert other.evaluate('window.scrollY') < 120, "Resume must not jump automatically"
            other.locator('#resumeReaderContinue').click()
            assert other.evaluate('window.scrollY') > 300
            other.locator('#navTab').click()
            assert other.locator('#navPanel').get_attribute('aria-hidden') == 'false'
            other.locator('#navOverlay').click(position={'x':4,'y':4},force=True)
            assert other.locator('#navPanel').get_attribute('aria-hidden') == 'true'

            # Revision toggle rebuilds screen nav without losing functionality.
            other.locator('#navTab').click()
            other.locator('#navToolsTab').click()
            other.locator('#navExportPanel summary').click()
            other.locator('#navToolsTab').click()
            other.locator('#includeRevisionChk').uncheck()
            other.wait_for_timeout(100)
            assert other.locator('#navToc .nav-chapter-link').count() == 33
            assert other.locator('.nav-shortcut',has_text='Revision').count() == 0
            other.locator('#navToolsTab').click()
            other.locator('#includeRevisionChk').check()
            other.wait_for_timeout(100)
            assert other.locator('.nav-shortcut',has_text='Revision').count() == 33

            # Mobile drawer fills screen and maintains a non-scrolling backdrop.
            mobile = context.new_page()
            mobile.set_viewport_size({'width':390,'height':844})
            mobile.on('pageerror',lambda e: errors.append(str(e)))
            mobile.goto(url,wait_until='load')
            mobile.locator('#navToc .nav-chapter-link').first.wait_for(state='attached')
            mobile.locator('#navTab').click()
            w = mobile.locator('#navPanel').bounding_box()
            assert w and w['width'] >= 385, w
            assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
            mobile.keyboard.press('Escape')
            assert mobile.evaluate("document.activeElement.id") == 'navTab'

            assert not errors, errors
            print(json.dumps({'chapterCount':33,'printSequence':[6,5,1,6],
                              'studyShortcuts':True,'search':True,'resume':True,
                              'keyboard':True,'mobile':True,'errors':errors},indent=2))
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
