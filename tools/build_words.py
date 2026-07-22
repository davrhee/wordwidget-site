#!/usr/bin/env python3
"""Regenerate the SETS array in index.html from the app's words.json.

The landing page's live word card embeds a curated sample of real entries,
grouped into sets of 3. The visible set rotates every 12 hours; three dots let
the visitor switch cards within the current set. words.json stays the single
source of truth; curate the sample by editing SETS below, then run:

    python tools/build_words.py [path-to-words.json]

Default words.json path assumes the app repo sits next to this one.
"""
import io
import json
import re
import sys
from pathlib import Path

# The curated sample, grouped into sets of 3. Every entry must exist in
# words.json and must have a quote (the card always shows one). Keep the total
# unique-word count within the ~15-word exposure ceiling (see wordwidget-site memo).
SETS = [
    ["deter", "ennui", "palimpsest"],
    ["fragile", "eloquent", "sanctimonious"],
    ["eschew", "harbinger", "apotheosis"],
    ["sanguine", "squander", "inscrutable"],
]

POS_ABBR = {"adjective", "noun", "verb", "adverb"}  # card JS abbreviates these

def main():
    root = Path(__file__).resolve().parent.parent
    words_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        root.parent / "wordwidget" / "wordwidget" / "words.json")
    index_path = root / "index.html"

    data = json.loads(words_path.read_text(encoding="utf-8"))
    data = data["words"] if isinstance(data, dict) else data
    by_word = {x["word"]: x for x in data}

    sets = []
    for group in SETS:
        assert len(group) == 3, f"each set needs exactly 3 words: {group}"
        entries = []
        for name in group:
            x = by_word.get(name)
            assert x is not None, f"{name!r} not found in {words_path}"
            assert x.get("quote"), f"{name!r} has no quote - every card needs one"
            assert x["partOfSpeech"] in POS_ABBR, f"{name!r}: unhandled part of speech"
            entries.append({
                "word": x["word"], "pos": x["partOfSpeech"], "pron": x["pronunciation"],
                "def": x["definition"], "quote": x["quote"], "author": x.get("quoteAuthor", ""),
            })
        sets.append(entries)

    js = json.dumps(sets, ensure_ascii=False, indent=1)
    for key in ("word", "pos", "pron", "def", "quote", "author"):
        js = js.replace(f'"{key}":', f"{key}:")

    html = io.open(index_path, encoding="utf-8").read()
    new_html, n = re.subn(
        r"(// SETS:BEGIN[^\n]*\n)const SETS = \[.*?\];\n(// SETS:END)",
        lambda m: m.group(1) + "const SETS = " + js + ";\n" + m.group(2),
        html, count=1, flags=re.S)
    assert n == 1, "SETS markers not found in index.html"
    io.open(index_path, "w", encoding="utf-8", newline="\n").write(new_html)
    total = sum(len(s) for s in sets)
    print(f"wrote {len(sets)} sets ({total} cards) to {index_path}")

if __name__ == "__main__":
    main()
