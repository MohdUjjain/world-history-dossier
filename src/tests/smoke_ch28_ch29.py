#!/usr/bin/env python3
"""Append-safe source and interactive smoke checks for Chapters 28–29."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
SRC=Path(__file__).resolve().parents[1]
DATA={
28:dict(title='The Sino-Soviet Alliance',sections=7,rows=9,aids=16,markers=['Changchun','Port Arthur','Tito','Korean War','Stalin','Khrushchev','joint','Secret Speech','1959','Zhenbao','Xinjiang','Kosygin','Zhou Enlai','1970s']),
29:dict(title='The Collapse of the Soviet Union and the End of the Cold War',sections=7,rows=11,aids=18,markers=['perestroika','glasnost','Anti-Alcohol','Uzbek Cotton','Chernobyl','Yeltsin','enterprise','Reykjavik','Sinatra','Vilnius','Nagorno-Karabakh','June 1990','August 1991','December 1991','Commonwealth of Independent States'])
}
for n,d in DATA.items():
 s=BeautifulSoup((SRC/'chapters'/f'ch{n:02}.html').read_text(),'html.parser')
 assert s.select_one('.chapter-source')['data-title']==d['title']
 assert s.select_one('.src-hero h1').get_text(' ',strip=True)==d['title']
 assert len(s.select('.src-main [data-section-key]'))==d['sections']+1
 assert len(s.select('table tbody tr'))==d['rows']
 assert len(s.select('.src-side > .block'))==d['aids']
 assert len(s.select('[data-revision-start="true"]'))==2
 assert all(b['data-for-section'] in {v['data-section-key'] for v in s.select('.src-main [data-section-key]')} for b in s.select('.src-side > .block'))
 cats=Counter(b['data-kind'] for b in s.select('.src-side > .block'))
 assert len(cats)>=5,cats
 missing=[x for x in d['markers'] if x.lower() not in s.get_text(' ',strip=True).lower()]
 assert not missing,(n,missing)
 print('PASS chapter',n,'rows',d['rows'],'sidebar',d['aids'],'kinds',dict(cats),flush=True)
fixture=(SRC/'shell.html').read_text().replace('/*__STYLES__*/',(SRC/'styles.css').read_text().strip('\n')).replace('/*__SCRIPT__*/',(SRC/'engine.js').read_text().strip('\n')).replace('<!--__CHAPTERS__-->','\n'.join((SRC/'chapters'/f'ch{n:02d}.html').read_text() for n in DATA))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 p=b.new_page(viewport={'width':1440,'height':900})
 errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
 p.set_content(fixture,wait_until='load')
 for n,d in DATA.items():
  assert p.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==d['title']
  assert p.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==d['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[d['title'] for d in DATA.values()]
 assert p.locator('#printView table tbody tr').count()==20
 assert p.locator('#printView .is-revision').count()==2
 assert not p.locator('#printView .col-main,#printView .col-side,#printView .col-full').evaluate_all('(a)=>a.some(e=>e.scrollHeight-e.clientHeight>2)')
 print('FOCUSED pages',p.locator('#printView .page').count(),'sidebar',p.locator('#printView .col-side > .block').count(),flush=True)
 p.emulate_media(media='screen'); p.locator('#navTab').click()
 p.locator('#includeRevisionChk').uncheck();assert p.locator('#screenView .revision-flow').count()==0
 p.locator('#includeRevisionChk').check();assert p.locator('#screenView .revision-flow').count()==2
 p.evaluate('window.print=()=>{}')
 p.locator('#rangeInput').fill('29,28,29');p.locator('#printBtn').click()
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[DATA[n]['title'] for n in (29,28,29)]
 assert p.locator('#printView .is-revision').count()==3
 p.emulate_media(media='screen');p.set_viewport_size({'width':390,'height':844})
 assert p.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth')
 assert not errs,errs
 b.close()
print('PASS Ch28–29 custom/repeated ordering, revisions, mobile, print and source')
