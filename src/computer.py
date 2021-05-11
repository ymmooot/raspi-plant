import psutil

from watcher import WatcherItem


class ComputerInfo(WatcherItem):
    def __init__(self):
        super().__init__()

    def memory(self):
        mem = psutil.virtual_memory()
        return mem.percent

    def cpu(self):
        return psutil.cpu_percent()

    def cpu_temp(self):
        return psutil.sensors_temperatures()["cpu_thermal"][0].current

    def read(self):
        return (self.cpu(), self.memory(), self.cpu_temp())
