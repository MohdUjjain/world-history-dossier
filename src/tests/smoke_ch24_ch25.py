#!/usr/bin/env python3
"""Append-safe test for Chapters 24 and 25, including a fast two-chapter browser fixture."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
SRC=Path(__file__).resolve().parents[1]
CASES={
 24:{'title':'A Third World?','sections':6,'rows':17,'aids':15,
 'markers':['Sauvy','Third Estate','Bandung','29 states','Nehru','Nasser','Sukarno','Nkrumah','Tito','Belgrade','Havana','UNCTAD','Group of 77','G77','NIEO','0.7%','Fourth World','Monroe Doctrine','African Union']},
 25:{'title':'Making the New Europe: European Integration since 1950','sections':6,'rows':18,'aids':16,
 'markers':['Marshall Plan','CEEC','OEEC','Council of Europe','Schuman','Monnet','ECSC','EDC','Messina','Euratom','EEC','CAP','Milward','Spaak','Beyen','Luxembourg','de Gaulle','European Council','Bretton Woods','1973','1995','2004','mailbox democracy']}}
for n,c in CASES.items():
 s=BeautifulSoup((SRC/'chapters'/f'ch{n:02}.html').read_text(encoding='utf8'),'html.parser')
 assert s.select_one('.chapter-source')['data-title']==c['title']
 assert s.select_one('.src-hero h1').get_text(' ',strip=True)==c['title']
 assert len(s.select('.src-main [data-section-key]'))==c['sections']+1
 assert len(s.select('table tbody tr'))==c['rows']
 assert len(s.select('.src-side > .block'))==c['aids']
 assert len(s.select('[data-revision-start="true"]'))==2
 keys={x['data-section-key'] for x in s.select('.src-main [data-section-key]')}
 assert all(b['data-for-section'] in keys for b in s.select('.src-side > .block'))
 kinds=Counter(x['data-kind'] for x in s.select('.src-side > .block'))
 assert len(kinds)>=5,kinds
 txt=s.get_text(' ',strip=True).lower()
 missing=[x for x in c['markers'] if x.lower() not in txt]
 assert not missing,(n,missing)
 print('PASS source',n,'rows',c['rows'],'aids',c['aids'],'kinds',dict(kinds))
fixture=(SRC/'shell.html').read_text().replace('/*__STYLES__*/',(SRC/'styles.css').read_text().strip('\n')).replace('/*__SCRIPT__*/',(SRC/'engine.js').read_text().strip('\n')).replace('<!--__CHAPTERS__-->','\n'.join((SRC/'chapters'/f'ch{n:02}.html').read_text() for n in (24,25)))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1440,'height':900})
 errors=[];p.on('pageerror',lambda err:errors.append(str(err)))
 p.set_content(fixture,wait_until='load')
 for n,c in CASES.items():
  assert p.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==c['title']
  assert p.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==c['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[CASES[n]['title'] for n in (24,25)]
 assert p.locator('#printView table tbody tr').count()==35
 assert p.locator('#printView .is-revision').count()==2
 assert not p.locator('#printView .col-main,#printView .col-side,#printView .col-full').evaluate_all('(els)=>els.some(e=>e.scrollHeight-e.clientHeight>2)')
 print('PRINT pages:',p.locator('#printView .page').count())
 p.emulate_media(media='screen')
 p.locator('#navTab').click();p.locator('#includeRevisionChk').uncheck()
 assert p.locator('#screenView .revision-flow').count()==0
 p.locator('#includeRevisionChk').check()
 assert p.locator('#screenView .revision-flow').count()==2
 p.evaluate('window.print=function(){}')
 p.locator('#rangeInput').fill('25,24,25');p.locator('#printBtn').click()
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[CASES[n]['title'] for n in (25,24,25)]
 assert p.locator('#printView .is-revision').count()==3
 p.emulate_media(media='screen');p.set_viewport_size({'width':390,'height':844})
 assert p.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth')
 assert not errors,errors
 b.close()
print('PASS Chapters 24–25 browser fixture, toggles, repeat/order, 16:9 print geometry and mobile')
