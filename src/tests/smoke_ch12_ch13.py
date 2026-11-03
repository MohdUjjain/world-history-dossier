#!/usr/bin/env python3
"""Source-specific and print-order regression for chapters 12 and 13.
Run from any working directory, after `python src/build.py`.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT.parent/'book.html'
CASES={
 12:{'title':'The Versailles System','sections':7,'rows':13,'aids':11,
     'markers':['Harold Nicolson','Fontainebleau','Reparations Commission','Dawes Plan','Young Plan','Article 231','Article 227','Article 228','International Military Control Commission','Saar Basin','Free City of Danzig','Locarno','Gustav Stresemann','Anschluss','International Labour Organization']},
 13:{'title':'The Legacy of the First World War','sections':4,'rows':9,'aids':12,
     'markers':['League of Nations','26 articles','Trianon','Neuilly','Sèvres','Anglo-French','Permanent Mandates Commission','Montagu Norman','Fridtjof Nansen','Nansen Passport','Minority','Åland','Vilna','Upper Silesia','Corfu','Bulgarian','Article 16']}
}
def run():
  for num,case in CASES.items():
   path=ROOT/'chapters'/f'ch{num:02}.html'
   html=path.read_text(encoding='utf8')
   assert f'data-chapter="{num:02}"' in html
   assert f'data-title="{case["title"]}"' in html
   assert html.count('data-kind="section-head"')==case['sections']+1
   assert html.count('<tbody>')>=1
   assert html.count('<tr><td>')==case['rows'],(num,html.count('<tr><td>'))
   assert len(re.findall(r'data-for-section="',html))==case['aids']
   assert html.count('data-revision-start="true"')==2
   assert all(x in html for x in case['markers']),(num,[x for x in case['markers'] if x not in html])
   assert all(f'data-section-key="s{i}"' in html for i in range(1,case['sections']+1))
   assert 'data-section-key="revision"' in html
   print(f'Ch{num} source PASS: {case["sections"]} main sections, {case["rows"]} table rows, {case["aids"]} sidebar aids; {len(case["markers"])} markers')
  with sync_playwright() as pw:
   browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
   page=browser.new_page(viewport={'width':1440,'height':900})
   errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
   page.set_content(BOOK.read_text(encoding='utf8'),wait_until='load')
   assert page.locator('#screenView .banner h1').all_text_contents()[12:14]==[CASES[i]['title'] for i in (12,13)]
   for num,case in CASES.items():
    assert page.locator(f'#chapterData .chapter-source[data-chapter="{num:02}"] .src-main table tbody tr').count()==case['rows']
    assert page.locator(f'#screenView #chapter-{num} .side-flow > .block').count()==case['aids']
   page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
   page.emulate_media(media='print')
   assert page.locator('#printView .hero-title').all_text_contents()[12:14]==[CASES[i]['title'] for i in (12,13)]
   assert page.locator('#printView table tbody tr').count()==page.locator('#chapterData table tbody tr').count()
   assert page.locator('#printView .is-revision').count()==len(list((ROOT/'chapters').glob('ch*.html')))
   assert not errors,errors
   browser.close()
  print('PASS: 12–13 book integration and print checks')
if __name__=='__main__':run()
