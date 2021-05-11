import time
from enum import Enum

from grove_sensor.digital_sensor import DigitalSensor


class ButtonInputType(Enum):
    UP = 0
    DOWN = 1


class DigitalButton(DigitalSensor):
    mode = ButtonInputType.UP  # not pressed
    pressed_at = None

    def __init__(self, pin, long_press_delay=0.8):
        super().__init__(pin, "INPUT")
        self.pin = pin
        self.long_press_delay = long_press_delay

    def handle(self, val):
        # user presses the button for the first time
        if val == 1 and self.mode is ButtonInputType.UP:
            self.mode = ButtonInputType.DOWN
            self.pressed_at = time.time()
            self.emit("down")
            return

        # user continues to press the button
        if val == 1 and self.mode is ButtonInputType.DOWN:
            return

        # user has lifted the finger
        if val == 0 and self.pressed_at is not None:
            diff = time.time() - self.pressed_at
            event_type = "singlepress" if diff <= self.long_press_delay else "longpress"
            self.mode = ButtonInputType.UP
            self.emit("up", event_type)

    def watch(self):
        @self.on("change")
        def handle(val):
            self.handle(val)

        return super().watch()
