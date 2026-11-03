#!/usr/bin/env python3
"""Append-safe Ch16/17 source-coverage, section-aid and print QA."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT.parent/'book.html'
CASES={
16:{'title':'The Challenge to Empire in the Middle East and Asia','sections':5,'rows':5,'aids':13,
'markers':['Hans Kohn','Subaltern Studies','Amritsar','Satyagraha','Swaraj','Hartal','Government of India Act','Wafd','Zaghlul','Faysal','National Bloc','VNQDD','Yen Bay','Ho Chi Minh','Nghe An/Ha Tinh','mission civilisatrice']},
17:{'title':"Mussolini's War in Ethiopia",'sections':4,'rows':9,'aids':12,
'markers':['Menelik II','Adowa','Haile Selassie','Rases','1923','proletarian nation','Fiat','Ansaldo','Wedding Ring','Stresa','Peace Ballot','Suez','Hoare','Laval','mustard gas','Wal Wal','Anschluss','Dark Valley']}}
for n,case in CASES.items():
 f=ROOT/'chapters'/f'ch{n:02}.html';d=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser');text=d.get_text(' ',strip=True)
 assert d.select_one('.chapter-source')['data-title']==case['title']
 assert len(d.select('.src-main [data-section-key]'))==case['sections']+1
 assert len(d.select('.src-main tbody tr'))==case['rows']
 assert len(d.select('.src-side > .block'))==case['aids']
 assert len(d.select('[data-revision-start="true"]'))==2
 assert all(d.select_one(f'[data-section-key="s{i}"]') for i in range(1,case['sections']+1))
 assert all(d.select_one(f'.src-main [data-section-key="{x.get("data-for-section")}"]') for x in d.select('.src-side > .block'))
 missing=[m for m in case['markers'] if m.lower() not in text.lower()]
 assert not missing,(n,missing)
 print('Source chapter',n,'PASS:',case['sections'],'sections,',case['rows'],'rows,',case['aids'],'sidebar cards')
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':900});errors=[]
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content(BOOK.read_text(encoding='utf8'),wait_until='load')
 for n,case in CASES.items():
  assert p.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==case['title']
  assert p.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==case['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()[16:18]==[CASES[n]['title'] for n in (16,17)]
 assert p.locator('#printView table tbody tr').count()==p.locator('#chapterData table tbody tr').count()
 assert p.locator('#printView .is-revision').count()==len(list((ROOT/'chapters').glob('ch*.html')))
 assert not errors,errors
 b.close()
print('PASS: 16/17 book integration and print checks')
