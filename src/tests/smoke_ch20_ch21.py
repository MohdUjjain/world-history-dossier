#!/usr/bin/env python3
"""Append-safe source fidelity, Sidebar V2 and PDF integration test, Ch20–21."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
SRC=Path(__file__).resolve().parents[1]
BOOK=SRC.parent/'book.html'
CASES={
20:{'title':'Stalin and the West','sections':6,'rows':8,'aids':12,
 'markers':['Arcos','Snitko','Brest-Litovsk','NEP','Metro-Vickers','Rapallo','Tashkent','Comintern','Popular Front','Litvinov','Molotov','Munich','Czechoslovakia','Poland','Finland','Suvorov','Glantz','Barbarossa','22 June 1941']},
21:{'title':'The United States and the End of Isolation','sections':6,'rows':10,'aids':14,
 'markers':['Roosevelt','Kristallnacht','Cash-and-carry','Burke','Wadsworth','destroyers-for-bases','99-year','Lend-Lease','America First','Reynolds','Greenland','Iceland','Greer','Hull','Plan A','Plan B','Tripartite Pact','Pearl Harbor']}}
for n,c in CASES.items():
 d=BeautifulSoup((SRC/'chapters'/f'ch{n:02d}.html').read_text(encoding='utf8'),'html.parser')
 root=d.select_one('.chapter-source')
 assert root['data-title']==c['title']
 assert d.select_one('.src-hero h1.ht').get_text(strip=True)==c['title']
 assert len(d.select('.src-main [data-section-key]'))==c['sections']+1
 assert len(d.select('.src-main tbody tr'))==c['rows']
 assert len(d.select('.src-side > .block'))==c['aids']
 assert len(d.select('[data-revision-start="true"]'))==2
 assert all(d.select_one('.src-main [data-section-key="'+x['data-for-section']+'"]') for x in d.select('.src-side > .block'))
 txt=root.get_text(' ',strip=True)
 missing=[x for x in c['markers'] if x.lower() not in txt.lower()]
 assert not missing,(n,missing)
 kinds=Counter(x.get('data-kind') for x in d.select('.src-side > .block'))
 assert len(kinds)>=5,(n,kinds)
 print('PASS source:',n,c['rows'],'table rows,',c['aids'],'aids,',dict(kinds))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=b.new_page(viewport={'width':1440,'height':900})
 errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content(BOOK.read_text(encoding='utf8'),wait_until='load')
 for n,c in CASES.items():
  assert p.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==c['title']
  assert p.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==c['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()[20:22]==[CASES[n]['title'] for n in (20,21)]
 assert p.locator('#printView .is-revision').count()==len(list((SRC/'chapters').glob('ch*.html')))
 assert p.locator('#printView table tbody tr').count()==p.locator('#chapterData table tbody tr').count()
 assert not errors,errors
 b.close()
print('PASS: Ch20–21 reader, export and table integrity')
