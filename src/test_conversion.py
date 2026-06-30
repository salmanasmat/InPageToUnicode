# -*- coding: utf-8 -*-
"""
Temporary CLI test harness to validate InPage ↔ Unicode conversion accuracy.
"""
import os
import sys

# Ensure parent directory is in path to import mapping module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mapping.glyph_map import inpage_to_unicode, unicode_to_inpage

def get_multiline_input(prompt):
    print(prompt)
    print("(Press Enter on a blank line to finish input)")
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

def main():
    # Force UTF-8 stdout if terminal supports it to avoid encoding errors print Urdu
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stdin, 'reconfigure'):
        sys.stdin.reconfigure(encoding='utf-8')

    while True:
        print("\n" + "="*40)
        print(" InPage ↔ Unicode Urdu Converter CLI")
        print("="*40)
        print("1. Convert InPage → Unicode")
        print("2. Convert Unicode → InPage")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            text = get_multiline_input("\nPaste/Type InPage text to convert:")
            if not text:
                print("No input provided.")
                continue
            
            # Print raw representation for debugging
            print(f"\n[Debug] Raw Input Bytes/Representation: {repr(text)}")
            converted = inpage_to_unicode(text)
            print("\nConverted Unicode Output:")
            print("-" * 30)
            print(converted)
            print("-" * 30)
            
        elif choice == '2':
            text = get_multiline_input("\nPaste/Type Unicode Urdu text to convert:")
            if not text:
                print("No input provided.")
                continue
            
            converted = unicode_to_inpage(text)
            print("\nConverted InPage Output:")
            print("-" * 30)
            print(converted)
            print("-" * 30)
            print(f"[Debug] Raw Output Bytes/Representation: {repr(converted)}")
            
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
