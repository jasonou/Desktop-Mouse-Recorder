import sys
import time
import os
import pyautogui as p
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
actions = []
cwd = os.getcwd()

def log(message):
    print(message)

def read():
    filename = f'{cwd}/output/{sys.argv[1]}.txt'
    with open(filename) as recoridngfile:
        global actions
        actions = [action.rstrip() for action in recoridngfile]
    log(f'[[ Reading Recording File ]] - [[ Success ]]')

def do_screenshot():
    img = p.screenshot()
    os.makedirs(f'{cwd}/logging', exist_ok=True) 
    img.save(f'{cwd}/logging/{time.time()}-PAUSED.PNG')

def do_notification():
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to=os.getenv('TWILIO_RECIEVING_NUMBER'),
        from_=os.getenv('TWILI_SENDING_NUMBER'),
        body="Bot has been paused...")
    log(f'[[ Notification Triggered ]]: texting')

def do_pause(min_seconds, max_seconds):
    sleepfor = randint(min_seconds*100, max_seconds*100)/100.0
    log(f'[[ Sleeping For ]] - [[ {str(sleepfor)} ]]')
    time.sleep(sleepfor)

def do_click(x_loc, y_loc):
    do_pause(0.1, 0.2)
    log(f'[[ Clicking ]]: x - {x_loc}, y - {y_loc}')
    p.click(x=x_loc, y=y_loc)

def verify(index, action, x, y, a, b, c, notify="False", type="Color"):
    log(f'[[ #{index + 1} Verifying ]]: type = {type}, action = {action}, notify = {str(notify)}')
    timetocheck = time.time()
    secondstowait = 30
    screenshot_done = False
    timestonotify = 5
    timesnotified = 0

    while True:
        color = p.pixel(int(x), int(y))
        time.sleep(0.05)
        if notify == 'True' and time.time() - timetocheck > secondstowait and timesnotified < timestonotify:
            if not screenshot_done:
                do_screenshot()
                screenshot_done = True
            timetocheck = time.time()
            do_notification()
            timesnotified += 1
        if type == 'Color':
            if color == (int(a), int(b), int(c)):
                do_click(int(x), int(y))
                break
        elif type == 'Image':
            os.makedirs(f'{cwd}/screenshots', exist_ok=True) 
            s8 = p.locateOnScreen(f'{cwd}/screenshots/{x}.PNG', confidence = 0.98)
            if s8 is not None:
                break

def act():
    global actions
    for index, action in enumerate(actions):
        if (action[0] != '#'):
            verify(index, *action.split(' '))
        else:
            print(action)

if __name__ == '__main__':
    read()
    while True:
        act()
