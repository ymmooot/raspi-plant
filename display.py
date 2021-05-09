import board
from grove_sensor.sensor import Sensor
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class Display:
  def __init__(self, addr):
    self.i2c = board.I2C()
    self.oled = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c, addr=addr)
    self.font = ImageFont.load_default()      
    self.clear()

  def clear(self):
    self.oled.fill(0)
    self.oled.show()

  def draw(self, val, position = (0, 0)):
    image = Image.new("1", (self.oled.width, self.oled.height))  
    draw = ImageDraw.Draw(image)
    draw.text(position, val, font=self.font, fill=255)
    self.oled.image(image)
    self.oled.show()