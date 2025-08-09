from .base import Mouth
from sounddevice import play


class PiperMouth(Mouth):
    def __str__(self):
        return "Piper Mouth " + self.tag

    def __init__(self, voice_provider: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.voice = voice_provider
        self.model = None

    def OnCreate(self, Engine):
        super().OnCreate(Engine)

        self.model = self.GetProvider(self.voice)

    def Say(self, text: str):
        sound = self.model.Use(text)

        play(sound, blocking=True, samplerate=self.model.sample_rate)