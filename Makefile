# Makefile
# Using bash and not sh, cf. http://stackoverflow.com/a/589300/
SHELL := /bin/bash -o pipefail

default:	clean rundebug
prod:	clean run

# Cleaner
clean:
	-mv -vf restored_image.bmp wait_for_detect.bmp upload/* download/* /tmp/
	-rm -rfv /tmp/fontify*/
	-mv -vf *.pyc */*.pyc /tmp/
	-rm -vfr __pycache__/ **/__pycache__/
	-rm -vf *.pyc */*.pyc

rundebug:
	# firefox http://0.0.0.0:5000/ &
	. env/bin/activate && python hello.py

run:
	# firefox http://0.0.0.0:5000/ &
	. env/bin/activate && python wsgi.py

install_env:
	virtualenv2 env
	. env/bin/activate && type pip python
	. env/bin/activate && pip install -r requirements.txt

test_pdf:
	xelatex static/test.tex
	xelatex static/test.tex
	-rm -vf static/test.aux static/test.fls static/test.log static/test.fdb_latexmk static/test.synctex.gz
	# xdg-open test.pdf &
	CP static/test.pdf ${Szam}publis/latex/test_handwritten_font_with_fontify.pdf

# Senders:
send:	send_zamok
send_zamok:	clean
	CP --exclude=.git --exclude=env ./ ${Szam}publis/fontify.git/

send_ws3:	clean
	CP ./ ${Sw}publis/fontify.git/
