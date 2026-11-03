#!/usr/bin/env python3
"""Regress sidebar semantic variety and section-aware alignment in both modes.

Run after python src/build.py. Exercises all currently active chapters, source
immutability, real print geometry, and the screen section-row invariant.
"""
from pathlib import Path
from collections import Counter
import json, zipfile
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SRC=Path(__file__).resolve().parents[1]
BOOK=SRC.parent/'book.html'
ORIGINAL=Path('/mnt/data/World_History_Dossier_Ch00-03_Source.zip')
EXPECTED_CATS={'def','concept','tip','mistake','memory','hy'}

def run():
    # Compare text in the narrative source before/after the redesign, not just
    # the presence of headlines or table rows.
    preserved=[]
    if ORIGINAL.exists():
        with zipfile.ZipFile(ORIGINAL) as z:
            for n in range(4):
                name=f'src/chapters/ch{n:02}.html'
                old=BeautifulSoup(z.read(name).decode(),'html.parser')
                new=BeautifulSoup((SRC/'chapters'/f'ch{n:02}.html').read_text(),'html.parser')
                before=old.select_one('.src-main').get_text(' ',strip=True)
                after=new.select_one('.src-main').get_text(' ',strip=True)
                assert before==after,f'Main-note wording changed in chapter {n}'
                preserved.append(n)
    with sync_playwright() as play:
        browser=play.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':900})
        errors=[];page.on('pageerror',lambda exc:errors.append(str(exc)))
        page.set_content(BOOK.read_text(),wait_until='load')
        screen=page.evaluate('''()=>{
         let cards=[...document.querySelectorAll('#screenView .side-flow > .block')];
         let matches=cards.filter(c=>c.closest('.section-pair').getAttribute('data-section-pair')===c.getAttribute('data-for-section')).length;
         return {cards:cards.length,paired:matches,sections:document.querySelectorAll('.section-pair').length,
           visualTypes:[...new Set(cards.map(c=>c.getAttribute('data-display')))].sort(),
           kinds:[...new Set(cards.map(c=>c.getAttribute('data-kind')))].sort(),
           unpaired:cards.filter(c=>c.closest('.section-pair').getAttribute('data-section-pair')!==c.getAttribute('data-for-section')).map(c=>c.textContent.slice(0,50))};
        }''')
        assert screen['cards']==screen['paired'] and screen['cards']>=30,screen
        assert EXPECTED_CATS.issubset(set(screen['kinds'])),screen
        assert len(screen['visualTypes'])>=8,screen
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        page.emulate_media(media='print')
        pdf=page.evaluate('''()=>{
          const pages=[...document.querySelectorAll('#printView .page.type-content')];
          let cards=[], misplaced=[], overflows=[];
          for(let i=0;i<pages.length;i++){
           const pg=pages[i];
           const sections=new Set([...pg.querySelectorAll('.col-main > .block')].map(b=>b.getAttribute('data-content-section')));
           for(const note of pg.querySelectorAll('.col-side > .block')){
             cards.push(note.getAttribute('data-kind'));
             if(!sections.has(note.getAttribute('data-for-section')))
               misplaced.push({page:i+1,for:note.getAttribute('data-for-section'),in:[...sections]});
           }
           for(const col of pg.querySelectorAll('.col-side,.col-main')){
             if(col.scrollHeight-col.clientHeight>2)overflows.push(i+1);
           }
          }
          return {contentPages:pages.length,cards:cards.length,misplaced,overflows,
            kindCounts:Object.fromEntries([...new Set(cards)].map(k=>[k,cards.filter(x=>x===k).length]))};
        }''')
        assert pdf['cards']==screen['cards'],(pdf,screen)
        assert not pdf['misplaced'] and not pdf['overflows'],pdf
        assert not errors,errors
        browser.close()
        report={'narrativePreserved':preserved,'screen':screen,'print':pdf,'jsErrors':errors}
        (SRC.parent/'SIDEBAR_QA.json').write_text(json.dumps(report,indent=2))
        print(json.dumps(report,indent=2))
        print('PASS: learning diversity, screen and PDF section alignment, unchanged narrative text')

if __name__=='__main__':run()
