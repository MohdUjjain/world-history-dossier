#!/usr/bin/env python3
"""Inspect every 16:9 PDF page; render and compare representative pages.

    python src/tests/inspect_pdf_release.py candidate.pdf \
      --reference '20th-Century International History.pdf' --out /tmp/pdf-evidence

Unchanged releases should render pixel-identically to the committed edition.
A legitimately changed PDF requires review of the contact sheet and diff
artifact; never replace that review with a blanket threshold increase.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz
from PIL import Image, ImageChops, ImageDraw, ImageStat


EXPECTED_RATIO = 16 / 9
PIXEL_TOLERANCE = 26
MAX_CHANGED_FRACTION = 0.08


def render(page: fitz.Page) -> Image.Image:
    pm = page.get_pixmap(matrix=fitz.Matrix(.72, .72),
                         colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


def sample_pages(doc: fitz.Document) -> list[int]:
    chapter_pages=[item[2]-1 for item in doc.get_toc()
                   if item[0] == 1]
    assert len(chapter_pages) == 33, len(chapter_pages)
    sample={0,1,len(doc)-1,len(doc)//2,
            chapter_pages[0],chapter_pages[16],chapter_pages[-1],
            max(0,len(doc)//4),max(0,3*len(doc)//4)}
    return sorted(x for x in sample if x < len(doc))


def contact_sheet(images: list[tuple[str, Image.Image]], output: Path):
    if not images:
        return
    w,h=images[0][1].size
    columns=3
    rows=(len(images)+columns-1)//columns
    sheet=Image.new("RGB",(w*columns,(h+30)*rows),"#ede5d4")
    draw=ImageDraw.Draw(sheet)
    for i,(caption,img) in enumerate(images):
        x=(i%columns)*w
        y=(i//columns)*(h+30)
        draw.text((x+10,y+7),caption,fill="#1b2a44")
        sheet.paste(img,(x,y+30))
    sheet.save(output)


def compare(left: Image.Image, right: Image.Image, file: Path) -> float:
    if left.size != right.size:
        return 1.0
    diff=ImageChops.difference(left,right).convert("L")
    mask=diff.point(lambda v:255 if v>=PIXEL_TOLERANCE else 0)
    fraction=ImageStat.Stat(mask).mean[0]/255
    if fraction>.001:
        mask.convert("RGB").save(file)
    return round(fraction,6)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("pdf",type=Path)
    p.add_argument("--reference",type=Path)
    p.add_argument("--out",type=Path,default=Path(".release-evidence/pdf"))
    p.add_argument("--allow-visual-change",action="store_true")
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    screenshots=[]
    mismatches=[]
    clipped=[]
    blank=[]
    with fitz.open(args.pdf) as doc:
        assert not doc.is_encrypted, "A downloadable study PDF must not be encrypted"
        assert len(doc) >= 200, f"Unexpected page loss: {len(doc)}"
        chapters=[x for x in doc.get_toc() if x[0]==1]
        sections=[x for x in doc.get_toc() if x[0]==2]
        assert len(chapters)==33 and len(sections)>=200
        for i,page in enumerate(doc):
            rect=page.rect
            assert abs(rect.width/rect.height-EXPECTED_RATIO)<.003, (
                i+1,rect)
            text=page.get_text("text").strip()
            if len(text)<12:
                blank.append({"page":i+1,"characters":len(text)})
            for word in page.get_text("words"):
                x0,y0,x1,y1=word[:4]
                # PyMuPDF bounding boxes can overhang the edge by a couple
                # of points due to font ascenders; 6pt is an explicit buffer.
                if x0 < -6 or y0 < -6 or x1 > rect.width+6 or y1 > rect.height+6:
                    clipped.append({"page":i+1,"word":word[4],
                                    "bounds":[x0,y0,x1,y1]})
                    if len(clipped)>15:
                        break
        assert not blank, f"Blank/suspiciously empty PDF pages: {blank[:10]}"
        assert not clipped, f"Text outside the page trim: {clipped[:10]}"

        samples=sample_pages(doc)
        reference=None
        if args.reference:
            reference=fitz.open(args.reference)
            assert len(reference)==len(doc), (
                "The PDF page count differs from the committed edition",
                len(reference),len(doc))
        for i in samples:
            img=render(doc[i])
            name=f"page-{i+1:03d}"
            img.save(args.out/(name+".png"))
            screenshots.append((f"Candidate p.{i+1}",img))
            if reference is not None:
                old=render(reference[i])
                old.save(args.out/(name+"-reference.png"))
                change=compare(old,img,args.out/(name+"-diff.png"))
                mismatches.append({"page":i+1,"changedPixels":change})
        if reference is not None:
            reference.close()
        contact_sheet(screenshots,args.out/"pdf-contact-sheet.png")
        report={
          "pages":len(doc),"chapters":len(chapters),
          "sectionBookmarks":len(sections),"ratio":EXPECTED_RATIO,
          "samples":[i+1 for i in samples],
          "blankPages":blank,"offPageWords":clipped,
          "visualComparisons":mismatches,
          "maxChangedFraction":MAX_CHANGED_FRACTION,
          "manuallyApproved":args.allow_visual_change,
        }
        (args.out/"pdf-report.json").write_text(json.dumps(report,indent=2))
        print(json.dumps(report,indent=2))
        changed=[m for m in mismatches
                 if m["changedPixels"]>MAX_CHANGED_FRACTION]
        if changed and not args.allow_visual_change:
            raise AssertionError(
                "PDF snapshot change requires visual review: "+str(changed))


if __name__=="__main__":
    main()
