#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib. Use pavucontrol to redirect output music.

Matplotlib and NumPy have to be installed.
python visualizer2.py -r 2048 -w 500 -n 21 -c hsv_r
python visualizer2.py -w 400 -n 50 -c gnuplot
python visualizer2.py -w 400 -n 50 -c prism
python visualizer2.py -n 45 -c flag -v 20
python visualizer2.py -w 400 -n 50 -c twilight -v 20

"""
import argparse
import queue
import sys
import os

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


from scipy import fft
def frequency_spectrum(x, sf):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    k = np.arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft.rfft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]

    return frqarr, abs(x)



parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    '-c', '--cmap', type=str, default='inferno',
    help='display colormap (default: %(default)s)')
parser.add_argument(
    '-v', '--convolutions', type=int, default=1,
    help='number of convolutions (default: %(default)s)')

args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')

mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])

from scipy.ndimage import zoom
def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    global signal
    global is_recording
    global tail
    global writingArray
    

    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        signal = np.roll(signal, -shift, axis=0)
        signal[-shift:, :] = data
        
        rms = np.sqrt(np.mean(np.square(signal)))
        #print(rms)
        spectrum = (frq, X) = frequency_spectrum(signal[:,0], args.samplerate)
        #yd=np.array([element for element in spectrum[0] for _ in range(2)])[:,np.newaxis]
        threshold = 0.05
        maxtail = 200


        
        #plotdata = np.repeat(X,2)[:,np.newaxis]*20
        #plotdata = np.repeat(plotdata,frameheight,axis=1)
        #if len(X)%2!=0:

        # BASS RESPONSE
        basspower = X[:int(len(X)/4)].sum()/X.sum()
        X*=basspower

        # ECHO
        #X = signal[signal % 2 == 0]
        #X += ((signal[-len(X):,0])**2)*0.1


        # WRAP
        X=np.roll(X,-1); X[-1]=X[-2]

        # CONVOLUTION
        for _ in range(args.convolutions):
            #offset1=np.roll(X,-1); offset1[-1]=offset[-2]
            #offset2=np.roll(X,+1); offset2[0]=offset2[1]
            X+= np.roll(X,-1)+np.roll(X,+1) 
            X/=3
            X[-1]=X[-2]
            X[0]=X[1]

        # SYMMETRY
        plotdatav = np.concatenate((np.flip(X),X))[:,np.newaxis]*50
        plotdata= plotdatav @ plotdatav.T



        #plotdata = signal
        if not is_recording and rms > threshold:
            is_recording = True
            tail=0
            print("peak detected: " + str(rms))
            writingArray = data.copy()
        if is_recording:
            writingArray = np.append(writingArray,data,axis=0)
            if rms < threshold:
                tail+=1
                #print("cooldown " + str(100*round(tail/maxtail,4)) + "%")
                if tail > maxtail:
                    is_recording = False
                    print("REC STOPPED")

            else:
                tail=0
                #print("refresh tail")


    for column, line in enumerate(lines):

        line.set_ydata(plotdata[:, column])

    im.set_data(plotdata)

    return im,
    #return lines

from matplotlib.colors import LogNorm
try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']
    '''
    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))
    signal   = np.zeros((length, len(args.channels)))
    is_recording = False
    writingArray = np.array([[]])
    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(args.channels) > 1:
        ax.legend(['channel {}'.format(c) for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    #ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    '''

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    frameheight=500
    #plotdata = np.zeros((length, frameheight))
    plotdata  = np.zeros((length, length))
    
    signal   = np.zeros((length, len(args.channels)))
    is_recording = False
    writingArray = np.array([[]])
    fig, ax = plt.subplots(figsize=(2,2))
    lines = ax.plot(plotdata[:,0])
    im    = ax.imshow(plotdata, cmap=args.cmap, norm=LogNorm(vmin=0.001, vmax=1))


    #axs[0].axis((0, len(plotdata), -.1, 5))
    
    # ax.tick_params(bottom=False, top=False, labelbottom=False,
    #                right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    

    #=========
    tail=0
    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    with stream:
        plt.show()
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))

#pacmd update-sink-proplist MySink device.description=MySink
#pacmd load-module module-loopback sink=MySink
