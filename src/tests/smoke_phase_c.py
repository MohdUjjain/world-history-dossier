#!/usr/bin/env python3
"""Phase C regression: reading rhythm, mobile tables and full PDF publication.

Run from repository root with Playwright Chromium:
    python src/tests/smoke_phase_c.py
"""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import os

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "20th-Century International History.pdf"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    assert PDF.read_bytes().startswith(b"%PDF"), "Full bookmarked PDF is missing"
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT))
    )
    Thread(target=server.serve_forever, daemon=True).start()
    errors = []
    try:
        with sync_playwright() as playwright:
            options = {"headless": True, "args": ["--no-sandbox"]}
            if os.environ.get("CHROMIUM_BIN"):
                options["executable_path"] = os.environ["CHROMIUM_BIN"]
            browser = playwright.chromium.launch(**options)
            page = browser.new_page(
                viewport={"width": 1360, "height": 850},
                reduced_motion="reduce",
            )
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="load")
            page.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")

            assert page.locator("#chapterData .chapter-source").count() == 33
            assert page.locator("#titlePage .tp-pdf-link").count() == 1
            assert page.locator("#navExportPanel .nav-pdf-access a").count() == 1
            pdf_links = page.locator('a[href$="20th-Century%20International%20History.pdf"]')
            assert pdf_links.count() == 2, pdf_links.count()  # <noscript> is raw text with JS enabled
            assert page.locator(
                'head link[rel="alternate"][type="application/pdf"]'
            ).get_attribute("href") == "./20th-Century%20International%20History.pdf"
            for link in pdf_links.all():
                assert link.get_attribute("href") == (
                    "./20th-Century%20International%20History.pdf"
                )

            pairing = page.evaluate("""() => {
              const rows=[...document.querySelectorAll('#screenView .section-pair')];
              const vacant=rows.filter(x=>x.classList.contains('no-side'));
              const cards=[...document.querySelectorAll('#screenView .side-flow > .block[data-for-section]')];
              const misplaced=cards.filter(x=>
                x.getAttribute('data-for-section') !==
                x.closest('.section-pair').getAttribute('data-section-pair'));
              return {
                rows:rows.length, vacant:vacant.length,cards:cards.length,
                misplaced:misplaced.length,
                hiddenEmptyRail:vacant.every(x=>
                  getComputedStyle(x.querySelector('.side-flow')).display==='none'),
                widenedRow:vacant.every(x=>getComputedStyle(x).gridTemplateColumns.split(' ').length===1),
                readerGap:getComputedStyle(document.documentElement)
                  .getPropertyValue('--reader-column-gap').trim()
              };
            }""")
            assert pairing["rows"] > 150, pairing
            assert pairing["vacant"] > 0, pairing
            assert pairing["cards"] > 50, pairing
            assert pairing["misplaced"] == 0, pairing
            assert pairing["hiddenEmptyRail"] and pairing["widenedRow"], pairing

            # Browser-generated PDF samples the real 16:9 print system.
            page.locator("#navTab").click()
            page.locator("#navExportPanel summary").click()
            page.locator("#rangeInput").fill("0,1")
            page.evaluate("window.print=()=>{}")
            page.locator("#printBtn").click()
            assert page.locator("#printView .page.type-hero").count() == 2
            page.emulate_media(media="print")
            print_report = page.evaluate("""() => {
              const cover=document.getElementById('titlePage');
              const pdf=document.querySelector('#printView .page.type-title');
              const fields=['series','title','subtitle','desc','imprint'];
              const copies=fields.map(x=>({
                field:x,
                same:cover.querySelector('.tp-'+x).textContent.trim()===
                    pdf.querySelector('.pt-'+x).textContent.trim()
              }));
              const rect=pdf.querySelector('.pt-inner').getBoundingClientRect();
              const pageRect=pdf.getBoundingClientRect();
              const footers=[...document.querySelectorAll('#printView .page-footer-bar')];
              return {
                fields:copies,
                coverFits:rect.top >= pageRect.top-1 && rect.bottom <= pageRect.bottom+1,
                footers:footers.length,
                names:footers.map(x=>x.querySelector('span').textContent.trim()),
                slots:document.querySelectorAll('#printView .page-slot').length
              };
            }""")
            assert all(x["same"] for x in print_report["fields"]), print_report
            assert print_report["coverFits"], print_report
            assert print_report["footers"] >= 4, print_report
            assert all(x == "World History Dossier" for x in print_report["names"]), print_report

            page.emulate_media(media="screen")
            # Mobile comparison tables show actual horizontal scroll (not a
            # table forced to microscopic columns), with a keyboard-usable region.
            mobile_report = []
            for width in (390, 320):
                page.set_viewport_size({"width": width, "height": 800})
                page.wait_for_timeout(75)
                report = page.evaluate("""() => {
                  const tables=[...document.querySelectorAll('#screenView .table-wrap')];
                  const wide=tables.filter(x=>x.scrollWidth>x.clientWidth+2);
                  const attributed=tables.filter(x=>x.getAttribute('role')==='region');
                  const bad=attributed.filter(x=>
                    x.tabIndex!==0 || !x.getAttribute('aria-label') ||
                    !x.getAttribute('aria-describedby') ||
                    !document.getElementById(x.getAttribute('aria-describedby')));
                  const stale=tables.filter(x=>
                    x.scrollWidth<=x.clientWidth+2 && x.hasAttribute('tabindex'));
                  let scrollable=wide.length>0;
                  if(wide.length){
                    const scroller=wide[0];
                    scroller.scrollLeft=0; // prior viewport may leave it scrolled
                    scroller.scrollLeft=90;
                    scrollable=scroller.scrollLeft>0;
                  }
                  return {innerWidth:innerWidth,documentWidth:document.documentElement.scrollWidth,
                    count:tables.length,wide:wide.length,attributed:attributed.length,
                    bad:bad.length,stale:stale.length,scrollable,
                    visibleHints:document.querySelectorAll('.table-scroll-hint').length};
                }""")
                assert report["documentWidth"] <= width+1, report
                assert report["count"] > 4 and report["wide"] > 0, report
                assert report["wide"] == report["attributed"] == report["visibleHints"], report
                assert report["bad"] == report["stale"] == 0, report
                assert report["scrollable"], report
                mobile_report.append(report)

            page.emulate_media(media="print")
            page_size = page.evaluate("""() => {
              const first=document.querySelector('#printView .page');
              const st=getComputedStyle(first);
              const columns=[...document.querySelectorAll('#printView .col-main,#printView .col-side')];
              return {width:st.width,height:st.height,
                overflow:columns.filter(c=>c.scrollHeight-c.clientHeight>2).length,
                screenHidden:getComputedStyle(document.querySelector('#screenView')).display==='none',
                extraPrintHints:document.querySelectorAll('#printView .table-scroll-hint').length};
            }""")
            assert page_size["width"] == "1280px" and page_size["height"] == "720px", page_size
            assert page_size["overflow"] == 0 and page_size["extraPrintHints"] == 0, page_size
            assert page_size["screenHidden"], page_size
            assert not errors, errors
            browser.close()
            print(json.dumps({
                "chapters": 33,
                "pdfAccess": True,
                "sectionPairs": pairing,
                "publication": print_report,
                "mobileTables": mobile_report,
                "printGeometry": page_size,
                "javascriptErrors": errors,
            }, indent=2))
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
