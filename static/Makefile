# Makefile for a dummy article with simple latexmk compilation
# Copyright (c) 2018 Lilian Besson (Naereen), https://github.com/Naereen
# The MIT License (MIT)
#
SHELL=/usr/bin/env /bin/bash

test:	pdf

pdf:
	latexmk -gg -pdf -pdflatex="xelatex %O %S" test.tex

clean:
	latexmk -c
	rm -vf *.bbl *.synctex.gz *.loa
