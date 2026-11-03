#!/usr/bin/env python3
"""Validate final full-PDF printed chapter index and native two-level bookmarks.

    python src/tests/validate_pdf_navigation.py "20th-Century International History.pdf"
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz

SRC = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path, help='Full-length batch-exported PDF to verify')
    args = parser.parse_args()
    chapters = json.loads((SRC / 'chapter_catalog.json').read_text(encoding='utf-8'))
    labels = [c['title'] for c in chapters]
    with fitz.open(args.pdf) as doc:
        toc = doc.get_toc()
        top = [e for e in toc if e[0] == 1]
        sub = [e for e in toc if e[0] == 2]
        assert len(top) == len(labels) == 33, (len(top), len(labels))
        assert len(sub) > 100, len(sub)
        assert all(entry[2] > 0 and entry[2] <= len(doc) for entry in toc)
        assert [entry[1].split(' · ', 1)[-1] for entry in top] == labels

        # Page 1 is a title. Only the pages before the first chapter hero
        # count as the chapter-only printed contents section.
        index_end = top[0][2] - 1
        assert 1 <= index_end <= 5, index_end
        index_pages = [doc[i] for i in range(1, index_end)]
        links = [link for page in index_pages for link in page.get_links()]
        assert len(links) == 33, len(links)
        assert all(link['kind'] == fitz.LINK_GOTO for link in links)
        assert [link['page'] + 1 for link in links] == [entry[2] for entry in top]
        assert all(abs(page.rect.width - 960) < 1 and abs(page.rect.height - 540) < 1 for page in doc)
        assert doc.xref_get_key(doc.pdf_catalog(), 'PageMode')[1] == '/UseOutlines'

        print(json.dumps({
            'pages': len(doc),
            'printedContentsPages': len(index_pages),
            'clickableChapterLinks': len(links),
            'chapterBookmarks': len(top),
            'sectionBookmarks': len(sub),
            'pageMode': 'UseOutlines',
            'pdf': str(args.pdf),
        }, indent=2))
    print('PASS — chapter-only printed contents, clickable targets, native bookmark hierarchy')


if __name__ == '__main__':
    main()
