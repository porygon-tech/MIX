import matplotlib.pyplot as plt 
from psutil import cpu_percent

y=[]
count=[]
frame = 200

i=0
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
