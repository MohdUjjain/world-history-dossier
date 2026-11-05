#!/usr/bin/env python3
"""Release gate for living CSS/JS references, test inventory and local links.

    python src/tests/verify_docs_sync.py
    python src/tests/verify_docs_sync.py --base origin/main
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
RELEASE_DOC = "src/docs/release/RELEASE_VERIFICATION.md"
STYLE_DOC = "src/CSS_DOC.md"
SCRIPT_DOC = "src/JS_DOC.md"
SCRIPT_SOURCES = {"src/engine.js", "src/reader-ui.js", "src/offline-reader.js"}
REQUIRED_FILES = (
    "src/styles.css", "src/engine.js", "src/reader-ui.js",
    STYLE_DOC, SCRIPT_DOC, RELEASE_DOC,
    "src/tests/verify_docs_sync.py", "src/tests/smoke_release_browser.py",
    "src/tests/smoke_release_offline.py", "src/tests/smoke_release_ranges.py",
    "src/tests/inspect_pdf_release.py",
    ".github/workflows/verify-pages.yml",
)


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def verify_links(path: str) -> int:
    source = text(path)
    count = 0
    for destination in re.findall(r"!?(?:\[[^\]]*\])\(([^)]+)\)", source):
        dest = destination.split(" ", 1)[0].strip("<>")
        if not dest or dest.startswith("#"):
            continue
        parsed = urlsplit(dest)
        if parsed.scheme or parsed.netloc or dest.startswith("/"):
            continue
        target = (ROOT / path).parent / unquote(parsed.path)
        if not target.exists():
            raise AssertionError(f"{path}: broken local link {destination!r}")
        count += 1
    return count


def changed_from(base: str) -> set[str]:
    # Fail visibly for unavailable refs rather than silently skipping a check.
    cmd = ["git", "-C", str(ROOT), "diff", "--name-only", f"{base}...HEAD"]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return set(result.stdout.splitlines())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", help="Git base ref for source-and-doc change coupling")
    args = ap.parse_args()
    for path in REQUIRED_FILES:
        assert (ROOT / path).is_file(), f"Release reference missing: {path}"

    css = text("src/styles.css")
    engine = text("src/engine.js")
    reader = text("src/reader-ui.js")
    css_docs = text(STYLE_DOC)
    js_docs = text(SCRIPT_DOC)
    release = text(RELEASE_DOC)
    workflow = text(".github/workflows/verify-pages.yml")

    css_roles = (
        "--reader-anchor-clearance", "--reader-aside-width",
        "--reader-column-gap", ".section-pair.no-side",
        ".table-scroll-hint", "--chapter-contrast-surface",
    )
    for marker in css_roles:
        assert marker in css and marker in css_docs, (
            f"CSS rule or documentation missing: {marker}"
        )

    js_roles = (
        "whd:screen-will-render", "whd:screen-rendered",
        "updateScreenTableAffordances", "appendPairedSections",
        "lastPrintSignature",
    )
    for marker in js_roles:
        assert marker in engine and marker in js_docs, (
            f"Engine rule or documentation missing: {marker}"
        )
    assert "closeDrawer(" in reader and "closeDrawer()" in js_docs
    assert "MutationObserver" not in reader, "Legacy TOC observer returned"

    tests = (
        "smoke_reader_ui.py", "smoke_phase_a.py",
        "smoke_reader_interactions.py", "smoke_phase_c.py",
        "smoke_release_browser.py", "smoke_release_accessibility.py",
        "smoke_release_offline.py",
        "smoke_release_ranges.py", "verify_docs_sync.py",
        "inspect_pdf_release.py",
    )
    for test in tests:
        assert test in workflow or test == "inspect_pdf_release.py", (
            f"Verification workflow is not exercising {test}"
        )
        assert test in release, f"Release runbook omitted {test}"

    checked_links = sum(
        verify_links(path) for path in (RELEASE_DOC, "src/docs/README.md")
    )
    if args.base:
        changes = changed_from(args.base)
        if "src/styles.css" in changes:
            assert STYLE_DOC in changes, "CSS changed without CSS_DOC.md update"
        if changes.intersection(SCRIPT_SOURCES):
            assert SCRIPT_DOC in changes, "JS changed without JS_DOC.md update"
        if changes.intersection({
            ".github/workflows/verify-pages.yml",
            ".github/workflows/build-bookmarked-pdf.yml",
        }):
            assert RELEASE_DOC in changes, (
                "Release CI changed without updating the release runbook"
            )
        print(f"PASS: documentation change coupling across {len(changes)} changed files")
    print(f"PASS: CSS/JS re-entry markers, {len(tests)} test references, "
          f"{checked_links} local documentation links")


if __name__ == "__main__":
    main()
