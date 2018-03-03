# Fontify
**Make your own typeface from your handwriting!**

- Download a PDF template to print and fill,
- Scan it with DPI >= 300,
- Upload your beautiful handwriting to the webapp,
- It creates a TrueType font, and let you preview it,
- If you are happy, save it and start to use it!
- See [this demo](https://github.com/Naereen/My-Own-HandWritting-Font)

## Development

> It only works on Python 2, so far.

1. First clone and `cd` into the repository.

```shell
cd /tmp/
git clone https://github.com/Naereen/fontify
cd fontify
git submodule init
git submodule update
```

2. Install the dependencies

```shell
sudo apt-get install imagemagick
sudo apt-get install fontforge
sudo apt-get install wkhtmltopdf
sudo apt-get install python-opencv
npm install -g ttf2woff
sudo pip2 install --upgrade virtualenv
```

3. Activate a virtualenv and start the app!

```shell
virtualenv env
source env/bin/activate
type pip python   # check that this is the local ones
pip install -r requirements.txt
python hello.py
```

4. And open the app to use it!

```shell
firefox http://0.0.0.0:5000/ &
```

5. Note: in development mode, the app is relaunched whenever a file is modified.