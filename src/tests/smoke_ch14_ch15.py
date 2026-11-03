#!/usr/bin/env python3
"""Append-safe Ch14/15 source completeness and browser/print integration checks."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT.parent/'book.html'
CASES={
14:{'title':'Why International Finance Mattered: 1919–1939','sections':4,'rows':12,'aids':11,
'markers':['City of London','gold standard','1925','gold exchange standard','Ruhr','1924','Wall Street','Benjamin Strong','Smoot','Morgan','Briand','Laval','Creditanstalt','Lausanne','1932','liberal internationalism','double fragility']},
15:{'title':'The Far Eastern Crisis and the Balance of Power, 1920–1941','sections':6,'rows':3,'aids':15,
'markers':['Washington','Nine-Power','Four-Power','Five-Power','5 : 5 : 3','Open Door','Kwantung','Mukden','Manchukuo','Lytton','Amau','Anti-Comintern','Nomonhan','Burma Road','Southern Advance','ABDA','oil','Stimson']}
}
def main():
 for n,case in CASES.items():
  p=ROOT/'chapters'/f'ch{n:02}.html';t=p.read_text(encoding='utf8');doc=BeautifulSoup(t,'html.parser')
  chap=doc.select_one('.chapter-source');assert chap['data-title']==case['title'];assert chap['data-chapter']==f'{n:02d}'
  assert len(doc.select('.src-main [data-section-key]'))==case['sections']+1
  assert len(doc.select('.src-main tbody tr'))==case['rows']
  assert len(doc.select('.src-side > .block'))==case['aids']
  assert len(doc.select('.src-main [data-revision-start=true]'))==1
  assert len(doc.select('.src-side [data-revision-start=true]'))==1
  for i in range(1,case['sections']+1):assert doc.select_one(f'[data-section-key="s{i}"]')
  for aid in doc.select('.src-side > .block'):
   key=aid.get('data-for-section');assert doc.select_one(f'.src-main [data-section-key="{key}"]')
  miss=[m for m in case['markers'] if m.lower() not in t.lower()];assert not miss,(n,miss)
  print(f'Ch{n}: PASS, {case["sections"]} sections, {case["rows"]} table rows, {case["aids"]} aids')
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':900})
  errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  page.set_content(BOOK.read_text(encoding='utf8'),wait_until='load')
  for n,c in CASES.items():
   assert page.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==c['title']
   assert page.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==c['aids']
  page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
  page.emulate_media(media='print')
  names=page.locator('#printView .hero-title').all_text_contents()
  assert names[14:16]==[CASES[14]['title'],CASES[15]['title']]
  assert page.locator('#printView table tbody tr').count()==page.locator('#chapterData table tbody tr').count()
  assert page.locator('#printView .is-revision').count()==len(list((ROOT/'chapters').glob('ch*.html')))
  assert not errors,errors
  browser.close()
 print('PASS: chapters 14 and 15 complete, source-anchored and print-safe')
if __name__=='__main__':main()
