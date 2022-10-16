import pyautogui as pag
import pynput
import time
import os


try: 
    while True:
        x, y = pag.position()
        print(f"X: {x}, Y: {y}")
        time.sleep(0.05)
        os.system("clear")
except KeyboardInterrupt:
    print("\n")

while True:
    input()
    pag.click()
    pag.moveRel(0, -110)

