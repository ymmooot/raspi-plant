import asyncio

from pyee import EventEmitter

from .watcher import Watcher

DELAY_DEFAULT = 0.1


class WatcherItem(EventEmitter):
    last_value = None
    current_value = None
    is_watching = False

    def __init__(self):
        super().__init__()

    def read():
        pass

    def watch(self, delay=None):
        delay = delay if delay is not None else DELAY_DEFAULT
        self.stop_watch()
        self.is_watching = True

        w = Watcher()
        w.append((self._watch, delay))

    async def _watch(self, delay):
        while self.is_watching:
            self.current_value = self.read()
            if self.current_value != self.last_value:
                self.emit("change", self.current_value)
            self.last_value = self.current_value
            await asyncio.sleep(delay)

    def stop_watch(self):
        self.is_watching = False
        self.last_value = None
