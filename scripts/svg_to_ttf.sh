#!/usr/bin/env bash

script_source="$( dirname "${BASH_SOURCE[0]}" )"
# cd "$( dirname "${BASH_SOURCE[0]}" )"

# $1 font name
# $2 input directory
# $3 output ttf
# $4 font variant (Regular, Italic etc)
echo -e "Generating metadata in '$2/metadata.json', for fontname = '$1', input directory = '$2', output ttf = '$3', and variant = '${4:-Regular}'..."
"${script_source}"/gen_metadata.py "$1" "$2" "$3" "${4:-Regular}" > "$2"/metadata.json

echo -e "Calling fontfourge script svgs2ttf..."
"${script_source}"/third-party/svgs2ttf/svgs2ttf "$2"/metadata.json
