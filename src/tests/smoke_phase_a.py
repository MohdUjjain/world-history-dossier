#!/usr/bin/env python3
"""Phase A browser regressions: historical palette, anchor clearance and print reuse.

Run from the repo root: python src/tests/smoke_phase_a.py
Requires Playwright Chromium, installed by verify-pages.yml.
"""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from pathlib import Path
import json
import os

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def main() -> None:
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(Handler, directory=str(ROOT))
    )
    Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/"
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
            page.goto(url, wait_until="load")
            page.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")
            assert page.locator("#chapterData .chapter-source").count() == 33

            # The untouched historical hues remain the visual accents. Derive
            # accessible text on both parchment and the navy chapter banners.
            screen = page.evaluate("""() => {
              function rgb(s) {
                if (s.startsWith('#')) return [1,3,5].map(i => parseInt(s.slice(i,i+2),16));
                return [...s.matchAll(/[\\d.]+/g)].slice(0,3).map(x=>Number(x[0]));
              }
              function lum(s) {
                const v=rgb(s).map(n=>n/255).map(n=>
                  n<=.04045 ? n/12.92 : Math.pow((n+.055)/1.055,2.4));
                return v[0]*.2126+v[1]*.7152+v[2]*.0722;
              }
              function ratio(a,b) {
                const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);
              }
              const summary=[];
              for (let n=0;n<8;n++) {
                const ch=document.getElementById('chapter-'+n);
                const styles=getComputedStyle(ch);
                const accent=styles.getPropertyValue('--chapter-color').trim();
                const revision=ch.querySelector('.revision-flow');
                const revStyles=getComputedStyle(revision);
                const badge=getComputedStyle(revision.querySelector('.revision-badge'));
                const kicker=getComputedStyle(ch.querySelector('.banner .kicker'));
                const num=getComputedStyle(ch.querySelector('.main-flow h2 .num'));
                summary.push({
                  chapter:n,accent,revision:styles.getPropertyValue('--chapter-contrast').trim(),
                  revisionRole:revStyles.getPropertyValue('--chapter-color').trim(),
                  bodyText:ratio(num.color,'#ECE4CE'),
                  heroText:ratio(kicker.color,'#1B2A44'),
                  revisionBadge:ratio(badge.color,badge.backgroundColor)
                });
              }
              return summary;
            }""")
            assert len(screen) == 8
            for row in screen:
                assert row["revision"] == row["revisionRole"], row
                for field in ("bodyText", "heroText", "revisionBadge"):
                    assert row[field] >= 4.48, (field, row)

            # Section navigation must stop visibly below the sticky header.
            page.locator("#navTab").click()
            page.locator('.nav-chapter[data-chapter="2"] .nav-chapter-toggle').click()
            target_link = page.locator(
                '.nav-chapter[data-chapter="2"] .nav-section-link'
            ).first
            target_id = target_link.get_attribute("data-target")
            target_link.click()
            page.wait_for_timeout(120)
            clearance = page.evaluate("""id => ({
              heading:document.getElementById(id).getBoundingClientRect().top,
              header:document.querySelector('.site-header').getBoundingClientRect().bottom
            })""", target_id)
            assert clearance["heading"] >= clearance["header"] - 2, clearance

            # Use eight chapters: enough to check every identity pair without
            # the expense of repaginating the full 33-chapter book repeatedly.
            page.locator("#navTab").click()
            page.locator('#navToolsTab').click()
            page.locator("#navExportPanel summary").click()
            page.locator('#navToolsTab').click()
            if not page.locator('#navExportPanel').evaluate('(e)=>e.open'):
                page.locator('#navExportPanel summary').click()
            page.locator("#rangeInput").fill("0-7")
            page.evaluate("window.print=()=>{}")
            page.locator("#printBtn").click()
            assert page.locator("#printView .page.type-hero").count() == 8
            first = page.evaluate("""() => {
              window.__phaseAPrintNode=document.querySelector('#printView .page-slot');
              return window.__phaseAPrintNode !== null;
            }""")
            assert first
            unchanged = page.evaluate("""() => {
              window.dispatchEvent(new Event('beforeprint'));
              return window.__phaseAPrintNode ===
                document.querySelector('#printView .page-slot');
            }""")
            assert unchanged, "beforeprint unnecessarily rebuilt the same print tree"

            page.emulate_media(media="print")
            print_check = page.evaluate("""() => {
              const hex=val=>val.trim().toUpperCase();
              const rgb=s=>s.startsWith('#') ? [1,3,5].map(i=>parseInt(s.slice(i,i+2),16)):
                [...s.matchAll(/[\\d.]+/g)].slice(0,3).map(x=>Number(x[0]));
              const lum=s=>rgb(s).map(n=>n/255).map(n=>
                n<=.04045?n/12.92:Math.pow((n+.055)/1.055,2.4))
                .reduce((p,c,i)=>p+c*[.2126,.7152,.0722][i],0);
              const contrast=(a,b)=>{let x=lum(a),y=lum(b);
                return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
              const heroes=[...document.querySelectorAll('#printView .page.type-hero')];
              const revisions=[...document.querySelectorAll('#printView .page.is-revision')];
              const errors=[];
              heroes.forEach((pg,i)=>{
                const color=hex(getComputedStyle(pg).getPropertyValue('--chapter-color'));
                const thesis=getComputedStyle(pg.querySelector('.hero-thesis'));
                const dot=getComputedStyle(pg.querySelector('.hero-ribbon .yr-pt'),'::before');
                const kicker=getComputedStyle(pg.querySelector('.hero-kicker'));
                if (hex(color)!==hex(getComputedStyle(document.querySelector('#chapter-'+i))
                      .getPropertyValue('--chapter-color'))) errors.push('chapter hue '+i);
                if (thesis.borderLeftColor!==dot.backgroundColor) errors.push('hero marker '+i);
                if (contrast(kicker.color,'#1B2A44')<4.48) errors.push('hero kicker '+i);
              });
              revisions.forEach(pg=>{
                const st=getComputedStyle(pg);
                const h=getComputedStyle(pg.querySelector('.page-header-bar'));
                const label=getComputedStyle(pg.querySelector('.page-header-bar .h-chap'));
                if(st.backgroundColor !== 'rgb(246, 241, 228)') errors.push('revision page CSS');
                if(contrast(h.backgroundColor,label.color)<4.48) errors.push('revision header contrast');
                if(st.getPropertyValue('--chapter-ink').trim() !==
                   st.getPropertyValue('--chapter-contrast-ink').trim()) errors.push('revision ink role');
                if(st.getPropertyValue('--chapter-color').trim() !==
                   st.getPropertyValue('--chapter-contrast').trim()) errors.push('revision accent role');
              });
              const overflows=[...document.querySelectorAll('#printView .page .col-main,#printView .page .col-side')]
                .filter(el=>el.scrollHeight-el.clientHeight>2).length;
              return {heroes:heroes.length,revisions:revisions.length,errors,overflows};
            }""")
            assert print_check["heroes"] == 8, print_check
            assert print_check["revisions"] >= 8, print_check
            assert not print_check["errors"], print_check
            assert print_check["overflows"] == 0, print_check

            # A real input change, unlike a duplicate beforeprint, must rebuild.
            page.emulate_media(media="screen")
            page.locator("#navTab").click()
            page.locator('#navToolsTab').click()
            page.locator("#includeRevisionChk").uncheck()
            changed = page.evaluate("""() => {
              const old=document.querySelector('#printView .page-slot');
              window.dispatchEvent(new Event('beforeprint'));
              return old!==document.querySelector('#printView .page-slot');
            }""")
            assert changed, "revision change reused a stale print tree"
            assert page.locator("#printView .page.is-revision").count() == 0
            assert not errors, errors
            browser.close()
            print(json.dumps({
                "chapters": 33,
                "palettePairsChecked": len(screen),
                "printHeroes": print_check["heroes"],
                "printRevisionPages": print_check["revisions"],
                "anchorClearance": clearance,
                "duplicateBuildAvoided": unchanged,
                "rebuildAfterRevisionChange": changed,
                "pageErrors": errors,
            }, indent=2))
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
