import time
from grove_sensor.analog_sensor import AnalogSensor
from grove_sensor.digital_button import DigitalButton
from grove_sensor.board import Board
from display import Display
from mode import Mode
import pump
import mode

WATER_PUMP_GPIO_OUT = 25
MOISTURE_SENSOR_INPUT = 0 # A0
BUTTON_INPUT = 2 # D2
DISPLAY_ADDR = 0x3c

MOISTURE_SENSOR_MAX_VOLT = 670
MOISTURE_SENSOR_DELAY = 1

def setup_modules():
  moisuture = AnalogSensor(MOISTURE_SENSOR_INPUT, "INPUT")
  moisuture.watch(MOISTURE_SENSOR_DELAY)
  button = DigitalButton(BUTTON_INPUT)
  button.watch()
  display = Display(DISPLAY_ADDR)
  return (moisuture, button, display)

def setup():
  moisuture, button, display = setup_modules()
  feature_mode = Mode.MOISTURE
  
  @moisuture.on('change')
  def moisutureSensorHandler(val):
    print(f"moi {val}")
    display.draw(f'Moisture: {val}%')
    
  @button.on('up')
  def button_handler(event_type):
    nonlocal feature_mode 
    feature_mode = feature_mode.next()
    if feature_mode is Mode.MOISTURE:
      moisuture.watch(MOISTURE_SENSOR_DELAY)
    elif feature_mode is Mode.COMPUTER:
      moisuture.stop_watch()
      print("stop")
      display.draw(f'computer')


print("started")
setup()
b = Board()
try:
  b.init()
except KeyboardInterrupt:
  b.stop()
print("\nstopped")

