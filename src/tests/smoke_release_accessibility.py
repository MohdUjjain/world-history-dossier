#!/usr/bin/env python3
"""Axe-core WCAG 2.0/2.1 AA auditing on representative reader surfaces."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import os

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
AXE = ROOT / "node_modules" / "axe-core" / "axe.min.js"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def audit(page, selector, label):
    result = page.evaluate("""async selector => {
      const root=document.querySelector(selector);
      if (!root) throw new Error('Missing accessibility scope: '+selector);
      const options = {
        runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']},
        resultTypes:['violations']
      };
      const result=await axe.run(root,options);
      return result.violations.map(v=>({
        id:v.id, impact:v.impact, help:v.help,
        nodes:v.nodes.slice(0,5).map(x=>({
          target:x.target, failureSummary:x.failureSummary
        }))
      }));
    }""", selector)
    severe = [v for v in result if v["impact"] in ("serious", "critical")]
    return {"scope":label,"selector":selector,"violations":result,
            "blocking":severe}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path,
                    default=ROOT / ".release-evidence" / "accessibility.json")
    args=ap.parse_args()
    assert AXE.is_file(), (
        "Install pinned axe-core first: npm install --no-save axe-core@4.10.3")
    server=ThreadingHTTPServer(
        ("127.0.0.1",0),partial(QuietHandler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    errors,results=[],[]
    try:
        with sync_playwright() as playwright:
            options={"headless":True,"args":["--no-sandbox"]}
            if os.environ.get("CHROMIUM_BIN"):
                options["executable_path"]=os.environ["CHROMIUM_BIN"]
            browser=playwright.chromium.launch(**options)
            context=browser.new_context(viewport={"width":1360,"height":850},
                                        reduced_motion="reduce",
                                        service_workers="block")
            page=context.new_page()
            page.on("pageerror",lambda error:errors.append(str(error)))
            page.goto(f"http://127.0.0.1:{server.server_port}/",wait_until="load")
            page.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")
            page.add_script_tag(path=str(AXE))
            assert page.evaluate("document.documentElement.lang") == "en"
            assert page.locator("main#screenView").count() == 1

            results.append(audit(page,"#titlePage","cover"))
            results.append(audit(page,
                "#screenView > .chapter-flow:first-of-type","chapter-00"))
            page.locator("#navTab").click()
            results.append(audit(page,"#navPanel","open-contents-drawer"))
            page.keyboard.press("Escape")

            page.set_viewport_size({"width":390,"height":844})
            page.locator("#navTab").click()
            results.append(audit(page,"#navPanel","mobile-contents-drawer"))
            page.keyboard.press("Escape")
            assert not errors, errors
            args.out.parent.mkdir(parents=True,exist_ok=True)
            report={"axeVersion":page.evaluate("axe.version"),
                    "audits":results,"browserErrors":errors}
            args.out.write_text(json.dumps(report,indent=2),encoding="utf-8")
            print(json.dumps({
                "axeVersion":report["axeVersion"],
                "scopes":[{"scope":x["scope"],
                           "violations":len(x["violations"]),
                           "blocking":len(x["blocking"])}
                          for x in results],
                "browserErrors":errors},indent=2))
            blocking=[{"scope":r["scope"],"violations":r["blocking"]}
                      for r in results if r["blocking"]]
            browser.close()
            if blocking:
                raise AssertionError(
                    "Serious or critical WCAG findings; see accessibility.json: "
                    + json.dumps(blocking)[:2400])
    finally:
        server.shutdown()


if __name__=="__main__":
    main()
