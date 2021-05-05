import board
import grovepi
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO
import time

WATER_PUMP_GPIO_OUT = 25
MOISUTURE_SENSOR_INPUT = 0 # A0
BUTTON_INPUT = 2 # D2

MOISUTURE_SENSOR_INTERVAL_SEC = 3
MOISUTURE_SENSOR_MAX_VOLT = 704

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

def setup():
  #Setup Water Pump Relay
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(WATER_PUMP_GPIO_OUT, GPIO.OUT)
  GPIO.output(WATER_PUMP_GPIO_OUT, GPIO.HIGH)
  # Setup Moisuture Grove Sensor
  grovepi.pinMode(MOISUTURE_SENSOR_INPUT, "INPUT")
  # Setup Button
  grovepi.pinMode(BUTTON_INPUT,"INPUT")

  # Clear Display
  oled.fill(0)
  oled.show()


def draw_display(moisuture, is_watering):
  image = Image.new("1", (oled.width, oled.height))  
  draw = ImageDraw.Draw(image)
  font = ImageFont.load_default()  
  draw.text((0, 0), f"Moisuture: {moisuture}%", font=font, fill=255)
  if is_watering:
    draw.text((0, 20), "Watering...", font=font, fill=255)
  oled.image(image)
  oled.show()

def water(val):
  if val:
    GPIO.output(WATER_PUMP_GPIO_OUT, GPIO.LOW)
  else:  
    GPIO.output(WATER_PUMP_GPIO_OUT, GPIO.HIGH)

def readMoistureSensor(is_watering):
  moisuture = grovepi.analogRead(MOISUTURE_SENSOR_INPUT)
  percentage = round(moisuture / MOISUTURE_SENSOR_MAX_VOLT * 100)
  percentage = min([percentage, 100])  
  draw_display(percentage, is_watering)
  return percentage

print("start")
setup()
count = 0
is_watering = False
while True:
    try:
      # read moisuture sensor and display the value
      count += 1
      if count % MOISUTURE_SENSOR_INTERVAL_SEC == 0 or is_watering:
        readMoistureSensor(is_watering)
        count = 0

      # water while button is pressed
      button = grovepi.digitalRead(BUTTON_INPUT)
      if button:
        is_watering = True
        readMoistureSensor(is_watering)
        water(True)
      elif is_watering:
        is_watering = False
        readMoistureSensor(is_watering)
        water(False)
      
      time.sleep(1)
    except KeyboardInterrupt:
      break    
GPIO.cleanup()
print("end")
