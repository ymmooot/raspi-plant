from grove_sensor import grovepi
from watcher import WatcherItem

DELAY_DEFAULT = 0.1


class Sensor(WatcherItem):
    def __init__(self, pin, pin_mode):
        super().__init__()
        grovepi.pinMode(pin, pin_mode)
