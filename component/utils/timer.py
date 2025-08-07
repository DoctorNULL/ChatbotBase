import time

from engine import Component, EnginePublic


class Timer(Component):
    def __init__(self, Handle, status: bool = True, Loop: bool = False, Delay: float = 0.1):
        super().__init__(status)
        self.handle = Handle
        self.loop = Loop
        self.delay = Delay
        self.StartTime = 0
        self.done = False

    def Start(self):
        self.StartTime = time.time()

    def Update(self, data: EnginePublic):

        if self.StartTime >= self.StartTime + self.delay and not self.done:
            self.handle()
            self.StartTime = time.time()
            if not self.loop:
                self.done = True