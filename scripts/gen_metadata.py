#!/usr/bin/env python2
# -*- coding: utf8 -*-
import sys
import json
import os
import re

from datetime import datetime
import locale  # See this bug, http://numba.pydata.org/numba-doc/dev/user/faq.html#llvm-locale-bug
locale.setlocale(locale.LC_TIME, 'C')
prettydate = '{:%H:%M, %d %B %Y}'.format(datetime.today()).title()  #: Month.Year date

from data import str_to_hex
from data import get_flat_chars
from data import get_flat_ligatures  # FIXME add support for ligatures

# sys arguments  # FIXME use a cli parser?
family = sys.argv[1]
input = sys.argv[2]
output = sys.argv[3]
style = sys.argv[4] if len(sys.argv) > 4 else "Regular"

metadata = {
    # Cf. https://fontforge.github.io/python.html#Font
    # And https://stackoverflow.com/a/27631737/ can help
    "props": {
        "ascent": 800,
        "descent": 200,
        "em": 1000,  # XXX default
        # "em": 800,  # XXX try to reduce horizontal lengths of each glyph
        "encoding": "UnicodeFull",
        "lang": "English (US)",
        "style": style,
        "family": family,
        "familyname": family,
        "fontname": "{}-{}".format(family, style),
        "fullname": "{} {}".format(family, style),
        "comment": "Created the {}, using the MIT-licensed open-source Python software Fontify, see https://github.com/Naereen/fontify".format(prettydate),
    },
    "input": input,
    "output": [output],
    "glyphs": {}
}

chars = get_flat_chars()

space_width = 280.0
min_width = 400.0
max_width = 0.0


for c in chars:
    # glyph_key = str(hex(ord(c)))
    glyph_key = str_to_hex(c)
    svg_name = glyph_key + ".svg"
    svg_path = os.path.join(sys.argv[2], svg_name)
    if not os.path.isfile(svg_path):
        sys.stderr.write(u"File {:>10} for glyph {:>4} not exists, skipped.\n".format(svg_name, c))
        continue

    with open(svg_path) as f:
        content = f.read()
        result = re.search('width="(\d+\.\d+)pt"', content)
        width = float(result.groups()[0]) / 72. * 1000
        max_width = max(max_width, width)

    width = max(min_width, width)
    if c == ' ':
        width = space_width
    sys.stderr.write(u"For character '{}', using file at '{}', of width '{}'...\n".format(glyph_key, svg_name, width))  # DEBUG

    metadata["glyphs"][glyph_key] = {
        "src": svg_name,
        "width": width,
    }

    # # https://fontforge.github.io/en-US/documentation/scripting/python/#g-addAnchorPoint
    # # ("anchor-class-name", "type", "x", "y", "ligature-index")
    # 1. for a ligature of 2 characters
    # "anchorPoints": [
    #     ("anchor-class-name", "ligature", 0, 0, 0),
    #     ("anchor-class-name", "ligature", width/2., 0, 1),
    # ]
    # 2. for a ligature of 3 characters
    # "anchorPoints": [
    #     ("anchor-class-name", "ligature", 0, 0, 0),
    #     ("anchor-class-name", "ligature", width/3., 0, 1),
    #     ("anchor-class-name", "ligature", 2. * width/3., 0, 2),
    # ]
    # if '_' in svg_name:
    #     # we have a glyph!
    #     length_of_glyph = svg_name.count('_') + 1
    #     metadata["glyphs"][glyph_key]["anchorPoints"] = [
    #         ("anchor-class-name", "ligature", float(i) * width/length_of_glyph, 0, i)
    #         for i in range(length_of_glyph)
    #     ]


# # XXX Weird hack for just the space?
# if ' ' not in chars:
#     width = max_width
#     c = ' '
#     glyph_key = str(hex(ord(c)))
#     svg_name = glyph_key + ".svg"
#     svg_path = os.path.join(sys.argv[2], svg_name)
#     # FIXME create the empty SVG!
#     if not os.path.isfile(svg_path):
#         sys.stderr.write(u"File {:>10} for glyph {:>4} do not exists, skipped.\n".format(svg_name, c))
#     else:
#         metadata["glyphs"][glyph_key] = {
#             "src": svg_name,
#             "width": width,
#         }

print(json.dumps(metadata, indent=2))
