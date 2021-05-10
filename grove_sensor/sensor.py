from watcher import WatcherItem
from grove_sensor import grovepi

DELAY_DEFAULT = .1

class Sensor(WatcherItem):
  def __init__(self, pin, pin_mode):
    super().__init__()
    grovepi.pinMode(pin, pin_mode)
