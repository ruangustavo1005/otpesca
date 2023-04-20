import cv2
import numpy
import pyautogui
import keyboard
import time
import os
from src.utils import otpWindow, capturaveis, output
from dotenv import load_dotenv

KEY_START_PAUSE = 'pause'


class Main:

  def __init__(self):
    load_dotenv()
    pyautogui.PAUSE = 0.1

    self.otpWindow: otpWindow.OtpWindow = otpWindow.OtpWindow()

    self.needlePescaReady = cv2.cvtColor(cv2.imread('img/pescaReady.jpg'), cv2.COLOR_BGR2GRAY)
    self.needleBattleVazio = cv2.cvtColor(cv2.imread('img/battleVazio.jpg'), cv2.COLOR_BGR2GRAY)
    self.needleRodVazia = cv2.cvtColor(cv2.imread('img/rodVazia.jpg'), cv2.COLOR_BGR2GRAY)

    self.outputAutoCaptura: output.Output = output.Output(0, 0)
    self.outputPauseStart: output.Output = output.Output(0, 60)
    self.outputResetCapturaveis: output.Output = output.Output(1, 60)
    self.outputUltimosCapturaveis: output.Output = output.Output(0, 145)
    self.ultimosCapturaveis = []
    self.outputUltimosMatchsCapturaveis: output.Output = output.Output(5, 0)
    self.ultimosMatchsCapturaveis = []

    self.countRodVazia: int = 0
    self.pausado: bool = True

    self.autoCaptura: bool = int(os.getenv('AUTO_CAPTURA')) == 1
    self.showInfoAutoCaptura()

    self.outputPauseStart.write('OTPesca pronto! Pressione a tecla PAUSE para iniciar.')

    if self.autoCaptura:
      try:
        self.capturaveis: capturaveis.Capturaveis = capturaveis.Capturaveis(self.otpWindow.get())
      except Exception as e:
        self.outputAutoCaptura.write(str(e), True, 0, 0, True)
        time.sleep(5)
        exit()

  def mainLoop(self):
    while True:
      self.verifyPauseStart()

      if (self.pausado):
        continue

      frame = self.otpWindow.getScreenshot()
      self.verifyPescaReady(frame)

      frame = self.otpWindow.getScreenshot()
      self.verifyBattleReady(frame)

      if self.autoCaptura:
        self.verifyCapturaveis(frame)

      self.verifyRodVazia(frame)

  def verifyPauseStart(self):
    if keyboard.is_pressed(KEY_START_PAUSE):
      self.pausado = not self.pausado
      self.outputPauseStart.write('OTPesca pausado. Pressione a tecla PAUSE para iniciar.' if self.pausado else 'Iniciando OTPesca...')
      self.atualizaUltimosCapturaveis()
      self.atualizaUltimosMatchsCapturaveis()
      time.sleep(1)

      if not self.pausado:
        if self.autoCaptura:
          self.outputResetCapturaveis.write('Recarregando configurações de capturáveis...')
          try:
            self.capturaveis.reset(self.otpWindow.get())
          except Exception as e:
            self.outputAutoCaptura.write(str(e), bold=True)
            time.sleep(5)
            exit()
          self.outputResetCapturaveis.write('Configurações de capturáveis carregadas.')
          self.atualizaUltimosCapturaveis()
          self.atualizaUltimosMatchsCapturaveis()
        self.otpWindow.reset().activate()
        time.sleep(1)
        self.windowLocX, self.windowLocY = self.otpWindow.getWindowLoc()
        self.outputPauseStart.write('OTPesca em execução. Pressione a tecla PAUSE por alguns segundos para pausar.')
        self.atualizaUltimosCapturaveis()
        self.atualizaUltimosMatchsCapturaveis()
    return self

  def verifyPescaReady(self, frame):
    max_val, x, y = self.matchTemplate(frame, self.needlePescaReady)
    if max_val > 0.9918:
      pyautogui.moveTo(x + 15, y + 10)
      pyautogui.click()
      pyautogui.click()
      pyautogui.click()

  def verifyBattleReady(self, frame):
    max_val, x, y = self.matchTemplate(frame, self.needleBattleVazio)

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

  def verifyCapturaveis(self, frame):
    log = {}
    for capturavelName, capturavel in self.capturaveis.get().items():
      max_val, x, y = self.matchTemplate(frame, capturavel['needle'])
      log[capturavelName] = f'{max_val:.3f}'
      if max_val > capturavel['conf']['limiar']:
        self.ultimosCapturaveis.insert(0, f'{capturavelName} disponível pra captura!')
        self.atualizaUltimosCapturaveis()
        pyautogui.press('p')
        time.sleep(0.2)
        pyautogui.moveTo(x + capturavel['conf']['gap-x'], y + capturavel['conf']['gap-y'])
        pyautogui.click()
        time.sleep(0.2)
    if len(log) > 0:
      self.ultimosMatchsCapturaveis.insert(0, log)
      self.atualizaUltimosMatchsCapturaveis()

  def atualizaUltimosCapturaveis(self):
    for i in range(min(10, len(self.ultimosCapturaveis))):
      self.outputUltimosCapturaveis.write(self.ultimosCapturaveis[i], i, autoErase=(i == 0))

  def atualizaUltimosMatchsCapturaveis(self):
    if len(self.ultimosMatchsCapturaveis) > 0:
      headers = []
      widthCols = {}

      for header in self.ultimosMatchsCapturaveis[0].keys():
        widthCols[header] = max(5, len(header))
        headers.append(header.ljust(widthCols[header]))

      self.outputUltimosMatchsCapturaveis.write(' | '.join(headers))

      for i in range(min(20, len(self.ultimosMatchsCapturaveis))):
        print(self.ultimosMatchsCapturaveis[i].items())
        log = []
        for key, value in self.ultimosMatchsCapturaveis[i].items():
          widthCol = widthCols[key]
          widthColL = int((widthCol - 5) / 2)
          widthColR = widthCol - widthColL - 5
          print(widthColL, widthColR)
          log.append((' ' * widthColL) + value + (' ' * widthColR))

        self.outputUltimosMatchsCapturaveis.write(' | '.join(log), i + 1, autoErase=False)

  def verifyRodVazia(self, frame):
    max_val, x, y = self.matchTemplate(frame, self.needleRodVazia)

    if max_val > 0.98:
      self.countRodVazia += 1
      if (self.countRodVazia > (1 if self.autoCaptura else 4)):
        pyautogui.moveTo(x + 125, y + 15)
        pyautogui.click()
        pyautogui.click()
        self.countRodVazia = 0

  def matchTemplate(self, frame, needle):
    match = cv2.matchTemplate(frame, needle, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, (x, y) = cv2.minMaxLoc(match)
    return max_val, x + self.windowLocX, y + self.windowLocY

  def showInfoAutoCaptura(self):
    self.outputAutoCaptura.write(f"""Auto captura: {"ATIVA" if self.autoCaptura else "INATIVA"}
Para alterar esta configuração, edite o arquivo ".env"
alterando o valor da variável "AUTO_CAPTURA" para {"0" if self.autoCaptura else "1"}.""")
