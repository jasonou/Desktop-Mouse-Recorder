import sys
import time
import os
import pyautogui as p
from pynput import mouse

actions = []
cwd = os.getcwd()

def log(message):
    print(message)

def output():
    os.makedirs(f'{cwd}/output', exist_ok=True) 
    filename = f'{cwd}/output/{sys.argv[1]}.txt'
    with open(filename, 'w') as f:
        for action in actions:
            f.write("%s\n" % action)
    return filename

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        color = p.pixel(x, y)
        comment = f'# action, update comment here'
        action = f'click {x} {y} {color[0]} {color[1]} {color[2]} False Color'
        actions.append(comment)
        actions.append(action)
        log(action)
    elif button == mouse.Button.right:
        log(f'[[ Stopping Recording ]] - [[ Right Click Pressed ]]')
        log(f'[[ Recording Generated ]] - [[ {output()} ]]')
        return False

if __name__ == '__main__':
    listener = mouse.Listener(on_click=on_click)
    log(f'[[ Starting Recording ]] - [[ Right Click to Stop ]]')
    listener.start()
    listener.join()
