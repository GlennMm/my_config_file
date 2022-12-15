#! /bin/bash

win=$(hyprctl activewindow -j | jq -r '.class')
echo -e $win
