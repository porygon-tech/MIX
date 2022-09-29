#sudo apt-get install python3-tk python3-dev
#recommended adding a similar alias to ~/.bash_aliases:
#alias dump_kl='python3 /home/roman/LAB/gadgets/keyLgLite2.py > "keys_$(date +%d.%m.%Y_%H.%M).txt"'
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
