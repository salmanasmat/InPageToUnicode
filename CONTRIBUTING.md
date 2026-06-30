# Contributing to InPage ↔ Unicode Urdu Converter

Thank you for your interest in contributing! This project aims to simplify Urdu text migrations. Following these guidelines helps ensure a smooth process for everyone.

---

## 🐛 Bug Reports

If you find a bug, please open an Issue on GitHub with the following details:
1.  **Clear Title**: Short summary of the bug.
2.  **Steps to Reproduce**: Detailed list of what you did.
3.  **Input Sample**: Provide the exact input string that caused the issue (preferably with the hex codes or raw copy).
4.  **Expected vs. Actual Output**: What did the app output, and what should it have output?
5.  **Environment**: Your Windows OS version.

---

## 💡 Feature Suggestions

We welcome ideas for improving the converter! When proposing a feature:
1.  Explain the **use case** (why is this feature useful?).
2.  Describe your proposed implementation or GUI layout changes.
3.  Keep in mind the project scope: offline-first, Windows-optimized, paste-based conversion.

---

## 🔧 Development Setup

To contribute code:

1.  **Fork the Repository**: Create a fork of `https://github.com/salmanasmat/InPageToUnicode`.
2.  **Clone Locally**:
    ```bash
    git clone https://github.com/salmanasmat/InPageToUnicode.git
    cd InPageToUnicode
    ```
3.  **Create a Branch**:
    ```bash
    git checkout -b feature/my-amazing-feature
    ```
4.  **Set up the Virtual Environment**:
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

---

## 🧪 Pre-Submission Checklist

Before submitting a Pull Request, please verify:

1.  **Code Integrity**: Run the existing unit tests to make sure no existing conversions are broken:
    ```bash
    python -m unittest discover -s tests
    ```
2.  **Write Tests**: If you are adding a new conversion rule, character mapping, or edge-case handling, add a corresponding test inside [test_pairs.py](file:///d:/Reports/Scripting/Antigravity/InPageToUnicode/tests/test_pairs.py).
3.  **Style Checks**: Keep Python code clean, properly formatted, and include clear inline comments where needed.
4.  **No Unrelated Modifications**: Avoid modifying files/dependencies unrelated to your change.

---

## 📬 Pull Request Workflow

1.  Push your branch to your fork:
    ```bash
    git push origin feature/my-amazing-feature
    ```
2.  Open a Pull Request (PR) on the main repository.
3.  Describe your changes clearly in the PR description, referencing any related issues.
4.  Once reviewed and approved, your changes will be merged!
