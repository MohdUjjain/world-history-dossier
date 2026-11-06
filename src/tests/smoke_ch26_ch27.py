#!/usr/bin/env python3
"""Append-safe source and interactive browser regression for chapters 26 and 27."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
CASES={
 26:dict(title='The Making of Modern Southeast Asia in the Age of Decolonization and the Cold War',sections=7,rows=9,aids=17,
   markers=['Guomindang','Sukarno','Ho Chi Minh','Sri Lanka','Commonwealth','1949','Vietminh','Dien Bien Phu','17th parallel','SEATO','domino theory','Bandung','Colombo Plan','ASEAN','1979','doi moi','Panchsheel']),
 27:dict(title="The Middle East, 1945–1991: The Making of a Mare's Nest",sections=6,rows=8,aids=17,
   markers=['Suez','Palestine','Bevin','Eisenhower','Baghdad Pact','Kuwait','Aden','Nixon','Saudi Arabia','Shah','Yom Kippur','Carter','Iran–Iraq','Iran–Contra','Desert Shield','Desert Storm','mare’s nest'])
}
for number,case in CASES.items():
 s=BeautifulSoup((ROOT/'chapters'/f'ch{number:02d}.html').read_text(),'html.parser')
 assert s.select_one('.chapter-source')['data-title']==case['title']
 assert s.select_one('.src-hero h1').get_text(' ',strip=True)==case['title']
 assert len(s.select('.src-main [data-section-key]'))==case['sections']+1
 assert len(s.select('table tbody tr'))==case['rows']
 assert len(s.select('.src-side > .block'))==case['aids']
 assert len(s.select('[data-revision-start="true"]'))==2
 keys={v['data-section-key'] for v in s.select('.src-main [data-section-key]')}
 assert all(b['data-for-section'] in keys for b in s.select('.src-side > .block'))
 kinds=Counter(x['data-kind'] for x in s.select('.src-side > .block'))
 assert len(kinds)>=5,kinds
 txt=s.get_text(' ',strip=True).lower()
 missing=[m for m in case['markers'] if m.lower() not in txt]
 assert not missing,(number,missing)
 print('PASS source',number,'rows',case['rows'],'aids',case['aids'],'kinds',dict(kinds))
fixture=(ROOT/'shell.html').read_text().replace('/*__STYLES__*/',(ROOT/'styles.css').read_text().strip('\n')).replace('/*__SCRIPT__*/',(ROOT/'engine.js').read_text().strip('\n')).replace('<!--__CHAPTERS__-->','\n'.join((ROOT/'chapters'/f'ch{n:02d}.html').read_text() for n in CASES))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1440,'height':900})
 errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
 p.set_content(fixture,wait_until='load')
 for number,case in CASES.items():
  assert p.locator(f'#screenView #chapter-{number} .banner h1').inner_text()==case['title']
  assert p.locator(f'#screenView #chapter-{number} .side-flow > .block').count()==case['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[x['title'] for x in CASES.values()]
 assert p.locator('#printView table tbody tr').count()==17
 assert p.locator('#printView .is-revision').count()==2
 assert not p.locator('#printView .col-main,#printView .col-side,#printView .col-full').evaluate_all('(els)=>els.some(e=>e.scrollHeight-e.clientHeight>2)')
 pairs=p.evaluate('''() => {let p=[...document.querySelectorAll('#printView .page')];return {pages:p.length,side:[...document.querySelectorAll('#printView .learning-card')].length,chapterLabels:p.map(x=>x.dataset.chapter).filter(Boolean)}}''')
 print('PRINT',pairs)
 p.emulate_media(media='screen');p.locator('#navTab').click()
 p.locator('#navToolsTab').click();p.locator('#includeRevisionChk').uncheck();assert p.locator('#screenView .revision-flow').count()==0
 p.locator('#includeRevisionChk').check();assert p.locator('#screenView .revision-flow').count()==2
 p.evaluate('window.print = function(){}')
 p.locator('#navExportPanel summary').click();p.locator('#rangeInput').fill('27,26,27');p.locator('#printBtn').click()
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[CASES[n]['title'] for n in (27,26,27)]
 assert p.locator('#printView .is-revision').count()==3
 p.emulate_media(media='screen');p.set_viewport_size({'width':390,'height':844})
 assert p.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth')
 assert not errs,errs
 b.close()
print('PASS Ch26/27 fixture print, export order/repeat, revision toggle, mobile')
