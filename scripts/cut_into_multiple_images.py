#!/usr/bin/env python2
# -*- coding: utf8 -*-
from __future__ import print_function
import os
from PIL import Image

from data import COLUMNS, ROWS, get_chars, get_chars_by_page


def cut(page, filepath):
    im = Image.open(filepath)
    imdir = os.path.dirname(filepath)
    if imdir == "":
        imdir = "."
    bmp_dir = os.path.join(imdir, "bmp")
    if not os.path.exists(bmp_dir):
        os.mkdir(bmp_dir)
    else:
        if not os.path.isdir(bmp_dir):
            raise ValueError("Error: the file {} exists but should be a folder!".format(bmp_dir))  # DEBUG

    image_width, image_height = im.size
    print("image_width, image_height =", image_width, image_height)  # DEBUG

    chars_by_page = get_chars_by_page()
    # chars = get_chars()
    chars = chars_by_page[page]

    COLUMNS, ROWS = len(chars[0]), len(chars)
    print("COLUMNS, ROWS =", COLUMNS, ROWS)  # DEBUG

    cell_width = image_width / COLUMNS
    # print("cell_width =", cell_width)  # DEBUG
    cell_height = image_height / ROWS
    # print("cell_height =", cell_height)  # DEBUG
    width_limit = cell_width * COLUMNS
    # print("width_limit =", width_limit)  # DEBUG
    height_limit = cell_height * ROWS
    # print("height_limit =", height_limit)  # DEBUG


    for i in range(0, height_limit, cell_height):
        for j in range(0, width_limit, cell_width):
            char = chars[i / cell_height][j / cell_width]
            if char == ' ':
                return
            # print(u"\ni =", i, "j =", j, "char =", char)  # DEBUG
            bar_height = int(cell_height * 0.28333)
            # print("bar_height =", bar_height)  # DEBUG
            margin_width = int(cell_width * 0.1)
            # print("margin_width =", margin_width)  # DEBUG
            margin_height_top = int(cell_height * 0.005)
            # print("margin_height_top =", margin_height_top)  # DEBUG
            margin_height_bottom = int(cell_height * 0.01)
            # print("margin_height_bottom =", margin_height_bottom)  # DEBUG
            char_im = im.crop(
                (
                    j + margin_width,
                    i + bar_height + margin_height_top,
                    j + cell_width - margin_width,
                    i + cell_height - margin_height_bottom
                )
            )
            glyph_path = os.path.join(bmp_dir, "{}.bmp".format(hex(ord(char))))
            char_im.save(glyph_path)
            print(u"Saved char '{}' at index i, j = {}, {} to file '{}'...".format(char, i, j, glyph_path))  # DEBUG
            # print(raw_input("[Enter to continue]"))  # DEBUG


if __name__ == "__main__":
    import sys
    page = int(sys.argv[1])
    image_filepath = sys.argv[2]
    cut(page, image_filepath)
