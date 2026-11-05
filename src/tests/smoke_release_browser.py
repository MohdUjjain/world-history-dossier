#!/usr/bin/env python3
"""Responsive smoke and controlled screenshot comparisons against the base book.

    python src/tests/smoke_release_browser.py --baseline /tmp/base-index.html
    python src/tests/smoke_release_browser.py --out /tmp/screenshots
"""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import os
from urllib.parse import urlsplit

from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
VIEWPORTS = ((1440, 900), (1024, 768), (768, 1024),
             (390, 844), (320, 720))
MAX_CHANGED_FRACTION = 0.035
PIXEL_TOLERANCE = 25


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def diff_images(old: Path, new: Path, output: Path) -> float:
    with Image.open(old) as img_a, Image.open(new) as img_b:
        a, b = img_a.convert("RGB"), img_b.convert("RGB")
        if a.size != b.size:
            return 1.0
        raw = ImageChops.difference(a, b).convert("L")
        binary = raw.point(lambda value: 255 if value >= PIXEL_TOLERANCE else 0)
        fraction = ImageStat.Stat(binary).mean[0] / 255
        # Make unexpected changes easy to inspect from the CI artifact.
        if fraction > 0.001:
            binary.convert("RGB").save(output)
        return round(fraction, 6)


def capture(browser, url: str, out: Path, baseline: Path | None):
    context = browser.new_context(reduced_motion="reduce", service_workers="block",
                                  viewport={"width": 1440, "height": 900})
    if baseline:
        body = baseline.read_text(encoding="utf-8")
        def route_document(route):
            path = urlsplit(route.request.url).path
            if route.request.resource_type == "document" and (
                path.endswith("/") or path.endswith("/index.html")
            ):
                route.fulfill(status=200, content_type="text/html; charset=utf-8",
                              body=body)
            else:
                route.continue_()
        context.route("**/*", route_document)

    page = context.new_page()
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(url, wait_until="load")
    page.locator("#navToc .nav-chapter-link").first.wait_for(state="attached")
    page.evaluate("() => document.fonts.ready.then(() => true)")
    checks = []
    out.mkdir(parents=True, exist_ok=True)

    def screenshot(name: str):
        page.screenshot(path=str(out / (name + ".png")),
                        animations="disabled", caret="hide")

    for width, height in VIEWPORTS:
        page.set_viewport_size({"width": width, "height": height})
        page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
        page.wait_for_timeout(100)
        dimensions = page.evaluate("""() => ({
            viewport:innerWidth, scrollWidth:document.documentElement.scrollWidth,
            chapters:document.querySelectorAll('#screenView .chapter-flow').length,
            navWidth:document.querySelector('#navPanel').getBoundingClientRect().width
        })""")
        assert dimensions["chapters"] == 33, dimensions
        assert dimensions["scrollWidth"] <= dimensions["viewport"] + 1, (
            width, dimensions)
        prefix = str(width)
        screenshot(prefix + "-cover")

        page.evaluate("""() => document.getElementById('chapter-12')
            .scrollIntoView({block:'start',behavior:'instant'})""")
        page.wait_for_timeout(170)
        assert page.locator("#currentChapterLabel").is_visible()
        assert "Ch.12" in page.locator("#currentChapterLabel").inner_text()
        screenshot(prefix + "-chapter")

        page.locator("#navTab").click()
        page.wait_for_timeout(70)
        assert page.locator("#navPanel").get_attribute("aria-hidden") == "false"
        assert page.evaluate("document.activeElement.id") == "navClose"
        screenshot(prefix + "-drawer")
        page.keyboard.press("Escape")
        assert page.locator("#navPanel").get_attribute("aria-hidden") == "true"
        if width <= 390:
            # A real horizontal comparison is keyboard/touch scrollable.
            page.evaluate("""() => {
                const el=[...document.querySelectorAll('#screenView .table-wrap')]
                  .find(x=>x.scrollWidth>x.clientWidth+2);
                if(!el) throw new Error('No wide comparison available');
                el.scrollIntoView({block:'center',behavior:'instant'});
                el.scrollLeft=0;
            }""")
            page.wait_for_timeout(100)
            screenshot(prefix + "-table")
        checks.append({"width":width,"height":height,
                       "scrollWidth":dimensions["scrollWidth"]})
    assert not errors, errors
    context.close()
    return checks


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline", type=Path,
                    help="Assembled index.html from trusted main at the PR base")
    ap.add_argument("--out", type=Path, default=ROOT / ".release-evidence" / "screens")
    ap.add_argument("--allow-visual-change", action="store_true",
                    help="Only for a documented, manually reviewed intentional redesign")
    args = ap.parse_args()
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/"
    try:
        with sync_playwright() as playwright:
            options = {"headless":True, "args":["--no-sandbox", "--disable-dev-shm-usage"]}
            if os.environ.get("CHROMIUM_BIN"):
                options["executable_path"] = os.environ["CHROMIUM_BIN"]
            browser = playwright.chromium.launch(**options)
            new_dir = args.out / "candidate"
            checks = capture(browser, url, new_dir, None)
            comparisons = []
            if args.baseline:
                old_dir = args.out / "baseline"
                capture(browser, url, old_dir, args.baseline)
                diff_dir = args.out / "diff"
                diff_dir.mkdir(parents=True, exist_ok=True)
                for candidate in sorted(new_dir.glob("*.png")):
                    fraction = diff_images(
                        old_dir / candidate.name, candidate,
                        diff_dir / candidate.name)
                    comparisons.append({"view":candidate.name,"changedPixels":fraction})
            browser.close()
            report = {"responsive":checks, "screenshots":len(list(new_dir.glob("*.png"))),
                      "baseline":str(args.baseline) if args.baseline else None,
                      "comparisons":comparisons,
                      "threshold":MAX_CHANGED_FRACTION,
                      "manualApproval":args.allow_visual_change}
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "visual-report.json").write_text(json.dumps(report,indent=2))
            print(json.dumps(report,indent=2))
            failures = [x for x in comparisons
                        if x["changedPixels"] > MAX_CHANGED_FRACTION]
            if failures and not args.allow_visual_change:
                raise AssertionError(
                    "Unreviewed visual delta (see baseline/candidate/diff artifacts): "
                    + str(failures))
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
