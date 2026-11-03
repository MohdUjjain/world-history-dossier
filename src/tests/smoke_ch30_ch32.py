#!/usr/bin/env python3
"""Final-3 source, section-aware learning-aid and interactive export checks.

Append-safe: creates a minimal book with only Chapters 30–32; tests custom
order, duplicate chapter, summaries, print geometry and phone view.
"""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
SRC=Path(__file__).resolve().parents[1]
DATA={
30:dict(title='War and Peace in the Global Community, 1989–2001',sections=6,rows=12,aids=15,markers=['Wilsonian','Fukuyama','Mandelbaum','Kuwait','Tiananmen','Golden Straitjacket','Electronic Herd','NAFTA','WTO','Somalia','Rwanda','Haiti','Kosovo','Dayton','NATO','September 11']),
31:dict(title='Globalization',sections=6,rows=15,aids=15,markers=['synergistic','telegraph','Keynes','GATT','IMF','IBRD','container','Intelsat','60,000','Stiglitz','1997','1914','Bretton Woods']),
32:dict(title='Terrorism: September 11, 2001 and its Consequences',sections=6,rows=12,aids=15,markers=['propaganda by deed','Robespierre','Aum Shinrikyo','al-Qaeda','Taliban','Article 5','Resolution 1368','Afghanistan','preemption','prevention','Iraq','Guantánamo','Abu Ghraib','Madrid','London'])}
for n,d in DATA.items():
 s=BeautifulSoup((SRC/'chapters'/f'ch{n:02}.html').read_text(),'html.parser')
 assert s.select_one('.chapter-source')['data-title']==d['title']
 assert s.select_one('.src-hero h1').get_text(' ',strip=True)==d['title']
 assert len(s.select('.src-main [data-section-key]'))==d['sections']+1
 assert len(s.select('table tbody tr'))==d['rows']
 assert len(s.select('.src-side > .block'))==d['aids']
 assert len(s.select('[data-revision-start="true"]'))==2
 keys={x['data-section-key'] for x in s.select('.src-main [data-section-key]')}
 assert all(x['data-for-section'] in keys for x in s.select('.src-side > .block'))
 cats=Counter(x['data-kind'] for x in s.select('.src-side > .block'))
 assert len(cats)>=5,cats
 missing=[m for m in d['markers'] if m.lower() not in s.get_text(' ',strip=True).lower()]
 assert not missing,(n,missing)
 print('PASS source',n,'rows',d['rows'],'aids',d['aids'],flush=True)
fixture=(SRC/'shell.html').read_text().replace('/*__STYLES__*/',(SRC/'styles.css').read_text().strip('\n')).replace('/*__SCRIPT__*/',(SRC/'engine.js').read_text().strip('\n')).replace('<!--__CHAPTERS__-->','\n'.join((SRC/'chapters'/f'ch{n:02d}.html').read_text() for n in DATA))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 p=b.new_page(viewport={'width':1440,'height':900})
 errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content(fixture,wait_until='load')
 for n,d in DATA.items():
  assert p.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==d['title']
  assert p.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==d['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[d['title'] for d in DATA.values()]
 assert p.locator('#printView table tbody tr').count()==39
 assert p.locator('#printView .is-revision').count()==3
 assert not p.locator('#printView .col-main,#printView .col-side,#printView .col-full').evaluate_all('(a)=>a.some(e=>e.scrollHeight-e.clientHeight>2)')
 print('FOCUSED pages',p.locator('#printView .page').count(),'sidebar',p.locator('#printView .col-side > .block').count(),flush=True)
 p.emulate_media(media='screen');p.locator('#navTab').click()
 p.locator('#includeRevisionChk').uncheck();assert p.locator('#screenView .revision-flow').count()==0
 p.locator('#includeRevisionChk').check();assert p.locator('#screenView .revision-flow').count()==3
 p.evaluate('window.print=()=>{}')
 p.locator('#rangeInput').fill('32,30,31,32');p.locator('#printBtn').click()
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[DATA[n]['title'] for n in (32,30,31,32)]
 assert p.locator('#printView .is-revision').count()==4
 p.emulate_media(media='screen');p.set_viewport_size({'width':390,'height':844})
 assert p.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth')
 assert not errors,errors
 b.close()
print('PASS final Ch30–32 custom/repeated order, revision toggle, mobile, print and source')
