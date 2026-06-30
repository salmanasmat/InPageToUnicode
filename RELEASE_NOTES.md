# Release Notes

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-30

### 🚀 New Features
- **Bidirectional Conversion**: Full support for converting between InPage legacy glyph encoding (CP-1252/custom) and standard Unicode Urdu text.
- **Direct Clipboard Integration**: Implemented a custom clipboard handler using native Windows `ctypes` API. This directly grabs CP-1252 raw bytes from the `CF_TEXT` format, bypassing Windows lossy ANSI/Unicode normalizations that strip key character indicators (like the non-breaking space `\xa0` representing *Noon*).
- **Nastaliq Rendering**: Bundled Google's open-source *Noto Nastaliq Urdu* font and configured automatic Right-to-Left (RTL) reading layout for Unicode text, ensuring consistent rendering on any Windows machine.
- **Optional File Export**: Added a direct toggle in the GUI to export converted outputs into a clean, UTF-8 encoded `.txt` file using native Windows save-file dialogs.

### ⚡ Improvements
- **Interactive UI Utilities**: Added helper buttons for "Paste from Clipboard" and "Clear", along with live input character counts.
- **Intelligent Font Loading**: Configured dynamic font loading via PyQt5's `QFontDatabase` to guarantee proper Nastaliq styling even if the system does not have Urdu fonts pre-installed.
- **Validation Dialogs**: Added warning notifications for empty text inputs and direction checking (raising a warning if the conversion output does not appear to contain valid Urdu characters).

### 🐛 Bug Fixes
- **Non-breaking Space Preservation**: Fixed a critical issue where standard text edit paste events would collapse the `\xa0` character into a standard space, breaking ligature reconstruction.
- **Error Boundaries**: Implemented try-catch safeguards around OS operations (like file system writes) to present formatted error dialogs to users instead of raw tracebacks.

### 📚 Documentation
- **Architecture & Code Docs**: Created [CODE_DOCUMENTATION.md](file:///d:/Reports/Scripting/Antigravity/InPageToUnicode/CODE_DOCUMENTATION.md) detailing the MVC layout, ctypes clipboard calls, and mapping flow.
- **Design Philosophy**: Created [DESIGN_PHILOSOPHY.md](file:///d:/Reports/Scripting/Antigravity/InPageToUnicode/DESIGN_PHILOSOPHY.md) outlining project architecture, decoupling decisions, and technical trade-offs.
- **Developer Guidelines**: Created [CONTRIBUTING.md](file:///d:/Reports/Scripting/Antigravity/InPageToUnicode/CONTRIBUTING.md) to onboard contributors with repository standards and branch setup.

### 🏗️ Infrastructure & Maintenance
- **Packaging Pipeline**: Created `InPageConverter.spec` for compiling the project into a standalone `.exe` using PyInstaller.
- **Standard Installer**: Created `inno_setup.iss` to package the compiled executable into a professional Windows Installer with Desktop/Start Menu shortcuts.
- **Automated Tests**: Structured automated unit and integration tests under the `tests/` directory verifying mapping logic, digit reversal, Hamza correction, and custom clipboard mechanics.
