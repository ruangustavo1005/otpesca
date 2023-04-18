import cv2, numpy, pyautogui, keyboard, time, os
from dotenv import load_dotenv
from get_capturaveis import get as getCapturaveis
load_dotenv()

pyautogui.PAUSE = 0.1

needle = cv2.cvtColor(cv2.imread('img/needle.jpg'), cv2.COLOR_BGR2GRAY)
battle = cv2.cvtColor(cv2.imread('img/battle.jpg'), cv2.COLOR_BGR2GRAY)
rod_vazia = cv2.cvtColor(cv2.imread('img/rod_vazia.jpg'), cv2.COLOR_BGR2GRAY)

count_rod_vazia = 0
pausado = True

print('pressione ESC para iniciar')
while True:
  if keyboard.is_pressed('esc'): 
    pausado = not pausado
    print('pause' if pausado else 'start')
    time.sleep(2)
    if not pausado:
      capturaveis = getCapturaveis() if os.getenv('AUTO_CAPTURA') == '1' else {};
    
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
  
  frame = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)
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
  
  if os.getenv('AUTO_CAPTURA') == '1':
    log = []
    frame = cv2.cvtColor(numpy.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)
    for capturavelName, capturavel in capturaveis.items():
      match = cv2.matchTemplate(frame, capturavel['needle'], cv2.TM_CCOEFF_NORMED)
      min_val, max_val, min_loc, (x, y) = cv2.minMaxLoc(match)
      log.append(f'{capturavelName}: {max_val:.2f}')
      if max_val > capturavel['conf']['limiar']:
        print(f'{capturavelName} disponível pra captura!')
        pyautogui.press('p')
        time.sleep(0.2)
        pyautogui.moveTo(x + capturavel['conf']['gap-x'], y + capturavel['conf']['gap-y'])
        pyautogui.click()
        time.sleep(0.2)
    if len(log) > 0:
      print(" | ".join(log))
  
  match = cv2.matchTemplate(frame, rod_vazia, cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
  
  if max_val > 0.98:
    count_rod_vazia += 1
    if (count_rod_vazia > (1 if os.getenv('AUTO_CAPTURA') == '1' else 4)):
      match = cv2.matchTemplate(frame, needle, cv2.TM_CCOEFF_NORMED)
      min_val, max_val, min_loc, (x, y) = cv2.minMaxLoc(match)

      pyautogui.moveTo(x + 10, y + 10)
      pyautogui.click()
      pyautogui.click()
      count_rod_vazia = 0