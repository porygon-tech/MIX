import cv2
import numpy as np
import time
import matplotlib.pyplot as plt  
import keyboard as kbd


def show_webcam(cam, mirror=False):
	while True:
		_, img = cam.read()
		
		if mirror: 
			img = cv2.flip(img, 1)
		cv2.imshow('my webcam', img)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
	cv2.destroyAllWindows()


def showdata(mat, color=plt.cm.gnuplot, symmetry=False):
	mat = np.copy(mat)
	if symmetry:
		top = np.max([np.abs(np.nanmax(mat)),np.abs(np.nanmin(mat))])
		plt.imshow(mat.astype('float32'), interpolation='none', cmap='seismic',vmax=top,vmin=-top)
	else:
		plt.imshow(mat.astype('float32'), interpolation='none', cmap=color)
	plt.colorbar()
	plt.show()


def stream_optical_flow():
	cv2.destroyAllWindows()
	cam = cv2.VideoCapture(0)
	_, A = cam.read()
	A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
	while True:
		B = A
		_, A = cam.read()
		A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(B, A, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
		magnitude, angle = cv2.cartToPolar(flow[:,:, 0], flow[:,:, 1])
		print(magnitude.mean())
		#time.sleep(2)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
	cv2.destroyAllWindows()
	cam.release()


cam.release()
#stream_optical_flow()










cv2.destroyAllWindows()
cam.release()
cam = cv2.VideoCapture(0)
_, A = cam.read()
A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
while True:
	B = A
	_, A = cam.read()
	A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
	flow = cv2.calcOpticalFlowFarneback(B, A, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
	magnitude, angle = cv2.cartToPolar(flow[:,:, 0], flow[:,:, 1])
	print(magnitude.mean(), magnitude.std(), angle.mean())
	#time.sleep(2)
	if cv2.waitKey(1) == 27: 
		break  # esc to quit
cv2.destroyAllWindows()
cam.release()




cv2.destroyAllWindows()
cam.release()
#cam = cv2.VideoCapture('/home/mroman/Videos/videoplayback.mp4')
cam = cv2.VideoCapture('/home/mroman/Videos/on_thin_ice.mp4')
_, A = cam.read()
A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
while (cam.isOpened()):
	B = A
	_, A = cam.read()
	#cv2.imshow('my webcam', A)
	A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
	flow = cv2.calcOpticalFlowFarneback(B, A, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
	magnitude, angle = cv2.cartToPolar(flow[:,:, 0], flow[:,:, 1])
	print(str(magnitude.mean()) + '\t' + str(magnitude.std()) + '\t' + str(angle.mean()) + '\t' + str(angle.std()))
	if 8>magnitude.mean()>4 :
		time.sleep(1)
		print('screenshot taken!')
		cv2.imwrite('/home/mroman/Pictures/captures/capture' + time.ctime() + '.png', A)
		
	#time.sleep(2)
	if kbd.is_pressed('s'):
		cam.release()
		cv2.destroyAllWindows()
		break  # esc to quit
	'''
	if cv2.waitKey(1) == 27: 
		cam.release()
		cv2.destroyAllWindows()
		break  # esc to quit
	'''
