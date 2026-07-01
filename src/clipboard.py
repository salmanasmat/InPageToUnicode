# -*- coding: utf-8 -*-
"""
Utility module for raw Windows clipboard data reading using ctypes.
Avoids lossy conversion of InPage text symbols by reading CF_TEXT bytes directly.
"""
import sys
from PyQt5.QtWidgets import QApplication

def get_raw_clipboard_bytes():
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

def get_preferred_clipboard_text():
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
        raw_bytes = get_raw_clipboard_bytes()
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
