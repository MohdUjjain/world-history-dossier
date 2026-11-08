#!/usr/bin/env python3
"""Fail-fast provenance and editorial-fidelity checks for the 33-chapter dossier.

The numbered Drive briefings (04–32) are the authority for this editorial pass.
Chapters 00–03 have no matching documents in the supplied folder. This test
does not pretend to be an independent historical fact-check.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
from build import build, worker_for  # noqa: E402

FORBIDDEN = [
    (r"\bthe supplied (?:notes|briefing|text|account|source|article|study)\b",
     "Artificial source-generation label"),
    (r"\b(?:the source mistakenly|source checking|not independently verified)\b",
     "Editorial source-correction claim"),
    (r"\b(?:independently verify before publication|check the original academic "
     r"source|check this assignment against|those dates should be checked)\b",
     "Unrequested external-verification instruction"),
    (r"\b(?:the account portray|the account characterize|the account criticize|"
     r"the account illustrate|the account’s account)\b",
     "Broken grammar from source-label cleanup"),
]
NATURAL_SUPPLIED = {
    8: "Sarajevo supplied the trigger",
    12: "supplied the legal foundation for reparations",
    13: "supplied models later adopted by the United Nations",
    24: "supplied enduring language for anti-colonialism",
    25: "supplied fresh reasons to cooperate",
    28: "Stalin supplied weapons",
}

def main() -> None:
    modules = sorted((SRC / "chapters").glob("ch*.html"))
    assert len(modules) == 33, f"Expected 33 authored chapters; got {len(modules)}"
    observed = {}
    for n, path in enumerate(modules):
        assert path.name == f"ch{n:02d}.html", path.name
        content = path.read_text(encoding="utf-8")
        assert f'data-chapter="{n}"' in content[:250], path.name
        for expression, description in FORBIDDEN:
            match = re.search(expression, content, re.I)
            assert not match, f"{path.name}: {description}: {match.group() if match else ''}"
        assert not re.search(r"\bexplainer(?:s)?\b", content, re.I), (
            f"{path.name}: input-generation term 'explainer' in study prose")
        uses = re.findall(r"\bsupplied\b", content, re.I)
        plain = " ".join(re.sub(r"<[^>]+>", " ", content).split())
        if n in NATURAL_SUPPLIED:
            assert len(uses) == 1 and NATURAL_SUPPLIED[n] in plain, (
                f"{path.name}: review the ordinary historical use of 'supplied'")
            observed[n] = 1
        else:
            assert not uses, f"{path.name}: unreviewed use of 'supplied': {uses}"

    assert set(observed) == set(NATURAL_SUPPLIED), observed
    assert "August 1933" in (SRC / "chapters/ch15.html").read_text(), (
        "Historical source date silently overwritten; source correction must be separate")
    for n, words in {
        12: ("1936", "Article 231", "Ruhr"),
        13: ("Åland", "Vilna", "Nansen"),
        17: ("Adowa", "League of Nations"),
        23: ("50,000", "Reagan"),
        29: ("Gorbachev", "Vilnius"),
        32: ("500,000", "Madrid", "London"),
    }.items():
        content = (SRC / f"chapters/ch{n:02d}.html").read_text()
        for term in words:
            assert term in content, f"Reading {n:02d} missing substantive source content: {term}"

    paths = [SRC / "audits" / f"source-fidelity-pass-{n}.json"
             for n in range(1, 11)]
    corrections = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(payload.get("edits"), list) and payload["edits"], path
        for edit in payload["edits"]:
            assert int(edit["chapter"]) in range(33), (path, edit)
            assert edit["old"] != edit["new"], (path, edit)
            assert edit.get("reason"), (path, edit)
        corrections.extend(payload["edits"])
    assert len(corrections) >= 245, len(corrections)

    generated, numbers = build()
    assert [int(x) for x in numbers] == list(range(33)), numbers
    published = (ROOT / "index.html").read_text(encoding="utf-8")
    assert generated == published, "Publication HTML differs from chapter modules"
    expected_worker, _ = worker_for(generated)
    actual_worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
    assert expected_worker == actual_worker, "Offline edition hash is stale"

    print(f"PASS: all 33 modules, {len(corrections)} audited corrections, "
          "29 mapped source briefings, 6 legitimate 'supplied' verbs, "
          "publication and offline build parity")

if __name__ == "__main__":
    main()
