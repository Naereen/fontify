#! /usr/bin/env python
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
        chars += unicode(u"/\\#~{}[]|_@+*`§%^<>")
        # French and Spanish accents
        chars += unicode(u"àáâäçèéêëîíïñòóôöŷÿùúüû")
        chars += unicode(u"ÀÁÂÄÇÈÉÊËÎÍÏÑÒÓÔÖŶŸÙÚÜÛ")
        # Some basic ligatures
        chars += unicode(u"æœßÆŒ")
        # non ASCII symbols (currency etc)
        chars += unicode(u"£€…¡¿")
        chars += unicode(u"«»‘’“”")
        chars += unicode(u"  ")  # space ' ' and unbreakable-space ' '
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


def get_flat_ligatures():
    ligatures = []
    # ligatures += [u"ﬀ", u"ﬁ", u"ﬂ", u"ﬃ", u"ﬄ", u"ﬅ", u"ﬆ", u"🙰"]
    ligatures += [u"ff", u"fi", u"fl", u"ffi", u"ffl", u"ft", u"st", u"et"]
    # then from other ligatures
    ligatures += [u"fa", u"fe", u"fj", u"fo", u"fr", u"fs", u"ft", u"fft", u"fb", u"ffb", u"fh", u"ffh", u"fu", u"fy"]
    ligatures += [u"ij", ]
    ligatures += [u"ct", u"ch", u"ck", u"tt", ]
    # and now from FiraCode, line by line from https://github.com/tonsky/FiraCode/#solution
    ligatures += [u".=", u"..=", u".-", u":=", u"=:=", u"=!=", u"__", ]
    ligatures += [u"==", u"!=", u"===", u"!==", u"=/=", ]

    ligatures += [u"<-<", u"<<-", u"<--", u"<-", u"<->", u"->", u"-->", u"->>", u">->", ]
    ligatures += [u"<=<", u"<<=", u"<==",        u"<=>", u"=>", u"==>", u"=>>", u">=>", ]
    ligatures += [u">>=", u">>-", u">-", u"<~>", u"-<", u"-<<", u"=<<", ]
    ligatures += [u"<~~", u"<~", u"~~", u"~>", u"~~>", ]

    ligatures += [u"<<<", u"<<", u"<=", u"<>", u">=", u">>", u">>>", ]
    ligatures += [u"{.", u"{|", u"[|", u"<:", u":>", u"|]", u"|}", u".}", ]
    ligatures += [u"<|||", u"<||", u"<|", u"<|>", u"|>", u"||>", u"|||>", ]
    ligatures += [u"<$", u"<$>", u"$>", ]
    ligatures += [u"<+", u"<+>", u"+>", ]
    ligatures += [u"<*", u"<*>", u"*>", ]

    ligatures += [u"/*", u"*/", u"///", u"//", ]
    ligatures += [u"</", u"<!--", u"</>", u"/>", ]

    # XXX these are harder, we would need to work on contextual vertical align...
    # ligatures += [u"0xf", u"10x10", ]  # WARNING
    # ligatures += [u"9:45", u"m+x", u"m-x", u"*ptr", ]  # WARNING

    ligatures += [u";;", u"::", u":::", u"[:]", u"..", u"...", u"..<", ]
    ligatures += [u"!!", u"??", u"%%", u"&&", u"||", u"?.", u"?:", ]
    ligatures += [u"++", u"+++", ]
    ligatures += [u"--", u"---", ]
    ligatures += [u"**", u"***", ]

    ligatures += [u"~=", u"~-", u"www", u"-~", u"~@", ]
    ligatures += [u"^=", u"?=", u"/=", u"/==", ]
    ligatures += [u"+=", u"-=", u"*=", ]  # mine
    ligatures += [u"-|", u"_|_", u"|-", u"|=", u"||=", ]
    ligatures += [u"#!", u"#=", u"##", u"#:", u"###", u"####", u"#####", u"######", ]  # mine also
    ligatures += [u"#{", u"#}", u"#[", u"]#", u"#(", u"#)", u"#?", u"#_", u"#_(", u"#_)", ]  # some are extra

    return ligatures


def get_grouped_chars():
    chars = get_flat_chars()
    MDIM = max(ROWS, COLUMNS)
    grouped_chars = [
        chars[i: i + MDIM]
        for i in range(0, len(chars), MDIM)
    ]
    # print("grouped_chars =", grouped_chars)  # DEBUG
    return grouped_chars


def get_grouped_ligatures():
    ligatures = get_flat_ligatures()
    MDIM = max(ROWS, COLUMNS)
    grouped_ligatures = [
        ligatures[i: i + MDIM]
        for i in range(0, len(ligatures), MDIM)
    ]
    # print("grouped_ligatures =", grouped_ligatures)  # DEBUG
    return grouped_ligatures


def get_chars():
    chars = get_grouped_chars()
    chars[-1] = chars[-1].ljust(COLUMNS)
    chars.extend([
        ' ' * ROWS
        for i in range(len(chars), ROWS)
    ])
    # print("chars =", chars)  # DEBUG
    return chars


def get_ligatures():
    ligatures = get_grouped_ligatures()
    ligatures[-1] = ligatures[-1].ljust(COLUMNS)
    ligatures.extend([
        ' ' * ROWS
        for i in range(len(ligatures), ROWS)
    ])
    # print("ligatures =", ligatures)  # DEBUG
    return ligatures


def get_chars_by_page():
    chars = get_flat_chars()
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


def get_ligatures_by_page():
    ligatures = get_flat_ligatures()
    grouped_ligatures = [
        ligatures[i: i + COLUMNS]
        for i in range(0, len(ligatures), COLUMNS)
    ]

    grouped_ligatures[-1] = grouped_ligatures[-1].ljust(COLUMNS)
    grouped_ligatures.extend([
        ' ' * ROWS
        for i in range(len(grouped_ligatures), ROWS)
    ])
    # print("grouped_ligatures =", grouped_ligatures)  # DEBUG
    # print("len(grouped_ligatures =", len(grouped_ligatures))  # DEBUG
    # print("ROWS =", ROWS)  # DEBUG
    nb_page = int(ceil(len(grouped_ligatures) / ROWS))
    # print("nb_page =", nb_page)  # DEBUG
    grouped_ligatures_by_page = [
        [
            grouped_ligatures[i]
            for i in range(page*ROWS, min((page+1)*ROWS, len(grouped_ligatures)))
        ]
        for page in range(0, nb_page)
    ]
    # print("grouped_ligatures_by_page =", grouped_ligatures_by_page)  # DEBUG
    return grouped_ligatures_by_page


def _get_sample_chars(test_unicode=True):
    if test_unicode:
        return iter(u"AaΩω")
    else:
        return iter(u"AaZz")


def get_sample_chars_no_unicode(): return _get_sample_chars(test_unicode=False)
def get_sample_chars(): return _get_sample_chars(test_unicode=True)


# --- Now we test everything

if __name__ == '__main__':
    print("DEBUG: data.py")  # DEBUG
    for f in [
            get_sample_chars, get_sample_chars_no_unicode,
            get_flat_chars, get_chars, get_grouped_chars, get_chars_by_page,
            get_flat_ligatures, get_ligatures, get_grouped_ligatures, get_ligatures_by_page,
        ]:
        name = f.__name__
        data = list(f())
        max_length_of_data = max(len(s) for s in data)
        print("\nThe function '{}' gives {} unicode symbols of max length {}...".format(name, len(data), max_length_of_data))  # DEBUG
        if isinstance(data[0], list):
            for page, d in enumerate(data):
                print("Page", page, "gives:")  # DEBUG
                print(u", ".join(d))  # DEBUG
        else:
            print(u", ".join(data))  # DEBUG
