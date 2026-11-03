#!/usr/bin/env python3
"""Append-safe chapter 18-19 coverage, metadata, sidebar and print test."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
CASES={
 18:{'title':'The Challenge in Europe, 1935–1941','sections':5,'rows':15,'aids':13,
 'markers':['Hollow Years','Four-Year Plan','Lebensraum','Roman','Gibraltar','Pact of Steel','Nazi–Soviet','Rhineland','Munich','Prague','Barbarossa','intentionalist','stab-in-the-back']},
 19:{'title':'Appeasement','sections':6,'rows':9,'aids':15,
 'markers':['Sargent','Ashton-Gwatkin','John Simon','Eden','Henderson','fourth arm','Rhineland','colonial','Munich','Anglo-German','Czechoslovakia','conscription','Poland','1939','reciprocity']}}
for n,c in CASES.items():
 root=BeautifulSoup((ROOT/'chapters'/f'ch{n:02}.html').read_text(),'html.parser')
 txt=root.get_text(' ',strip=True)
 assert root.select_one('.chapter-source')['data-title']==c['title']
 assert root.select_one('.src-hero .ht').get_text(strip=True)==c['title']
 assert len(root.select('.src-main [data-section-key]'))==c['sections']+1
 assert len(root.select('.src-main tbody tr'))==c['rows']
 assert len(root.select('.src-side > .block'))==c['aids']
 assert len(root.select('[data-revision-start="true"]'))==2
 assert all(root.select_one(f'.src-main [data-section-key="{x["data-for-section"]}"]') for x in root.select('.src-side > .block'))
 missing=[m for m in c['markers'] if m.lower() not in txt.lower()]
 assert not missing,(n,missing)
 print('PASS: Chapter',n,'source:',c['sections'],'sections,',c['rows'],'rows,',c['aids'],'cards')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 p=browser.new_page(viewport={'width':1440,'height':900})
 errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.set_content((ROOT.parent/'book.html').read_text(),wait_until='load')
 for n,c in CASES.items():
  assert p.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==c['title']
  assert p.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==c['aids']
 p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
 p.emulate_media(media='print')
 assert p.locator('#printView .hero-title').all_text_contents()[18:20]==[CASES[x]['title'] for x in (18,19)]
 assert p.locator('#printView table tbody tr').count()==p.locator('#chapterData table tbody tr').count()
 assert p.locator('#printView .is-revision').count()==len(list((ROOT/'chapters').glob('ch*.html')))
 assert not errors,errors
 browser.close()
print('PASS: Chapters 18–19 integrated into print and reading views')
