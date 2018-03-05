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

from data import get_flat_chars

metadata = {
    # Cf. https://fontforge.github.io/python.html#Font
    # And https://stackoverflow.com/a/27631737/ can help
    "props": {
        "ascent": 800,
        "descent": 200,
        # "em": 1000,  # XXX default
        "em": 900,  # XXX try to reduce horizontal lengths of each glyph
        "encoding": "UnicodeFull",
        "lang": "English (US)",
        "style": sys.argv[4],
        "family": sys.argv[1],
        "familyname": sys.argv[1],
        "fontname": "{}-{}".format(sys.argv[1], sys.argv[4]),
        "fullname": "{} {}".format(sys.argv[1], sys.argv[4]),
        "comment": "Created the {}, using the MIT-licensed open-source Python software Fontify, see https://github.com/Naereen/fontify".format(prettydate),
    },
    "input": sys.argv[2],
    "output": [sys.argv[3]],
    "glyphs": {}
}

chars = get_flat_chars()

for c in chars:
    glyph_key = str(hex(ord(c)))
    svg_name = glyph_key + ".svg"
    svg_path = os.path.join(sys.argv[2], svg_name)
    if not os.path.isfile(svg_path):
        sys.stderr.write(u"File {:>10} for glyph {:>4} not exists, skipped.\n".format(svg_name, c))
        continue

    with open(svg_path) as f:
        content = f.read()
        result = re.search('width="(\d+\.\d+)pt"', content)
        width = float(result.groups()[0]) / 72 * 1000

    metadata["glyphs"][glyph_key] = {
        "src": svg_name,
        "width": width
    }

print(json.dumps(metadata, indent=2))
