import cv2, os, json, sys, pygetwindow as gw
from screeninfo import get_monitors

def get():
  print('recarregando configurações de pokémons capturáveis...')
  widthOtp, heigthOtp = gw.getWindowsWithTitle('otPokemon')[0].size
  frx = widthOtp / get_monitors()[0].width
  fry = heigthOtp / get_monitors()[0].height
  fr = max(frx, fry)

  try:
    with open('capturaveis.json') as file:
      paramsCapturaveis = json.load(file)
  except:
    print('Não foi possível carregar os parâmetros dos pokémons capturáveis!')
    sys.exit()

  capturaveis = {}
  for capturavelName in os.listdir('img/pokes'):
    capturavelId = capturavelName.split('.')[0];
    if not capturavelId in paramsCapturaveis:
      print(f'Não foi possível carregar o parâmetro do pokémon "{capturavelId}"!')
      sys.exit()

    capturaveis[capturavelId] = {
      'needle': cv2.resize(cv2.cvtColor(cv2.imread(f'img/pokes/{capturavelName}'), cv2.COLOR_BGR2GRAY), None, fx = fr, fy = fr, interpolation=cv2.INTER_LINEAR),
      'conf': paramsCapturaveis[capturavelId]
    }
  
  return capturaveis
