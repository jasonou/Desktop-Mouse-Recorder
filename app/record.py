import sys
import os
import pyautogui
from dotenv import load_dotenv
from pynput import mouse
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button
from pynput.keyboard import Key

load_dotenv()
mouse_listener = None
keyboard_listener = None
current_working_dir = os.getcwd()
actions = [
    f'settings replay_loops {os.getenv("REPLAY_LOOPS")}',
    f'settings log_comments {os.getenv("LOG_COMMENTS")}',
    f'settings log_actions {os.getenv("LOG_ACTIONS")}',
    f'settings log_debug {os.getenv("LOG_DEBUGS")}',
    f'settings click_delay_min {os.getenv("CLICK_DELAY_MIN")}',
    f'settings click_delay_max {os.getenv("CLICK_DELAY_MAX")}',
    f'settings notification_delay {os.getenv("NOTIFICATION_DELAY")}',
    f'settings notification_loops {os.getenv("NOTIFICATION_LOOPS")}'
]


def output():
    os.makedirs(f'{current_working_dir}/output', exist_ok=True)
    filename = f'{current_working_dir}/output/{sys.argv[1]}.txt'
    with open(filename, 'w') as f:
        for action in actions:
            f.write('%s\n' % action)
    print(f'[[ Recording Generated ]] - [[ {filename} ]]')


def on_click(x, y, button, pressed):
    color = pyautogui.pixel(x, y)
    comment = f'# '
    action = f'click {x} {y} {color[0]} {color[1]} {color[2]} False Color'

    if button == Button.left and pressed:
        actions.append(comment)
        actions.append(action)
        print(f'<< Recording... >> - << {action} >>')
    elif button == Button.right and pressed:
        pass


def on_press(key):
    if key == Key.esc:
        output()
        print(f'[[ Exiting... ]]')
        os._exit(0)


def setup_listeners():
    global mouse_listener, keyboard_listener
    mouse_listener = MouseListener(on_click=on_click)
    keyboard_listener = KeyboardListener(on_press=on_press)


def start_listeners():
    mouse_listener.start()
    keyboard_listener.start()


def join_listeners():
    print(f'[[ Starting Recording ]] - [[ Press "esc" to exit ]]')
    mouse_listener.join()
    keyboard_listener.join()


if __name__ == '__main__':
    setup_listeners()
    start_listeners()
    join_listeners()
