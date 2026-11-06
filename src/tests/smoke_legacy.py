#!/usr/bin/env python3
"""Browser regression using archived chapters as non-production test fixtures.\n\nRun: python3 src/tests/smoke_legacy.py\nNeeds Playwright with a Chromium executable. Does not edit active chapters.\n"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

SRC=Path(__file__).resolve().parents[1]

def assemble(chapters):
    shell=(SRC/'shell.html').read_text(encoding='utf8')
    return (shell.replace('/*__STYLES__*/',(SRC/'styles.css').read_text(encoding='utf8'))
                 .replace('/*__SCRIPT__*/',(SRC/'engine.js').read_text(encoding='utf8'))
                 .replace('<!--__CHAPTERS__-->','\n\n'.join(p.read_text(encoding='utf8') for p in chapters)))


def main():
    fixtures=sorted((SRC/'archive/legacy-chapters').glob('ch*.html'))
    if len(fixtures)<2:
        raise RuntimeError('Expected two archived chapter fixtures')
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':900})
        js_errors=[]
        page.on('pageerror',lambda e:js_errors.append(str(e)))
        page.set_content(assemble(fixtures),wait_until='load')
        screen=page.evaluate('''() => ({
            chapters:document.querySelectorAll('.chapter-flow').length,
            mainConcepts:document.querySelectorAll('.chapter-flow .main-flow [data-kind="concept"]').length,
            sideConcepts:document.querySelectorAll('.chapter-flow .side-flow [data-kind="concept"]').length,
            originalMainConcepts:document.querySelectorAll('#chapterData .src-main [data-kind="concept"]').length,
            navFont:getComputedStyle(document.querySelector('.nav-sections a')).fontSize
        })''')
        assert screen['chapters']==2 and screen['mainConcepts']==0
        assert screen['sideConcepts']==screen['originalMainConcepts']==7
        page.locator('#navTab').click();page.locator('#navClose').click()
        page.locator('#navTab').click();page.locator('#includeRevisionChk').uncheck()
        assert page.locator('.revision-flow').count()==0
        page.locator('#navToolsTab').click()
        page.locator('#includeRevisionChk').check()
        assert page.locator('.revision-flow').count()==2
        page.locator('#navClose').click()
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        page.emulate_media(media='print')
        pr=page.evaluate('''() => {
          const pages=[...document.querySelectorAll('#printView .page')];
          return {pages:pages.length, tocPages:pages.filter(el=>el.classList.contains('type-toc')).length,
            printTocFont:getComputedStyle(document.querySelector('.toc-row.chapter')).fontSize,
            tocChapters:document.querySelectorAll('.toc-row.chapter').length,
            tocSections:document.querySelectorAll('.toc-row.section').length,
            mainConcepts:document.querySelectorAll('.page.type-content .col-main [data-kind="concept"]').length,
            sideConcepts:document.querySelectorAll('.page.type-content .col-side [data-kind="concept"]').length,
            overflow:[...document.querySelectorAll('.col-main,.col-side,.col-full')].filter(c=>c.scrollHeight-c.clientHeight>2).length};
        }''')
        assert pr['mainConcepts']==0 and pr['sideConcepts']==7 and pr['overflow']==0, pr
        assert pr['tocChapters']==2 and pr['tocSections']==0, pr
        page.emulate_media(media='screen')
        page.locator('#navTab').click()
        page.locator('#navToolsTab').click()
        if not page.locator('#navExportPanel').evaluate('(e)=>e.open'):
            page.locator('#navExportPanel summary').click()
        page.locator('#rangeInput').fill('1,0,1')
        # Avoid blocking Chromium's native print dialog during the custom-order test.
        page.evaluate('window.print=function(){}')
        page.locator('#printBtn').click()
        page.emulate_media(media='print')
        heroes=page.evaluate('''()=>[...document.querySelectorAll('#printView .type-hero .hero-title')].map(el=>el.textContent)''')
        assert heroes==['Imperialism','The Changing Face of Empire','Imperialism'],heroes
        page.set_viewport_size({'width':390,'height':844})
        page.emulate_media(media='screen')
        mobile=page.evaluate('''()=>({scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth})''')
        assert mobile['scrollWidth']<=mobile['clientWidth'],mobile
        browser.close()
        assert not js_errors,js_errors
        print(json.dumps({'screen':screen,'print':pr,'customOrder':heroes,'mobile':mobile,'jsErrors':js_errors},indent=2))
        print('PASS: legacy fixtures are absent from active book but safely validate the upgraded engine')

if __name__=='__main__':main()
