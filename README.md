# wordwidget-site

Landing page for WordWidget, a light-touch word-a-day vocabulary app for iOS.
Plain static HTML/CSS/JS, no build step, hosted on GitHub Pages.

## Files

- `index.html` - the landing page. The word card is live: it rotates through a
  curated sample of real app entries on the app's own slot schedule
  (4am / 12pm / 8pm local).
- `privacy.html` - privacy policy (required for App Store submission).
- `phone.html` - dev tool: renders index.html in an iPhone-sized frame. Not
  linked from the site.
- `tools/build_words.py` - regenerates the card's word sample from the app's
  `words.json`. Curate the sample by editing `CURATED` in that script, then run
  `python tools/build_words.py`. Never hand-edit the WORDS array in index.html.

## Editing notes

- Headline verb synonyms: `const VERBS` in index.html.
- Screenshots: drop into `images/` and wire into the three "Explore the app"
  thumbnails + lightbox (currently CSS placeholder mockups).
- Copy rule: plain dashes, no em dashes.
