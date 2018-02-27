# Fontify
Make your own typeface from your handwriting!

## Development

First clone and `cd` into the repository.

Install wkhtmltopdf: http://wkhtmltopdf.org/downloads.html

```shell
npm install -g ttf2woff
git submodule init
git submodule update
sudo apt-get install fontforge
sudo apt-get install python-opencv

virtualenv env
source env/bin/activate
pip install -r requirements.txt
python hello.py
```

And in another process

```shell
firefox http://0.0.0.0:5000/
```
