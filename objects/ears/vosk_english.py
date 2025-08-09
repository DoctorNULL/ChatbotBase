from engine import EngineObject, EnginePublic
from component import Printer


class EnglishEar(EngineObject):
    def __str__(self):
        return "English Ear"

    def __init__(self, MicProvider: str, VoskProvider: str, ResponseVariable: str, Log = False, Activation = True):
        super().__init__(activation=Activation)
        self.printer = self.RegisterComponent(Printer())
        self.MicProvider = MicProvider
        self.VoskProvider = VoskProvider

        self.mic = None
        self.model = None

        self.log = Log

        self.out = ResponseVariable

    def OnCreate(self, Engine):
        super().OnCreate(Engine)

        self.mic = self.GetProvider(self.MicProvider)
        self.model = self.GetProvider(self.VoskProvider)

    def Update(self, data: EnginePublic):
        text = self.model.Use(self.mic.Use())

        if len(text.split()) < 3 and text != data.name.lower():
            return

        data.UpdateVariable(self.out, text)

        if self.log:
            self.printer.Print(text)