# Embedded type

The subsets here are inlined into every generated SVG as base64 `@font-face`
rules, because a README image cannot fetch a webfont: naming IBM Plex only
works for readers who happen to have it installed, and everyone else silently
gets a different typeface from the portfolio.

They are subset to the 89 glyphs the art actually draws, plus a little
headroom — 100 KB of full faces down to about 19 KB. Regenerate with
`fontTools.subset` if new characters appear in the data.

Source: `@fontsource/ibm-plex-sans` and `@fontsource/ibm-plex-mono`, the same
packages the site uses.
