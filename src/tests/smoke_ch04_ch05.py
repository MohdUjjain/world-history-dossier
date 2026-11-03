#!/usr/bin/env python3
"""Content and visual-contract smoke for chapters 04 and 05.

Run after `python3 src/build.py`. Checks the supplied dates, statistics,
key arguments, reconstructed table data, semantic sidebar variety and
section-aware alignment without introducing outside historical assertions.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SRC=Path(__file__).resolve().parents[1]
BOOK=SRC.parent/'book.html'

expected={
4: {
 'title':'A Shrinking World',
 'sentinels':['Jeffrey A. Engel','Punic Wars','Genghis Khan','1853','Morse code',
 'American cotton','Indian rice','Australian beef','Alexander Graham Bell',
 '1925','1983','Marconi','Titanic','Zimmerman Telegram',
 '8,000 in 1946','45 million by 1960','Moon landing','Berlin Wall',
 'Michael Jordan','David Beckham','12.5 hours','under three hours',
 'Interstate Highway Act','Los Angeles smog','Ralph Nader',
 '59 seconds','1903','1909','Douglas DC-3','de Havilland Comet',
 'Boeing','Juan Trippe','Zworkin','morally neutral','annihilation of time and distance'],
 'rows':7,
 'side':10,
 'sections':4,
},
5: {
 'title':'A Changing Diplomatic World',
 'sentinels':['steamship and railway','telegraph','Clausewitz','Woodrow Wilson',
 'democratization','free trade','collective security','Amnesty International',
 'Greenpeace','NATO','European Union','Prussia','1827','1855','1858','1861',
 'unpaid attaché','Rogers Act of 1924','477 (1945)','9,293 (2004)',
 '1,228 (1900)','15,506 (1997)','350 (1900)','6,550',
 'France merged the services in 1907','Germany in 1918','Britain in 1943',
 'Alliance Française','British Council','family embassy','Geneva tea parties',
 'Tehran','Yalta','Kaiser','Foreign Affairs and Restructuring Act of 1999',
 'CIA','USAID','USIA','CNN','Al-Jazeera','Gulf War','G8',
 'Council of the European Union'],
 'rows':3,
 'side':10,
 'sections':5,
}}

def check_sources():
 for n,exp in expected.items():
  doc=BeautifulSoup((SRC/'chapters'/f'ch{n:02}.html').read_text(encoding='utf8'),'html.parser')
  assert doc.select_one('.chapter-source')['data-title']==exp['title']
  alltext=doc.get_text(' ',strip=True)
  missing=[v for v in exp['sentinels'] if v.lower() not in alltext.lower()]
  assert not missing, (n,missing)
  assert len(doc.select('.src-main table tbody tr'))==exp['rows']
  assert len(doc.select('.src-side > .block'))==exp['side']
  assert len(doc.select('.src-main [data-kind=section-head]'))==exp['sections']
  assert len(doc.select('.src-main [data-revision-start=true]'))==1
  assert len(doc.select('.src-side [data-revision-start=true]'))==1
  for side in doc.select('.src-side > .block'):
   assert side.get('data-for-section') and side.get('data-display')
  print(f'PASS: ch{n:02} — {len(exp["sentinels"])} source markers, {exp["rows"]} table rows, {exp["side"]} cards')


def browser():
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1365,'height':900})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(BOOK.read_text(encoding='utf8'),wait_until='load')
  for n in (4,5):
   chap=page.locator(f'#screenView #chapter-{n}')
   assert chap.locator('.banner h1').inner_text()==expected[n]['title']
   assert chap.locator('.side-flow > .block').count()==expected[n]['side']
   assert chap.locator('.main-flow [data-kind=concept]').count()==0
  page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
  page.emulate_media(media='print')
  assert [t for t in page.locator('#printView .hero-title').all_text_contents() if t in [expected[4]['title'],expected[5]['title']]]==[expected[4]['title'],expected[5]['title']]
  assert page.locator('#printView table.compare tbody tr').count()==page.locator('#chapterData table.compare tbody tr').count()
  assert not errors,errors
  browser.close()
  print('PASS: chapters 04–05 still appear on screen and in print; all active table rows preserved; zero JS errors')

if __name__=='__main__':
 check_sources(); browser()
