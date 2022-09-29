#sudo apt-get install python3-tk python3-dev
#rm keystrokes_*
from pynput.keyboard import Key, Listener

def on_press(key):
    if key == Key.esc:
        f.close()
        return False
    try:
        print('{0}'.format(key.char), end ="")
    except AttributeError:
        print('\n\t{0}'.format(key))


with Listener(
        on_press=lambda event: on_press(event)
        ) as listener:
    listener.join()