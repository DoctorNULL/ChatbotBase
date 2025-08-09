from engine import EngineObject, EnginePublic
from abc import ABC, abstractmethod


class Mouth (EngineObject, ABC):
    def __str__(self):
        return "Mouth " + self.tag

    def __init__(self, ListenVar: str, tag = "", activation = True):
        super().__init__(tag, activation)

        self.input = ListenVar

    def Update(self, data: EnginePublic):
        super().Update(data)

        value = data.FetchVariable(self.input)

        if value:
            if isinstance(value, str):
                self.Say(value)
                data.UpdateVariable(self.input, "")

    @abstractmethod
    def Say(self, text: str):
        pass