import time

from grove_sensor.digital_button import DigitalButton
from grove_sensor.moisture_sensor import MoistureSensor
from mode import Mode
from modules import ComputerInfo, Display, Pump
from watcher import Watcher

WATER_PUMP_GPIO_OUT = 25
MOISTURE_SENSOR_INPUT = 0  # A0
BUTTON_INPUT = 2  # D2
DISPLAY_ADDR = 0x3C

MOISTURE_SENSOR_DELAY = 2
COMPUTER_INFO_DELAY = 3
LONG_PRESS_THRESHOLD = 0.7
MOISTURE_SENSOR_MAX_VOLT = 670


def setup_modules(feature_mode):
    button = DigitalButton(BUTTON_INPUT, LONG_PRESS_THRESHOLD)
    button.watch()
    display = Display(DISPLAY_ADDR)
    water = Pump(WATER_PUMP_GPIO_OUT)

    moisuture = MoistureSensor(MOISTURE_SENSOR_INPUT, MOISTURE_SENSOR_MAX_VOLT)
    computer = ComputerInfo()
    if feature_mode is Mode.MOISTURE:
        moisuture.watch(MOISTURE_SENSOR_DELAY)
    elif Mode.COMPUTER:
        computer.watch(COMPUTER_INFO_DELAY)

    return (moisuture, button, display, computer, water)


def setup():
    feature_mode = Mode.MOISTURE
    moisuture, button, display, computer, water = setup_modules(feature_mode)

    @button.on("up")
    def button_handler(event_type):
        nonlocal feature_mode

        # WATER mode では長押しでポンプを作動させるので次のモードに移行しない
        if feature_mode is not Mode.WATER or event_type == "singlepress":
            feature_mode = feature_mode.next()

        water.toggle(False)

        if feature_mode is Mode.MOISTURE:
            moisuture.watch(MOISTURE_SENSOR_DELAY)
            computer.stop_watch()
        elif feature_mode is Mode.COMPUTER:
            moisuture.stop_watch()
            computer.watch(COMPUTER_INFO_DELAY)
        elif feature_mode is Mode.WATER:
            moisuture.stop_watch()
            computer.stop_watch()
            display.draw("Long Press to\n Start Watering")

    @button.on("down")
    def button_up_handler():
        if feature_mode is Mode.WATER:
            started_at = time.time()
            while button.read() == 1:
                diff = time.time() - started_at
                remain = min(3, round(3.4 + LONG_PRESS_THRESHOLD - diff))
                if diff < LONG_PRESS_THRESHOLD:
                    continue
                elif remain > 0:
                    display.draw(f"{remain} sec to Start")
                else:
                    display.draw("Watering...")
                    water.toggle(True)
                time.sleep(0.1)

    @moisuture.on("change-percent")
    def moisutureSensorHandler(val):
        display.draw(f"Moisture: {val}%")

    @computer.on("change")
    def computer_info_handler(val):
        cpu, mem, temp = val
        temp = round(temp)
        display.draw(f"CPU: {cpu}%  {temp}C\nMEM: {mem}%")


print("started")
setup()
w = Watcher()
w.init()

print("\nstopped")
