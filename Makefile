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

activate:
	. env/bin/activate

rundebug:	activate
	# firefox http://0.0.0.0:5000/ &
	python hello.py

run:	activate
	# firefox http://0.0.0.0:5000/ &
	python wsgi.py

test_pdf:
	xelatex static/test.tex
	xelatex static/test.tex
	-rm -vf static/test.aux static/test.fls static/test.log static/test.fdb_latexmk static/test.synctex.gz
	# xdg-open test.pdf &
	CP static/test.pdf ${Szam}publis/latex/test_handwritten_font_with_fontify.pdf
