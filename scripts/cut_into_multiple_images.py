#!/usr/bin/env python2
# -*- coding: utf8 -*-
from __future__ import print_function
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage
import cv2

from data import COLUMNS, ROWS, get_chars, get_chars_by_page


def postprocess_char(im_char, debug=False):
    """See http://www.scipy-lectures.org/advanced/image_processing/auto_examples/plot_propagation.html"""
    np_im_char = np.array(im_char)
    input_shape = np.shape(np_im_char)
    if debug:
        print("type(im_char) =", type(im_char))  # DEBUG
        print("type(np_im_char) =", type(np_im_char))  # DEBUG
        print("np.shape(np_im_char) =", np.shape(np_im_char))  # DEBUG
        print("np_im_char.dtype =", np_im_char.dtype)  # DEBUG
        print("np.min(np_im_char) =", np.min(np_im_char))  # DEBUG
        print("np.max(np_im_char) =", np.max(np_im_char))  # DEBUG

    open_im = ndimage.binary_opening(1 - np_im_char)

    eroded_im = ndimage.binary_erosion(1 - np_im_char)
    reconstruction = ndimage.binary_propagation(eroded_im, mask=1 - np_im_char)

    final_reconstruction = 1 - ndimage.binary_opening(1 - reconstruction)
    np_im_output = np.array((1 - final_reconstruction), dtype=np.bool).reshape(input_shape)
    if debug:
        print("type(np_im_output) =", type(np_im_output))  # DEBUG
        print("np.shape(np_im_output) =", np.shape(np_im_output))  # DEBUG
        print("np_im_output.dtype =", np_im_output.dtype)  # DEBUG
        print("np.min(np_im_output) =", np.min(np_im_output))  # DEBUG
        print("np.max(np_im_output) =", np.max(np_im_output))  # DEBUG

    if debug:
        plt.clf()
        plt.subplot(151)
        plt.imshow(np_im_char, cmap=plt.cm.gray, interpolation='nearest')
        plt.subplot(152)
        plt.imshow(1 - open_im, cmap=plt.cm.gray, interpolation='nearest')
        plt.subplot(153)
        plt.imshow(1 - eroded_im, cmap=plt.cm.gray, interpolation='nearest')
        plt.subplot(154)
        plt.imshow(1 - reconstruction, cmap=plt.cm.gray, interpolation='nearest')
        plt.subplot(155)
        plt.imshow(np_im_output, cmap=plt.cm.gray, interpolation='nearest')
        print("np.mean(np.abs(np_im_char - np_im_output)) =", np.mean(np.abs(np.asarray(np_im_char, dtype=np.int) - np.asarray(np_im_output, dtype=np.int))))  # DEBUG
        plt.show()
        plt.draw()

    # np_im_char[:] = np_im_output[:]
    # np_im_char[0:10,0:10] = 1.0
    # np_im_output[:] = np_im_char[:]

    # xs = np.where(np_im_char == np_im_output)[0]
    # ys = np.where(np_im_char == np_im_output)[1]
    # for x, y in zip(xs, ys):
    #     np_im_char[x, y] = np_im_output[x, y]

    # for x in np.arange(input_shape[0]):
    #     for y in np.arange(input_shape[1]):
    #         # print("x = {}, y = {}, pixel {} and {}...".format(x, y, np_im_char[x, y], np_im_output[x, y]))  # DEBUG
    #         np_im_char[x, y] = np_im_output[x, y]

    # xs = np.where(np_im_char != np_im_output)[0]
    # ys = np.where(np_im_char != np_im_output)[1]
    # for x, y in zip(xs, ys):
    #     print("x = {}, y = {}, pixel from {} to {}...".format(x, y, np_im_char[x, y], np_im_output[x, y]))  # DEBUG
    #     np_im_char[x, y] = np_im_output[x, y]

    im_output = Image.fromarray(np_im_char, mode='L')
    # im_output = Image.fromarray(np_im_output, mode='L')
    return im_output


NORMALIZE = 1
NORMALIZE = 255


def smooth_and_thicken(im_char, normalize=NORMALIZE):
    """ See https://stackoverflow.com/a/37410236/"""
    _blur = ((1, 1), 1)
    _erode = (1, 1)
    _dilate = (1, 1)
    np_im_char = np.asarray(im_char)
    if normalize != 1:
        im_input = np_im_char / normalize
    else:
        im_input = np_im_char
    im_blurred = cv2.GaussianBlur(im_input, _blur[0], _blur[1])
    im_eroded = cv2.erode(im_blurred, np.ones(_erode))
    im_dilated = cv2.dilate(im_eroded, np.ones(_dilate))
    if normalize != 1:
        np_im_output = im_dilated * normalize
    else:
        np_im_output = im_dilated
    im_output = Image.fromarray(np.uint8(np_im_output))
    return im_output


def cut(page, filepath, postprocess=True):
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
    print("cell_width =", cell_width)  # DEBUG
    cell_height = image_height / ROWS
    print("cell_height =", cell_height)  # DEBUG
    width_limit = cell_width * COLUMNS
    print("width_limit =", width_limit)  # DEBUG
    height_limit = cell_height * ROWS
    print("height_limit =", height_limit)  # DEBUG


    for i in range(0, height_limit, cell_height):
        for j in range(0, width_limit, cell_width):
            char = chars[i / cell_height][j / cell_width]
            if char == ' ':
                return
            print(u"\ni =", i, "j =", j, "char =", char)  # DEBUG
            bar_height = int(cell_height * 0.28333)
            print("bar_height =", bar_height)  # DEBUG
            margin_width = int(cell_width * 0.1)
            print("margin_width =", margin_width)  # DEBUG
            margin_height_top = int(cell_height * 0.005)
            print("margin_height_top =", margin_height_top)  # DEBUG
            margin_height_bottom = int(cell_height * 0.01)
            print("margin_height_bottom =", margin_height_bottom)  # DEBUG
            char_im = im.crop(
                (
                    j + margin_width,
                    i + bar_height + margin_height_top,
                    j + cell_width - margin_width,
                    i + cell_height - margin_height_bottom
                )
            )
            glyph_path = os.path.join(bmp_dir, "{}.bmp".format(hex(ord(char))))

            # FIXME try to do your best job at postprocessing the image!
            if postprocess:
                new_char_im = postprocess_char(char_im)
            else:
                new_char_im = char_im

            new_char_im.save(glyph_path)
            print(u"Saved char '{}' at index i, j = {}, {} to file '{}'...".format(char, i, j, glyph_path))  # DEBUG
            # print(raw_input("[Enter to continue]"))  # DEBUG


if __name__ == "__main__":
    import sys
    page = int(sys.argv[1])
    image_filepath = sys.argv[2]
    cut(page, image_filepath)
