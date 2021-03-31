import argparse 
import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib.animation as animation 
import math
#python3 patern2.py --interval 100 



def DURL(mat, bordervalue=0):
    height, width = mat.shape
    D = np.delete((np.insert(mat, height, bordervalue, axis=0)), 0, axis=0)
    U = np.delete((np.insert(mat, 0, bordervalue, axis=0)), height, axis=0)
    R = np.delete((np.insert(mat, width, bordervalue, axis=1)), 0, axis=1)
    L = np.delete((np.insert(mat, 0, bordervalue, axis=1)), width, axis=1)
    return (D,U,R,L)


def flowt(A,B,k):  
    return k*A*(B-A)*(A-1)

def curvecum(x,v,L):
    return (1-((1)/(v*(x-1)+1)))*L

def tanh(x,v,t):
    return 0.5 + math.tanh((x-t)/v)/math.pi


height = 300
width  = 400
n=1

def randomGrid(height, width): 
    return np.random.rand(height, width)

kdiffA = 0.96
kdiffB = 1

def update(frameNum, img, A, B):
    
    global n
    Anew = A.copy()
    Bnew = B.copy()

    D,U,R,L = DURL(Anew)
    y_smooth = (Anew + (U + D)*kdiffA)/3
    x_smooth = (Anew + (L + R)*kdiffA)/3
    Anew = (y_smooth + x_smooth)/2
    
    D,U,R,L = DURL(Bnew)
    y_smooth = (Bnew + (U + D)*kdiffB)/3
    x_smooth = (Bnew + (L + R)*kdiffB)/3
    Bnew = (y_smooth + x_smooth)/2

    ADD1 = curvecum(n,0.011,0.8)
    ADD2 = tanh(n,2,70)

    #Anew = Anew + flowt(Anew,Bnew+0.2*(Anew**2-Anew),0.9) + ADD
    Anew = Anew + flowt(Anew,Bnew*(1-ADD1),0.9)
    Bnew = Bnew + flowt(Bnew*ADD2,Anew,0.1)
    
    img.set_data(Anew) 
    A[:] = Anew[:] 
    B[:] = Bnew[:]
    print(str(ADD1)+"\t"+str(n)+"\r", end = "")
    n+=1
    return img,

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', dest='interval', required=False) 
    args = parser.parse_args() 

    updateInterval = 5
    if args.interval: 
        updateInterval = int(args.interval)

    A = np.array([])
    B = np.array([])  
    A = randomGrid(height, width) 
    B = randomGrid(height, width)



    fig, ax = plt.subplots() 
    img = ax.matshow(A, interpolation='gaussian',cmap = 'gnuplot2') 
    #img = ax.matshow(B, interpolation='gaussian',cmap = 'jet') 
    #img = ax.matshow(A, interpolation='gaussian',cmap = 'flag_r') 
    ani = animation.FuncAnimation(fig, update, fargs=(img, A, B), 
                                  frames = 100, #duration
                                  interval=updateInterval, 
                                  save_count=50) 

    save=0
    if save==1:
        Writer = animation.writers['ffmpeg'] #requires installing ffmpeg
        writer = Writer(fps=15, metadata=dict(artist='Miki'), bitrate=1800)
        ani.save('pat3.mp4')

    else:
        plt.show() 







if __name__ == '__main__': 
    main() 
