from enum import IntEnum, auto


class Mode(IntEnum):
    MOISTURE = 0
    COMPUTER = auto()
    WATER = auto()

    def next(self):
        return Mode((self + 1) % len(Mode))
