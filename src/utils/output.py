import curses
curses.initscr()


class Output:

  def __init__(self, lineNumber: int, rowNumber: int, maxLines: int = 0, maxRows: int = 0):
    self.win = curses.newwin(maxLines, maxRows, lineNumber, rowNumber)

  def write(self, text: str, line: int = 0, row: int = 0, autoRefresh: bool = True, bold: bool = False, autoErase: bool = True):
    if autoErase:
      self.win.erase()
    self.win.addstr(line, row, text, curses.A_BOLD if bold else 0)
    if autoRefresh:
      self.win.refresh()
