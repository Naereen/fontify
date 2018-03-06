#!/bin/bash
# fontify_tmux.sh for https://github.com/Naereen/fontify/
# MIT Licensed, https://lbesson.mit-license.org/
#
# Script to start a new tab in a tmux session, launching the app and ngrok in two panes


echo -e "${yellow}Starting '${black}fontify_tmux.sh'${reset} ..."

if [ -L "${BASH_SOURCE[0]}" ]; then
    # We have a symlink... how to deal with it?
    cd "$( dirname "$(readlink -f "${BASH_SOURCE[0]}")" )"
else
    cd "$( dirname "${BASH_SOURCE[0]}" )"
fi;

# XXX assume runing inside a tmux session
if [ "X${TMUX}" = "X" ]; then
    echo -e "${red}This script ${black}${0}${red} has to be run inside a tmux session.${reset}"
    exit 1
fi

# Reference tmux man page (eg. https://linux.die.net/man/1/tmux)
# start a new window,
# name it ulogme
tmux new-window -a -n 'fontify' "tmux split-window -d \"make rundebug\" ; ngrok http 5000"
# launch 'make rundebug' in first one
# split it half
# launch 'ngrok http 5000' in second one

sleep 2
# return to current tab at the end
tmux last-window
