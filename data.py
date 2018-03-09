#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function, division

try:  # python 2/3 compatibility
    unicode
except NameError:
    unicode = str

from math import ceil
import string


# --- Constants to configure the application

# Options, see https://github.com/JazzCore/python-pdfkit
TMPL_OPTIONS = {
    # 'page-size': 'Letter',
    # 'print-media-type': False,
    'encoding': 'UTF-8',
    'margin-top': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'margin-right': '0.5in',
    # 'user-style-sheet': '/tmp/static/css/template.css',
}

# WARNING don't change now! everything works, DON'T CHANGE THIS!
ROWS = 9
COLUMNS = 9
# print("Shape of the characters: on {} rows and {} columns...".format(ROWS, COLUMNS))  # DEBUG
PERCENTAGE_TO_CROP_SCAN_IMG = 0.008

# Use the extended charset or not
EXTENDED = True
EXTENDED = False  # only for debugging
# Use the full charset or not
FULL = False

CROPPED_IMG_NAME = "cropped_picture"
CROPPED_IMG_EXT = "bmp"
CUT_CHAR_IMGS_DIR = "cutting_output_images"


# --- utility function

def _ljust(input, width, fillchar=None):
    """Either ljust on a string or a list of string. Extend with fillchar."""
    if fillchar is None:
        fillchar = ' '
    if isinstance(input, str):
        return input.ljust(width, fillchar)
    else:
        delta_len = width - len(input)
        if delta_len <= 0:
            return input
        else:
            return input + [fillchar for _ in range(delta_len)]


# --- get list of unicode characters or ligatures

def get_flat_chars(extended=EXTENDED, full=FULL):
    """ Return a list of unicode characters for each single-width character."""
    chars = []
    # ASCII letters
    chars += list(unicode(string.ascii_lowercase))
    chars += list(unicode(' '))
    return chars  # FIXME
    chars += list(unicode(string.ascii_uppercase))
    # Numbers
    chars += list(unicode(string.digits))
    if not extended:
        chars += list(unicode(string.punctuation))
        # # French accents
        # chars += list(unicode(u"àçèéêëîïôÿúüû"))
        # chars += list(unicode(u"ÀÇÈÉÊËÎÏÔŸÚÜÛ"))
    else:
        # Punctuations and symbols
        chars += list(unicode(u"!?\"$&'(),-.:;"))
        chars += list(unicode(u"/\\#~{}[]|_@+*`§%^<>="))
        # French and Spanish accents
        chars += list(unicode(u"àáâäçèéêëîíïñòóôöŷÿùúüû"))
        chars += list(unicode(u"ÀÁÂÄÇÈÉÊËÎÍÏÑÒÓÔÖŶŸÙÚÜÛ"))
        # Some basic ligatures
        chars += list(unicode(u"æœßÆŒ"))
        # non ASCII symbols (currency etc)
        chars += list(unicode(u"£€…¡¿"))
        chars += list(unicode(u"«»‘’“”"))
        # chars += list(unicode(u"  "))  # space ' ' and unbreakable-space ' '
        # Greek upper and lower
        chars += list(unicode(u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"))
        chars += list(unicode(u"αβγδεζηθικλμνξοπρςστυφχψω"))
        if not full:
            return chars
        # Special ligatures
        # https://en.wikipedia.org/wiki/Typographic_ligature#Ligatures_in_list(unicode_(Latin_alphabets)
        chars += list(unicode(u"ﬀﬁﬂﬃﬄﬅﬆ"))
        chars += list(unicode(u"🙰"))
        # non ASCII symbols (currency etc)
        chars += list(unicode(u"¥₩₹₺₽元"))
        # Greek special caracters, nobody use that!
        # chars += list(unicode(u"΄΅Ά·ΈΉΊΌΎΏΐΰ"))
        chars += list(unicode(u"ΪΫάέήίϊϋόύώ"))
        # Maths
        chars += list(unicode(u"ℕℝℂℙℤℚ∀∂∃∅∇∩∪∫≠≤≥⊂⊃"))
        chars += list(unicode(u"°±×÷ø–—‰′″‴→↓↑←↔⇒⇔∈∉∏∑√∛∝∞∧∨∬∭∮∯∰∴∵≈≝≠≡≪≫⊄⊆⊈⊕"))
    return chars


def get_flat_ligatures(extended=EXTENDED, full=FULL):
    """ Return a list of unicode characters for each ligature."""
    ligatures = []
    # ligatures += [u"ﬀ", u"ﬁ", u"ﬂ", u"ﬃ", u"ﬄ", u"ﬅ", u"ﬆ", u"🙰"]
    ligatures += [u"ff", u"fi", u"fl", u"ffi", u"ffl", u"ft", u"st", u"et"]
    # then from other ligatures
    ligatures += [u"fa", u"fe", u"fj", u"fo", u"fr", u"fs", u"ft", u"fft", u"fb", u"ffb", u"fh", u"ffh", u"fu", u"fy"]
    ligatures += [u"ij", ]
    ligatures += [u"ct", u"ch", u"ck", u"tt", ]
    if not extended:
        return ligatures
    # and now from FiraCode, line by line, code-related ligatures
    # from https://github.com/tonsky/FiraCode/#solution
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

    if not full:
        return ligatures

    # mine, extra... LaTeX related
    ligatures += [u"TeX", u"LaTeX", u"KaTeX", u"XeLaTeX", ]
    # FIXME don't do that... please...
    ligatures += [u"Lilian", u"Besson", u"Naereen", ]

    return ligatures


# --- get grouped data (unused)

def _get_grouped(get_flat_input):
    inputs = get_flat_input()
    grouped_inputs = [
        inputs[i: i + ROWS]
        for i in range(0, len(inputs), ROWS)
    ]
    # print("grouped_inputs =", grouped_inputs)  # DEBUG
    return grouped_inputs


def get_grouped_chars(): return _get_grouped(get_flat_chars)
def get_grouped_ligatures(): return _get_grouped(get_flat_ligatures)

# --- get grouped and padded data (non used)

def _get_grouped_and_padded(get_grouped_inputs):
    inputs = get_grouped_inputs()
    inputs[-1] = _ljust(inputs[-1], COLUMNS)
    inputs.extend([
        ' ' * ROWS
        for i in range(len(inputs), ROWS)
    ])
    # print("inputs =", inputs)  # DEBUG
    return inputs


def get_chars(): return _get_grouped_and_padded(get_grouped_chars)
def get_ligatures(): return _get_grouped_and_padded(get_grouped_ligatures)


# --- get data grouped by pages

def _get_by_page(get_flat_inputs):
    inputs = get_flat_inputs()
    grouped_inputs = [
        inputs[i: i + COLUMNS]
        for i in range(0, len(inputs), COLUMNS)
    ]

    grouped_inputs[-1] = _ljust(grouped_inputs[-1], COLUMNS)
    grouped_inputs.extend([
        ' ' * ROWS
        for i in range(len(grouped_inputs), ROWS)
    ])
    # print("grouped_inputs =", grouped_inputs)  # DEBUG
    # print("len(grouped_inputs =", len(grouped_inputs))  # DEBUG
    # print("ROWS =", ROWS)  # DEBUG
    nb_page = int(ceil(len(grouped_inputs) / ROWS))
    # print("nb_page =", nb_page)  # DEBUG
    grouped_inputs_by_page = [
        [
            grouped_inputs[i]
            for i in range(page*ROWS, min((page+1)*ROWS, len(grouped_inputs)))
        ]
        for page in range(0, nb_page)
    ]
    # print("grouped_inputs_by_page =", grouped_inputs_by_page)  # DEBUG
    return grouped_inputs_by_page


def get_chars_by_page(): return _get_by_page(get_flat_chars)
def get_ligatures_by_page(): return _get_by_page(get_flat_ligatures)


# --- sample characters (in light gray in the template)

def _get_sample_chars(test_unicode=True):
    # WARNING the leading space ' ' char is because there is a space in the data
    if test_unicode:
        return iter(u" AaΩω")
    else:
        return iter(u" AaZz")


def get_sample_chars_no_unicode(): return _get_sample_chars(test_unicode=False)
def get_sample_chars(): return _get_sample_chars(test_unicode=True)


def get_sample_ligatures():
    return iter([u"ff", u"st"])


# --- Now we test everything

if __name__ == '__main__':
    print("DEBUG: data.py")  # DEBUG
    for f in [
            # --- samples
            get_sample_chars, get_sample_chars_no_unicode,
            get_sample_ligatures,
            # --- chars
            get_flat_chars,
            # get_grouped_chars,
            # get_chars,
            get_chars_by_page,
            # --- ligatures
            get_flat_ligatures,
            # get_grouped_ligatures,
            # get_ligatures,
            get_ligatures_by_page,
        ]:
        # get name and get data
        name = f.__name__
        data = f()
        # convert the iterators to list...
        if isinstance(data, type(iter(u'okok'))) or isinstance(data, type(iter([u'ok', u'ok']))):
            data = [ i for i in f() ]
            data = list(data)
        # DEBUG
        max_length_of_data = max(len(s) for s in data)
        print("\nThe function '{}' gives output of type {} and length {}, which is seen as data of type {}, each of max length {}...".format(name, type(data), len(data), type(data[0]), max_length_of_data))  # DEBUG

        # print(data)  # DEBUG

        # print the data correctly...
        if isinstance(data[0], list):
            if isinstance(data[0][0], list):
                for page, page_data in enumerate(data):
                    joined_data = [ u", ".join(x) for x in page_data ]
                    print("Page {}/{} has {} columns and {} rows, with {} data of max length {}:".format(page + 1, len(data), len(page_data), len(joined_data), sum([len(s) for s in page_data]), max([max([len(c) for c in x]) for x in page_data]) ))  # DEBUG
                    print(u"\t" + u"\n\t".join(joined_data))  # DEBUG
            else:
                for page, page_data in enumerate(data):
                    print(u", ".join(page_data))  # DEBUG
        else:
            print(u", ".join(data))  # DEBUG
