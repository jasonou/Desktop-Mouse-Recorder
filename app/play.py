import sys
import os
import logging
import time
import keyboard
import pyautogui
from pprint import pformat
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv
from objects import DetectType, NotificationType, Settings, ScriptLogInfo

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='+ %(levelname)s %(funcName)s:%(lineno)s - %(message)s',
)
pyautogui.FAILSAFE = False

actions = []
cwd = os.getcwd()
previous_action = None
previous_action_completed = False
retries = 0
current_action_comment = None
startTime = time.time()
exit_script = False


def stop_script():
    global exit_script
    logging.info(f'Success: Exiting')
    exit_script = True


def setup_listener():
    logging.info(f'Success: Keyboard Listener Enabled, Press \'Esc\' to Stop.')
    keyboard.add_hotkey("esc", stop_script)


def read_settings():
    global actions
    global settings

    actions.pop(0)
    settings = Settings(*actions[0].split(' ', 1)[1].split())
    actions.pop(0)
    if len(sys.argv) == 3:
        settings.replay_loops = int(sys.argv[2])
    logging.info('Success: Settings loaded.')


def load_script():
    global actions

    try:
        with open(f'{cwd}/output/{sys.argv[1]}.txt') as script:
            actions = [action.rstrip() for action in script]
            logging.debug(f'{pformat(actions)}')
        logging.info('Success: Script file found.')
    except IOError:
        logging.error(
            f'Error: {sys.argv[1]}.txt not found')
        sys.exit(1)


def do_screenshot():
    os.makedirs(f'{cwd}/logging', exist_ok=True)
    pyautogui.screenshot().save(f'{cwd}/logging/{time.time()}-PAUSED.PNG')


def get_current_status(status):
    return f'[ {status} ]\n+ Filename: {sys.argv[1]}.txt\n+ Action: {current_action_comment}\n{ScriptLogInfo(str(time.time() - startTime), settings.loops_done, retries).getScriptLogInfoString()}'


def do_notification(status):
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to=os.getenv('TWILIO_RECIEVING_NUMBER'),
        from_=os.getenv('TWILI_SENDING_NUMBER'),
        body=get_current_status(status))
    logging.debug(f'Success: Notification Triggered')


def do_pause(min_seconds, max_seconds):
    time.sleep(randint(min_seconds * 100, max_seconds * 100) / 100.0)


def do_click(x, y):
    logging.info(
        f'{settings.loops_done}/{settings.replay_loops}: {current_action_comment}')
    do_pause(settings.click_delay_min, settings.click_delay_max)
    pyautogui.click(x, y)


def check_notify(notify, timetocheck, timesnotified):
    return notify == 'True' and time.time() - \
        timetocheck > settings.notification_delay and timesnotified < settings.notification_loops


def verify(action, x, y, a, b, c, repeat=1, notify="False", type="color"):
    global previous_action_completed
    global retries

    logging.debug(
        f'{settings.loops_done}/{settings.replay_loops}: type={type}, action={action}, notify={str(notify)}')

    previous_action_completed = False
    timetocheck = time.time()
    screenshot_done = False
    timesnotified = 0

    while not exit_script and not previous_action_completed:
        if check_notify(notify, timetocheck, timesnotified):
            logging.info("Attemping previous action...")
            if do_action(*previous_action.split(' ')):
                logging.info("Success: Previous Action Completed")
                previous_action_completed = True
                retries += 1
            else:
                if not screenshot_done and os.getenv('SCREENSHOT') == 'True':
                    do_screenshot()
                    screenshot_done = True
                timetocheck = time.time()
                do_notification(NotificationType().paused)
                timesnotified += 1
        if do_action(action, x, y, a, b, c, repeat, notify, type):
            break


def do_action(action, x, y, a, b, c, repeat=1, notify="False", type="color"):
    status = False
    for i in range(0, int(repeat)):
        if type == DetectType().color:
            if pyautogui.pixel(int(x), int(y)) == (int(a), int(b), int(c)):
                do_click(int(x), int(y))
                status = True
        elif type == DetectType().image:
            os.makedirs(f'{cwd}/screenshots', exist_ok=True)
            s8 = pyautogui.locateOnScreen(
                f'{cwd}/screenshots/68.jpg',
                confidence=0.99)
            if s8 is not None:
                do_click(int(x), int(y))
                status = True
        elif type == DetectType().noverify:
            do_click(int(x), int(y))
            status = True
    return status


def do_actions():
    global previous_action
    global current_action_comment

    for action in actions:
        if action[0] != '#':
            verify(*action.split(' '))
            previous_action = action
            do_pause(settings.click_delay_min, settings.click_delay_max)
        elif action[0] == '#':
            current_action_comment = action


def run_script():
    global settings

    while (settings.loops_done <
           settings.replay_loops or settings.replay_loops == 0) and not exit_script:
        do_actions()
        settings.loops_done += 1


if __name__ == '__main__':
    load_script()
    read_settings()
    setup_listener()
    run_script()
    do_notification(NotificationType().completed)
    logging.info(get_current_status(NotificationType().completed))
