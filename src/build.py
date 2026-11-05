#!/usr/bin/env python3
"""Build the modular World History Dossier and its content-hashed offline worker.

    python src/build.py                  # legacy standalone book.html
    python src/build.py -o index.html    # publish HTML + service-worker.js
    python src/build.py -o index.html --check  # strict reproducibility check
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import os
import re
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
ROOT = SRC_DIR.parent

# These publication assets are small; the large pre-rendered PDF is deliberately
# excluded from offline precaching and from edition/cache hash calculation.
ASSETS = (
    "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png",
    "og-image.jpg", "404.html", "sitemap.xml", "robots.txt",
    "src/service-worker.template.js",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build() -> tuple[str, list[str]]:
    shell = read(SRC_DIR / "shell.html")
    css = read(SRC_DIR / "styles.css").strip("\n")
    js = read(SRC_DIR / "engine.js").strip("\n")
    offline = read(SRC_DIR / "offline-reader.js").strip("\n")

    chapter_files = sorted(
        glob.glob(str(SRC_DIR / "chapters" / "ch*.html")),
        key=lambda path: int(re.search(r"ch(\d+)\.html$", path).group(1)),
    )
    if not chapter_files:
        print("INFO: no active chapter files", file=sys.stderr)
    chapter_blocks = []
    seen_numbers = []
    for filename in chapter_files:
        content = read(Path(filename)).rstrip("\n")
        match = re.search(r'data-chapter="(\d+)"', content[:200])
        if not match:
            print(f"WARNING: {filename} missing data-chapter near start", file=sys.stderr)
            continue
        chapter_id = match.group(1)
        if chapter_id in seen_numbers:
            print(f"WARNING: duplicate chapter {chapter_id}", file=sys.stderr)
        if Path(filename).name != f"ch{int(chapter_id):02}.html":
            print(f"WARNING: chapter filename mismatch: {filename}", file=sys.stderr)
        seen_numbers.append(chapter_id)
        chapter_blocks.append(content)

    values = {
        "/*__STYLES__*/": css,
        "/*__SCRIPT__*/": js,
        "/*__OFFLINE_READER__*/": offline,
        "<!--__CHAPTERS__-->": "\n\n".join(chapter_blocks),
    }
    for marker in values:
        if shell.count(marker) != 1:
            raise ValueError(f"Expected exactly one {marker} in src/shell.html")
    out = shell
    for marker, content in values.items():
        out = out.replace(marker, content)
    return out, seen_numbers


def worker_for(html: str) -> tuple[str, str]:
    # Git-blob hashing makes every resource's identity explicit. A change in
    # any published asset updates the cache without a manual version bump.
    def blob_sha(data: bytes) -> str:
        raw = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
        return hashlib.sha1(raw).hexdigest()

    items = [("index.html", blob_sha(html.encode("utf-8")))] + [
        (path, blob_sha((ROOT / path).read_bytes())) for path in ASSETS
    ]
    seed = "".join(f"{name}={sha}\n" for name, sha in items)
    revision = hashlib.sha256(seed.encode("ascii")).hexdigest()[:12]
    template = read(SRC_DIR / "service-worker.template.js")
    if template.count("__REVISION__") != 1:
        raise ValueError("Expected exactly one __REVISION__ in worker template")
    return template.replace("__REVISION__", revision), revision


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", type=Path, default=ROOT / "book.html")
    parser.add_argument("--check", action="store_true",
                        help="Compare generated files with the published files; nonzero exit if stale")
    args = parser.parse_args()
    try:
        html, chapters = build()
        target = args.output.resolve()
        is_publication = target == (ROOT / "index.html").resolve()
        outputs = {target: html}
        version = None
        if is_publication:
            worker, version = worker_for(html)
            outputs[(ROOT / "service-worker.js").resolve()] = worker
        for path, content in outputs.items():
            if args.check:
                if not path.is_file() or read(path) != content:
                    print(f"STALE or missing: {path.relative_to(ROOT)}", file=sys.stderr)
                    return 1
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        mode = "VERIFIED" if args.check else "BUILT"
        print(f"{mode}: {len(chapters)} chapters; " +
              ", ".join(str(path.relative_to(ROOT)) for path in outputs) +
              (f"; offline revision {version}" if version else ""))
        return 0
    except (OSError, ValueError) as exc:
        print(f"Build error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
