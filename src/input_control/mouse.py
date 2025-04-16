############################
# @author EliasDH Team     #
# @see https://eliasdh.com #
# @since 01/01/2025        #
############################

import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

def move_mouse_to(x, y):
    pyautogui.moveTo(x, y)

def simulate_click():
    pyautogui.click()