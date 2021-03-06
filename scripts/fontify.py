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
from data import get_ligatures_by_page  # FIXME add support for ligatures


VARIANTS = ["Italic", "Bold", "Light", "Medium", "Regular"]


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


def process(tmpdir, images, font_name, variant='Regular'):
    assert variant in VARIANTS, "Error, variant '{}' should be one of {}...".format(variant, VARIANTS)
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
    ttf = os.path.join(tmpdir, 'fontify.ttf')
    subprocess.call([
            svg_to_ttf_fullpath,
            font_name,
            svgdir,
            ttf,
            variant,
        ],
        cwd=scriptdir
    )
    # 5.c. Finally use the npm script ttf2woff to also generate a .woff file
    woff = os.path.join(tmpdir, 'fontify.woff')
    print("Converting from {} to {}...".format(ttf, woff))  # DEBUG
    subprocess.call([
        'ttf2woff',
        ttf,
        woff
        ],
        # cwd=scriptdir
    )
    # 5.b. Finally and the Python script woff2otf to also generate a .otf file
    otf = os.path.join(tmpdir, 'fontify.otf')
    print("Converting from {} to {}...".format(woff, otf))  # DEBUG
    woff2otf_fullpath = os.path.join(scriptdir, "third-party", "woff2otf", "woff2otf.py")
    subprocess.call([
        woff2otf_fullpath,
        woff,
        ],
        # cwd=scriptdir
    )


def tear_down(tmpdir, output, font_name='Fontify', variant='Regular'):
    assert output.endswith('.ttf'), "Error: 'output' = {} should be have the .ttf extension!".format(output)
    if output == "":
        output = "{}-{}.ttf".format(font_name, variant)
    if output.endswith('fontify.ttf'):
        output = output.replace('fontify.ttf', "{}-{}.ttf".format(font_name, variant))
    shutil.copyfile(os.path.join(tmpdir, 'fontify.ttf'), output)
    shutil.copyfile(os.path.join(tmpdir, 'fontify.woff'), output.replace('.ttf', '.woff'))
    shutil.copyfile(os.path.join(tmpdir, 'fontify.otf'), output.replace('.ttf', '.otf'))
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
        "-v", "--variant", default="Regular", help="font variant (default: Regular)"
    )
    parser.add_argument(
        "-o", metavar="OUTPUT", default="",
        help="output font file (default to Name-Variant.ttf in current directory)"
    )
    args = parser.parse_args()
    check_input(args.images)
    tmpdir, images = setup_work_dir(args.images)
    process(tmpdir, images, args.name, variant=args.variant)
    tear_down(tmpdir, args.o, font_name=args.name, variant=args.variant)
