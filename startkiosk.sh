#!/bin/bash

# disable DPMS (Energy Star) features.
xset -dpms

# disable screen saver
xset s off

# don't blank the video device
xset s noblank

# disable mouse pointer
#unclutter -idle 0 -root &

# run window manager
matchbox-window-manager -use_cursor yes -use_titlebar no  &

# run chromuim
#chromium-browser --noerrdialogs --kiosk --incognito https://www.google.co.kr/
if [ $# -ne 0 ];
then
	        chromium-browser --noerrdialogs --kiosk --incognito $1
else
		chromium-browser --noerrdialogs --start-fullscreen http://localhost:8000 
fi
