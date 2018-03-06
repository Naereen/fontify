#!/usr/bin/env python2
# -*- coding: utf8 -*-
from __future__ import print_function
import os
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image
from scipy import ndimage
import cv2

from data import COLUMNS, ROWS, get_chars, get_chars_by_page


def postprocess_char_complex_and_save(im_char, glyph_path, debug=False):
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

    eroded_im = ndimage.binary_erosion(1 - np_im_char, iterations=3)

    reconstruction = ndimage.binary_propagation(eroded_im, mask=1 - np_im_char)
    np_im_output = np.array((1 - reconstruction), dtype=np.bool).reshape(input_shape)

    # final_reconstruction = 1 - ndimage.binary_opening(1 - reconstruction)
    # np_im_output = np.array((1 - final_reconstruction), dtype=np.bool).reshape(input_shape)
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
        plt.axis('off')
        plt.title("input")
        plt.subplot(152)
        plt.imshow(1 - open_im, cmap=plt.cm.gray, interpolation='nearest')
        plt.axis('off')
        plt.title("1 - open")
        plt.subplot(153)
        plt.imshow(1 - eroded_im, cmap=plt.cm.gray, interpolation='nearest')
        plt.axis('off')
        plt.title("1 - eroded")
        plt.subplot(154)
        plt.imshow(1 - reconstruction, cmap=plt.cm.gray, interpolation='nearest')
        plt.axis('off')
        plt.title("1 - reconstruction")
        plt.subplot(155)
        plt.imshow(np_im_output, cmap=plt.cm.gray, interpolation='nearest')
        plt.axis('off')
        plt.title("output")
        print("np.mean(np.abs(np_im_char - np_im_output)) =", np.mean(np.abs(np.asarray(np_im_char, dtype=np.int) - np.asarray(np_im_output, dtype=np.int))))  # DEBUG
        plt.show()
        plt.draw()

    misc.imsave(glyph_path, np.asarray(np_im_output, dtype=np.int))

    # # im_output = Image.fromarray(np_im_char, mode='L')
    # im_output = Image.fromarray(np_im_output, mode='L')
    # return im_output


def postprocess_char_old(im_char, debug=False, deltay=3):
    np_im_char = np.array(im_char)

    c = Counter(list(np_im_char.flatten()))
    default_pixel = c[True] > c[False]

    if debug:
        print("im_char.mode =", im_char.mode)  # DEBUG
        print("type(im_char) =", type(im_char))  # DEBUG
        print("type(np_im_char) =", type(np_im_char))  # DEBUG
        print("np.shape(np_im_char) =", np.shape(np_im_char))  # DEBUG
        print("np_im_char.dtype =", np_im_char.dtype)  # DEBUG
        print("np.min(np_im_char) =", np.min(np_im_char))  # DEBUG
        print("np.max(np_im_char) =", np.max(np_im_char))  # DEBUG
        print("set(np_im_char.flatten()) =", set(np_im_char.flatten()))  # DEBUG
        print("Counter(list(np_im_char.flatten())) =", c)  # DEBUG
        print("Default pixel =", default_pixel)  # DEBUG

    # Manually erasing top and bottom lines!
    top_and_bottom = list(range(deltay)) + list(range(-1, -1-deltay, -1))
    for i in top_and_bottom:
        c = Counter(np_im_char[i, :])
        print("Counter(np_im_char[{}, :]) =".format(i), Counter(np_im_char[i, :]))  # DEBUG
        # if c[False] > 0 and c[True] > 0:
        # print("  From: np_im_char[{},:]".format(i), np_im_char[i,:])  # DEBUG
        # np_im_char[i, :] = c[True] >= c[False]  # just use the most present value?
        np_im_char[i, :] = default_pixel  # just use the most present value?
        # print("  To:   np_im_char[{},:]".format(i), np_im_char[i,:])  # DEBUG

    if debug:
        print("Some pixels were changed...")  # DEBUG
        print("Counter(list(np_im_char.flatten())) =", Counter(list(np_im_char.flatten())))  # DEBUG

    im_output = Image.fromarray(np_im_char, mode='L')
    return im_output


number_of_time_we_saw_a_space = 0


def cut(page, filepath, postprocess=True, debug=False):
    global number_of_time_we_saw_a_space
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

    bar_height = int(cell_height * 0.26)
    print("bar_height =", bar_height)  # DEBUG
    margin_width = int(cell_width * 0.09)
    print("margin_width =", margin_width)  # DEBUG
    margin_height_top = int(cell_height * 0.010)
    print("margin_height_top =", margin_height_top)  # DEBUG
    margin_height_bottom = int(cell_height * 0.02)
    print("margin_height_bottom =", margin_height_bottom)  # DEBUG

    for i in range(0, height_limit, cell_height):
        for j in range(0, width_limit, cell_width):
            char = chars[i / cell_height][j / cell_width]
            if char == ' ':
                number_of_time_we_saw_a_space += 1
                if number_of_time_we_saw_a_space > 1:
                    return
            print(u"\ni =", i, "j =", j, "char =", char)  # DEBUG
            # Coordinates as [ymin, xmin, ymax, xmax] rectangle
            coordinates = (
                    j + margin_width,
                    i + bar_height + margin_height_top,
                    j + cell_width - margin_width,
                    i + cell_height - margin_height_bottom
                )
            print("\tUsing a square of coordinates, ", coordinates)  # DEBUG
            char_im = im.crop(coordinates)
            glyph_path = os.path.join(bmp_dir, "{}.bmp".format(hex(ord(char))))

            if postprocess:
                postprocess_char_complex_and_save(char_im, glyph_path)
            else:
                char_im.save(glyph_path)

            print(u"Saved char '{}' at index i, j = {}, {} to file '{}'...".format(char, i, j, glyph_path))  # DEBUG
            if debug:
                print(raw_input("[Enter to continue]"))  # DEBUG


if __name__ == "__main__":
    import sys
    page = int(sys.argv[1])
    image_filepath = sys.argv[2]
    cut(page, image_filepath)
