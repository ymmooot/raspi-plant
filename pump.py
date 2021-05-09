import RPi.GPIO as GPIO
import time

class Pump:
  def __init__(self, pin):
    self.pin = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

  def toggle(self, val):
    if val:
      GPIO.output(self.pin, GPIO.LOW)
    else:  
      GPIO.output(self.pin, GPIO.HIGH)
  
  def on(self, sec):
    self.toggle(True)
    time.sleep(sec)
    self.toggle(False)
