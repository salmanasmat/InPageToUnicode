# Design Philosophy - InPage ↔ Unicode Urdu Converter

This document details the engineering challenges, core design principles, target audience, and architectural trade-offs that guided the creation of the InPage ↔ Unicode Urdu Converter.

---

## 1. Problem Definition

For decades, **InPage** was the de facto standard software for Urdu desktop publishing in South Asia. However, InPage was built before Unicode emerged as the global standard for text. To represent Urdu Nastaliq script, InPage developed a **proprietary 2-byte glyph-based encoding** linked directly to custom layout engines.

In this legacy scheme:
1.  **No Contextual Convergence**: Unlike Unicode, where characters are encoded by their semantic value (e.g. Alif is always `\u0627`) and contextual shape rendering is left to the font engine, InPage stores the *exact glyph form* (isolated, initial, medial, or final) as a separate character byte code.
2.  **Many-to-One Collapsing**: A forward translation (InPage → Unicode) collapses many shapes into single Unicode points. A backward translation (Unicode → InPage) is highly contextual and cannot be trivially derived by reversing a lookup table.
3.  **ANSI Clipboard Lossiness**: When copying text out of InPage, Windows attempts to translate it via ANSI codepages. If not handled defensively, non-breaking spaces (representing the letter *Noon* `\xa0` in CP-1252) and custom glyph boundaries are stripped, corrupting the text.

---

## 2. Why This Solution?

Our design answers these challenges with a three-pronged approach:

1.  **Offline Desktop Application (PyQt5)**: We chose a lightweight desktop architecture rather than a web-based app. The conversion needs to be used by publishers who work with large text datasets, often in locations with unreliable internet connectivity. An offline desktop GUI guarantees fast execution and complete privacy.
2.  **Explicit Windows API Clipboard Hooking (`ctypes`)**: Web browsers and standard text widgets are bound by Windows' default Unicode clipboard routines, which lose legacy formatting metadata. By implementing a direct Windows API connection using Python `ctypes`, we grab raw byte streams before Windows processes them, preventing loss of characters like the Arabic *Noon Ghunna* or spaces.
3.  **Application-Embedded Font Rendering**: Standard Windows environments do not ship with Urdu Nastaliq-compatible fonts preinstalled, leading to broken block rendering. We bundle the open-source **Noto Nastaliq Urdu** font directly inside the binary and dynamically register it at runtime via `QFontDatabase`, ensuring visual accuracy out of the box.

---

## 3. Design Principles

*   **Offline-First & Security-Minded**: The application makes zero network requests. Telemetry, analytics, and auto-updates are omitted to keep the app secure and completely private.
*   **Predictable Performance**: Startup time is optimized to less than 1.5 seconds. Text parsing operations are written in memory with precompiled regular expressions to handle millions of characters instantly.
*   **Zero-Dependency Deployment**: The final output is packaged as a standalone executable. Users do not need to install Python, PyQt5, or fonts on their machines.
*   **Separation of Concerns**: Core converter maps are written as isolated python objects, enabling terminal tests and simple porting to other programming languages.

---

## 4. Target Audience & Use Cases

*   **Urdu News Publishers**: Migrating archives of legacy InPage files (`.inp` text) to modern web databases.
*   **Researchers & Translators**: Translating or digitizing old books/manuscripts written in InPage.
*   **Web Developers**: Building web catalogs from legacy print media assets.

---

## 5. Trade-offs & Constraints

*   **Plain Text Only**: The converter focuses exclusively on character content. Layout structure, columns, image blocks, font sizes, colors, and line spacing are out of scope.
*   **Platform Dependency**: The custom raw clipboard ctypes hook is native to the Windows clipboard API. On non-Windows platforms, the app falls back to standard clipboard mechanisms (which may suffer from lossy translation if legacy text formats are pasted).
*   **Contextual Imperfections**: InPage fonts sometimes use non-standard ligatures that do not strictly comply with standard CP-1252 maps. A minor manual editorial pass may be required for complex calligraphy files.
