# Fontify
**Make your own typeface from your handwriting!**

- Download a PDF template to print and fill with a not too fin black pen,
- Scan it with DPI >= 300,
- Upload your beautiful handwriting to the webapp,
- It creates a TrueType font, and let you preview it,
- If you are happy, save it and start to use it!
- See [this demo](https://github.com/Naereen/My-Own-HandWritting-Font) showing how a font generated with Fontify can look, on a website, a LaTeX document or slideshows, or slides made [with Marp](https://yhatt.github.io/marp/).

## Warning
:boom: **I will not try to run the app somewhere online.**

:raised_hand_with_fingers_splayed: If you want to use Fontify, you need a laptop under Debian or Ubuntu (or maybe Mac OS X), with Python installed, and use the instructions explained below.

## Demo

> Here are a few screenshots of the webapp:

|1. Print the template|2. Upload the scanned template|
|--|--|
| <img width="100%" src="screenshots/demo1.png"> | <img width="100%" src="screenshots/demo2.png"> |

| It generates the font and you can preview it |
|--|
| <img width="90%" src="screenshots/demo3.png"> |

---
## Development (*only* on Debian/Ubuntu)

> - It *only* works on [Python](https://www.python.org/) 2, so far (but I'm almost sure it would also work for [Python](https://www.python.org/) 3).
> - I will try to set up a [Docker image](https://www.docker.com/) to ease this experiment... maybe.

1. First clone and `cd` into the repository, fetch the [third-party dependencies](scripts/third-party).

```shell
cd /tmp/
git clone https://github.com/Naereen/fontify
cd fontify
git submodule init
git submodule update
```

2. Install all the dependencies.

```shell
sudo apt-get install potrace imagemagick fontforge fontforge-extras wkhtmltopdf python-opencv python-fontforge  # try to use 'brew' on Mac OS X ?
npm install -g ttf2woff
sudo pip2 install --upgrade virtualenv
```

3. Activate a [virtualenv](http://virtualenv.pypa.io/) and start the app!

```shell
virtualenv env
source env/bin/activate
type pip python   # check that this is the local ones
pip install -r requirements.txt
python hello.py  # or 'make rundebug'
```

4. And open the app to use it!

```shell
firefox http://0.0.0.0:5000/ &
```

5. Note: in "development mode", the app is relaunched whenever a file is modified. Use [`make run`](Makefile) to run "in production" mode.

6. To open the app to anyone on Internet, you can use [ngrok](https://ngrok.com/) (:boom: and also, be crazy, as this app has NO GUARANTEE TO BE SECURE):

```shell
ngrok http 5000
```

7. There is also a [XeLaTeX file](static/test.tex) showing how to use a custom font in a LaTeX document, and [here is how it looks](https://perso.crans.org/besson/publis/latex/test_handwritten_font_with_fontify.pdf).

---

### :scroll: License ? [![GitHub license](https://img.shields.io/github/license/Naereen/fontify.svg)](https://github.com/Naereen/fontify/blob/master/LICENSE)
This (small) repository are published under the terms of the [MIT license](http://lbesson.mit-license.org/) (file [LICENSE](LICENSE)).
© [Lilian Besson](https://GitHub.com/Naereen), 2018.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/fontify/graphs/commit-activity)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/fontify)
[![Analytics](https://ga-beacon.appspot.com/UA-38514290-17/github.com/Naereen/fontify/README.md?pixel)](https://GitHub.com/Naereen/fontify/)

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)
[![ForTheBadge uses-badges](http://ForTheBadge.com/images/badges/uses-badges.svg)](http://ForTheBadge.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![ForTheBadge uses-js](http://ForTheBadge.com/images/badges/uses-js.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-html](http://ForTheBadge.com/images/badges/uses-html.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-css](http://ForTheBadge.com/images/badges/uses-css.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)
