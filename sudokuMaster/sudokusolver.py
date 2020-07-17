#!usr/bin/env/python
import numpy as np
grid = []
with open('sudoku1_translation.txt', 'r') as f:
	rawtxt = f.read()

rows = rawtxt.split("\n")
for row in rows:
	row = list(map(int,row))
	grid.append(row)


grid = np.array(grid).T


print(grid.T)
def subregion(x):
	intrv = (np.array([3*(np.floor(x/3)),3*(np.floor(x/3)+1)])).astype('int64')
	return list(range(intrv[0],intrv[1]))


def candidate (value, x, y):
	'''
	if grid[x,y] != 0:
		#print("error")
		return False
	'''
	#check column x
	for row in range(9):
		if grid[x, row] == value:
			#print("column")
			return False
	#check row y
	for column in range(9):
		if grid[column, y] == value:
			#print("line")
			return False
	#check subregion
	for column in subregion(x):
		for row in subregion(y):
			if grid[column, row] == value:
				#print("subreg")
				return False
	return True	
'''
x=4
y=8
print(subregion(x))
print(candidate(1,x,y))
print(grid[x,y])

'''

def solve():
	global grid
	#print("----try " + str(count))
	for x in range(9):
		for y in range(9):
			if grid[x,y] == 0:
				for v in range(1,10):
					if candidate(v,x,y):
						#print("trying " + str(v) + " at "  + str(x+1) + "," + str(y+1))
						grid[x,y] = v
						solve()
						#print(grid)
						grid[x,y] = 0
				#print("no possibilities left at " + str(x+1) + "," + str(y+1))
				#print("")
				return
	print(grid.T)
	print("")

					
solve()

