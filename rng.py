from datetime import datetime
import math

#from uniform(0,1) to gaussian-like distribution 
def expansor(x,D=0.5):
	return(D * 0.5 * math.log(x / (1 - x)))

x = datetime.now().microsecond / 1000000
for i in range(1,50):
	x = x * 4 * (1 - x)
	print(expansor(x,20))

	
	
	
	
import matplotlib.pyplot as plt 

y=[]
count=[]
frame = 200
up = 60
down = -60

i=0
x = datetime.now().microsecond / 1000000

while True:
	i+=1
	plt.axis([0, i, down, up])
	count.append(i)
	x = x * 4 * (1 - x)
	y.append(expansor(x,10))
	if len(count) >= frame:
		plt.axis([i-frame, i, down, up])
		count.pop(0)
		y.pop(0)
	plt.plot(count, y, 'r-')
	plt.pause(0.05)

#plt.show()
