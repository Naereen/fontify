# Quick Makefile
# __author__ = "Lilian Besson"
# __version__ = "0.9"

# Using bash and not sh, cf. http://stackoverflow.com/a/589300/
SHELL := /bin/bash -o pipefail

# Cleaner
clean:
	-mv -vf *.pyc */*.pyc /tmp/
	-rm -vfr __pycache__/ **/__pycache__/
	-rm -vf *.pyc */*.pyc

