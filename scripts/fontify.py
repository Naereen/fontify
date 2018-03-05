#!/usr/bin/env python2
# -*- coding: utf8 -*-
from __future__ import print_function
import argparse
import tempfile
import shutil
import os
import sys
import subprocess

sys.path.insert(0, '..')  # just to import data correctly
sys.path.insert(0, 'scripts')  # just to import data correctly
import crop_image
import cut_into_multiple_images
import bmp_to_svg
import data
from data import get_chars_by_page


def check_input(images):
    for image in images:
        if not os.path.isfile(image):
            raise FileNotFoundError
        _, ext = os.path.splitext(image)
        if ext.lower() not in [".jpg", ".jpeg", ".png"]:
            raise ValueError("Unrecognized image extension")


def setup_work_dir(images):
    tmpdir = tempfile.mkdtemp(prefix="fontify")
    destinations = []
    for page, image in enumerate(images):
        _, ext = os.path.splitext(image)
        dst = "input-{}{}".format(page, ext)
        shutil.copyfile(image, os.path.join(tmpdir, dst))
        for dirname in [os.path.join(tmpdir, 'bmp'), os.path.join(tmpdir, 'svg')]:
            if os.path.exists(dirname):
                if not os.path.isdir(dirname):
                    raise ValueError("The folder '{}' appears to exists but is not a folder, invalid. Try to manually remove the file.".format(dirname))  # DEBUG
            else:
                os.mkdir(dirname)
        destinations.append(dst)
    return tmpdir, destinations


def process(tmpdir, images, font_name):
    # 1. Crop the image using the two black circles
    trimmed_filepaths = []
    for page, image in enumerate(images):
        print("Processing the page #{} with path {} ...".format(page, image))  # DEBUG
        trimmed_filepath = crop_image.crop_whole(page, os.path.join(tmpdir, image))
        trimmed_filepaths.append(trimmed_filepath)
        print("Trimmed image is at: {}...".format(trimmed_filepath))  # DEBUG
    # 2. Cut images into square pieces
    # for page, trimmed_filepath in enumerate(trimmed_filepaths):
        cut_into_multiple_images.cut(page, trimmed_filepath)
    # 3. Convert them from BMP to SVG
    bmp_to_svg.bmp_to_svg(tmpdir)
    # 4. Then use the fontforge script svgs2ttf
    scriptdir = os.path.realpath(os.path.dirname(__file__))
    svg_to_ttf_fullpath = os.path.join(scriptdir, 'svg_to_ttf.sh')
    svgdir = os.path.join(tmpdir, 'svg')
    subprocess.call(
        [svg_to_ttf_fullpath, font_name, svgdir, os.path.join(tmpdir, 'fontify.ttf')],
        cwd=scriptdir
    )
    # 5.c. Finally use the npm script ttf2woff to also generate a .woff file
    subprocess.call(
        ['ttf2woff', os.path.join(tmpdir, 'fontify.ttf'), os.path.join(tmpdir, 'fontify.woff')],
    )
    # 5.b. Finally and the Python script woff2otf to also generate a .woff file
    woff2otf_fullpath = os.path.join(scriptdir, "third-party", "woff2otf")
    subprocess.call(
        [woff2otf_fullpath, os.path.join(tmpdir, 'fontify.woff')],
    )


def tear_down(tmpdir, output):
    if output == "":
        output = "fontify.ttf"
    shutil.copyfile(os.path.join(tmpdir, 'fontify.ttf'), output)
    shutil.copyfile(os.path.join(tmpdir, 'fontify.woff'), output[:-3] + 'woff')
    # shutil.rmtree(tmpdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "images", nargs='+',
        help="input images (JPG or PNG)"
    )
    parser.add_argument(
        "-n", "--name", default="Fontify", help="font name (default: Fontify)"
    )
    parser.add_argument(
        "-o", metavar="OUTPUT", default="",
        help="output font file (default to fontify.ttf in current directory)"
    )
    args = parser.parse_args()
    check_input(args.images)
    tmpdir, images = setup_work_dir(args.images)
    process(tmpdir, images, args.name)
    tear_down(tmpdir, args.o)
