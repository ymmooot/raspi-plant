import asyncio

MAX_SENSOR_LIMIT = 20

class Board(object):
  queue = asyncio.Queue()
  tasks = []

  def __new__(cls, *args, **kargs):
    if not hasattr(cls, "_instance"):
        cls._instance = super(Board, cls).__new__(cls)
    return cls._instance
  
  async def worker(self):
    while True:
      (watcher, delay) = await self.queue.get()
      await watcher(delay)
      self.queue.task_done()
  
  def init(self): 
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(MAX_SENSOR_LIMIT):
      task = loop.create_task(self.worker())
      self.tasks.append(task)
    
    joined = self.queue.join()
    loop.run_until_complete(joined)
    gathered = asyncio.gather(*self.tasks, return_exceptions=True)
    loop.run_until_complete(gathered)
    print("done")
    
  def append(self, val):
    self.queue.put_nowait(val)
  
  def stop(self):
    for task in self.tasks:
      task.cancel()    
    

