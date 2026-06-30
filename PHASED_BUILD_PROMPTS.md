# InPage ↔ Unicode Urdu Converter — Phased Build Prompts (for Antigravity)

Scope: Paste-based text only (no .inp file parsing). Bidirectional (InPage→Unicode and Unicode→InPage). PyQt5 desktop app. Output shown on-screen and/or saved to file. Mapping table sourced from existing open-source converters (not built from scratch).

Feed these prompts to Antigravity one phase at a time. Confirm each phase works before moving to the next.

---

## Phase 0 — Project Setup

```
Create a new Python desktop project for a PyQt5 application called "InPage Unicode Converter".
Set up:
- A virtual environment
- requirements.txt with PyQt5
- Folder structure: /src, /assets, /mapping
- A main.py entry point that opens a blank PyQt5 window titled "InPage ↔ Unicode Urdu Converter", size 900x600
Do not add any conversion logic yet. Just confirm the window opens.
```

## Phase 1 — Mapping Table Module

```
Create a Python module /mapping/glyph_map.py that contains the InPage-to-Unicode and Unicode-to-InPage
character/glyph mapping tables, sourced from the open-source ltrc/inPageToUnicode (inPage2Unicode.js) logic
and umer0586/unicode-inpage-converter (Converter.h) logic.
Port the contextual glyph mapping rules (initial/medial/final/isolated forms, ligatures, kashida) faithfully —
do not invent or simplify the mapping.
Expose two functions:
- inpage_to_unicode(text: str) -> str
- unicode_to_inpage(text: str) -> str
Include a small set of test strings with expected output as comments or a test file.
```

## Phase 2 — Core Conversion Logic Test (CLI, no GUI yet)

```
Create a temporary CLI script /src/test_conversion.py that imports glyph_map.py and lets me paste InPage
text in the terminal and see the Unicode output, and vice versa, via a simple menu (1 = InPage→Unicode,
2 = Unicode→InPage, 3 = exit).
This is just to validate mapping accuracy before building the GUI.
```

## Phase 3 — Main GUI Layout

```
Build the main PyQt5 window layout in /src/main_window.py:
- A direction selector (radio buttons or dropdown): "InPage → Unicode" / "Unicode → InPage"
- An input text box (large, multi-line, paste-enabled) with a label "Input"
- An output text box (large, multi-line, read-only) with a label "Output"
- A "Convert" button between them
- The output box should auto-set text direction (RTL) and font appropriately when Unicode Urdu is shown
Wire the Convert button to call the appropriate function from glyph_map.py based on the selected direction.
Do not add file save/load yet — just paste in, convert, see result on screen.
```

## Phase 4 — Output Options (Text vs File)

```
Add an output mode toggle: "Show in app" (default, already working) vs "Save to file".
When "Save to file" is selected, after clicking Convert, open a native Save File dialog
(.txt by default) and write the converted text (UTF-8 encoded) to the chosen path.
Show a confirmation message after saving.
Keep both modes available — user can still see it in the output box even when saving to file.
```

## Phase 5 — Input Convenience Features

```
Add these small UX improvements to the input panel:
- A "Paste from Clipboard" button that pastes clipboard contents into the input box
- A "Clear" button that clears both input and output boxes
- A live character count label under the input box
```

## Phase 6 — Font & Display Polish

```
Improve text rendering quality:
- Bundle a Nastaliq Urdu font (e.g., Jameel Noori Nastaleeq or Noto Nastaliq Urdu) in /assets and load it
  via QFontDatabase so Unicode Urdu output renders properly even if not installed on the system
- Apply correct font size and line spacing for readability
- Ensure RTL alignment applies automatically when output is Urdu Unicode, and LTR/monospace when output
  is InPage-style text
```

## Phase 7 — Error Handling & Edge Cases

```
Add error handling:
- If input box is empty when Convert is clicked, show a warning dialog instead of converting
- If conversion produces no recognizable Urdu characters (likely wrong direction selected), show a
  warning suggesting the user check the direction toggle
- Wrap the save-to-file logic in try/except with a user-facing error dialog on failure
```

## Phase 8 — Packaging

```
Package the app into a standalone Windows .exe using PyInstaller, with the icon and bundled font included.
Make sure mapping data and assets are correctly bundled (not left external).
Provide the PyInstaller spec file and build instructions.
```

---

Optional later phases (not in current scope, mention only if you revisit):
- Direct .inp file parsing (binary format) instead of paste-only
- Batch conversion of multiple files
- Drag-and-drop file support
