# -*- coding: utf8 -*-
from __future__ import print_function
import argparse
import tempfile
import shutil
import os
import subprocess

import crop_image
import cut_into_multiple_images
import bmp_to_svg
import data


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
    for image in images:
        _, ext = os.path.splitext(image)
        dst = 'input' + ext
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
    for image in images:
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
