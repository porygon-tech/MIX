README for SudokuMaster suite
-----------------------------------------------------------------------------------------
TRANSLATOR
qqwing_translator.pl transforms the compact-style format used for sudokus at https://qqwing.com/generate.html into a zero-based one.
The following:

.2..6.4.5
....2..1.
13.....7.
........7
7..43218.
41..75..6
....483..
....51.2.
.........

will be converted into something like this:

020060405
000020010
130000070
000000007
700432180
410075006
000048300
000051020
000000000
-----------------------------------------------------------------------------------------
SOLVER
sudokusolver.py solves any sudoku game using backtracking recursion. It may take a while, one minute or two (still faster than you).

-----------------------------------------------------------------------------------------
GENERATOR - coming soon!
