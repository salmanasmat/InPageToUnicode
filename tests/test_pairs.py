# -*- coding: utf-8 -*-
import unittest
import sys
import os

# Add parent directory to path so we can import mapping module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mapping.glyph_map import inpage_to_unicode, unicode_to_inpage

class TestInPageUnicodeConversion(unittest.TestCase):
    
    def test_basic_words(self):
        # 1. "پاکستان" (Pakistan)
        # Unicode: پ ا ک س ت ا ن (\u067e\u0627\u06a9\u0633\u062a\u0627\u0646)
        # InPage CP1252: \x04\u0192 (پ) \x04\x81 (ا) \x04\u0153 (ک) \x04\u2019 (س) \x04\u201e (ت) \x04\x81 (ا) \x04\xa0 (ن)
        inpage_pak = '\x04\u0192\x04\x81\x04\u0153\x04\u2019\x04\u201e\x04\x81\x04\xa0'
        unicode_pak = 'پاکستان'
        
        self.assertEqual(inpage_to_unicode(inpage_pak), unicode_pak)
        # Verify unicode_to_inpage converts it back to CP1252 InPage representation
        self.assertEqual(unicode_to_inpage(unicode_pak), inpage_pak)

        # 2. "اردو" (Urdu)
        # Unicode: ا ر د و (\u0627\u0631\u062f\u0648)
        # InPage CP1252: \x04\x81 (ا) \x04\u017d (ر) \x04\u2039 (د) \x04\xa2 (و)
        inpage_urdu = '\x04\x81\x04\u017d\x04\u2039\x04\xa2'
        unicode_urdu = 'اردو'
        
        self.assertEqual(inpage_to_unicode(inpage_urdu), unicode_urdu)
        self.assertEqual(unicode_to_inpage(unicode_urdu), inpage_urdu)

    def test_numbers_and_reversal(self):
        # InPage digits 12345: \x04\xd1 \x04\xd2 \x04\xd3 \x04\xd4 \x04\xd5
        # Mapped to unicode: ۱۲۳۴۵
        # With reverse_digits=True, they should be reversed to ۵۴۳۲۱ so they read LTR correctly
        inpage_num = '\x04\xd1\x04\xd2\x04\xd3\x04\xd4\x04\xd5'
        
        # When reverse_digits is True (default)
        self.assertEqual(inpage_to_unicode(inpage_num), '۵۴۳۲۱')
        
        # When reverse_digits is False
        self.assertEqual(inpage_to_unicode(inpage_num, {'reverse_digits': False}), '۱۲۳۴۵')
        
        # Unicode -> InPage for digits
        # Standard unicode digits: ۱۲۳۴۵
        # Should convert to InPage representation (without any reversal in current unicode_to_inpage logic)
        self.assertEqual(unicode_to_inpage('۱۲۳۴۵'), inpage_num)

    def test_heh_hamza(self):
        # InPage: \x04\xa6\x04\xbf (Heh + Hamza combinations)
        # default option: heh_hamza = True -> 'ۂ' (\u06c2)
        # default option: heh_hamza = False -> 'ئہ'
        inpage_hh = '\x04\xa6\x04\xbf'
        
        self.assertEqual(inpage_to_unicode(inpage_hh), 'ۂ')
        self.assertEqual(inpage_to_unicode(inpage_hh, {'heh_hamza': False}), 'ئہ')

    def test_kashida(self):
        # \x04\xa9 is Kashida. 
        # default: remove_kashida = False -> 'ـ' (\u0640)
        # remove_kashida = True -> ''
        inpage_kashida = '\x04\xa9'
        self.assertEqual(inpage_to_unicode(inpage_kashida), 'ـ')
        self.assertEqual(inpage_to_unicode(inpage_kashida, {'remove_kashida': True}), '')
        self.assertEqual(unicode_to_inpage('ـ'), inpage_kashida)

    def test_quotes(self):
        # \x04\xfd and \x04\xfe quotes
        # reverse_quotes = False (default): \x04\xfd -> ’ (\u2019), \x04\xfe -> ‘ (\u2018)
        # reverse_quotes = True: \x04\xfd -> ‘ (\u2018), \x04\xfe -> ’ (\u2019)
        inpage_q1 = '\x04\xfd'
        inpage_q2 = '\x04\xfe'
        
        self.assertEqual(inpage_to_unicode(inpage_q1), '’')
        self.assertEqual(inpage_to_unicode(inpage_q2), '‘')
        
        self.assertEqual(inpage_to_unicode(inpage_q1, {'reverse_quotes': True}), '‘')
        self.assertEqual(inpage_to_unicode(inpage_q2, {'reverse_quotes': True}), '’')

    def test_cp1252_pasted_text(self):
        # Test case using CP-1252 style InPage text (without \x04 prefixes)
        # “¦Ž¤Ž -> شهریار (if \x81/alif is missing: شہریر)
        # We test with \x81 restored to get 'شہریار'
        inpage_cp1252 = "\u201c\xa6\u017d\xa4\x81\u017d \u2030\u0178\u2039 \xa2\u2021\u017d \xa2\u017e\xa6"
        expected_unicode = "شہریار حمد وجر ولہ"
        self.assertEqual(inpage_to_unicode(inpage_cp1252), expected_unicode)

        # Exact user string (where \x81 was stripped by browser copy/paste)
        user_literal = "“¦Ž¤Ž ‰Ÿ‹ ¢‡Ž ¢ž¦"
        expected_user_unicode = "شہریر حمد وجر ولہ"
        self.assertEqual(inpage_to_unicode(user_literal), expected_user_unicode)

    def test_round_trip(self):
        # Round trip test for clean text
        original_unicode = 'پاکستان ایک خوبصورت ملک ہے۔'
        # Convert to InPage
        inpage_text = unicode_to_inpage(original_unicode)
        # Convert back to Unicode
        # Since options like bari_yee, space correction etc. might touch formatting,
        # we will test with basic options.
        round_trip_unicode = inpage_to_unicode(inpage_text, {
            'reverse_digits': False,
            'bari_yee': False,
            'remove_double_space': False
        })
        # Let's see if they match.
        self.assertEqual(round_trip_unicode, original_unicode)

if __name__ == '__main__':
    unittest.main()
