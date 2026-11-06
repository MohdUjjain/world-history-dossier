#!/usr/bin/env python3
"""Batch 1 browser reproduction: modal isolation and competing bottom notices."""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            for width in (390,1360):
                context=browser.new_context(viewport={'width':width,'height':844},
                                            reduced_motion='reduce',service_workers='block')
                context.add_init_script("""() => localStorage.setItem('whd-reading-place-v1',
                  JSON.stringify({chapter:'16',section:null,chapterRatio:0.25,
                                  sectionRatio:0,savedAt:Date.now()}))""")
                page=context.new_page()
                page.goto(f'http://127.0.0.1:{server.server_port}/',wait_until='load')
                page.locator('#navToc .nav-chapter-link').first.wait_for()
                page.locator('#resumeReaderPrompt').wait_for(state='visible',timeout=6000)
                page.locator('#navTab').click()
                assert page.locator('#navPanel').get_attribute('aria-modal')=='true'
                snapshot=page.evaluate("""() => ({
                    screen:document.getElementById('screenView').inert,
                    cover:document.getElementById('titlePage').inert,
                    header:document.querySelector('header.site-header').inert,
                    resume:document.getElementById('resumeReaderPrompt').inert,
                    modal:document.getElementById('navPanel').inert,
                    focus:document.activeElement.id
                })""")
                assert snapshot['screen'] and snapshot['cover'] and snapshot['header'] and snapshot['resume'], snapshot
                assert not snapshot['modal'],snapshot
                assert snapshot['focus']=='navClose',snapshot
                page.keyboard.press('Escape')
                released=page.evaluate("""() => ({
                    screen:document.getElementById('screenView').inert,
                    cover:document.getElementById('titlePage').inert,
                    header:document.querySelector('header.site-header').inert,
                    resume:document.getElementById('resumeReaderPrompt').inert,
                    modal:document.getElementById('navPanel').inert,
                    focus:document.activeElement.id
                })""")
                assert not any(released[k] for k in ('screen','cover','header','resume')),released
                assert released['modal'] and released['focus']=='navTab',released

                # The real offline controllerchange listener shows the edition
                # notice on a *subsequent* controller replacement.
                page.evaluate("""() => {
                    navigator.serviceWorker.dispatchEvent(new Event('controllerchange'));
                    navigator.serviceWorker.dispatchEvent(new Event('controllerchange'));
                }""")
                page.locator('#editionUpdateNotice').wait_for(state='visible',timeout=4000)
                assert page.locator('#resumeReaderPrompt').is_hidden(), (
                    'Resume and edition notices are simultaneously visible')
                page.locator('#editionDismissBtn').click()
                assert page.locator('#editionUpdateNotice').is_hidden()
                assert page.locator('#resumeReaderPrompt').is_visible(), (
                    'Deferred resume suggestion must return when update dismissed')
                context.close()
            browser.close()
    finally:
        server.shutdown()
    print('PASS: modal background isolation, focus restoration and edition/resume priority on mobile and desktop')

if __name__=='__main__':
    main()
