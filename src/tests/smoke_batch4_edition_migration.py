#!/usr/bin/env python3
"""Batch D: source-edition reordering, inserted section, saved checkpoint and revision reflow."""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
KEY='whd-reading-place-v1'
HTML=(ROOT/'index.html').read_text(encoding='utf8')
point=HTML.index('var PAGE_W=1280')
at=HTML.rfind('<script',0,point)
assert at>0,'No insertion point before the History print and screen engine'
MUTATION=r"""<script>
(function(){
 const source=document.querySelector('#chapterData .chapter-source[data-chapter="16"]'),
   main=source?.querySelector('.src-main');
 if(!main)throw Error('No authored chapter 16 source');
 const heads=[...main.querySelectorAll(':scope > .block[data-kind="section-head"]')];
 const saved=heads.find(x=>x.getAttribute('data-section-key')==='s3');
 const first=heads.find(x=>x.getAttribute('data-section-key')==='s1');
 if(!saved||!first)throw Error('Stable source section keys missing');
 const before=heads.indexOf(saved);
 const chunk=[];
 for(let n=saved;n&&(n===saved||n.getAttribute('data-kind')!=='section-head');n=n.nextElementSibling)
   chunk.push(n);
 chunk.forEach(n=>main.insertBefore(n,first));
 const added=document.createElement('div');
 added.className='block';added.setAttribute('data-kind','section-head');
 added.setAttribute('data-keep','together');
 added.setAttribute('data-section-key','new-interlude');
 added.setAttribute('data-title','سياق جديد — New contextual interpretation');
 added.innerHTML='<h2 lang="ar" dir="rtl">سياق جديد — New contextual interpretation</h2>';
 main.insertBefore(added,first);
 const p=document.createElement('div');
 p.className='block';p.setAttribute('data-kind','p');p.setAttribute('data-keep','together');
 p.innerHTML='<p>Fresh analysis newly inserted before the original chapter sections.</p>';
 main.insertBefore(p,first);
 window.__batchD={before,after:[...main.querySelectorAll(':scope > .block[data-kind="section-head"]')].indexOf(saved),
   chunk:chunk.length,inserted:!!main.querySelector('[data-section-key="new-interlude"]')};
})();
</script>"""
ALTERED=HTML[:at]+MUTATION+HTML[at:]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*_):pass

def main():
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
 Thread(target=server.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
   url=f'http://127.0.0.1:{server.server_port}/index.html'
   def open_edition(saved,width):
    ctx=browser.new_context(viewport={'width':width,'height':844},reduced_motion='reduce',service_workers='block')
    ctx.add_init_script(script=f"localStorage.setItem({json.dumps(KEY)},{json.dumps(json.dumps(saved))});")
    ctx.route('**/index.html',lambda route:route.fulfill(status=200,content_type='text/html',body=ALTERED))
    page=ctx.new_page();page.goto(url,wait_until='load')
    page.locator('#navToc .nav-chapter-link').first.wait_for(state='attached')
    result=page.evaluate('window.__batchD')
    assert result and result['inserted'] and result['before']!=result['after'] and result['chunk']>=2,result
    assert page.locator('#whd-sec-16-new-interlude[lang="ar"][dir="rtl"]').count()==1 or page.locator('#whd-sec-16-new-interlude h2[lang="ar"][dir="rtl"]').count()==1
    assert page.evaluate('key=>JSON.parse(localStorage.getItem(key))',KEY)==saved
    page.locator('#resumeReaderPrompt').wait_for(state='visible',timeout=8000)
    return ctx,page

   for width in (390,1360):
    checkpoint={'chapter':'16','section':'whd-sec-16-s3','chapterRatio':.46,
                'sectionRatio':.25,'savedAt':1730000000000}
    ctx,page=open_edition(checkpoint,width)
    assert page.locator('#whd-sec-16-s3').count()==1
    page.locator('#resumeReaderContinue').click()
    page.wait_for_function('() => scrollY>100')
    loc=page.evaluate("""() => {
      const h=document.getElementById('whd-sec-16-s3'),ch=document.getElementById('chapter-16'),
        all=[...ch.querySelectorAll('[data-kind="section-head"]')],i=all.indexOf(h),
        n=all[i+1],start=h.getBoundingClientRect().top+scrollY,
        end=n?n.getBoundingClientRect().top+scrollY:ch.getBoundingClientRect().bottom+scrollY;
      return {index:i,actual:scrollY,expected:Math.max(0,start+.25*Math.max(0,end-start)-innerHeight*.25),
        chapter:ch.id};
    }""")
    assert loc['chapter']=='chapter-16' and loc['index']!=2,loc
    assert abs(loc['actual']-loc['expected'])<90,loc
    assert page.evaluate('key=>JSON.parse(localStorage.getItem(key)).section',KEY)=='whd-sec-16-s3'
    # History's checkbox is a per-session setting. Live rebuilds must retain
    # the reading viewport and must not rewrite the pre-existing chapter bookmark.
    page.locator('#navTab').click()
    page.locator('#navExportPanel summary').click()
    page.locator('#includeRevisionChk').uncheck()
    assert page.locator('#chapter-16 .revision-flow').count()==0
    assert page.evaluate('key=>JSON.parse(localStorage.getItem(key)).chapter',KEY)=='16'
    page.locator('#includeRevisionChk').check()
    assert page.locator('#chapter-16 .revision-flow').count()==1
    assert page.locator('#whd-sec-16-s3').count()==1
    page.locator('#navClose').click()
    bounds=page.locator('#chapter-16').bounding_box()
    assert bounds and bounds['y']<844 and bounds['y']+bounds['height']>0,bounds
    ctx.close()

    missing={'chapter':'16','section':'whd-old-edition-deleted','chapterRatio':.58,
             'sectionRatio':.35,'savedAt':1730000000000}
    ctx,page=open_edition(missing,width)
    page.locator('#resumeReaderContinue').click()
    page.wait_for_function('() => scrollY>100')
    loc=page.evaluate("""() => {
      const r=document.getElementById('chapter-16').getBoundingClientRect();
      return {actual:scrollY,expected:Math.max(0,r.top+scrollY+.58*r.height-innerHeight*.25)};
    }""")
    assert abs(loc['actual']-loc['expected'])<90,loc
    assert page.evaluate('key=>JSON.parse(localStorage.getItem(key)).section',KEY)=='whd-old-edition-deleted'
    ctx.close()
   browser.close()
 finally:
  server.shutdown();server.server_close()
 print('PASS Batch D World History: moved source blocks with stable section keys, inserted bilingual heading, old deleted section fallback, revision reflow and chapter-relative restoration')

if __name__=='__main__':main()
