# -*- coding: utf8 -*-
import os
from PIL import Image

from data import COLUMNS, ROWS, get_chars


def cut(filepath):
    im = Image.open(filepath)
    imdir = os.path.dirname(filepath)
    if imdir == "":
        imdir = "."
    image_width, image_height = im.size

    cell_width = image_width / COLUMNS
    cell_height = image_height / ROWS
    width_limit = cell_width * COLUMNS
    height_limit = cell_height * ROWS
    chars = get_chars()

    for i in xrange(0, height_limit, cell_height):
        for j in xrange(0, width_limit, cell_width):
            char = chars[i / cell_height][j / cell_width]
            if char == ' ':
                return
            bar_height = int(cell_height * 0.22)
            margin_width = int(cell_width * 0.1)
            margin_height = int(cell_height * 0.1)
            char_im = im.crop(
                (
                    j + margin_width,
                    i + bar_height + margin_height,
                    j + cell_width - margin_width,
                    i + cell_height - margin_height
                )
            )
            char_im.save("{}/bmp/{}.bmp".format(imdir, hex(ord(char))))


if __name__ == "__main__":
    import sys
    image_filepath = sys.argv[1]
    cut(image_filepath)
