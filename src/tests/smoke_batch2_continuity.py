#!/usr/bin/env python3
"""Batch 2: missing/renamed section checkpoint across revised HTML and visibility."""
from __future__ import annotations
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
FIX=json.loads((ROOT/'src/tests/fixtures/batch2_modified_edition.json').read_text())
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*_):pass
def main():
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
 Thread(target=server.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
   for width in (390,1360):
    ctx=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce',service_workers='block')
    ctx.add_init_script(script=f"localStorage.setItem({json.dumps(FIX['key'])},{json.dumps(json.dumps(FIX['checkpoint']))});")
    page=ctx.new_page()
    page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load')
    page.locator('#navToc .nav-chapter-link').first.wait_for(state='attached')
    page.locator('#resumeReaderPrompt').wait_for(state='visible',timeout=7000)
    assert page.evaluate("key=>JSON.parse(localStorage.getItem(key)).section",FIX['key'])==FIX['lostSection']
    assert page.locator('#'+FIX['lostSection']).count()==0
    page.locator('#resumeReaderContinue').click()
    page.wait_for_function("() => scrollY>100")
    rect=page.locator('#chapter-'+FIX['chapter']).bounding_box()
    assert rect and rect['y']<844 and rect['y']+rect['height']>0,rect
    # Visibility is a transient reading choice, not a checkpoint rewrite.
    old=page.evaluate("key=>JSON.parse(localStorage.getItem(key)).chapter",FIX['key'])
    page.locator('#navTab').click()
    page.locator('#navExportPanel summary').click()
    page.locator('#includeRevisionChk').uncheck()
    assert page.locator('#chapter-'+FIX['chapter']+' .revision-flow').count()==0
    assert page.evaluate("key=>JSON.parse(localStorage.getItem(key)).chapter",FIX['key'])==old
    page.locator('#navClose').click()
    assert page.evaluate('window.scrollY')>100
    ctx.close()
   browser.close()
 finally:
  server.shutdown();server.server_close()
 print('PASS: old section falls back inside same chapter; summary visibility does not corrupt saved chapter')
if __name__=='__main__':main()
