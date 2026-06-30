# PROJECT_SPEC.md — InPage ↔ Unicode Urdu Converter (Desktop App)

## 1. Purpose
A Windows desktop application that converts Urdu text between InPage's legacy glyph encoding and standard Unicode. Paste-based only (no .inp binary file parsing). Bidirectional. Built in Python with PyQt5.

## 2. Scope (Locked)
- Input: pasted text only (via textbox paste or "Paste from Clipboard" button). NOT reading .inp files directly.
- Direction: both InPage → Unicode AND Unicode → InPage, user-selectable.
- Output: shown on-screen in the app, OR saved to a .txt file (user choice via toggle), UTF-8 encoded.
- Platform: Windows desktop, packaged as standalone .exe via PyInstaller.
- GUI framework: PyQt5.

## 3. Out of Scope (do not build unless explicitly requested later)
- Reading/parsing .inp binary files directly
- Batch/multi-file conversion
- Drag-and-drop file support
- Cloud sync, accounts, telemetry, ads, network calls of any kind
- Mac/Linux builds

## 4. Functional Requirements
1. User selects conversion direction: "InPage → Unicode" or "Unicode → InPage" (radio buttons or dropdown).
2. User pastes/types text into an "Input" textbox (multi-line, large).
3. User clicks "Convert".
4. Converted text appears in a read-only "Output" textbox.
5. Output text direction/alignment auto-adjusts: RTL + Nastaliq-style font when output is Unicode Urdu; LTR/monospace when output is InPage-style text.
6. User can optionally toggle "Save to file" mode — on Convert, a native Save File dialog opens (.txt default) and writes the UTF-8 output to disk, plus shows a confirmation message. Output is still also shown in the app.
7. "Paste from Clipboard" button pastes clipboard contents into Input box.
8. "Clear" button clears both Input and Output boxes.
9. Live character count under Input box.
10. Empty input on Convert → warning dialog, no conversion attempted.
11. If conversion direction is likely wrong (no recognizable Urdu output) → warning dialog suggesting user check direction toggle.
12. Save-to-file errors are caught and shown in a user-facing error dialog (never a silent crash or raw traceback).

## 5. Non-Functional Requirements
- Must work fully offline (no internet dependency).
- Startup time should be fast (<2s on typical Windows machine).
- Bundled Nastaliq Urdu font (e.g., Noto Nastaliq Urdu or Jameel Noori Nastaleeq) must be loaded via QFontDatabase so correct rendering doesn't depend on system fonts being pre-installed.
- App icon and all assets must be bundled correctly into the final .exe (not left as external dependencies).

## 6. Tech Stack
- Python 3.x
- PyQt5
- PyInstaller (for packaging)
- Mapping logic ported from existing open-source converters (see MAPPING_REQUIREMENTS.md) — not invented from scratch.

## 7. Project Structure
```
/src
  main.py                # entry point
  main_window.py          # PyQt5 GUI window/layout
  test_conversion.py      # temporary CLI test harness (Phase 2 only, can be removed later)
/mapping
  glyph_map.py             # InPage<->Unicode mapping tables + conversion functions
/assets
  fonts/                   # bundled Nastaliq Urdu font file(s)
  icon.ico
requirements.txt
README.md
```

## 8. Core Module Contract
`/mapping/glyph_map.py` must expose:
```python
def inpage_to_unicode(text: str) -> str: ...
def unicode_to_inpage(text: str) -> str: ...
```
These are the ONLY two functions the GUI layer should call for conversion. Keep mapping logic fully decoupled from PyQt5 code so it can be tested independently (see Phase 2 CLI harness).

## 9. Build Phases
See PHASED_BUILD_PROMPTS.md for the exact step-by-step prompts to execute this spec, in order. Each phase should be completed and verified before moving to the next. Do not skip ahead or combine phases.

## 10. Acceptance Criteria (Definition of Done)
- [ ] Both conversion directions work correctly on test strings (see MAPPING_REQUIREMENTS.md test set)
- [ ] GUI matches Section 4 functional requirements exactly
- [ ] App runs as a standalone .exe with no missing asset/font errors
- [ ] No unhandled exceptions surface to the user as raw tracebacks
- [ ] App works fully offline
