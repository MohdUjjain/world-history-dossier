#!/usr/bin/env python3
"""Chapters 06 and 07: ensure historic notes content and Sidebar V2 markup survive assembly.
Source claims are intentionally not checked against outside sources.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
SRC=Path(__file__).resolve().parents[1]
BOOK=SRC.parent/'book.html'
EXPECT={
6: {
 'title':'The Triple Alliance', 'sections':5, 'rows':25, 'side':13,
 'terms':['Bismarck','Franco-Prussian War','Congress of Berlin','Big Bulgaria',
          'revanchisme','Dual Alliance','Dreikaiserbund','Reinsurance Treaty',
          'Triplice','Tunisia','casus foederis','Bülow','Weltpolitik',
          'Italia irredenta','Mürzsteg Convention','1902','1904','1897','1912',
          'Archduke Franz Ferdinand','neutrality in August 1914','1915',
          'Hohenzollern','Habsburg','coalition'],
},
7: {
 'title':'The Ententes, 1894–1914', 'sections':7,'rows':11,'side':11,
 'terms':['Congress of Vienna','Franco-Russian Alliance','1894','1861 and 1914',
          'capital','Russia','splendid isolation','Risk Fleet','Tirpitz','Dreadnought',
          'Fashoda Crisis','Sino-Japanese War','Anglo-Japanese Alliance',
          'Entente Cordiale','Delcassé','Lansdowne','Anglo-Russian Convention',
          'Persia','Afghanistan','Tibet','Edward Grey','Liberal Imperialist',
          '1905','1908','1911','Agadir','Morocco','Bosnia','July 1914',
          'August 1914','lesser of two evils','German attacks'],
}}

def sources():
    for n,exp in EXPECT.items():
        soup=BeautifulSoup((SRC/'chapters'/f'ch{n:02}.html').read_text(encoding='utf-8'),'html.parser')
        assert soup.select_one('.chapter-source')['data-title']==exp['title']
        txt=soup.get_text(' ',strip=True)
        missing=[t for t in exp['terms'] if t.casefold() not in txt.casefold()]
        assert not missing,(n,missing)
        assert len(soup.select('.src-main [data-section-key]'))==exp['sections']
        assert len(soup.select('.src-main tbody tr'))==exp['rows']
        assert len(soup.select('.src-side > .block'))==exp['side']
        if n == 6:
            buttons = soup.select('.src-main .glossary-term')
            glossary_rows = soup.select('.src-main .glossary-revision tbody tr')
            assert len(buttons) == len(glossary_rows) == 15
            assert len(set(b.get_text(' ', strip=True).casefold() for b in buttons)) == 15
        assert len(soup.select('.src-side [data-revision-start=true]'))==1
        assert len(soup.select('.src-main [data-revision-start=true]'))==1
        keys={x['data-section-key'] for x in soup.select('.src-main [data-section-key]')}
        kinds=set()
        for card in soup.select('.src-side > .block'):
            assert card['data-for-section'] in keys
            assert card.has_attr('data-display')
            kinds.add(card['data-kind'])
        assert len(kinds)>=5
        print(f'Ch{n:02} — {len(exp["terms"])} source markers; {exp["rows"]} rows; {exp["side"]} aids; {len(kinds)} purposes')

def browser():
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':900})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(BOOK.read_text(encoding='utf-8'),wait_until='load')
        assert [page.locator(f'#screenView #chapter-{n} .banner h1').inner_text() for n in (6,7)]==[EXPECT[6]['title'],EXPECT[7]['title']]
        for n in (6,7):
            ch=page.locator(f'#screenView #chapter-{n}')
            assert ch.locator('.side-flow > .block').count()==EXPECT[n]['side']
            assert ch.locator('.main-flow .box.learning-card').count()==0
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        page.emulate_media(media='print')
        assert all(title in page.locator('#printView .hero-title').all_text_contents() for title in [EXPECT[6]['title'],EXPECT[7]['title']])
        assert page.locator('#printView table tbody tr').count()==page.locator('#chapterData table tbody tr').count()
        assert not errors, errors
        browser.close()
        print('PASS: new chapters, correct section-side learning aids, PDF table rows intact')

if __name__=='__main__': sources();browser()
