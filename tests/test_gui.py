# -*- coding: utf-8 -*-
import unittest
import sys
import os
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main_window import MainWindow

# Create the QApplication instance once per test suite
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()

    def test_initial_state(self):
        self.assertEqual(self.window.input_box.toPlainText(), "")
        self.assertEqual(self.window.output_box.toPlainText(), "")
        self.assertEqual(self.window.char_count_label.text(), "0 characters")

    def test_character_count_updates(self):
        # Type some characters in input box
        self.window.input_box.setPlainText("Hello")
        self.assertEqual(self.window.char_count_label.text(), "5 characters")
        
        # Test singular form
        self.window.input_box.setPlainText("A")
        self.assertEqual(self.window.char_count_label.text(), "1 character")
        
        # Test empty form
        self.window.input_box.setPlainText("")
        self.assertEqual(self.window.char_count_label.text(), "0 characters")

    def test_nbsp_preservation(self):
        # Set text with non-breaking space (which represents Noon in InPage)
        self.window.input_box.setPlainText("a\xa0b")
        # Standard QTextEdit normalizes it to "a b"
        # Verify our custom InPageInputTextEdit preserves "a\xa0b"
        self.assertEqual(self.window.input_box.toPlainText(), "a\xa0b")

    def test_clear_button(self):
        # Set text in input and output
        self.window.input_box.setPlainText("Test input")
        self.window.output_box.setPlainText("Test output")
        
        # Click the clear button
        QTest.mouseClick(self.window.clear_btn, Qt.LeftButton)
        
        # Verify both are empty
        self.assertEqual(self.window.input_box.toPlainText(), "")
        self.assertEqual(self.window.output_box.toPlainText(), "")
        self.assertEqual(self.window.char_count_label.text(), "0 characters")

    def test_paste_button(self):
        # Process pending deletions from previous tests
        QApplication.processEvents()
        
        # Set some text to the clipboard
        clipboard = QApplication.clipboard()
        test_text = "Text from clipboard"
        clipboard.setText(test_text)
        
        # Sync clipboard
        QApplication.processEvents()
        
        # Click the paste button
        QTest.mouseClick(self.window.paste_btn, Qt.LeftButton)
        
        # Verify it pasted correctly
        self.assertEqual(self.window.input_box.toPlainText(), test_text)

    @patch('src.main_window.QMessageBox.warning')
    def test_empty_input_warning(self, mock_warning):
        self.window.input_box.setPlainText("")
        QTest.mouseClick(self.window.convert_btn, Qt.LeftButton)
        mock_warning.assert_called_once_with(
            self.window,
            "Empty Input",
            "Please enter text to convert."
        )

    @patch('src.main_window.QMessageBox.warning')
    def test_wrong_direction_warning_to_unicode(self, mock_warning):
        self.window.radio_inpage_to_unicode.setChecked(True)
        self.window.input_box.setPlainText("Hello English")
        QTest.mouseClick(self.window.convert_btn, Qt.LeftButton)
        mock_warning.assert_called_once_with(
            self.window,
            "Conversion Warning",
            "Output doesn't appear to contain Urdu. Check your conversion direction."
        )

    @patch('src.main_window.QMessageBox.warning')
    def test_wrong_direction_warning_to_inpage(self, mock_warning):
        self.window.radio_unicode_to_inpage.setChecked(True)
        self.window.input_box.setPlainText("Hello English")
        QTest.mouseClick(self.window.convert_btn, Qt.LeftButton)
        mock_warning.assert_called_once_with(
            self.window,
            "Conversion Warning",
            "Output doesn't appear to contain Urdu. Check your conversion direction."
        )

    @patch('src.main_window.QMessageBox.warning')
    def test_valid_conversion_no_warning(self, mock_warning):
        self.window.radio_inpage_to_unicode.setChecked(True)
        self.window.input_box.setPlainText('\x04\u0192\x04\x81') # InPage "پا"
        QTest.mouseClick(self.window.convert_btn, Qt.LeftButton)
        mock_warning.assert_not_called()
        self.assertEqual(self.window.output_box.toPlainText(), "پا")

    def test_copy_preserves_nbsp(self):
        # Verify that copying text containing \xa0 preserves it in clipboard instead of normalizing to space
        self.window.output_box.setPlainText("a\xa0b")
        self.window.output_box.selectAll()
        self.window.output_box.copy()
        
        clipboard = QApplication.clipboard()
        self.assertEqual(clipboard.text(), "a\xa0b")

if __name__ == '__main__':
    unittest.main()
