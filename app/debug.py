from pynput import keyboard
import time
import pyautogui

stopScript = False


def on_press(key):
    global stopScript

    if key == keyboard.Key.esc:
        print(f'- Success: Exiting', flush=True)
        stopScript = True
        return False


def debug():
    posXY = pyautogui.position()
    color = pyautogui.pixel(posXY[0], posXY[1])
    print(
        f'click {posXY[0]} {posXY[1]} {color[0]} {color[1]} {color[2]} False Color',
        flush=True)


def run():
    with keyboard.Listener(on_press=on_press) as listener:
        print(f'- Success: Debugging, Press \'Esc\' to Stop.', flush=True)
        while stopScript == False:
            debug()
            time.sleep(0.5)


if __name__ == '__main__':
    run()
