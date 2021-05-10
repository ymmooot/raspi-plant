from grove_sensor.sensor import Sensor
from grove_sensor import grovepi

class AnalogSensor(Sensor):
  def __init__(self, pin, pin_mode):
    super().__init__(pin, pin_mode)
    self.pin = pin
  
  def read(self): 
    return grovepi.analogRead(self.pin)

  def write(self, val):
    return grovepi.analogWrite(self.pin, val)
