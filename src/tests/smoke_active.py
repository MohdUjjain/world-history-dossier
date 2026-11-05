#!/usr/bin/env python3
"""Reusable regression smoke test for all active chapters in the World History Dossier.

Run after build: python3 src/tests/smoke_active.py
Validates flows, official titles, preservation of table rows, revision toggles,
custom ordered export with duplication, print overflow and mobile geometry.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

SRC=Path(__file__).resolve().parents[1]
BOOK=SRC.parent/'book.html'
CATALOG={int(c['number']):c['title'] for c in json.loads((SRC/'chapter_catalog.json').read_text(encoding='utf8'))}
CHNUMS=sorted(int(x.stem[2:]) for x in (SRC/'chapters').glob('ch*.html'))
TITLES=[CATALOG[n] for n in CHNUMS]

def main():
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':900})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(BOOK.read_text(encoding='utf8'),wait_until='load')
        src=page.evaluate('''()=>({
          n:document.querySelectorAll('#chapterData .chapter-source').length,
          concepts:document.querySelectorAll('#chapterData [data-kind="concept"]').length,
          rows:document.querySelectorAll('#chapterData table.compare tbody tr').length,
          blocks:document.querySelectorAll('#chapterData .block').length,
          revisions:document.querySelectorAll('#chapterData .src-main [data-revision-start="true"]').length
        })''')
        assert src['n']==len(CHNUMS),src
        assert page.locator('#screenView .banner h1').all_text_contents()==TITLES
        assert page.locator('#screenView .main-flow [data-kind="concept"]').count()==0
        assert page.locator('#screenView .side-flow [data-kind="concept"]').count()==src['concepts']
        assert page.locator('#screenView .revision-flow').count()==src['revisions']
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        page.emulate_media(media='print')
        pr=page.evaluate('''()=>({
          pages:document.querySelectorAll('#printView .page').length,
          rows:document.querySelectorAll('#printView table.compare tbody tr').length,
          sideConcepts:document.querySelectorAll('#printView .col-side [data-kind="concept"]').length,
          mainConcepts:document.querySelectorAll('#printView .col-main [data-kind="concept"]').length,
          overflows:[...document.querySelectorAll('#printView .col-main,#printView .col-side,#printView .col-full')]
            .filter(e=>e.scrollHeight-e.clientHeight>2).length,
          heroOverflows:[...document.querySelectorAll('#printView .type-hero')]
            .filter(e=>e.scrollHeight-e.clientHeight>2).length
        })''')
        assert page.locator('#printView .hero-title').all_text_contents()==TITLES
        assert page.locator('#printView .toc-row.chapter').count()==len(CHNUMS)
        assert page.locator('#printView .toc-row.section').count()==0
        assert page.locator('#printView .toc-row.chapter a[href^="#pg-"]').count()==len(CHNUMS)
        assert pr['rows']==src['rows'] and pr['sideConcepts']==src['concepts'] and pr['mainConcepts']==0, (src,pr)
        assert pr['overflows']==0 and pr['heroOverflows']==0,pr
        page.emulate_media(media='screen')
        page.locator('#navTab').click()
        page.locator('#navExportPanel summary').click()
        page.locator('#includeRevisionChk').uncheck()
        assert page.locator('#screenView .revision-flow').count()==0
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        page.emulate_media(media='print')
        assert page.locator('#printView .is-revision').count()==0
        page.emulate_media(media='screen')
        page.locator('#includeRevisionChk').check()
        assert page.locator('#screenView .revision-flow').count()==src['revisions']
        if CHNUMS:
            # A three-chapter selection verifies order/duplicate semantics without
            # triggering another full-book rebuild for each release.
            order=[CHNUMS[-1],CHNUMS[0],CHNUMS[-1]]
            page.evaluate('window.print=function(){}')
            page.locator('#rangeInput').fill(','.join(map(str,order)))
            page.locator('#printBtn').click()
            page.emulate_media(media='print')
            assert page.locator('#printView .hero-title').all_text_contents()==[CATALOG[n] for n in order]
        assert page.locator('#chapterData .block').count()==src['blocks']
        page.emulate_media(media='screen')
        page.set_viewport_size({'width':390,'height':844})
        mobile=page.evaluate('''()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]''')
        assert mobile[0]<=mobile[1],mobile
        assert not errors,errors
        browser.close()
        print(json.dumps({'chapters':CHNUMS,'source':src,'print':pr,'mobile':mobile,'js_errors':errors},indent=2))
        print('PASS: content, print pagination, concept routing, revision toggle, custom order, mobile')

if __name__=='__main__':main()
