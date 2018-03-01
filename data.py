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

ROWS = 9
# print("ROWS =", ROWS)  # DEBUG
COLUMNS = 9
# print("COLUMNS =", COLUMNS)  # DEBUG
PERCENTAGE_TO_CROP_SCAN_IMG = 0.008

# Use the extended charset or not
EXTENDED = True
EXTENDED = False

CROPPED_IMG_NAME = "cropped_picture.bmp"
CUT_CHAR_IMGS_DIR = "cutting_output_images"


def get_flat_chars(extended=EXTENDED):
    # ASCII letters
    chars  = unicode(string.lowercase)
    chars += unicode(string.uppercase)
    # Numbers
    chars += unicode(string.digits)
    if not extended:
        chars += unicode(string.punctuation)
    else:
        # Punctuations and symbols
        chars += unicode(u"!\"$&'(),-.:;?")
        chars += unicode(u"/\\#~{}[]|_@+*$`")
        # Some basic ligatures
        chars += unicode(u"æœßÆŒ")
        # Special ligatures
        # https://en.wikipedia.org/wiki/Typographic_ligature#Ligatures_in_Unicode_(Latin_alphabets)
        chars += unicode(u"ﬀﬁﬂﬃﬄﬅﬆ")
        return chars
        # FIXME remove when done testing!
        chars += unicode(u"🙰")
        # French and Spanish accents
        chars += unicode(u"àáâäçèéêëîíïñòóôöŷÿùúüû")
        chars += unicode(u"ÀÁÂÄÇÈÉÊËÎÍÏÑÒÓÔÖŶŸÙÚÜÛ")
        # non ASCII symbols (currency etc)
        chars += unicode(u"£¥₩€₹₺₽元…¡«»¿‘’“”")
        # Greek upper and lower
        chars += unicode(u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
        chars += unicode(u"αβγδεζηθικλμνξοπρςστυφχψω")
        # Greek special caracters, nobody use that
        # chars += unicode(u"΄΅Ά·ΈΉΊΌΎΏΐΪΫάέήίΰϊϋόύώ")
        # Maths
        chars += unicode(u"°ℕℝℂℙℤℚ±×÷ø–—‰′″‴→↓↑←↔⇒⇔∀∂∃∅∇∈∉∏∑√∛∝∞∧∨∩∪∫∬∭∮∯∰∴∵≈≝≠≡≤≥≪≫⊂⊃⊄⊆⊈⊕")
    return chars


def get_grouped_chars():
    chars = get_flat_chars()
    MDIM = max(ROWS, COLUMNS)
    grouped_chars = [
        chars[i: i + MDIM]
        for i in xrange(0, len(chars), MDIM)
    ]
    # print("grouped_chars =", grouped_chars)  # DEBUG
    return grouped_chars


def get_chars():
    # mDIM, MDIM = min(ROWS, COLUMNS), max(ROWS, COLUMNS)
    chars = get_grouped_chars()
    chars[-1] = chars[-1].ljust(COLUMNS)
    chars.extend([
        ' ' * ROWS
        for i in xrange(len(chars), ROWS)
    ])
    # print("chars =", chars)  # DEBUG
    return chars


def get_chars_by_page():
    chars = get_flat_chars()
    grouped_chars = [
        chars[i: i + COLUMNS]
        for i in xrange(0, len(chars), COLUMNS)
    ]
    grouped_chars[-1] = grouped_chars[-1].ljust(COLUMNS)
    grouped_chars.extend([
        ' ' * ROWS
        for i in xrange(len(grouped_chars), ROWS)
    ])
    # print("grouped_chars =", grouped_chars)  # DEBUG
    # print("len(grouped_chars =", len(grouped_chars))  # DEBUG
    # print("ROWS =", ROWS)  # DEBUG
    nb_page = int(ceil(len(grouped_chars) / ROWS))
    # print("nb_page =", nb_page)  # DEBUG
    grouped_chars_by_page = [
        [
            grouped_chars[i]
            for i in xrange(page*ROWS, min((page+1)*ROWS, len(grouped_chars)))
        ]
        for page in xrange(0, nb_page)
    ]
    # print("grouped_chars_by_page =", grouped_chars_by_page)  # DEBUG
    return grouped_chars_by_page


def get_sample_chars():
    return iter(u"AaΩω")
    # return iter("AaBb")
