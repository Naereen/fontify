import string

TMPL_OPTIONS = {
    'page-size': 'Letter'
}

ROWS = 8
COLUMNS = 8
PERCENTAGE_TO_CROP_SCAN_IMG = 0.008

CROPPED_IMG_NAME = "cropped_picture.bmp"
CUT_CHAR_IMGS_DIR = "cutting_output_images"


def get_flat_chars():
    chars  = unicode(string.lowercase)
    chars += unicode(string.uppercase)
    chars += unicode(string.digits)
    # chars += unicode(string.punctuation)
    # XXX Check that this works!
    chars += unicode(u"!\"$&'(),-.:;?¡«»¿")
    chars += unicode(u"/\\#~{}[]|_@+*$")
    chars += unicode(u"àáâäçèéêëîíïñòóôöŷÿùúüû")
    chars += unicode(u"ÀÁÂÄÇÈÉÊËÎÍÏÑÒÓÔÖŶŸÙÚÜÛ")
    chars += unicode(u"æœßÆŒ")
    # Greek
    # chars += unicode(u"΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώ")
    return chars


def get_grouped_chars():
    chars = get_flat_chars()
    return [
        chars[i:i + COLUMNS]
        for i in xrange(0, len(chars), COLUMNS)
    ]


def get_chars():
    chars = get_grouped_chars()
    chars[-1] = chars[-1].ljust(COLUMNS)
    chars.extend([
        ' ' * COLUMNS
        for i in xrange(len(chars), ROWS)
    ])
    return chars


def get_sample_chars():
    return iter("AaBb")
