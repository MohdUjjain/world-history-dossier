#!/usr/bin/env python3
"""Export the assembled World History Dossier to a true 16:9 PDF in safe batches.

Uses the book's *own JavaScript pagination engine* to construct the exact
# printView used by the in-browser Export command. Saves that DOM, prints it
in small Chromium batches, merges the pages and reconstructs clickable TOC
links to pages across batch boundaries. No JS or CSS production changes.

Requires: playwright, beautifulsoup4, PyMuPDF (fitz), local Chromium.
Typical use:
  python src/build.py
  python src/tools/export_full_pdf.py --chromium /usr/bin/chromium
  python src/tools/export_full_pdf.py --batch-size 16 --out my-book.pdf

Note: The resulting PDF has clickable page destinations but does not contain
native PDF outline/bookmark objects. The HTML's dynamic export control is
unchanged. Always visually inspect representative pages after exporting.
"""
from __future__ import annotations
import argparse
import json
import re
import tempfile
from pathlib import Path

import fitz
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SRC = Path(__file__).resolve().parents[1]
ROOT = SRC.parent


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--book', type=Path, default=ROOT / 'book.html')
    ap.add_argument('--out', type=Path, default=ROOT / 'book.pdf')
    ap.add_argument('--batch-size', type=int, default=20)
    ap.add_argument('--chromium', type=str, default='/usr/bin/chromium')
    ap.add_argument('--qa', type=Path, default=ROOT / 'PDF_MERGE_QA.json')
    args = ap.parse_args()
    if args.batch_size < 1:
        ap.error('--batch-size must be positive')

    css = (SRC / 'styles.css').read_text(encoding='utf8')
    book = args.book.read_text(encoding='utf8')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.chromium,
                                     args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.set_content(book, wait_until='load')
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        # Record counts on the engine's actual original 1280x720 print page DOM.
        report = page.evaluate('''() => {
          const q=s=>[...document.querySelectorAll(s)];
          const cols=q('#printView .col-main,#printView .col-side,#printView .col-full');
          const over=cols.filter(x=>x.scrollHeight-x.clientHeight>2);
          return {chapters:q('#chapterData .chapter-source').length,
            pageCount:q('#printView .page').length,
            heroes:q('#printView .hero-title').map(x=>x.textContent.trim()),
            revisions:q('#printView .page.is-revision').length,
            tableRows:q('#printView table tbody tr').length,
            sidebarItems:q('#printView .col-side > .block').length,
            overflowColumns:over.length}
        }''')
        if errors or report['overflowColumns']:
            raise RuntimeError(f'Print DOM errors: {errors}; overflow: {report}')
        # #printView is hidden in screen media, so capture link geometry in print mode.
        page.emulate_media(media='print')
        links = page.evaluate('''() => [...document.querySelectorAll('#printView .page-slot')]
        .flatMap((slot,i)=>{let b=slot.querySelector('.page').getBoundingClientRect();
          return [...slot.querySelectorAll('a[href^="#pg-"]')].map(a=>{
            let r=a.getBoundingClientRect();return {
              from:i,to:Number(a.getAttribute('href').slice(4))-1,
              box:[r.left-b.left,r.top-b.top,r.right-b.left,r.bottom-b.top]
            }})})''')
        body = page.locator('#printView').inner_html()
        page.close()
        snapshot = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>' + css + '</style></head><body><div id="printView">' + body + '</div></body></html>'
        soup = BeautifulSoup(snapshot, 'lxml')
        slots = soup.select('#printView > .page-slot')
        if len(slots) != report['pageCount']:
            raise RuntimeError('Print snapshot page count differs from engine count')
        if any(not (0<=x['from']<len(slots) and 0<=x['to']<len(slots)) for x in links):
            raise RuntimeError('Invalid TOC destination in print DOM')
        with tempfile.TemporaryDirectory(prefix='whd_pdf_') as temp:
            temp = Path(temp)
            pdfs = []
            for start in range(0, len(slots), args.batch_size):
                end = min(start+args.batch_size, len(slots))
                html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>' + css + '</style></head><body><div id="printView">' + ''.join(map(str, slots[start:end])) + '</div></body></html>'
                p = browser.new_page(viewport={'width': 1440, 'height': 900})
                p.emulate_media(media='print')
                p.set_content(html, wait_until='load')
                dest = temp / f'part_{start:04}.pdf'
                p.pdf(path=str(dest), print_background=True, prefer_css_page_size=True)
                p.close()
                with fitz.open(dest) as chunk:
                    if len(chunk) != end-start:
                        raise RuntimeError(f'Chunk pages mismatch: {start}:{end} -> {len(chunk)}')
                pdfs.append(dest)
                print(f'Printed pages {start+1}–{end} of {len(slots)}', flush=True)
            browser.close()
            out = fitz.open()
            for part in pdfs:
                with fitz.open(part) as chunk:
                    out.insert_pdf(chunk, links=False, annots=False)
            if len(out) != len(slots):
                raise RuntimeError('Merged page count mismatch')
            linked=0
            for l in links:
                x0,y0,x1,y1=l['box']
                rect=fitz.Rect(max(0, x0*.75),max(0,y0*.75),min(960,x1*.75),min(540,y1*.75))
                if rect.is_empty or rect.width<=1 or rect.height<=1:
                    continue
                out[l['from']].insert_link({'kind':fitz.LINK_GOTO,
                                            'from':rect,'page':l['to'],'to':fitz.Point(0,0)})
                linked+=1
            out.set_metadata({'title':'World History Dossier',
                              'author':'Mohammed Husain Ujjainwala',
                              'subject':'Twentieth-Century International History study notes'})
            args.out.parent.mkdir(parents=True,exist_ok=True)
            out.save(args.out, garbage=1, deflate=True)
            out.close()
    with fitz.open(args.out) as finished:
        report['pdfPages']=len(finished)
        report['pdfLinks']=sum(len(p.get_links()) for p in finished)
        report['landscape169']=all(abs(p.rect.width-960)<1 and abs(p.rect.height-540)<1 for p in finished)
        if not report['landscape169'] or report['pdfPages'] != report['pageCount']:
            raise RuntimeError(f'PDF validation failed: {report}')
        if report['pdfLinks'] < linked:
            raise RuntimeError('Some TOC links lost during merge')
    args.qa.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    print('PASS',json.dumps(report,ensure_ascii=False),flush=True)

if __name__ == '__main__':
    main()
