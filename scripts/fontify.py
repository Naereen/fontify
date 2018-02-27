#!/usr/bin/env python2
# -*- coding: utf8 -*-
import argparse
import tempfile
import shutil
import os
import subprocess

import crop_image
import cut_into_multiple_images
import bmp_to_svg
import data


def check_input(image):
    if not os.path.isfile(image):
        raise FileNotFoundError
    _, ext = os.path.splitext(image)
    if ext.lower() not in [".jpg", ".jpeg", ".png"]:
        raise ValueError("Unrecognized image extension")


def setup_work_dir(image):
    tmpdir = tempfile.mkdtemp(prefix="fontify")
    _, ext = os.path.splitext(image)
    dst = 'input' + ext
    shutil.copyfile(image, os.path.join(tmpdir, dst))
    os.mkdir(os.path.join(tmpdir, 'bmp'))
    os.mkdir(os.path.join(tmpdir, 'svg'))
    return tmpdir, dst


def process(tmpdir, image, font_name):
    crop_image.crop_whole(os.path.join(tmpdir, image))
    cut_into_multiple_images.cut(os.path.join(tmpdir, data.CROPPED_IMG_NAME))
    bmp_to_svg.bmp_to_svg(tmpdir)
    scriptdir = os.path.realpath(os.path.dirname(__file__))
    sh_fullpath = os.path.join(scriptdir, 'svg_to_ttf.sh')
    svgdir = os.path.join(tmpdir, 'svg')
    subprocess.call(
        [sh_fullpath, font_name, svgdir, os.path.join(tmpdir, 'fontify.ttf')],
        cwd=scriptdir
    )
    subprocess.call(
        ['ttf2woff', os.path.join(tmpdir, 'fontify.ttf'), os.path.join(tmpdir, 'fontify.woff')],
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
        "image", help="input image (JPG or PNG)"
    )
    parser.add_argument(
        "-n", "--name", default="Fontify", help="font name (default: Fontify)"
    )
    parser.add_argument(
        "-o", metavar="OUTPUT", default="",
        help="output font file (default to fontify.ttf in current directory)"
    )
    args = parser.parse_args()
    check_input(args.image)
    tmpdir, image = setup_work_dir(args.image)
    process(tmpdir, image, args.name)
    tear_down(tmpdir, args.o)
