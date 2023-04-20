import cv2
import os
import json
import pygetwindow as gw


class Capturaveis:

  def __init__(self, window):
    self.heightTela = int(os.getenv('ALTURA_TELA'))
    self.widthTela = int(os.getenv('LARGURA_TELA'))
    self.reset(window)

  def get(self):
    return self.capturaveis

  def reset(self, otpWindow):
    width, heigth = otpWindow.size
    fr = max(width / self.widthTela, heigth / self.heightTela)

    capturaveisFileName = 'capturaveis.json'
    try:
      with open(capturaveisFileName) as file:
        paramsCapturaveis = json.load(file)
    except:
      raise Exception(f'Não foi possível encontrar o arquivo ({capturaveisFileName}) de parâmetros dos pokémons capturáveis!')

    self.capturaveis = {}
    for capturavelName in os.listdir('img/pokes'):
      capturavelId = capturavelName.split('.')[0]
      if not capturavelId in paramsCapturaveis:
        raise Exception(f'Não foi possível carregar o parâmetro do pokémon "{capturavelId}"!')

      self.capturaveis[capturavelId] = {
        'needle': cv2.resize(cv2.cvtColor(cv2.imread(f'img/pokes/{capturavelName}'), cv2.COLOR_BGR2GRAY), None, fx=fr, fy=fr, interpolation=cv2.INTER_LINEAR),
        'conf': paramsCapturaveis[capturavelId]
      }

    self.capturaveis
    return self
