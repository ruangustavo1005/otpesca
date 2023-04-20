import sys
from src.main import Main

sys.path.append('src')
sys.path.append('src/utils')

main = Main()
main.mainLoop()