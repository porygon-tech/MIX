# MIX
A mix of miscellaneous tiny scripts.

------------


### Sublime Text themes
They can be easily installed as described [here](https://colorsublime.github.io/how-to-install-a-theme/ "here").
There is also a very user-friendly [theme editor](https://tmtheme-editor.herokuapp.com "theme editor")

example:
```
cd ~/.config/sublime-text-3/Packages/Colorsublime-Themes 
wget https://github.com/porygon-tech/MIX/blob/master/sublimeThemes/nether2.tmTheme
```
------------


### gadgets/watchdog
Watchdog is a scrappy surveillance webcam software created using python and OpenCV. Simply put, you set the webcam in the surveillance zone, open a terminal and run `python3 watchdog.py 15 2`, where 15 is the threshold and 2 the time delay (in seconds) (params should be tested and modified depending on the hardware). Watchdog computes the dense optical flow (DOF) from stream, taking pictures when the DOF reaches the threshold value. The delay is the number of seconds between the detection and the shot.

------------


### gadgets/keyLgLite
keyLgLite is a super lightweight keylogger made using pynput.

------------

### gadgets/readeer
readeer extracts keywords from selected text and can summarize it using GPT-3.5 (API key required in a text file in the same directory). Currently only tested in linux.

------------

### image/borderDetector
Homemade silly old algorithm to detect image borders based on color 3D euclidean distance (now i think it\'s the same as convolution?¿¿?)

------------


### sudokuMaster
`qqwing_translator.pl` transforms the compact-style format used for sudokus at https://qqwing.com/generate.html into a zero-based one, suitable for the solver.
`sudokusolver.py` solves *any* sudoku game using backtracking recursion. It may take a while, one minute or two (still faster than you). 
For more information, check the readme inside the directory.
