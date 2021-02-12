import sys
import os
import logging
import imageio
import numpy as np
print('packages loaded')

# example:  python3 borderDetector.py 1.5 gato.png 

sensitivity = float(sys.argv[1])
filename = sys.argv[2]

pic = imageio.imread(filename)
pic = pic.astype('uint16')

cmx = np.zeros(pic.shape) #contrast matrix
print('measuring image size')
height = pic.shape[0]
width = pic.shape[1]

maxContrast = np.sqrt(3*(255)**2)
print('detecting borders...')

# generation of DownUpRightLeft pixel-displaced matrices.
# they are basically the original image one-pixel displaced in each four directions.
D = np.delete((np.insert(pic, height, [0,0,0], axis=0)), 0, axis=0)
U = np.delete((np.insert(pic, 0, [0,0,0], axis=0)), height, axis=0)
R = np.delete((np.insert(pic, width, [0,0,0], axis=1)), 0, axis=1) 
L = np.delete((np.insert(pic, 0, [0,0,0], axis=1)), width, axis=1)

# colour distance with the four most adjacent pixels.
D_dist = np.sqrt(np.sum(((pic - D)**2), axis=2))
U_dist = np.sqrt(np.sum(((pic - U)**2), axis=2))
R_dist = np.sqrt(np.sum(((pic - R)**2), axis=2))
L_dist = np.sqrt(np.sum(((pic - L)**2), axis=2))

# some math shit for contrast calculation
def augment(x, slope):
	return((-1 / slope**x + 1)*255)

# x is the average of squared distances to the four adjacent pixels
# slope is a parameter of sensitivity. The higher, the more edges will be detected
cmx = augment(x=((U_dist**2 + D_dist**2 + L_dist**2 + R_dist**2)/4)/255, slope = sensitivity)

print('done')
outName = os.path.splitext(filename)[0] + '_borders.png'
print('exporting...')
cmx = cmx.astype('uint8')

imageio.imwrite(outName, cmx)
print('finished, exported to "' + outName + '"')

