import sys
import time
import os
import keyboard
import pyautogui as p
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv
from objects import Settings, DetectType, NotificationType

load_dotenv()
actions = []
cwd = os.getcwd()
settings_read = False
previous_action = None
current_action_comment = None


def stop():
    print(f'[[ Exiting... ]]')
    os._exit(0)


keyboard.add_hotkey("ctrl+esc", stop)


def read_settings():
    global actions
    global settings

    settings = Settings(*actions[0].split(' ', 1)[1].split())
    actions.pop(0)


def read_script():
    filename = f'{cwd}/output/{sys.argv[1]}.txt'
    with open(filename) as recordingfile:
        global actions
        actions = [action.rstrip() for action in recordingfile]


def read():
    filename = f'{cwd}/output/{sys.argv[1]}.txt'
    with open(filename) as recordingfile:
        global actions
        actions = [action.rstrip() for action in recordingfile]


def do_screenshot():
    img = p.screenshot()
    os.makedirs(f'{cwd}/logging', exist_ok=True)
    img.save(f'{cwd}/logging/{time.time()}-PAUSED.PNG')


def do_notification(status):
    global current_action_comment

    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to=os.getenv('TWILIO_RECIEVING_NUMBER'),
        from_=os.getenv('TWILI_SENDING_NUMBER'),
        body=f'Bot for file <<{sys.argv[1]}.txt>> has been {status}...\nCurrent Action: {current_action_comment}')
    if settings.log_debug:
        print(f'[[ Notification Triggered ]]: texting')


def do_pause(min_seconds, max_seconds):
    sleepfor = randint(min_seconds * 100, max_seconds * 100) / 100.0
    if settings.log_debug:
        print(f'[[ Sleeping For ]] - [[ {str(sleepfor)} ]]')
    time.sleep(sleepfor)


def do_click(x, y):
    do_pause(settings.click_delay_min, settings.click_delay_max)
    if settings.log_debug:
        print(f'[[ Clicking ]]: x - {x}, y - {y}')
    p.click(x, y)


def verify(action, x, y, a, b, c, notify="False", type="color"):
    if settings.log_actions:
        print(
            f'<< #{settings.loops_done} >> [[ Verifying ]]: type = {type}, action = {action}, notify = {str(notify)}')

    timetocheck = time.time()
    secondstowait = settings.notification_delay
    screenshot_done = False
    timestonotify = settings.notification_loops
    timesnotified = 0

    while True:
        color = p.pixel(int(x), int(y))
        time.sleep(0.2)

        if notify == 'True' and time.time(
        ) - timetocheck > secondstowait and timesnotified < timestonotify:
            if not screenshot_done:
                do_screenshot()
                screenshot_done = True
            timetocheck = time.time()
            do_notification(NotificationType().paused)
            timesnotified += 1
        if type == DetectType().color:
            if color == (int(a), int(b), int(c)):
                do_click(int(x), int(y))
                break
        elif type == DetectType().image:
            os.makedirs(f'{cwd}/screenshots', exist_ok=True)
            s8 = p.locateOnScreen(
                f'{cwd}/screenshots/68.jpg',
                confidence=0.99)
            if s8 is not None:
                do_click(int(x), int(y))
                break
        elif type == DetectType().noverify:
            do_click(int(x), int(y))
            break


def do_actions():
    global previous_action
    global current_action_comment

    for action in actions:
        if action[0] != '#':
            verify(*action.split(' '))
            previous_action = action
        elif action[0] == '#' and settings.log_comments:
            current_action_comment = action
            print(current_action_comment)


def do_loops():
    global settings

    while settings.loops_done < settings.replay_loops or settings.replay_loops == 0:
        do_actions()
        settings.loops_done += 1


if __name__ == '__main__':
    read_script()
    read_settings()
    do_loops()
    do_notification(NotificationType().stopped)
