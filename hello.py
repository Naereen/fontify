#! /usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import print_function

import os
import subprocess
import tempfile
import glob
try:
    from StringIO import StringIO
except ImportError:  # in Python 3
    from io.StringIO import StringIO

from flask import Flask
from flask import request
from flask import send_from_directory
from flask import url_for
from flask import redirect
from flask import make_response
from flask import render_template
from flask import jsonify

from pdfkit import from_string
from PyPDF2 import PdfFileMerger

# local imports
from data import TMPL_OPTIONS
from data import get_sample_chars, get_chars, get_chars_by_page
from data import get_sample_ligatures, get_ligatures, get_ligatures_by_page  # FIXME add support for ligatures


# --- configuration for the application

HOST = '0.0.0.0'
PORT = 5000

UPLOAD_FOLDER = './upload'
DOWNLOAD_FOLDER = './download'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'pdf'])
DPI = 300       # for PDF to PNG conversion
THRESHOLD = 75  # for gray-scale to black-white conversion


# --- create the Flask app and start to configure it

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


# --- Flask app routes

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/finish")
def finish():
    key = request.args.get('key')
    font_name = request.args.get('font_name')
    font_variant = request.args.get('font_variant')
    return render_template(
        'finish.html',
        key=key,
        font_name=font_name,
        font_variant=font_variant
    )


# --- DEBUG just to debug the template

def _template_html(get_inputs, get_sample_inputs):
    return render_template(
        'template.html',
        chars=get_inputs(),
        sample=get_sample_inputs(),
        css='static/css/template.css'
    )

@app.route("/template_html")
def template_html():
    return _template_html(get_chars, get_sample_chars)

@app.route("/template_ligatures_html")
def template_ligatures_html():
    return _template_html(get_ligatures, get_sample_ligatures)


# --- PDF template

def _template(get_inputs_by_page, get_sample_inputs):
    chars_by_page = get_inputs_by_page()
    assert isinstance(chars_by_page, list)
    assert isinstance(chars_by_page[0], list)
    print("Number of pages:", len(chars_by_page))
    pages = []
    # create a fake PDF for each page
    for page, chars in enumerate(chars_by_page):
        print("Using chars =\n", chars)  # DEBUG
        html = render_template(
            'template.html',
            chars=chars,
            sample=get_sample_inputs()
        )
        pdf = from_string(
            html,
            False,
            options=TMPL_OPTIONS,
            css='static/css/template.css',
        )
        pages.append(pdf)
    # now merge the PDF
    pdf = StringIO()
    merger = PdfFileMerger()
    for pgnb, page in enumerate(pages):
        fakepdf = StringIO(page)
        merger.append(fakepdf)
    merger.write(pdf)
    pdf_string = pdf.getvalue()
    response = make_response(pdf_string)
    response.headers['Content-Disposition'] = "filename=template.pdf"
    response.mimetype = 'application/pdf'
    return response


@app.route("/template")
def template():
    return _template(get_chars_by_page, get_sample_chars)

@app.route("/template_ligatures")
def template_ligatures():
    return _template(get_ligatures_by_page, get_sample_ligatures)


# --- demo of LaTeX & PDF document

@app.route('/test.tex')
def test_tex():
    return app.send_static_file('test.tex')

@app.route('/test.pdf')
def test_pdf():
    return app.send_static_file('test.pdf')


# @app.route("/download/<key>/<full_font_name>/<font_variant>")
# def download(key, full_font_name, font_variant='Regular'):
@app.route("/download/<key>/<full_font_name>")
def download(key, full_font_name):
    return send_from_directory(
        os.path.join(app.config['DOWNLOAD_FOLDER'], key),
        full_font_name,
        as_attachment=True
    )


# --- first non trivial method

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload-file", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            _, ext = os.path.splitext(file.filename)
            _, filename = tempfile.mkstemp(
                prefix='',
                suffix=ext,
                dir=app.config['UPLOAD_FOLDER']
            )
            file.save(filename)
            filenames = [filename]

            if filename.endswith('.pdf'):
                filename_png = filename.replace('.pdf', '.png')
                print("Converting '{}' to '{}'...".format(filename, filename_png))  # DEBUG
                return_code = subprocess.call([
                    "convert",
                    "-density", str(DPI),
                    "-quality", "100",
                    filename,
                    filename_png
                ])
                if return_code != 0:
                    raise ValueError("Call to 'convert -density 300 -quality 100 {} {}' failed... do you have 'convert' from imagemagick installed?".format(filename, filename_png))
                filename = filename_png
                filenames = [filename]
                if not os.path.exists(filename):
                    filenames = sorted(glob.glob(filename.replace('.png', '-[0-9]*.png')))
                    for image in filenames:
                        print("Converting '{}' with colours to '{}' in gray scale...".format(image, image))  # DEBUG
                        return_code = subprocess.call([
                            "convert",
                            "-set", "colorspace", "Gray",
                            "-separate", "-average",
                            image,
                            image
                        ])
                        if return_code != 0:
                            raise ValueError("Call to 'convert -set colorspace Gray -separate -average {} {}' failed... do you have 'convert' from imagemagick installed?".format(image, image))

            # now convert to black-white only!
            for image in filenames:
                print("Converting '{}' in gray scale to '{}' in black and white (threshold = {})...".format(image, image, THRESHOLD))  # DEBUG
                return_code = subprocess.call([
                    "convert",
                    "-threshold", "{}%".format(THRESHOLD),
                    image,
                    image
                ])
                if return_code != 0:
                    raise ValueError("Call to 'convert -threshold {}% {} {}' failed... do you have 'convert' from imagemagick installed?".format(THRESHOLD, image, image))

            font_name = request.form['font_name']
            print("Using font_name =", font_name)
            font_variant = request.form['font_variant']
            print("Using font_variant =", font_variant)
            key = filenames[0].split('/')[-1].split('.')[0]
            print("Using key =", key)

            os.mkdir(os.path.join(app.config['DOWNLOAD_FOLDER'], key))

            call_to_fontify = [
                "python",
                "scripts/fontify.py",
                "-n", font_name,
                "-v", font_variant,
                "-o", os.path.join(app.config['DOWNLOAD_FOLDER'], key, "fontify.ttf"),
                ] + filenames

            return_code = subprocess.call(call_to_fontify)
            if return_code != 0:
                raise ValueError("Call to 'scripts/fontify.py' failed... Check log above.")
            return jsonify(font_name=font_name, key=key, font_variant=font_variant)
    return ''


# --- launch the application

if __name__ == "__main__":
    for dirname in [ UPLOAD_FOLDER, DOWNLOAD_FOLDER ]:
        if not os.path.isdir(dirname):
            print("Directory {} is absent... creating it.".format(dirname))  # DEBUG
            os.mkdir(dirname)
    app.run(debug=True, host=HOST, port=PORT)
