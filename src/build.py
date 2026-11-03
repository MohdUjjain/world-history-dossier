#!/usr/bin/env python3
"""
Build script for the World History Dossier.

Assembles the final, single-file book.html from:
  shell.html          — the page skeleton (head, header, nav panel, body
                         containers). Contains two placeholder markers:
                         /*__STYLES__*/ and /*__SCRIPT__*/, plus
                         <!--__CHAPTERS__--> inside #chapterData.
  styles.css          — all CSS, injected verbatim into shell's <style> block.
  engine.js           — all JS (pagination engine, screen renderer, nav
                         panel, export logic), injected into shell's <script>.
  chapters/chNN.html  — one file per chapter, each containing exactly one
                         <div class="chapter-source" data-chapter="NN" ...>
                         block. Concatenated in filename (=chapter number)
                         order and injected at <!--__CHAPTERS__-->.

Usage:
    python3 build.py                # writes ../book.html
    python3 build.py -o out.html    # writes to a custom path
    python3 build.py --check        # builds, then diffs against ../book.html
                                     # and reports whether they match (useful
                                     # after manually editing book.html to
                                     # confirm the split sources stay in sync)

Adding a new chapter: drop a new chapters/chNN.html (same
<div class="chapter-source" ...> format as the others — see any
existing file for the block-authoring convention) and rerun this script.
Nothing else needs to change; chapters are discovered automatically and
ordered by the numeric part of the filename, not by array position.
"""
import argparse
import glob
import os
import re
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def build():
    shell = read(os.path.join(SRC_DIR, 'shell.html'))
    css = read(os.path.join(SRC_DIR, 'styles.css')).strip('\n')
    js = read(os.path.join(SRC_DIR, 'engine.js')).strip('\n')

    chapter_files = sorted(
        glob.glob(os.path.join(SRC_DIR, 'chapters', 'ch*.html')),
        key=lambda p: int(re.search(r'ch(\d+)\.html$', p).group(1))
    )
    if not chapter_files:
        print('INFO: no active chapter files yet — ready for replacement notes', file=sys.stderr)

    chapter_blocks = []
    seen_numbers = []
    for cf in chapter_files:
        content = read(cf).rstrip('\n')
        m = re.search(r'data-chapter="(\d+)"', content[:200])
        if not m:
            print(f'WARNING: {cf} has no data-chapter attribute near its start — skipping', file=sys.stderr)
            continue
        num = m.group(1)
        if num in seen_numbers:
            print(f'WARNING: duplicate data-chapter="{num}" ({cf}) — check for a copy/paste mistake', file=sys.stderr)
        seen_numbers.append(num)
        expected_name = f'ch{int(num):02d}.html'
        actual_name = os.path.basename(cf)
        if actual_name != expected_name:
            print(f'WARNING: {actual_name} contains data-chapter="{num}" — filename should be {expected_name}', file=sys.stderr)
        chapter_blocks.append(content)

    chapters_html = '\n\n'.join(chapter_blocks)

    out = shell.replace('/*__STYLES__*/', css)
    out = out.replace('/*__SCRIPT__*/', js)
    out = out.replace('<!--__CHAPTERS__-->', chapters_html)

    return out, seen_numbers


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('-o', '--output', default=os.path.join(SRC_DIR, '..', 'book.html'),
                     help='Output path for the assembled file (default: ../book.html)')
    ap.add_argument('--check', action='store_true',
                     help="Build, then diff against the output path's existing content instead of overwriting it")
    args = ap.parse_args()

    html, chapter_numbers = build()
    print(f'Assembled {len(chapter_numbers)} chapter(s): {", ".join(chapter_numbers)}')
    print(f'Final size: {len(html):,} chars')

    if args.check:
        existing = read(args.output) if os.path.exists(args.output) else None
        if existing == html:
            print(f'MATCH — {args.output} is byte-identical to a fresh build.')
        else:
            print(f'DIFFERS — {args.output} does not match a fresh build from src/.')
            print('(This is expected if book.html was hand-edited since the last build —')
            print(' port those edits back into src/ and rebuild, so src/ stays the source of truth.)')
        return

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
