# Makefile

# Using bash and not sh, cf. http://stackoverflow.com/a/589300/
SHELL := /bin/bash -o pipefail

# Cleaner
clean:
	-mv -vf restored_image.bmp wait_for_detect.bmp upload/* download/* /tmp/
	-mv -vf *.pyc */*.pyc /tmp/
	-rm -vfr __pycache__/ **/__pycache__/
	-rm -vf *.pyc */*.pyc

activate:
	. env/bin/activate

run:	activate
	# firefox http://0.0.0.0:5000/ &
	python hello.py
