import sys
import os
import pyautogui
import time

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button
from pynput.keyboard import Key

from dotenv import load_dotenv

from objects import Action, ActionType, DetectType, Settings

load_dotenv()
current_working_dir = os.getcwd()
keyboard_listener = None
mouse_listener = None
actions = []
settings = None
stopScript = False


def verify_environment():
    try:
        file = open('.env', 'r')
        print('- Success: Environment file found.', flush=True)
    except IOError:
        print(
            '- Error: Please copy the ".env-template" file and create a ".env" file.',
            flush=True)
        sys.exit(1)


def load_environment():
    global actions
    global settings

    settings = Settings(
        os.getenv('REPLAY_LOOPS'),
        os.getenv('CLICK_DELAY_MIN'),
        os.getenv('CLICK_DELAY_MAX'),
        os.getenv('NOTIFICATION_DELAY'),
        os.getenv('NOTIFICATION_LOOPS'))

    actions = [
        settings.getSettingsColumns(),
        settings.getSettingsString()]
    print('- Success: Environment file loaded.', flush=True)


def on_press(key):
    global stopScript

    if key == Key.esc:
        print(f'- Success: Exiting', flush=True)
        stopScript = True
        return False


def on_click(x, y, button, pressed):
    global actions

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
        print(f'+ Recording: {action}', flush=True)
    if stopScript:
        return False
    elif button == Button.right and pressed:
        pass


def output():
    os.makedirs(f'{current_working_dir}/output', exist_ok=True)
    filename = f'{current_working_dir}/output/{sys.argv[1]}.txt'
    with open(filename, 'w') as f:
        for action in actions:
            f.write('%s\n' % action)
    print(f'= Recorded: {filename}', flush=True)


def configure_listeners():
    global keyboard_listener, mouse_listener

    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()
    print(f'- Success: Keyboard Listener Enabled, Press \'Esc\' to Stop.', flush=True)

    with MouseListener(on_click=on_click) as listener:
        print(f'- Success: Mouse Listener Enabled', flush=True)
        while stopScript == False:
            time.sleep(0.3)


if __name__ == '__main__':
    verify_environment()
    load_environment()
    configure_listeners()
    output()
