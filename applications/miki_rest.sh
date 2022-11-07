#!/bin/bash

#espeak "Hora de descansar" -s 140 -v europe/es
notify-send "running miki_rest.sh"
sleep 25m
espeak "Look at some point at least 20 meters away for 1 minute." -s 140
notify-send "time to rest"
zenity --info --text="Look at some point at least 20m away for 1 minute, and take a rest"
sleep 5m
zenity --info --text="Back to work"
notify-send "miki_rest.sh finished"
