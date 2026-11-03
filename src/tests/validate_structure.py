#!/usr/bin/env python3
"""Basic static checks for incoming replacement chapter sources.\n\nRun: python3 src/tests/validate_structure.py\nIntentionally accepts zero chapters while the new notes are being supplied.\n"""
from pathlib import Path
import json
import html
import re
import sys
from html.parser import HTMLParser

SRC = Path(__file__).resolve().parents[1]
CHAPTERS = SRC / 'chapters'
CATALOG = {int(row['number']): row['title'] for row in json.loads((SRC / 'chapter_catalog.json').read_text(encoding='utf8'))}
assert set(CATALOG) == set(range(33)), 'The complete chapter catalogue must contain 00–32'

class ChapterTags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def main():
    sources = sorted(CHAPTERS.glob('ch*.html'))
    errors = []
    warnings = []
    seen = set()
    if not sources:
        print('OK: 0 active chapters; awaiting replacement notes')
        return 0
    for fn in sources:
        text = fn.read_text(encoding='utf8')
        parser = ChapterTags(); parser.feed(text)
        sources_list = [a for tag, a in parser.tags if tag == 'div' and 'chapter-source' in a.get('class','').split()]
        if len(sources_list) != 1:
            errors.append(f'{fn.name}: expected exactly one chapter-source root, got {len(sources_list)}')
            continue
        a = sources_list[0]
        num = a.get('data-chapter','')
        if not num.isdecimal():
            errors.append(f'{fn.name}: invalid data-chapter={num!r}')
            continue
        if int(num) in seen:
            errors.append(f'{fn.name}: duplicate chapter {num}')
        seen.add(int(num))
        if fn.name != f'ch{int(num):02}.html':
            errors.append(f'{fn.name}: filename must be ch{int(num):02}.html')
        if not a.get('data-title'):
            errors.append(f'{fn.name}: title is blank')
        official_title = CATALOG.get(int(num))
        if official_title is None:
            errors.append(f'{fn.name}: chapter {num} is not in the 00–32 catalogue')
        elif a.get('data-title') != official_title:
            errors.append(f'{fn.name}: data-title must equal official chapter title: {official_title!r}')
        hero_h1 = re.search(r'<h1 class="ht">([^<]+)</h1>', text)
        if not hero_h1 or html.unescape(hero_h1.group(1)) != official_title:
            errors.append(f'{fn.name}: hero H1 must equal the official chapter title')
        kicker = re.search(r'<span class="hk">([^<]+)</span>', text)
        if not kicker or f'Chapter {int(num):02d}' not in kicker.group(1):
            errors.append(f'{fn.name}: hero kicker must identify Chapter {int(num):02d}')
        classes = [a2.get('class','').split() for tag,a2 in parser.tags if tag == 'div']
        for section in ('src-hero','src-main','src-side'):
            if sum(section in c for c in classes)!=1:
                errors.append(f'{fn.name}: expected exactly one .{section}')
        if not any('hthesis' in c for c in classes):
            warnings.append(f'{fn.name}: no .hthesis found; hero rendering expects it')
        # Authoring warning only; JS normalization routes these safely to the side.
        main_markup = text.split('<div class="src-main">', 1)[1].split('<div class="src-side">', 1)[0]
        if 'data-kind="concept"' in main_markup:
            warnings.append(f'{fn.name}: verify all concept blocks are authored in .src-side (automatic fallback exists)')
        print(f'Checked {fn.name}: chapter {num}, {a.get("data-title")}')
    for msg in warnings: print('WARNING:',msg)
    for msg in errors: print('ERROR:',msg)
    print(f'Result: {len(sources)} active chapter(s), {len(errors)} errors, {len(warnings)} warnings')
    return 1 if errors else 0

if __name__=='__main__':
    sys.exit(main())
