#!/usr/bin/env python3
"""Coverage and browser checks for the two new source-based chapters.
Preserves source claims without independent external historical verification.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
SRC=Path(__file__).resolve().parents[1]
BOOK=SRC.parent/'book.html'
CASES={
 8:{'title':'The July Crisis','sections':6,'rows':34,'side':12,
    'terms':['Agadir','Joffre','Poincaré','136,000','Balkan League','Albania','Berchtold','Pašić','Apis',
      'Princip','Grabež','Čabrinović','28 June','5–6 July','blank cheque','48-hour','30 July',
      'general mobilization','Belgium','August','Harvest Leave','Plan B','Fischer','Versailles','advertent',
      'Austria-Hungary','France','Britain','Serbia','Russia']},
 9:{'title':'Wartime Promises and Postwar Europe','sections':7,'rows':11,'side':11,
    'terms':['Clausewitz','Lloyd George','Article 231','1960s','1970s','Balfour','Kitchener',
      'Alsace-Lorraine','1790','Saarland','Rhineland','Salonika','Constantinople','Bosphorus',
      'Polish buffer','Bethmann Hollweg','September Memorandum','Mitteleuropa','Vassal',
      'Fritz Fischer','Brest-Litovsk','90%','50%','Trentino','South Tyrol','Istria','Dalmatia',
      'Macedonian','Bucharest','Transylvania','Bukovina','Banat','1917','Bolshevik','self-determination',
      'Woodrow Wilson','associated','1918','Straits Agreement']}}

def main():
 for n,x in CASES.items():
  doc=BeautifulSoup((SRC/'chapters'/f'ch{n:02}.html').read_text(), 'html.parser')
  txt=doc.get_text(' ',strip=True)
  missed=[s for s in x['terms'] if s.casefold() not in txt.casefold()]
  assert not missed,(n,missed)
  assert doc.select_one('.chapter-source')['data-title']==x['title']
  assert len(doc.select('.src-main [data-section-key]'))==x['sections']
  assert len(doc.select('.src-main tbody tr'))==x['rows']
  assert len(doc.select('.src-side > .block'))==x['side']
  if n==8:
   assert doc.select_one('.chapter-source')['data-author']=='Samuel R. Williamson Jr.'
   assert len(doc.select('.src-main .glossary-term'))==22
   assert len(doc.select('.src-main .glossary-revision tbody tr'))==22
   assert len(set(b.get_text(' ',strip=True).casefold() for b in doc.select('.src-main .glossary-term')))==22
   assert '24 July' in txt and '30 July' in txt and 'no hard evidence' in txt.lower()
   assert 'chief' in txt.lower() or 'paramount' in txt.lower()
  assert len(doc.select('.src-main [data-revision-start=true]'))==1
  assert len(doc.select('.src-side [data-revision-start=true]'))==1
  keys={s['data-section-key'] for s in doc.select('.src-main [data-section-key]')}
  kind=set();displays=set()
  for b in doc.select('.src-side > .block'):
   assert b['data-for-section'] in keys
   kind.add(b['data-kind']);displays.add(b['data-display'])
  assert len(kind)>=5 and len(displays)>=5
  print(f'Ch{n:02}: {len(x["terms"])} markers, {x["sections"]} sections, {x["rows"]} table rows, {x["side"]} varied aids')
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':900})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(BOOK.read_text(),wait_until='load')
  for n,x in CASES.items():
   assert page.locator(f'#screenView #chapter-{n} .banner h1').inner_text()==x['title']
   assert page.locator(f'#screenView #chapter-{n} .side-flow > .block').count()==x['side']
  page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
  page.emulate_media(media='print')
  assert page.locator('#printView .hero-title').all_text_contents()[8:10]==[CASES[8]['title'],CASES[9]['title']]
  assert page.locator('#printView table tbody tr').count()==page.locator('#chapterData table tbody tr').count()
  assert not errors,errors
  browser.close()
 print('PASS: 08–09 source coverage and export contracts')
if __name__=='__main__':main()
