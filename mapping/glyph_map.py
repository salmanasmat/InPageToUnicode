# -*- coding: utf-8 -*-
"""
InPage ↔ Unicode Urdu Glyph Mapping Module
Ported and unified from ltrc/inPageToUnicode (JS) and umer0586/unicode-inpage-converter (C++).
"""

import re

# Configurable options with Urdu-centric defaults
DEFAULT_OPTIONS = {
    'heh_hamza': True,           # Correct Heh with Hamza (ۂ)
    'remove_kashida': False,      # Remove Tatweel/Kashida sign (ـ)
    'reverse_quotes': False,      # Reverse quotation marks
    'reverse_digits': True,       # Reverse digits to restore correct reading order (LTR)
    'reverse_s_sign': True,       # Reverse Solidus (/) sign in numbers
    'thousands_separator': True,  # Reverse thousands separator (,) in numbers
    'bari_yee': True,             # Correct Bari Yee contextual forms in middle of words
    'remove_double_space': True,  # Remove consecutive double spaces
    'remove_erabs': False,        # Remove all Urdu diacritics/erabs
    'year_sign': True,            # Correct Year sign order (؁)
}

# Unified InPage-to-Unicode mapping (sorted by key length descending)
# Maps both raw bytes (from files) and CP-1252 mapped characters (from Windows clipboard)
ITU_MAP = {
    '\x04\xa4\x04\xbf': '\u06cc\u0626',
    '\x04\x81\x04\x08': '\u0627\x04\x08',
    '\x04\x81\x04\xbf': '\u0623',
    '\x04\xa2\x04\xbf': '\u0624',
    '\x04\x81\x04\xb3': '\u0622',
    '\x04\xa1': '\u06ba',
    '\x04\xa8': '\u064d',
    '\x04\xd1': '\u06f1',
    '\x04\xd2': '\u06f2',
    '\x04\xd3': '\u06f3',
    '\x04\xd4': '\u06f4',
    '\x04\xd5': '\u06f5',
    '\x04\xd6': '\u06f6',
    '\x04\xd7': '\u06f7',
    '\x04\xd8': '\u06f8',
    '\x04\xd9': '\u06f9',
    '\x04\xd0': '\u06f0',
    '\x04\u203a': '\u0642',
    '\x04\x9b': '\u0642',
    '\x04\xa2': '\u0648',
    '\x04\u02dc': '\u0639',
    '\x04\x98': '\u0639',
    '\x04\u017d': '\u0631',
    '\x04\x8e': '\u0631',
    '\x04\u201e': '\u062a',
    '\x04\x84': '\u062a',
    '\x04\xa5': '\u06d2',
    '\x04\xa3': '\u0626',
    '\x04\xa4': '\u06cc',
    '\x04\xa6': '\u06c1',
    '\x04\u0192': '\u067e',
    '\x04\x83': '\u067e',
    '\x04\xf2': '\u060e',
    '\x04\x81': '\u0627',
    '\x04\u2019': '\u0633',
    '\x04\x92': '\u0633',
    '\x04\u2039': '\u062f',
    '\x04\x8b': '\u062f',
    '\x04\u0161': '\u0641',
    '\x04\x9a': '\u0641',
    '\x04\x9d': '\u06af',
    '\x04\xa7': '\u06be',
    '\x04\u2021': '\u062c',
    '\x04\x87': '\u062c',
    '\x04\u0153': '\u06a9',
    '\x04\x9c': '\u06a9',
    '\x04\u017e': '\u0644',
    '\x04\x9e': '\u0644',
    '\x04\xea': '\u061b',
    '\x04\x90': '\u0632',
    '\x04\u201c': '\u0634',
    '\x04\x93': '\u0634',
    '\x04\u02c6': '\u0686',
    '\x04\x88': '\u0686',
    '\x04\u2013': '\u0637',
    '\x04\x96': '\u0637',
    '\x04\u201a': '\u0628',
    '\x04\x82': '\u0628',
    '\x04\xa0': '\u0646',
    '\x04\u0178': '\u0645',
    '\x04\x9f': '\u0645',
    '\x04\xed': '\u060c',
    '\x04\xf3': '\u06d4',
    '\x04\xc7': '\u064b',
    '\x04\xb8': '\u064a',
    '\x04\xf8': '\u0610',
    '\x04\xb5': '\u064c',
    '\x04\xad': '\u0651',
    '\x04\xb1': '\u0652',
    '\x04\xf6': '\ufdfa',
    '\x04\xae': '\u0611',
    '\x04\x8f': '\u0691',
    '\x04\u2026': '\u0679',
    '\x04\x85': '\u0679',
    '\x04\xf7': '\u0601',
    '\x04\xbe': '\u0657',
    '\x04\xbd': '\u0670',
    '\x04\xb9': '\u06c3',
    '\x04\xac': '\u064f',
    '\x04\xfd': '\u2018',
    '\x04\xfe': '\u2019',
    '\x04\xcf': '\u0614',
    '\x04\xb3': '\u0653',
    '\x04\u201d': '\u0635',
    '\x04\x94': '\u0635',
    '\x04\u0152': '\u0688',
    '\x04\x8c': '\u0688',
    '\x04\xb0': '\u0656',
    '\x04\u2122': '\u063a',
    '\x04\x99': '\u063a',
    '\x04\u2030': '\u062d',
    '\x04\x89': '\u062d',
    '\x04\u2022': '\u0636',
    '\x04\x95': '\u0636',
    '\x04\u0160': '\u062e',
    '\x04\x8a': '\u062e',
    '\x04\xe7': '\u0612',
    '\x04\x8d': '\u0630',
    '\x04\u2018': '\u0698',
    '\x04\x91': '\u0698',
    '\x04\u2020': '\u062b',
    '\x04\x86': '\u062b',
    '\x04\u2014': '\u0638',
    '\x04\x97': '\u0638',
    '\x04\xe6': '\u0613',
    '\x04\xaa': '\u0650',
    '\x04\xab': '\u064e',
    '\x04\xee': '\u061f',
    '\x04\xfa': '[',
    '\x04\xfb': ']',
    '\x04\xfc': '.',
    '\x04\xda': '!',
    '\x04\xf9': ',',
    '\x04\xf1': '/',
    '\x04\xe1': ')',
    '\x04\xe2': '(',
    '\x04\xe9': ':',
    '\x04\xa9': ' ',
    '\x04\xb4': '',
    '\x04 ': ' ',
}

# Unicode-to-InPage mapping
UTI_MAP = {
    '\u0627\x04\x08': '\x04\x81\x04\x08',
    '\u06cc\u0626': '\x04\xa4\x04\xbf',
    '\u0623': '\x04\x81\x04\xbf',
    '\u0624': '\x04\xa2\x04\xbf',
    '\u0622': '\x04\x81\x04\xb3',
    '\u06ba': '\x04\xa1',
    '\u064d': '\x04\xa8',
    '\u06f1': '\x04\xd1',
    '\u06f2': '\x04\xd2',
    '\u06f3': '\x04\xd3',
    '\u06f4': '\x04\xd4',
    '\u06f5': '\x04\xd5',
    '\u06f6': '\x04\xd6',
    '\u06f7': '\x04\xd7',
    '\u06f8': '\x04\xd8',
    '\u06f9': '\x04\xd9',
    '\u06f0': '\x04\xd0',
    '\u0642': '\x04\u203a',
    '\u0648': '\x04\xa2',
    '\u0639': '\x04\u02dc',
    '\u0631': '\x04\u017d',
    '\u062a': '\x04\u201e',
    '\u06d2': '\x04\xa5',
    '\u0621': '\x04\xa3',
    '\u06cc': '\x04\xa4',
    '\u06c1': '\x04\xa6',
    '\u067e': '\x04\u0192',
    '\u060e': '\x04\xf2',
    '\u0627': '\x04\x81',
    '\u0633': '\x04\u2019',
    '\u062f': '\x04\u2039',
    '\u0641': '\x04\u0161',
    '\u06af': '\x04\x9d',
    '\u06be': '\x04\xa7',
    '\u062c': '\x04\u2021',
    '\u06a9': '\x04\u0153',
    '\u0644': '\x04\u017e',
    '\u061b': '\x04\xea',
    '\u0632': '\x04\x90',
    '\u0634': '\x04\u201c',
    '\u0686': '\x04\u02c6',
    '\u0637': '\x04\u2013',
    '\u0628': '\x04\u201a',
    '\u0646': '\x04\xa0',
    '\u0645': '\x04\u0178',
    '\u060c': '\x04\xed',
    '\u06d4': '\x04\xf3',
    '\u064b': '\x04\xc7',
    '\u064a': '\x04\xb8',
    '\u0610': '\x04\xf8',
    '\u0626': '\x04\xa3',
    '\u064c': '\x04\xb5',
    '\u0651': '\x04\xad',
    '\u0652': '\x04\xb1',
    '\ufdfa': '\x04\xf6',
    '\u0611': '\x04\xae',
    '\u0691': '\x04\x8f',
    '\u0679': '\x04\u2026',
    '\u0601': '\x04\xf7',
    '\u0657': '\x04\xbe',
    '\u0670': '\x04\xbd',
    '\u06c3': '\x04\xb9',
    '\u064f': '\x04\xac',
    '\u2018': '\x04\xfd',
    '\u2019': '\x04\xfe',
    '\u0614': '\x04\xcf',
    '\u0653': '\x04\xb3',
    '\u0635': '\x04\u201d',
    '\u0688': '\x04\u0152',
    '\u0656': '\x04\xb0',
    '\u063a': '\x04\u2122',
    '\u062d': '\x04\u2030',
    '\u0636': '\x04\u2022',
    '\u062e': '\x04\u0160',
    '\u0612': '\x04\xe7',
    '\u0630': '\x04\x8d',
    '\u0698': '\x04\u2018',
    '\u062b': '\x04\u2020',
    '\u0638': '\x04\u2014',
    '\u0613': '\x04\xe6',
    '\u0650': '\x04\xaa',
    '\u064e': '\x04\xab',
    '\u061f': '\x04\xee',
    '[': '\x04\xfa',
    ']': '\x04\xfb',
    '.': '\x04\xfc',
    '!': '\x04\xda',
    ',': '\x04\xf9',
    '/': '\x04\xf1',
    ')': '\x04\xe1',
    '(': '\x04\xe2',
    ':': '\x04\xe9',
    'ـ': '\x04\xa9',
    ' ': '\x04 ',
    '': '\x04\xb4',
}

MANUAL_KEYS = {
    '\x04\xa9', '\x04\xfd', '\x04\xfe',
    '\x04\xa3\x04\xa2', '\x04\xbf\x04\xa2', '\x04\xbf\x04\xa6',
    '\x04\xa3\x04\xa6', '\x04\xa2\x04\xbf', '\x04\xa6\x04\xbf'
}

# Precompile pattern to perform a single-pass regex replacement instead of 110 separate replace passes
sorted_keys = sorted([k for k in ITU_MAP if k not in MANUAL_KEYS], key=len, reverse=True)
ITU_REGEX = re.compile("|".join(re.escape(k) for k in sorted_keys))


def inpage_to_unicode(text: str, options: dict = None) -> str:
    """
    Convert legacy InPage-encoded Urdu text to standard Unicode.
    
    Args:
        text (str): Legacy InPage characters.
        options (dict, optional): Dict to override DEFAULT_OPTIONS.
        
    Returns:
        str: Unicode Urdu text.
    """
    opts = DEFAULT_OPTIONS.copy()
    if options:
        opts.update(options)
        
    if not text:
        return ""

    # Preprocess text to add \x04 prefix to characters that are not preceded by it
    # and are not control/whitespace characters (except space). This allows
    # converting pasted InPage text which is in CP-1252 encoding and doesn't contain \x04.
    text = re.sub(r'(?<!\x04)([^\r\n\t\x04])', "\x04\\1", text)


    # 1. Multi-character contextual replacements (Heh-Hamza combinations)
    if opts['heh_hamza']:
        text = text.replace('\x04\xa3\x04\xa2', 'ؤ')
        text = text.replace('\x04\xbf\x04\xa2', 'ؤ')
        text = text.replace('\x04\xbf\x04\xa6', 'ۂ')
        text = text.replace('\x04\xa3\x04\xa6', 'ۂ')
        text = text.replace('\x04\xa2\x04\xbf', 'ؤ')
        text = text.replace('\x04\xa6\x04\xbf', 'ۂ')
    else:
        text = text.replace('\x04\xa3\x04\xa2', 'ئو')
        text = text.replace('\x04\xbf\x04\xa2', 'ئو')
        text = text.replace('\x04\xbf\x04\xa6', 'ئہ')
        text = text.replace('\x04\xa3\x04\xa6', 'ئہ')
        text = text.replace('\x04\xa2\x04\xbf', 'ئو')
        text = text.replace('\x04\xa6\x04\xbf', 'ئہ')

    # 2. Kashida handling
    if opts['remove_kashida']:
        text = text.replace('\x04\xa9', '')
    else:
        text = text.replace('\x04\xa9', 'ـ')

    # 3. Quotation marks handling
    if opts['reverse_quotes']:
        text = text.replace('\x04\xfe', '’')
        text = text.replace('\x04\xfd', '‘')
    else:
        text = text.replace('\x04\xfd', '’')
        text = text.replace('\x04\xfe', '‘')

    # 4. Apply standard mappings (excluding the ones handled manually above) in a single regex pass
    text = ITU_REGEX.sub(lambda m: ITU_MAP[m.group(0)], text)

    # Strip any remaining \x04 characters that did not map
    text = text.replace('\x04', '')

    # 5. Digit Reversal for Numbers/Digits (LTR display)
    if opts['reverse_digits']:
        if opts['thousands_separator'] and opts['reverse_s_sign']:
            # Matches Urdu digits mixed with arithmetic symbols
            pattern = r"[۰-۹][۰-۹/+×\u00f7%,]*"
            def repl_digits(match):
                val = match.group(0)
                if val.endswith('/'):
                    return val[:-1][::-1] + '/'
                return val[::-1]
            text = re.sub(pattern, repl_digits, text)
        else:
            pattern = r"[۰-۹]+"
            text = re.sub(pattern, lambda m: m.group(0)[::-1], text)

    # 6. Linguistic corrections and normalization
    alphabet_chars = "ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکكگلمنوئیےؤهۂةأـآيھإہۃں"
    ahrab_chars = "ًٌٍَُِّٰٖٗ"
    
    # Reverse solidus equal combination
    text = text.replace('/=', '=/')
    
    # Noon Ghunna spacing inside words
    text = re.sub(f"(ں)([{alphabet_chars}])", r"\1 \2", text)
    
    # Double Hamza correction
    text = text.replace('ءء', 'ئء')
    
    # Hamza in middle of word
    text = re.sub(f"ء([{alphabet_chars}])", r"ئ\1", text)
    text = re.sub(f"ء([{ahrab_chars}])([{alphabet_chars}])", r"ئ\1\2", text)
    
    # Bari Yee contextual correction
    if opts['bari_yee']:
        text = re.sub(f"ے([{alphabet_chars}])", r"ی\1", text)
        
    # Arabic Yeh spacing
    text = re.sub(f"(ي)([{alphabet_chars}])", r"\1 \2", text)
    
    # Year sign alignment
    if opts['year_sign']:
        text = re.sub(r"(ھ)(؁)", r"\2\1", text)
        text = re.sub(r"(ء)(؁)", r"\2\1", text)
        
    # Double space removal
    if opts['remove_double_space']:
        text = re.sub(r"[ ]+", " ", text)
        
    # Erab/diacritic removal
    if opts['remove_erabs']:
        text = re.sub(f"[{ahrab_chars}]", "", text)
        
    return text


def unicode_to_inpage(text: str, options: dict = None) -> str:
    """
    Convert standard Unicode Urdu text to legacy InPage encoding.
    
    Args:
        text (str): Unicode Urdu text.
        options (dict, optional): Dict to override DEFAULT_OPTIONS.
        
    Returns:
        str: InPage encoded text.
    """
    opts = DEFAULT_OPTIONS.copy()
    if options:
        opts.update(options)

    if not text:
        return ""

    # 1. Digit Reversal for Numbers/Digits (as InPage expects them reversed in raw streams)
    if opts['reverse_digits']:
        if opts['thousands_separator'] and opts['reverse_s_sign']:
            pattern = r"[۰-۹][۰-۹/+×\u00f7%,]*"
            def repl_digits(match):
                val = match.group(0)
                if val.endswith('/'):
                    return val[:-1][::-1] + '/'
                return val[::-1]
            text = re.sub(pattern, repl_digits, text)
        else:
            pattern = r"[۰-۹]+"
            text = re.sub(pattern, lambda m: m.group(0)[::-1], text)

    # 2. Multi-character replacements (longest first)
    text = text.replace('\u06cc\u0626', '\x04\xa4\x04\xbf')
    text = text.replace('\u0627\x04\x08', '\x04\x81\x04\x08')
    
    # 3. Character-by-character translation
    result = []
    for char in text:
        result.append(UTI_MAP.get(char, char))
        
    return "".join(result)
