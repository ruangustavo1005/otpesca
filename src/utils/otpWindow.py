import pygetwindow as gw
import cv2
import numpy
from PIL import ImageGrab

OTP_WINDOW_NAME = 'otPokemon'


class OtpWindow:

  def __init__(self):
    self.reset()

  def get(self):
    return self.window

  def reset(self):
    windowsFinded = gw.getWindowsWithTitle(OTP_WINDOW_NAME)
    if len(windowsFinded) > 0:
      self.window = windowsFinded[0]
    return self

  def activate(self):
    if not self.window.isMinimized:
      self.window.minimize()
    self.window.restore()
    self.window.activate()
    return self

  def getScreenshot(self):
    left, top, width, height = self.window.left + 8, self.window.top + 8, self.window.width - 16, self.window.height - 16
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height), all_screens=True)
    return cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2GRAY)
  
  def getWindowLoc(self):
    return self.window.left + 8, self.window.top + 8
