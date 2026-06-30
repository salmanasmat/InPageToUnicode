# MAPPING_REQUIREMENTS.md — InPage ↔ Unicode Glyph Mapping

## 1. Why This Is the Hard Part
InPage does not use Unicode internally — it uses a custom glyph-based encoding tied to specific fonts, where the same Urdu letter can map to different byte codes depending on its position in a word (isolated / initial / medial / final form) and on ligatures (e.g., combinations involving "لا"). A correct converter must replicate this contextual mapping, not just swap characters 1:1.

## 2. Do Not Build the Mapping From Scratch
Port the mapping logic from existing, proven open-source converters rather than re-deriving it. Use these as reference sources, in this priority order:

1. **ltrc/inPageToUnicode** — https://github.com/ltrc/inPageToUnicode
   - File of interest: `inPage2Unicode.js`
   - This is a JS port of the original IT Duniya InPage converter logic. Treat this as the primary reference for InPage → Unicode direction, including contextual/ligature handling.

2. **umer0586/unicode-inpage-converter** — https://github.com/umer0586/unicode-inpage-converter
   - Files of interest: `Converter.h` / `Converter.cpp`
   - C++ implementation with BOTH directions (`inpageToUnicode` and `unicodeToInpage`). Use this primarily as the reference for the Unicode → InPage direction (the reverse mapping), since ltrc's repo is InPage→Unicode focused.

3. **HassamChundrigar/InpageToUnicode** — https://github.com/HassamChundrigar/InpageToUnicode
   - A direct Python port of the ltrc JS logic. Useful as a cross-check / starting point for Python syntax conventions, since our target language is Python.

## 3. Porting Instructions (for Gemini/dev agent)
- Fetch/read the source files from the above repos.
- Faithfully translate the character map dictionaries AND the contextual substitution rules (not just the lookup table) into Python.
- Preserve handling for: Heh+Hamza, Kashida, quotation marks, reversed digits, reversed S-sign, thousands separator, Bari Yee — these are noted as configurable options in ltrc's demo and should at minimum be handled with sensible defaults if not exposed as UI toggles.
- Keep the two directions in clearly separate functions/sections within `glyph_map.py` — do not try to auto-derive Unicode→InPage by reversing the InPage→Unicode dict, since the mapping is not a clean 1:1 reversal (contextual forms collapse many-to-one).

## 4. Test Set (must pass before GUI integration — Phase 2)
Create a test file with at least 5-10 known InPage/Unicode text pairs (can be sourced from the test/sample files in KamalAbdali/InpageToUnicode repo, e.g. `story.inp` / `story.txt`, or from manually verified short phrases) and confirm:
- InPage → Unicode output matches expected Unicode string
- Unicode → InPage output matches expected InPage string
- Round-trip (InPage → Unicode → InPage) produces the original or an acceptably equivalent string

## 5. Known Limitations to Document in README
- Conversion accuracy depends entirely on how closely the source text follows standard InPage encoding conventions; non-standard or corrupted InPage text may not convert perfectly.
- This is a text-only converter — InPage formatting (bold, font size, layout, images, page structure) is not preserved, since it's plain text in and plain text out.
