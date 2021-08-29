import cv2
import numpy as np
import time
import keyboard as kbd
import sys

#sudo python3 Documents/surveillance.py 15 2

threshold = int(sys.argv[1])
delay     = int(sys.argv[2])

def stream_optical_flow():
	cv2.destroyAllWindows()
	cam = cv2.VideoCapture(0)
	_, A = cam.read()
	A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
	while True:
		B = A
		_, A = cam.read()
		img = A
		A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(B, A, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
		magnitude, angle = cv2.cartToPolar(flow[:,:, 0], flow[:,:, 1])
		#print(str(magnitude.mean()) + '\t' + str(magnitude.std()) + '\t' + str(angle.mean()) + '\t' + str(angle.std()) + ('\r'))
		if magnitude.mean() > threshold:
			time.sleep(delay)
			t = time.ctime()
			print('screenshot taken (' + str(t) + ')')
			print('\taverage optical flow: ' + str(magnitude.mean()))
			print('\taverage angle:        ' + str(angle.mean()))
			print('\toptical flow std:     ' + str(magnitude.std()) + '\n')
			cv2.imwrite('/home/mroman/Pictures/captures/capture ' + t + '.png', img)
		
		if kbd.is_pressed('s'):
			break  # esc to quit

	cv2.destroyAllWindows()
	cam.release()


cv2.destroyAllWindows()
stream_optical_flow()



