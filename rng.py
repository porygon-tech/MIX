from datetime import datetime
import math

#from uniform(0,1) to gaussian-like distribution 
def expansor(x,D=0.5):
	return(D * 0.5 * math.log(x / (1 - x)))

x = datetime.now().microsecond / 1000000
for i in range(1,50):
	x = x * 4 * (1 - x)
	print(expansor(x,20))
