from enum import Enum
from display import Display
from display_mode import DisplayMode

class DisplayMode(Enum):
  MOISTURE = 1
  COMPUTER = 2

class DisplayManager:
  mode = DisplayMode.MOISTURE

  def __init__(self, addr, read_moisture_func):
    self.display = Display(addr)
    self.read_moisture_func = read_moisture_func
  
  # def update(val)

  def next(self):
    self.mode = DisplayMode.MOISTURE if self.mode == DisplayMode.COMPUTER else DisplayMode.COMPUTER

    if self.mode == DisplayMode.MOISTURE:
      val = self.read_moisture_func()
      self.display.draw(f'Moisture: {val}')
    else:
      self.display.draw(f'computer')

