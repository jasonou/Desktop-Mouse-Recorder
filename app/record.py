import sys
import os
import pyautogui
from dotenv import load_dotenv
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button
from pynput.keyboard import Key
from objects import Action, ActionType, DetectType, Settings


load_dotenv()
mouse_listener = None
keyboard_listener = None
current_working_dir = os.getcwd()
actions = [
    Settings(
        os.getenv('REPLAY_LOOPS'),
        os.getenv('LOG_COMMENTS'),
        os.getenv('LOG_ACTIONS'),
        os.getenv('LOG_DEBUGS'),
        os.getenv('CLICK_DELAY_MIN'),
        os.getenv('CLICK_DELAY_MAX'),
        os.getenv('NOTIFICATION_DELAY'),
        os.getenv('NOTIFICATION_LOOPS')).getSettingsString()]


def output():
    os.makedirs(f'{current_working_dir}/output', exist_ok=True)
    filename = f'{current_working_dir}/output/{sys.argv[1]}.txt'
    with open(filename, 'w') as f:
        for action in actions:
            f.write('%s\n' % action)
    print(f'[[ Recording Generated ]] - [[ {filename} ]]')


def on_click(x, y, button, pressed):
    color = pyautogui.pixel(x, y)
    comment = f'# {sys.argv[1]} '
    action = Action(
        ActionType().click,
        x,
        y,
        color[0],
        color[1],
        color[2],
        "True",
        DetectType().color).getActionString()

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
