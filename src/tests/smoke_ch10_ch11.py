#!/usr/bin/env python3
"""Chapters 10–11: content sentinels, section-linked learning aids and print export.
Sources: supplied concise notes, without external historical fact-checking.
Designed to be append-safe when chapters 12+ are added.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parents[1]
BOOK=P.parent/'book.html'
CASES={
 10: dict(title='Wartime Promises and the Postwar Empires',sections=5,rows=10,side=11,
  terms=['Ottoman Empire','October 1914','Gallipoli','Husayn','McMahon','Mersin','Palestine','Sykes','Picot','Balfour','1917','Istanbul','free port','Togoland','Cameroons','Tanganyika','Lettow-Vorbeck','askaris','two million','200,000','New Guinea','Samoa','Twenty-One Demands','Shantung','racial equality','mandate system','Class C','Class B','provisionally recognized','Zionism','Vilayet']),
 11: dict(title='Envisioning a New World Order',sections=5,rows=12,side=10,
  terms=['Nicholas II','Wilhelm II','Franz Joseph','Woodrow Wilson','Vladimir Lenin','Christian','Monroe Doctrine','Fourteen Points','January 1918','self-determination','Labour rights','League of Nations','balance-of-power','monopoly capitalism','finance capital','Comintern','1919','proletariat','class struggle','Poland','Czechoslovakia','Versailles','American Socialist Party','Hands off Russia','Hungary','Bavaria','socialism in one country','1920','Third International'])}

def main():
 for n,case in CASES.items():
  html=(P/'chapters'/f'ch{n:02}.html').read_text(encoding='utf8')
  s=BeautifulSoup(html,'html.parser')
  assert s.select_one('.chapter-source')['data-title']==case['title']
  assert len(s.select('.src-main [data-section-key]'))==case['sections']
  assert len(s.select('.src-main tbody tr'))==case['rows']
  assert len(s.select('.src-side > .block'))==case['side']
  assert len(s.select('.src-main [data-revision-start=true]'))==1
  assert len(s.select('.src-side [data-revision-start=true]'))>=1
  t=s.get_text(' ',strip=True).casefold()
  missing=[k for k in case['terms'] if k.casefold() not in t]
  assert not missing,(n,'missing source anchors',missing)
  keys={x['data-section-key'] for x in s.select('.src-main [data-section-key]')}
  kinds=set();displays=set()
  for block in s.select('.src-side > .block'):
   assert block['data-for-section'] in keys
   kinds.add(block['data-kind']);displays.add(block['data-display'])
  assert len(kinds)>=5 and len(displays)>=5,(n,kinds,displays)
  print(f'Ch{n:02} PASS: {len(case["terms"])} key markers; {case["rows"]} table rows; {case["side"]} varied aids')
 with sync_playwright() as play:
  browser=play.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':900})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(BOOK.read_text(encoding='utf8'),wait_until='load')
  for n,c in CASES.items():
   assert page.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==c['title']
   assert page.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==c['side']
  page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
  page.emulate_media(media='print')
  titles=page.locator('#printView .hero-title').all_text_contents()
  assert titles[10:12]==[CASES[i]['title'] for i in [10,11]],titles
  for n,c in CASES.items():
   assert page.locator(f'#printView table tbody tr').count()==page.locator('#chapterData table tbody tr').count()
  assert not errors,errors
  browser.close()
 print('PASS: new chapters remain intact in full-book HTML and 16:9 print export')

if __name__=='__main__': main()
