import vosk
from .base import Provider
import json

class VoskModel(Provider):

    def Use(self, WaveForm, *args, **kwargs):
        assert self.model, "Model is Not Provided"

        if self.model.AcceptWaveform(WaveForm):
            return json.loads(self.model.Result())["text"]

        return ""

    def __init__(self, name: str, path: str, rate: int = 16000):
        super().__init__(name)
        self.model = vosk.KaldiRecognizer(vosk.Model(path), rate)


