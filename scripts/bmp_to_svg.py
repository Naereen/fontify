#!/usr/bin/env python2
# -*- coding: utf8 -*-
from __future__ import print_function
import os
import sys
import subprocess
import crop_image
from PIL import Image, ImageChops


def is_white(filepath):
    img = Image.open(filepath)
    return not ImageChops.invert(img).getbbox()


def bmp_to_svg(basedir):
    bmpdir = os.path.join(basedir, 'bmp')
    if not os.path.isdir(bmpdir):
        raise SystemError
    files = os.listdir(bmpdir)
    for f in files:
        if f.startswith('0x') and f.endswith('.bmp'):
            name, ext = os.path.splitext(f)
            infile = os.path.join(bmpdir, f)
            outfile = os.path.join(bmpdir, name + '.pbm')
            print("Converting {} to {}...".format(infile, outfile))  # DEBUG
            ret = subprocess.call([
                'mkbitmap',
                '-x',
                infile,
                '-t', '0.7',
                '-b', '2',
                '-s', '2',
                '-3',
                '-o', outfile
            ])
            if ret != 0:
                sys.stderr.write("Error converting %s to binary\n" % infile)
                continue
            crop_image.crop_char(outfile)
            # if is_white(outfile):
            #     print("Skipping empty character", outfile)
            #     continue
            infile = outfile
            outfile = os.path.join(basedir, 'svg', name + '.svg')
            print("  and then {} to {}...".format(infile, outfile))  # DEBUG
            ret = subprocess.call([
                'potrace',
                '--svg',
                infile,
                '-H', '1',
                '-o', outfile
            ])
            if ret != 0:
                sys.stderr.write("Error converting %s to svg\n" % infile)


if __name__ == "__main__":
    import sys
    basedir = sys.argv[1]
    bmp_to_svg(basedir)
