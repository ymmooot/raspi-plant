from grove_sensor.analog_sensor import AnalogSensor


class MoistureSensor(AnalogSensor):
    last_percent_value = None

    def __init__(self, pin, max_volt):
        super().__init__(pin, "INPUT")
        self.pin = pin
        self.max_volt = max_volt

    def calc_moisture_rate(self, val):
        m = min(val, self.max_volt)
        percentage = round(m / self.max_volt * 100)
        return min(percentage, 100)

    def readAsPercentage(self):
        val = super().read()
        return self.calc_moisture_rate(val)

    def handle(self, val):
        rate = self.calc_moisture_rate(val)
        if self.last_percent_value != rate:
            self.last_percent_value = rate
            self.emit("change-percent", rate)

    def watch(self, delay):
        @self.on("change")
        def handle(val):
            self.handle(val)

        return super().watch(delay)

    def stop_watch(self):
        self.last_percent_value = None
        super().stop_watch()
