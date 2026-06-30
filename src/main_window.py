# -*- coding: utf-8 -*-
"""
Main window layout and GUI logic for the InPage ↔ Unicode Urdu Converter.
"""
import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QRadioButton, QButtonGroup, QLabel, QTextEdit, QPushButton,
    QCheckBox, QFileDialog, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QFont, QFontDatabase, QTextBlockFormat, QTextCursor, QIcon, QKeySequence

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, relative_path)


class InPageInputTextEdit(QTextEdit):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window

    def insertFromMimeData(self, source):
        # In InPage -> Unicode mode, try to retrieve text using our preferred clipboard method
        # which automatically chooses between raw bytes and unicode text based on lossy conversion detection.
        if self.main_window.radio_inpage_to_unicode.isChecked():
            try:
                text = self.main_window.get_preferred_clipboard_text()
                if text:
                    self.insertPlainText(text)
                    return
            except Exception:
                pass
        super().insertFromMimeData(source)

    def toPlainText(self):
        # Override toPlainText to preserve non-breaking spaces (\xa0),
        # which represent Noon (ن) in InPage CP-1252.
        # Standard QPlainTextEdit/QTextEdit normalizes \xa0 to standard space ' '.
        text_list = []
        block = self.document().begin()
        while block.isValid():
            fragment = block.begin()
            block_text = ""
            while not fragment.atEnd():
                frag = fragment.fragment()
                if frag.isValid():
                    block_text += frag.text()
                fragment += 1
            text_list.append(block_text)
            block = block.next()
        return "\n".join(text_list)

    def get_selected_text_preserved(self):
        cursor = self.textCursor()
        doc = self.document()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        
        selected_text = ""
        block = doc.begin()
        while block.isValid():
            block_pos = block.position()
            block_len = block.length()
            if block_pos + block_len > start and block_pos < end:
                fragment = block.begin()
                while not fragment.atEnd():
                    frag = fragment.fragment()
                    if frag.isValid():
                        frag_pos = frag.position()
                        frag_len = frag.length()
                        if frag_pos + frag_len > start and frag_pos < end:
                            frag_text = frag.text()
                            f_start = max(0, start - frag_pos)
                            f_end = min(frag_len, end - frag_pos)
                            selected_text += frag_text[f_start:f_end]
                    fragment += 1
                if block_pos + block_len < end:
                    selected_text += "\n"
            block = block.next()
        return selected_text

    def copy(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return
        selected_text = self.get_selected_text_preserved()
        clipboard = QApplication.clipboard()
        mime = QMimeData()
        mime.setText(selected_text)
        clipboard.setMimeData(mime)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy()
            event.accept()
        else:
            super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        for action in menu.actions():
            if "Copy" in action.text() or action.shortcut() == QKeySequence.Copy:
                try:
                    action.disconnect()
                except Exception:
                    pass
                action.triggered.connect(self.copy)
        menu.exec_(event.globalPos())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InPage ↔ Unicode Urdu Converter")
        self.resize(900, 650)
        
        # Load window icon
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Load custom Urdu font
        self.urdu_font_family = "Noto Nastaliq Urdu"
        font_path = get_resource_path(os.path.join("assets", "fonts", "NotoNastaliqUrdu-Regular.ttf"))
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.urdu_font_family = families[0]
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)
        
        # Header Label
        header_label = QLabel("InPage ↔ Unicode Urdu Converter")
        header_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1a1a1a; margin-bottom: 5px;")
        main_layout.addWidget(header_label)
        
        # Direction selector panel
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Conversion Direction:")
        dir_layout.addWidget(dir_label)
        
        self.radio_inpage_to_unicode = QRadioButton("InPage → Unicode")
        self.radio_inpage_to_unicode.setChecked(True)
        self.radio_unicode_to_inpage = QRadioButton("Unicode → InPage")
        
        # Group radio buttons together
        self.dir_group = QButtonGroup(self)
        self.dir_group.addButton(self.radio_inpage_to_unicode)
        self.dir_group.addButton(self.radio_unicode_to_inpage)
        
        dir_layout.addWidget(self.radio_inpage_to_unicode)
        dir_layout.addWidget(self.radio_unicode_to_inpage)
        dir_layout.addStretch()
        
        main_layout.addLayout(dir_layout)
        
        # Input section
        self.input_label = QLabel("Input Text:")
        main_layout.addWidget(self.input_label)
        
        self.input_box = InPageInputTextEdit(self)
        main_layout.addWidget(self.input_box)
        
        # Input info/action bar (character count, paste, clear)
        input_bar_layout = QHBoxLayout()
        
        self.char_count_label = QLabel("0 characters")
        self.char_count_label.setObjectName("char_count_label")
        input_bar_layout.addWidget(self.char_count_label)
        
        input_bar_layout.addStretch()
        
        self.paste_btn = QPushButton("Paste from Clipboard")
        self.paste_btn.setObjectName("paste_btn")
        input_bar_layout.addWidget(self.paste_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("clear_btn")
        input_bar_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(input_bar_layout)
        
        # Convert Button (placed between input and output)
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setObjectName("convert_btn")
        main_layout.addWidget(self.convert_btn)
        
        # Save to file option
        self.save_to_file_cb = QCheckBox("Also save to file")
        main_layout.addWidget(self.save_to_file_cb)
        
        # Output section
        self.output_label = QLabel("Converted Output:")
        main_layout.addWidget(self.output_label)
        
        self.output_box = InPageInputTextEdit(self)
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Converted text will appear here...")
        main_layout.addWidget(self.output_box)
        
        # Wire events
        self.convert_btn.clicked.connect(self.handle_conversion)
        self.radio_inpage_to_unicode.toggled.connect(self.handle_direction_change)
        self.paste_btn.clicked.connect(self.handle_paste)
        self.clear_btn.clicked.connect(self.handle_clear)
        self.input_box.textChanged.connect(self.handle_text_changed)
        
        # Apply CSS styling and initial state formatting
        self.apply_styles()
        self.handle_direction_change()

    def apply_styles(self):
        """Apply custom QSS style sheet to make the UI look modern and clean."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 11pt;
                font-weight: bold;
                color: #343a40;
            }
            QRadioButton {
                font-size: 11pt;
                color: #495057;
            }
            QCheckBox {
                font-size: 11pt;
                color: #495057;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 10px;
                color: #212529;
            }
            QTextEdit:focus {
                border: 1.5px solid #228be6;
            }
            QPushButton#convert_btn {
                background-color: #228be6;
                color: white;
                font-weight: bold;
                font-size: 12pt;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                min-height: 42px;
            }
            QPushButton#convert_btn:hover {
                background-color: #1c7ed6;
            }
            QPushButton#convert_btn:pressed {
                background-color: #1864ab;
            }
            QPushButton#paste_btn, QPushButton#clear_btn {
                background-color: #e9ecef;
                color: #495057;
                font-weight: normal;
                font-size: 10pt;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 6px 12px;
                min-height: 32px;
            }
            QPushButton#paste_btn:hover, QPushButton#clear_btn:hover {
                background-color: #dee2e6;
                color: #212529;
                border-color: #adb5bd;
            }
            QPushButton#paste_btn:pressed, QPushButton#clear_btn:pressed {
                background-color: #ced4da;
            }
            QLabel#char_count_label {
                font-size: 10pt;
                font-weight: normal;
                color: #868e96;
            }
        """)

    def handle_direction_change(self):
        """Update placeholder text, text alignment, and fonts when the direction changes."""
        to_unicode = self.radio_inpage_to_unicode.isChecked()
        
        if to_unicode:
            # Input is InPage text: LTR alignment, monospace font representation
            self.input_box.setPlaceholderText("Paste InPage text here (e.g. \\x04\\u0192\\x04\\x81\\x04\\u0153...)")
            self.input_box.setLayoutDirection(Qt.LeftToRight)
            self.input_box.setStyleSheet("""
                QTextEdit {
                    background-color: #ffffff;
                    border: 1px solid #ced4da;
                    border-radius: 6px;
                    padding: 10px;
                    color: #212529;
                    font-family: 'Courier New', 'Consolas', 'monospace';
                    font-size: 12pt;
                }
                QTextEdit:focus {
                    border: 1.5px solid #228be6;
                }
            """)
            self.input_box.setAlignment(Qt.AlignLeft)
            self.set_line_height(self.input_box, 100)
            
            # Output is Unicode Urdu: RTL alignment, Nastaliq font styles
            self.output_box.setPlaceholderText("Converted Unicode Urdu will appear here...")
            self.output_box.setLayoutDirection(Qt.RightToLeft)
            self.output_box.setStyleSheet(f"""
                QTextEdit {{
                    background-color: #ffffff;
                    border: 1px solid #ced4da;
                    border-radius: 6px;
                    padding: 10px;
                    color: #212529;
                    font-family: '{self.urdu_font_family}', 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', 'Tahoma', 'serif';
                    font-size: 16pt;
                }}
                QTextEdit:focus {{
                    border: 1.5px solid #228be6;
                }}
            """)
            self.output_box.setAlignment(Qt.AlignRight)
            self.set_line_height(self.output_box, 150)
            
        else:
            # Input is Unicode Urdu: RTL alignment, Nastaliq font styles
            self.input_box.setPlaceholderText("Type or paste Unicode Urdu here...")
            self.input_box.setLayoutDirection(Qt.RightToLeft)
            self.input_box.setStyleSheet(f"""
                QTextEdit {{
                    background-color: #ffffff;
                    border: 1px solid #ced4da;
                    border-radius: 6px;
                    padding: 10px;
                    color: #212529;
                    font-family: '{self.urdu_font_family}', 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', 'Tahoma', 'serif';
                    font-size: 16pt;
                }}
                QTextEdit:focus {{
                    border: 1.5px solid #228be6;
                }}
            """)
            self.input_box.setAlignment(Qt.AlignRight)
            self.set_line_height(self.input_box, 150)
            
            # Output is InPage text: LTR alignment, monospace font representation
            self.output_box.setPlaceholderText("Converted InPage text representation will appear here...")
            self.output_box.setLayoutDirection(Qt.LeftToRight)
            self.output_box.setStyleSheet("""
                QTextEdit {
                    background-color: #ffffff;
                    border: 1px solid #ced4da;
                    border-radius: 6px;
                    padding: 10px;
                    color: #212529;
                    font-family: 'Courier New', 'Consolas', 'monospace';
                    font-size: 12pt;
                }
                QTextEdit:focus {
                    border: 1.5px solid #228be6;
                }
            """)
            self.output_box.setAlignment(Qt.AlignLeft)
            self.set_line_height(self.output_box, 100)

    def handle_conversion(self):
        """Invoke conversion function from glyph_map based on selection and update output."""
        from mapping.glyph_map import inpage_to_unicode, unicode_to_inpage
        
        input_text = self.input_box.toPlainText()
        
        # Guard for empty input
        if not input_text.strip():
            QMessageBox.warning(self, "Empty Input", "Please enter text to convert.")
            return
            
        to_unicode = self.radio_inpage_to_unicode.isChecked()
        
        if to_unicode:
            converted = inpage_to_unicode(input_text)
        else:
            converted = unicode_to_inpage(input_text)
            
        self.output_box.setPlainText(converted)
        
        # Re-apply output text alignment and line height because setPlainText resets formatting
        if to_unicode:
            self.output_box.setAlignment(Qt.AlignRight)
            self.set_line_height(self.output_box, 150)
        else:
            self.output_box.setAlignment(Qt.AlignLeft)
            self.set_line_height(self.output_box, 100)

        # Check if the output has recognizable Urdu / InPage characters
        if to_unicode:
            # We expect Unicode Urdu characters in range \u0600-\u06ff
            has_urdu = any('\u0600' <= char <= '\u06ff' for char in converted)
        else:
            # We expect InPage characters representing Urdu letters (prefix \x04 followed by Urdu letter byte)
            non_letter_bytes = {
                '\xa9', '\xfd', '\xfe', '\xfa', '\xfb', '\xfc', '\xda', '\xf9', '\xf1',
                '\xe1', '\xe2', '\xe9', ' ', '\xb4',
                '\xd0', '\xd1', '\xd2', '\xd3', '\xd4', '\xd5', '\xd6', '\xd7', '\xd8', '\xd9'
            }
            has_urdu = False
            for i in range(len(converted) - 1):
                if converted[i] == '\x04' and converted[i+1] not in non_letter_bytes:
                    has_urdu = True
                    break

        if not has_urdu:
            QMessageBox.warning(
                self,
                "Conversion Warning",
                "Output doesn't appear to contain Urdu. Check your conversion direction."
            )
            return

        # Save to file if option is enabled
        if self.save_to_file_cb.isChecked():
            self.save_to_file(converted)

    def save_to_file(self, content):
        """Open file dialog and save content to a file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Converted Text",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                QMessageBox.information(
                    self,
                    "Success",
                    f"File successfully saved to:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save file:\n{str(e)}"
                )

    def get_raw_clipboard_bytes(self):
        """Read raw CF_TEXT format bytes directly from Windows clipboard using ctypes."""
        if sys.platform != 'win32':
            return None
        import ctypes
        from ctypes import wintypes
        
        # Windows API declarations
        OpenClipboard = ctypes.windll.user32.OpenClipboard
        OpenClipboard.argtypes = [wintypes.HWND]
        OpenClipboard.restype = wintypes.BOOL
        
        CloseClipboard = ctypes.windll.user32.CloseClipboard
        CloseClipboard.argtypes = []
        CloseClipboard.restype = wintypes.BOOL
        
        GetClipboardData = ctypes.windll.user32.GetClipboardData
        GetClipboardData.argtypes = [wintypes.UINT]
        GetClipboardData.restype = wintypes.HANDLE
        
        GlobalLock = ctypes.windll.kernel32.GlobalLock
        GlobalLock.argtypes = [wintypes.HANDLE]
        GlobalLock.restype = ctypes.c_void_p
        
        GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
        GlobalUnlock.argtypes = [wintypes.HANDLE]
        GlobalUnlock.restype = wintypes.BOOL
        
        CF_TEXT = 1
        
        if not OpenClipboard(None):
            return None
        try:
            handle = GetClipboardData(CF_TEXT)
            if not handle:
                return None
            ptr = GlobalLock(handle)
            if not ptr:
                return None
            try:
                return ctypes.c_char_p(ptr).value
            finally:
                GlobalUnlock(handle)
        finally:
            CloseClipboard()

    def get_preferred_clipboard_text(self):
        """
        Choose the most reliable clipboard text format. Bypasses ANSI translation if
        direct InPage text is detected, but prefers standard unicode text if the raw bytes
        were corrupted/lossily-converted by Windows.
        """
        clipboard = QApplication.clipboard()
        text_from_qt = clipboard.text()
        
        # If on non-Windows or standard clipboard is empty, fallback directly
        if sys.platform != 'win32' or not text_from_qt:
            return text_from_qt
            
        try:
            raw_bytes = self.get_raw_clipboard_bytes()
            if raw_bytes:
                text_from_raw = raw_bytes.decode('latin1')
                
                # Check for lossy conversion in CF_TEXT:
                # 1. If standard clipboard has NBSP (\xa0) but raw bytes do not, CF_TEXT lost it.
                # 2. If raw bytes contain more '?' characters than standard text, CF_TEXT is corrupted.
                if ('\xa0' in text_from_qt and '\xa0' not in text_from_raw) or \
                   (text_from_raw.count('?') > text_from_qt.count('?')):
                    return text_from_qt
                    
                return text_from_raw
        except Exception:
            pass
            
        return text_from_qt

    def handle_paste(self):
        """Paste text from clipboard into the input box and apply alignment/line height."""
        to_unicode = self.radio_inpage_to_unicode.isChecked()
        text = None
        if to_unicode:
            text = self.get_preferred_clipboard_text()
            
        if text is None:
            clipboard = QApplication.clipboard()
            text = clipboard.text()
            
        self.input_box.setPlainText(text)
        
        if to_unicode:
            self.input_box.setAlignment(Qt.AlignLeft)
            self.set_line_height(self.input_box, 100)
        else:
            self.input_box.setAlignment(Qt.AlignRight)
            self.set_line_height(self.input_box, 150)

    def handle_clear(self):
        """Clear both input and output text boxes and reset formatting."""
        self.input_box.clear()
        self.output_box.clear()
        
        to_unicode = self.radio_inpage_to_unicode.isChecked()
        if to_unicode:
            self.input_box.setAlignment(Qt.AlignLeft)
            self.set_line_height(self.input_box, 100)
            self.output_box.setAlignment(Qt.AlignRight)
            self.set_line_height(self.output_box, 150)
        else:
            self.input_box.setAlignment(Qt.AlignRight)
            self.set_line_height(self.input_box, 150)
            self.output_box.setAlignment(Qt.AlignLeft)
            self.set_line_height(self.output_box, 100)

    def handle_text_changed(self):
        """Update the live character count label."""
        count = len(self.input_box.toPlainText())
        if count == 1:
            self.char_count_label.setText("1 character")
        else:
            self.char_count_label.setText(f"{count} characters")

    def set_line_height(self, text_edit, percentage):
        """Set the line spacing (line height) of a QTextEdit as a percentage."""
        cursor = text_edit.textCursor()
        block_fmt = QTextBlockFormat()
        block_fmt.setLineHeight(percentage, QTextBlockFormat.ProportionalHeight)
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(block_fmt)
