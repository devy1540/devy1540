# Profile content

`content.json` stores translated copy and shared links. `header.html` stores the shared image layout.

After updating either source or the automatic-language sections in `assets/profile-*.svg`, run:

```sh
python3 scripts/render_readmes.py
python3 scripts/render_readmes.py --check
```

The root `README.md` uses English body text and browser-selected SVG copy. Each `README.<locale>.md` explicitly selects matching SVG text with `#locale-<locale>`.

SVG automatic matching selects the first available language in this order: Korean, Japanese, Simplified Chinese, Spanish, French, then English as the fallback. The order of a browser's language list does not reorder these SVG alternatives.
