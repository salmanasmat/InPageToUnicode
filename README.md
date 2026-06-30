# InPage ↔ Unicode Urdu Converter

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](#)
[![GitHub Release](https://img.shields.io/github/v/release/salmanasmat/InPageToUnicode.svg)](https://github.com/salmanasmat/InPageToUnicode/releases/latest)

Convert old InPage Urdu documents into modern Unicode text — works fully offline, no internet required, and no data ever leaves your computer.

For developers and advanced users, the application is built in Python and PyQt5 to provide bidirectional conversion between InPage's legacy glyph encoding (CP-1252/custom) and standard Unicode. This paste-based text utility bypasses the need to parse binary `.inp` files, designed to easily migrate text databases between legacy print layouts and modern web formats.

![InPage ↔ Unicode Urdu Converter Screenshot](Screenshot/main.png)

---

## Who is this for?

*   **Urdu Publishers & Typesetters**: Digitizing old InPage books and newspapers into modern digital formats.
*   **Students & Researchers**: Converting legacy InPage thesis files and documents to edit them in modern tools.
*   **IT Administrators**: Migrating legacy office archives to modern content management systems.
*   **Everyday Users**: Anyone who has legacy `.inp`-era copied or pasted text that renders as gibberish (e.g., CP-1252 character maps) in Microsoft Word or web browsers.

---

## Download

*   🚀 **[Download Installer (for everyday users, no Python needed)](https://github.com/salmanasmat/InPageToUnicode/releases/latest)**: Download the latest setup executable to install the application instantly on Windows.
*   💻 **[Build from source (for developers)](#🛠️-developer-setup--installation)**: Follow the instructions below to run the code locally or package it manually.

---
## 🚀 Key Features
*   **Bidirectional Conversion**: Select between `InPage → Unicode` and `Unicode → InPage` modes.
*   **Offline-First**: Runs entirely on the local machine with no external network calls, telemetry, or API requirements.
*   **Nastaliq Rendering**: Bundles Google's **Noto Nastaliq Urdu** font and automatically configures Right-to-Left (RTL) reading layout for Unicode text, ensuring consistent rendering on any Windows machine.
*   **Raw Clipboard Bypass**: Uses a Windows `ctypes` clipboard integration to access raw clipboard bytes directly, bypassing lossy Windows ANSI/Unicode translations that strip character markers (like non-breaking spaces `\xa0` representing *Noon*).
*   **Optional File Output**: Direct toggle to export converted outputs into a clean, UTF-8 encoded `.txt` file via native Windows file dialogs.
*   **Character Statistics & Validation**: Live input character count, warning dialogs for empty entries, and basic heuristic checking to prevent incorrect conversion directions.
---
## 🛠️ Developer Setup & Installation
### Prerequisites
*   **Python 3.8+**
*   Windows OS (for ctypes raw clipboard operations and packaging)
### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/salmanasmat/InPageToUnicode.git
    cd InPageToUnicode
    ```
2.  **Create and activate a virtual environment**:
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application**:
    ```bash
    python src/main.py
    ```
---
## 🧪 Running Unit Tests
The codebase includes comprehensive unit tests verifying mapping coverage, digits reversal, Hamza correction, quotation rules, and clipboard handling.
To execute the test suite:
```bash
python -m unittest discover -s tests
```
---
## 📦 Build & Packaging Instructions
### Standalone Executable (.exe)
The application can be compiled into a single executable using PyInstaller. A spec file is already provided:
```bash
pyinstaller InPageConverter.spec
```
The packaged executable will be generated inside the `dist/` directory with all assets (icon, Nastaliq font, mapping module) bundled natively.
### Windows Installer
An Inno Setup compiler script (`inno_setup.iss`) is included to package the executable into a setup installer:
1.  Ensure you have **Inno Setup 6** installed.
2.  Compile the installer:
    ```powershell
    ISCC.exe inno_setup.iss
    ```
The output installer will be saved to the `installer-output/` directory.
---
## ⚠️ Known Limitations
*   **Text-only Conversion**: This application processes plain text only. InPage text styling (e.g. bold, italics, custom font sizes, text boxes, tables, pages, and images) is **not** preserved.
*   **Encoding Dependability**: Accuracy depends on standard InPage glyph mapping conventions. Highly corrupted or non-standard font maps in legacy files may require manual correction.
---
## 📄 License
This project is licensed under the **GNU General Public License v3 (GPL v3)**. See the [LICENSE](LICENSE) file for the full text.
Copyright (C) 2026 [Salman Asmat](https://github.com/salmanasmat)

<!--
Recommended GitHub Topics to add via repository settings:
urdu, inpage, unicode, pyqt5, nastaliq, urdu-converter, pakistan, offline-tool, python-desktop-app, urdu-typing
-->
