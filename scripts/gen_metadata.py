#!/usr/bin/env python2
# -*- coding: utf8 -*-
import sys
import json
import os
import re

from data import get_flat_chars

metadata = {
    "props": {
        "ascent": 800,
        "descent": 200,
        "em": 1000,
        "encoding": "UnicodeFull",
        "lang": "English (US)",
        "style": sys.argv[4],
        "family": sys.argv[1],
        "familyname": sys.argv[1],
        "fontname": "{}-{}".format(sys.argv[1], sys.argv[4]),
        "fullname": "{} {}".format(sys.argv[1], sys.argv[4]),
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
