# -*- coding: utf8 -*-
from __future__ import print_function, division
from math import ceil
import string

# Options, see https://github.com/JazzCore/python-pdfkit
TMPL_OPTIONS = {
    # 'page-size': 'Letter',
    # 'print-media-type': False,
    'encoding': 'UTF-8',
    'margin-top': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'margin-right': '0.5in',
}

# FIXME don't change now!
ROWS = 9
COLUMNS = 9
# print("Shape of the characters: on {} rows and {} columns...".format(ROWS, COLUMNS))  # DEBUG
PERCENTAGE_TO_CROP_SCAN_IMG = 0.008

# Use the extended charset or not
EXTENDED = False
EXTENDED = True

FULL = False

CROPPED_IMG_NAME = "cropped_picture"
CROPPED_IMG_EXT = "bmp"
CUT_CHAR_IMGS_DIR = "cutting_output_images"


def get_flat_chars(extended=EXTENDED, full=FULL):
    # ASCII letters
    chars  = unicode(string.lowercase)
    chars += unicode(string.uppercase)
    # Numbers
    chars += unicode(string.digits)
    if not extended:
        chars += unicode(string.punctuation)
    else:
        # Punctuations and symbols
        chars += unicode(u"!?\"$&'(),-.:;")
        chars += unicode(u"/\\#~{}[]|_@+*`§%^")
        # French and Spanish accents
        chars += unicode(u"àáâäçèéêëîíïñòóôöŷÿùúüû")
        chars += unicode(u"ÀÁÂÄÇÈÉÊËÎÍÏÑÒÓÔÖŶŸÙÚÜÛ")
        # Some basic ligatures
        chars += unicode(u"æœßÆŒ")
        # non ASCII symbols (currency etc)
        chars += unicode(u"£€…¡¿")
        chars += unicode(u"«»‘’“”")
        # chars += unicode(u"  ")  # space and unbreakable-space  
        # Greek upper and lower
        chars += unicode(u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
        chars += unicode(u"αβγδεζηθικλμνξοπρςστυφχψω")
        if not full:
            return chars
        # Special ligatures
        # https://en.wikipedia.org/wiki/Typographic_ligature#Ligatures_in_Unicode_(Latin_alphabets)
        chars += unicode(u"ﬀﬁﬂﬃﬄﬅﬆ")
        chars += unicode(u"🙰")
        # non ASCII symbols (currency etc)
        chars += unicode(u"¥₩₹₺₽元")
        # Greek special caracters, nobody use that!
        # chars += unicode(u"΄΅Ά·ΈΉΊΌΎΏΐΰ")
        chars += unicode(u"ΪΫάέήίϊϋόύώ")
        # Maths
        chars += unicode(u"ℕℝℂℙℤℚ∀∂∃∅∇∩∪∫≠≤≥⊂⊃")
        chars += unicode(u"°±×÷ø–—‰′″‴→↓↑←↔⇒⇔∈∉∏∑√∛∝∞∧∨∬∭∮∯∰∴∵≈≝≠≡≪≫⊄⊆⊈⊕")
    return chars


def get_grouped_chars():
    chars = get_flat_chars()
    MDIM = max(ROWS, COLUMNS)
    grouped_chars = [
        chars[i: i + MDIM]
        for i in range(0, len(chars), MDIM)
    ]
    # print("grouped_chars =", grouped_chars)  # DEBUG
    return grouped_chars


def get_chars():
    chars = get_grouped_chars()
    chars[-1] = chars[-1].ljust(COLUMNS)
    chars.extend([
        ' ' * ROWS
        for i in range(len(chars), ROWS)
    ])
    # print("chars =", chars)  # DEBUG
    return chars


def get_chars_by_page(hack_for_last_bottom_right_cell=False):
    chars = get_flat_chars()
    if hack_for_last_bottom_right_cell:
        grouped_chars = []
        # This small hack is to avoid having the big black dot in the last bottom right cell (ugly as I can't remove it easily...)
        delta = 0
        for i in range(0, len(chars), COLUMNS):
            if ((i//COLUMNS) % ROWS) == (ROWS - 1):
                grouped_chars.append(chars[delta + i: delta + i + COLUMNS - 1] + ' ')
                delta -= 1
            else:
                grouped_chars.append(chars[delta + i: delta + i + COLUMNS])
    else:
        grouped_chars = [
            chars[i: i + COLUMNS]
            for i in range(0, len(chars), COLUMNS)
        ]

    grouped_chars[-1] = grouped_chars[-1].ljust(COLUMNS)
    grouped_chars.extend([
        ' ' * ROWS
        for i in range(len(grouped_chars), ROWS)
    ])
    # print("grouped_chars =", grouped_chars)  # DEBUG
    # print("len(grouped_chars =", len(grouped_chars))  # DEBUG
    # print("ROWS =", ROWS)  # DEBUG
    nb_page = int(ceil(len(grouped_chars) / ROWS))
    # print("nb_page =", nb_page)  # DEBUG
    grouped_chars_by_page = [
        [
            grouped_chars[i]
            for i in range(page*ROWS, min((page+1)*ROWS, len(grouped_chars)))
        ]
        for page in range(0, nb_page)
    ]
    # print("grouped_chars_by_page =", grouped_chars_by_page)  # DEBUG
    return grouped_chars_by_page


def get_sample_chars():
    return iter(u"AaΩω")
