# -*- coding: utf8 -*-
from __future__ import print_function
import string

TMPL_OPTIONS = {
    'page-size': 'Letter'
}

ROWS = 6
print("ROWS =", ROWS)
COLUMNS = 9
print("COLUMNS =", COLUMNS)
PERCENTAGE_TO_CROP_SCAN_IMG = 0.008

CROPPED_IMG_NAME = "cropped_picture.bmp"
CUT_CHAR_IMGS_DIR = "cutting_output_images"


def get_flat_chars():
    # ASCII letters
    chars  = unicode(string.lowercase)
    chars += unicode(string.uppercase)
    # Numbers
    chars += unicode(string.digits)
    # Punctuations and symbols
    chars += unicode(u"!\"$&'(),-.:;?")
    chars += unicode(u"/\\#~{}[]|_@+*$`")
    # French and Spanish accents
    chars += unicode(u"àáâäçèéêëîíïñòóôöŷÿùúüû")
    chars += unicode(u"ÀÁÂÄÇÈÉÊËÎÍÏÑÒÓÔÖŶŸÙÚÜÛ")
    # Special ligatures
    chars += unicode(u"æœßÆŒ")
    # non ASCII symbols (currency etc)
    chars += unicode(u"£¥₩€₹₺₽元…¡«»¿‘’“”")
    # Greek upper and lower
    chars += unicode(u"ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
    chars += unicode(u"αβγδεζηθικλμνξοπρςστυφχψω")
    # Gree special caracters
    # chars += unicode(u"΄΅Ά·ΈΉΊΌΎΏΐΪΫάέήίΰϊϋόύώ")
    # Maths
    # FIXME remove the useless caracters nobody ever use
    chars += unicode(u"°±×÷ø–—‰′″‴→↔⇒⇔∀∂∃∅∇∈∉∏∑√∛∝∞∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵≈≝≠≡≤≥≪≫⊂⊃⊄⊆⊈⊕")
    # chars += unicode(u"∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆≇≈≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿")
    # Special ligatures
    # TODO
    return chars


def get_grouped_chars():
    chars = get_flat_chars()
    MDIM = max(ROWS, COLUMNS)
    grouped_chars = [
        chars[i: i + MDIM]
        for i in xrange(0, len(chars), MDIM)
    ]
    print("grouped_chars =", grouped_chars)
    return grouped_chars


def get_chars():
    # mDIM, MDIM = min(ROWS, COLUMNS), max(ROWS, COLUMNS)
    chars = get_grouped_chars()
    chars[-1] = chars[-1].ljust(COLUMNS)
    chars.extend([
        ' ' * ROWS
        for i in xrange(len(chars), ROWS)
    ])
    print("chars =", chars)
    return chars


def get_sample_chars():
    return iter("AaBb")
