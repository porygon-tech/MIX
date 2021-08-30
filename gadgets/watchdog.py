import cv2
import numpy as np
import time
import sys
import matplotlib.pyplot as plt 


#sudo python3 ~/Documents/watchdog.py 15 2
#sudo python3 ~/Documents/watchdog.py 12 2 silent

threshold = int(sys.argv[1])
delay     = int(sys.argv[2])
if len(sys.argv) > 3:
	silent = sys.argv[3]
else:
	silent = 'nonsilent'

def stream_optical_flow(silent=False):
	if silent:
		print('running in silent mode\n')
	cv2.destroyAllWindows()
	cam = cv2.VideoCapture(0)
	_, A = cam.read()
	A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
	y=[]
	count=[]
	frame = 50
	maxpeak = 20
	i=0
	while True:
		B = A
		_, A = cam.read()
		img = A
		A = cv2.cvtColor(np.float32(A), cv2.COLOR_BGR2GRAY)
		#flow = cv2.calcOpticalFlowFarneback(B, A, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 10, poly_n = 5, poly_sigma = 1.1, flags = 0)
		flow = cv2.calcOpticalFlowFarneback(B, A, None, pyr_scale = 0.5, levels = 10, winsize = 19, iterations = 10, poly_n = 7, poly_sigma = 1.5, flags = 0)
		magnitude, angle = cv2.cartToPolar(flow[:,:, 0], flow[:,:, 1])

#========
		if not silent:
			print(str(magnitude.mean()) + '\t' + str(magnitude.std()) + '\t' + str(angle.mean()) + '\t' + str(angle.std()) + ('\r'))
			# Create mask
			mask = np.zeros_like(img)
			# Set image saturation to maximum value as we do not need it
			mask[:,:, 1] = 255
			# Set image hue according to the optical flow direction
			mask[:,:, 0] = angle * 180 / np.pi / 2
			# Set image value according to the optical flow magnitude (normalized)
			mask[:,:, 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
			# Convert HSV to RGB (BGR) color representation
			rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
			dense_flow = cv2.addWeighted(img, 1,rgb, 2, 0)
			cv2.imshow('dense optical flow', dense_flow)
		#========
		
			i+=1
			plt.axis([0, i, 0, maxpeak])
			count.append(i)
			y.append(magnitude.mean())
			if len(count) >= frame:
				plt.axis([i-frame, i, 0, maxpeak])
				count.pop(0)
				y.pop(0)
			plt.plot(count, y, 'c-')
			plt.pause(0.05)
		
			
		#========
			if cv2.waitKey(1) == 27: 
				break  # esc to quit
			
#========
		if magnitude.mean() > threshold:
			time.sleep(delay)
			t = time.ctime()

			print('screenshot taken (' + str(t) + ')')
			print('\taverage optical flow: ' + str(magnitude.mean()))
			print('\taverage angle:        ' + str(angle.mean()))
			print('\toptical flow std:     ' + str(magnitude.std()) + '\n')
			cv2.imwrite('/home/mroman/Pictures/captures/capture ' + t + '.png', img)

	plt.show()
	cv2.destroyAllWindows()
	cam.release()


cv2.destroyAllWindows()
stream_optical_flow(silent=='silent')









while True:
	i+=1
	plt.axis([0, i, 0, 100])
	count.append(i)
	y.append(cpu_percent())
	if len(count) >= frame:
		plt.axis([i-frame, i, 0, 100])
		count.pop(0)
		y.pop(0)
	plt.plot(count, y, 'c-')
	plt.pause(0.05)
plt.show()
