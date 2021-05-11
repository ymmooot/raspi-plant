from grove_sensor import grovepi
from grove_sensor.sensor import Sensor


class DigitalSensor(Sensor):
    def __init__(self, pin, pin_mode):
        super().__init__(pin, pin_mode)
        self.pin = pin

    def read(self):
        return grovepi.digitalRead(self.pin)

    def write(self, val):
        return grovepi.digitalWrite(self.pin, val)
