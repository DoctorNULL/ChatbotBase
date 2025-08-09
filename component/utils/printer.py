from engine import Component


class Printer(Component):
    def __init__(self, status: bool = True):
        super().__init__(status)
        self.prefix = "Uninitialized Printer : "

    def Start(self):
        self.prefix = f"{self.object._engine.public.name} - {self.object} : "

    def Print(self, Message):
        if Message:
            print(self.prefix, Message)