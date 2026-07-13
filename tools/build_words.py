#!/usr/bin/env python3
"""Regenerate the WORDS array in index.html from the app's words.json.

The landing page's live word card embeds a curated sample of real entries.
words.json stays the single source of truth; curate the sample by editing
CURATED below, then run:

    python tools/build_words.py [path-to-words.json]

Default words.json path assumes the app repo sits next to this one.
"""
import io
import json
import re
import sys
from pathlib import Path

# The curated sample, in rotation order. Every entry must exist in words.json
# and must have a quote (the card always shows one).
CURATED = [
    "halcyon",
    "serendipity",
    "magnanimous",
    "baleful",
    "acquiesce",
    "perfidious",
    "corroborate",
    "thrive",
    "bumptious",
    "culpable",
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

    entries = []
    for name in CURATED:
        x = by_word.get(name)
        assert x is not None, f"{name!r} not found in {words_path}"
        assert x.get("quote"), f"{name!r} has no quote - every card needs one"
        assert x["partOfSpeech"] in POS_ABBR, f"{name!r}: unhandled part of speech"
        entries.append({
            "word": x["word"], "pos": x["partOfSpeech"], "pron": x["pronunciation"],
            "def": x["definition"], "quote": x["quote"], "author": x.get("quoteAuthor", ""),
        })

    js = json.dumps(entries, ensure_ascii=False, indent=1)
    for key in ("word", "pos", "pron", "def", "quote", "author"):
        js = js.replace(f'"{key}":', f"{key}:")

    html = io.open(index_path, encoding="utf-8").read()
    new_html, n = re.subn(
        r"(// WORDS:BEGIN[^\n]*\n)const WORDS = \[.*?\];\n(// WORDS:END)",
        lambda m: m.group(1) + "const WORDS = " + js + ";\n" + m.group(2),
        html, count=1, flags=re.S)
    assert n == 1, "WORDS markers not found in index.html"
    io.open(index_path, "w", encoding="utf-8", newline="\n").write(new_html)
    print(f"wrote {len(entries)} entries to {index_path}")

if __name__ == "__main__":
    main()
