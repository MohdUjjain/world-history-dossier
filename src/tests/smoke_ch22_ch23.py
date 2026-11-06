#!/usr/bin/env python3
"""Append-safe source and browser print checks for Chapters 22–23."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
S=Path(__file__).resolve().parents[1]
CASES={
22:{'title':'The Grand Alliance, 1941–1945','sections':5,'rows':6,'aids':14,
 'markers':['Atlantic Charter','Declaration by United Nations','ABC-1','Molotov','TORCH','Sicily','OVERLORD','Teheran','Poland','Four Policemen','Greece','Romania','Bulgaria','Yalta','Lublin','Truman','European Advisory Commission','Casablanca']},
23:{'title':'A Bipolar World','sections':6,'rows':12,'aids':15,
 'markers':['NATO','Warsaw Pact','Yugoslavia','France','Kennan','Iron Curtain','Marshall Plan','FRG','GDR','Korean War','Sputnik','Cuban Missile Crisis','Test Ban','Ostpolitik','Helsinki','Afghanistan','Reagan','Strategic Defense Initiative','KAL 007','Gorbachev','1991']}}
for n,c in CASES.items():
 d=BeautifulSoup((S/'chapters'/f'ch{n}.html').read_text(encoding='utf-8'),'html.parser')
 assert d.select_one('.chapter-source')['data-title']==c['title']
 assert d.select_one('.src-hero .ht').get_text(strip=True)==c['title']
 assert len(d.select('.src-main [data-section-key]'))==c['sections']+1
 assert len(d.select('.src-main table tbody tr'))==c['rows']
 assert len(d.select('.src-side > .block'))==c['aids']
 assert len(d.select('[data-revision-start="true"]'))==2
 keys={x['data-section-key'] for x in d.select('.src-main [data-section-key]')}
 assert all(b['data-for-section'] in keys for b in d.select('.src-side > .block'))
 kinds=Counter(b['data-kind'] for b in d.select('.src-side > .block'))
 assert len(kinds)>=5,kinds
 txt=d.get_text(' ',strip=True).lower()
 missing=[m for m in c['markers'] if m.lower() not in txt]
 assert not missing,(n,missing)
 print('PASS source',n,'rows',c['rows'],'aids',c['aids'],'types',dict(kinds))
# Render just these two new chapters in the production shell to keep the test fast
# and append-safe even when the complete dossier exceeds 150 print pages.
source_html=(S/"shell.html").read_text(encoding="utf-8")
source_html=(source_html.replace("/*__STYLES__*/",(S/"styles.css").read_text(encoding="utf-8"))
 .replace("/*__SCRIPT__*/",(S/"engine.js").read_text(encoding="utf-8"))
 .replace("<!--__CHAPTERS__-->","\n".join((S/"chapters"/f"ch{n}.html").read_text(encoding="utf-8") for n in (22,23))))
full=BeautifulSoup((S.parent/"book.html").read_text(encoding="utf-8"),"html.parser")
assert [x.get("data-title") for x in full.select(".chapter-source")][22:24]==[CASES[22]["title"],CASES[23]["title"]]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1440,'height':900});errors=[]
 p.on('pageerror',lambda e: errors.append(str(e)))
 p.set_content(source_html,wait_until='load')
 for n,c in CASES.items():
  assert p.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==c['title']
  assert p.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==c['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[CASES[n]['title'] for n in (22,23)]
 assert p.locator('#printView table tbody tr').count()==p.locator('#chapterData table tbody tr').count()
 assert p.locator('#printView .is-revision').count()==2
 assert not p.locator('#printView .col-main,#printView .col-side').evaluate_all('(els)=>els.some(e=>e.scrollHeight-e.clientHeight>2)')
 # Verify the live export workflow on the two-chapter test fixture.
 p.emulate_media(media='screen')
 p.locator('#navTab').click()
 p.locator('#navToolsTab').click();p.locator('#includeRevisionChk').uncheck()
 assert p.locator('#screenView .revision-flow').count()==0
 p.locator('#includeRevisionChk').check()
 assert p.locator('#screenView .revision-flow').count()==2
 p.evaluate('window.print=function(){}')
 p.locator('#navExportPanel summary').click();p.locator('#rangeInput').fill('23,22,23')
 p.locator('#printBtn').click()
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()==[CASES[n]['title'] for n in (23,22,23)]
 assert p.locator('#printView .is-revision').count()==3
 p.emulate_media(media='screen')
 p.set_viewport_size({'width':390,'height':844})
 mobile=p.evaluate('''()=>({width:document.documentElement.scrollWidth,view:document.documentElement.clientWidth})''')
 assert mobile['width']<=mobile['view'],mobile
 assert not errors,errors
 b.close()
print('PASS: Chapters 22–23 reader, 16:9 print source and table integrity')
