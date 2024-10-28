
import time
import random
from colorama import Fore, Back, Style
import pyautogui

def idd():
    # print(pyautogui.size())
    pyautogui.click(button="right")
    
def printer(txt):
    txt = txt.upper()
    print('#### '+ txt)
    # print(Fore.YELLOW + '#### '+txt)
    # print(Style.RESET_ALL)

def input_timer(el, text):
    for character in text:
        var_sp = round(random.uniform(0.1, 0.32), 2)
        print(var_sp)
        time.sleep(var_sp) # pause for 0.3 seconds
        el.send_keys(character)