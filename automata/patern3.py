import argparse 
import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib.animation as animation 
#python3 patern2.py --interval 100 



def DURL(mat, bordervalue=0):
    height, width = mat.shape
    D = np.delete((np.insert(mat, height, bordervalue, axis=0)), 0, axis=0)
    U = np.delete((np.insert(mat, 0, bordervalue, axis=0)), height, axis=0)
    R = np.delete((np.insert(mat, width, bordervalue, axis=1)), 0, axis=1)
    L = np.delete((np.insert(mat, 0, bordervalue, axis=1)), width, axis=1)
    return (D,U,R,L)


def flowA(A,B,v):  
    return v*B*(0.5-B)*(B-1)

def flowB(A,B,v,k):
    return flowA(B,-k*A**2+A,v)

height = 200
width  = 200
t = 0.51

def randomGrid(height, width): 
    return np.random.rand(height, width)

def update(frameNum, img, A, B):
    k=0.01
    v=0.2
    Anew = A.copy()
    Bnew = B.copy()

    D,U,R,L = DURL(Anew, 0)
    y_smooth = (D + Anew + U)/3
    x_smooth = (R + Anew + L)/3
    Anew = (y_smooth + x_smooth)/2
    
    D,U,R,L = DURL(Bnew)
    y_smooth = (D + Bnew + U)/3
    x_smooth = (R + Bnew + L)/3
    Bnew = (y_smooth + x_smooth)/2

    Anew = Anew + flowA(Anew,Bnew,v)
    Bnew = Bnew + flowB(Anew,Bnew,v,k)
    img.set_data(Anew) 
    A[:] = Anew[:] 
    B[:] = Bnew[:] 
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
    img = ax.matshow(A, interpolation='gaussian',cmap = 'jet') 
    #img = ax.matshow(B, interpolation='gaussian',cmap = 'gnuplot2') 
    #img = ax.matshow(B, interpolation='gaussian',cmap = 'flag') 
    ani = animation.FuncAnimation(fig, update, fargs=(img, A, B), 
                                  frames = 10, #duration
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
