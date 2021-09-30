import pyautogui as p

while True: 
    posXY = p.position() 
    color = p.pixel(posXY[0], posXY[1])
    print(f'click {posXY[0]} {posXY[1]} {color[0]} {color[1]} {color[2]} False Color')
