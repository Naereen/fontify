#!/usr/bin/env bash

# $1 font name
# $2 input directory
# $3 output ttf
# $4 font variant (Regular, Italic etc)
./gen_metadata.py "$1" "$2" "$3" "${4:-Regular}" > "$2"/metadata.json
third-party/svgs2ttf/svgs2ttf "$2"/metadata.json
