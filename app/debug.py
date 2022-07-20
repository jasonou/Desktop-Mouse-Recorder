import os
import time
import keyboard
import pyautogui as p


def stop():
    print(f'[[ Exiting... ]]')
    os._exit(0)


keyboard.add_hotkey("esc", stop)

while True:
    time.sleep(0.5)
    posXY = p.position()
    color = p.pixel(posXY[0], posXY[1])
    print(
        f'click {posXY[0]} {posXY[1]} {color[0]} {color[1]} {color[2]} False Color')
