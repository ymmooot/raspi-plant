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

  def read(self):
    return (self.cpu(), self.memory())