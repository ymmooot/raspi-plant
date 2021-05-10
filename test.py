import time
from grove_sensor.analog_sensor import AnalogSensor
from grove_sensor.digital_button import DigitalButton
from display import Display
from mode import Mode
from watcher import Watcher
import pump
from computer import ComputerInfo

WATER_PUMP_GPIO_OUT = 25
MOISTURE_SENSOR_INPUT = 0 # A0
BUTTON_INPUT = 2 # D2
DISPLAY_ADDR = 0x3c

MOISTURE_SENSOR_MAX_VOLT = 670
MOISTURE_SENSOR_DELAY = 2
COMPUTER_INFO_DELAY = 3

def setup_modules(feature_mode):
  button = DigitalButton(BUTTON_INPUT)
  button.watch()
  display = Display(DISPLAY_ADDR)

  moisuture = AnalogSensor(MOISTURE_SENSOR_INPUT, "INPUT")
  computer = ComputerInfo()
  if feature_mode is Mode.MOISTURE:
    moisuture.watch(MOISTURE_SENSOR_DELAY)
  else:
    computer.watch(COMPUTER_INFO_DELAY)

  return (moisuture, button, display, computer)

def calc_moisture_rate(val):
  m = min(val, MOISTURE_SENSOR_MAX_VOLT)
  percentage = round(m / MOISTURE_SENSOR_MAX_VOLT * 100)
  return min(percentage, 100)   

def setup():
  feature_mode = Mode.COMPUTER
  moisuture, button, display, computer = setup_modules(feature_mode)
  
  @moisuture.on('change')
  def moisutureSensorHandler(val):
    m = calc_moisture_rate(val)    
    display.draw(f'Moisture: {m}%')
    
  @button.on('down')
  def button_handler(event_type):
    nonlocal feature_mode
    feature_mode = feature_mode.next()
    if feature_mode is Mode.MOISTURE:
      moisuture.watch(MOISTURE_SENSOR_DELAY)
      computer.stop_watch()
    elif feature_mode is Mode.COMPUTER:
      moisuture.stop_watch()
      computer.watch(COMPUTER_INFO_DELAY)

  @computer.on('change')
  def computer_info_handler(val):
    cpu, mem = val
    display.draw(f'Computer Resources\nCPU: {cpu}%|MEM: {mem}%')

    


print("started")
setup()
w = Watcher()
w.init()

print("\nstopped")

