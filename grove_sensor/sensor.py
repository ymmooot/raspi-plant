import time
import sys
import grovepi
import asyncio
from grove_sensor.board import Board
from pyee import EventEmitter
import random

DELAY_DEFAULT = .1

class Sensor(EventEmitter):
  last_value = None
  current_value = None
  is_watching = False 
  delay = DELAY_DEFAULT   
  
  def __init__(self, pin, pin_mode):
    super().__init__()
    grovepi.pinMode(pin, pin_mode)

  def read():
    pass

  def watch(self, delay = None):
    self.delay = delay if delay is not None else DELAY_DEFAULT
    self.stop_watch()    
    self.is_watching = True  

    b = Board()
    b.append((self._watch, self.delay))

  async def _watch(self, delay): 
    while self.is_watching:      
      self.current_value = self.read()
      if self.current_value != self.last_value:
        self.emit('change', self.current_value)
      self.last_value = self.current_value
      await asyncio.sleep(delay)

  def stop_watch(self):
    self.is_watching = False
