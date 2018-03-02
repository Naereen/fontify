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

from data import get_chars
from data import get_chars_by_page
from data import get_sample_chars
from data import TMPL_OPTIONS

UPLOAD_FOLDER = './upload'
DOWNLOAD_FOLDER = './download'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'pdf'])
DPI = 300

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/finish")
def finish():
    key = request.args.get('key')
    font_name = request.args.get('fontname')
    return render_template(
        'finish.html',
        key=key,
        font_name=font_name
    )


# DEBUG Just to debug the template
@app.route("/oldtemplate_html")
def oldtemplate_html():
    return render_template(
        'template.html',
        chars=get_chars(),
        sample=get_sample_chars(),
    )


@app.route("/oldtemplate")
def oldtemplate():
    html = render_template(
        'template.html',
        chars=get_chars(),
        sample=get_sample_chars()
    )
    pdf = from_string(
        html,
        False,
        options=TMPL_OPTIONS,
    )
    response = make_response(pdf)
    response.headers['Content-Disposition'] = "filename=template.pdf"
    response.mimetype = 'application/pdf'
    return response


@app.route("/template_bypage")
def template_bypage():
    html = render_template(
        'template_bypage.html',
        chars_by_page=get_chars_by_page(),
        sample=get_sample_chars()
    )
    pdf = from_string(
        html,
        False,
        options=TMPL_OPTIONS,
        css='static/css/template.css'
    )
    response = make_response(pdf)
    response.headers['Content-Disposition'] = "filename=template.pdf"
    response.mimetype = 'application/pdf'
    return response


# DEBUG Just to debug the template
@app.route("/template_html")
def template_html():
    return render_template(
        'template.html',
        chars=get_chars(),
        sample=get_sample_chars(),
        css='static/css/template.css'
    )


@app.route("/template")
def template():
    chars_by_page = get_chars_by_page()
    print("Number of pages:", len(chars_by_page))
    pages = []
    # create a fake PDF for each page
    for chars in chars_by_page:
        html = render_template(
            'template.html',
            chars=chars,
            sample=get_sample_chars()
        )
        pdf = from_string(
            html,
            False,
            options=TMPL_OPTIONS,
            css='static/css/template.css'
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


@app.route('/test.tex')
def test_tex():
    return app.send_static_file('test.tex')

@app.route('/test.pdf')
def test_pdf():
    return app.send_static_file('test.pdf')


@app.route("/download/<key>/<fontname>")
def download(key, fontname):
    return send_from_directory(
        os.path.join(app.config['DOWNLOAD_FOLDER'], key),
        fontname,
        as_attachment=True
    )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload-file", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            _, ext = os.path.splitext(file.filename)
            f, filename = tempfile.mkstemp(
                prefix='',
                suffix=ext,
                dir=app.config['UPLOAD_FOLDER']
            )
            file.save(filename)
            filenames = [filename]

            if filename.endswith('.pdf'):
                filename_png = filename.replace('.pdf', '.png')
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
                    filenames = glob.glob(filename.replace('.png', '-[0-9]*.png'))
                    for image in filenames:
                        return_code = subprocess.call([
                            "convert",
                            "-set", "colorspace", "Gray",
                            "-separate", "-average",
                            image,
                            image
                        ])
                        if return_code != 0:
                            raise ValueError("Call to 'convert -set colorspace Gray -separate -average {} {}' failed... do you have 'convert' from imagemagick installed?".format(image, image))

            font_name = request.form['font-name']
            key = filenames[0].split('/')[-1].split('.')[0]

            os.mkdir(os.path.join(app.config['DOWNLOAD_FOLDER'], key))

            call_to_fontify = [
                "python",
                "scripts/fontify.py",
                "-n", font_name,
                "-o", os.path.join(app.config['DOWNLOAD_FOLDER'], key, "fontify.ttf"),
                ] + filenames

            return_code = subprocess.call(call_to_fontify)
            if return_code != 0:
                raise ValueError("Call to 'scripts/fontify.py' failed... Check log above.")
            return jsonify(font_name=font_name, key=key)
    return ''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
