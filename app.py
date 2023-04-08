import cv2, numpy, pyautogui, keyboard, time

pyautogui.PAUSE = 0.1

needle = cv2.cvtColor(cv2.imread('needle.jpg'), cv2.COLOR_BGR2GRAY)
battle = cv2.cvtColor(cv2.imread('battle.jpg'), cv2.COLOR_BGR2GRAY)
rod_vazia = cv2.cvtColor(cv2.imread('rod_vazia.jpg'), cv2.COLOR_BGR2GRAY)

frame = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)
match = cv2.matchTemplate(frame, needle, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, (x, y) = cv2.minMaxLoc(match)

pyautogui.moveTo(x + 10, y + 10)
pyautogui.click()
pyautogui.click()

count_rod_vazia = 0
pausado = False

while True:
    if keyboard.is_pressed('esc'): 
        pausado = not pausado
        print('pause' if pausado else 'start')
        time.sleep(2)
        
    if (pausado):
        continue
        
    frame = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)
    match = cv2.matchTemplate(frame, needle, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, (x, y) = cv2.minMaxLoc(match)
  
    if max_val > 0.9918:
        pyautogui.moveTo(x + 10, y + 10)
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()
    
    match = cv2.matchTemplate(frame, battle, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, (x, y) = cv2.minMaxLoc(match)
    
    if max_val < 0.98:
        pyautogui.moveTo(x + 10, y + 70)
        pyautogui.click()
        
        pyautogui.press('f1')
        pyautogui.press('f2')
        pyautogui.press('f3')
        pyautogui.press('f4')
        pyautogui.press('f5')
        pyautogui.press('f6')
        pyautogui.press('f7')
        pyautogui.press('f8')
        pyautogui.press('f9')
        pyautogui.press('f10')
    
    
    match = cv2.matchTemplate(frame, rod_vazia, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    
    if max_val > 0.98:
        count_rod_vazia += 1
        if (count_rod_vazia > 5):
            frame = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)
            match = cv2.matchTemplate(frame, needle, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, (x, y) = cv2.minMaxLoc(match)

            pyautogui.moveTo(x + 10, y + 10)
            pyautogui.click()
            pyautogui.click()
            count_rod_vazia = 0