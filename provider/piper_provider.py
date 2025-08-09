import numpy as np

from provider import Provider
from piper import PiperVoice, SynthesisConfig, AudioChunk
from torch.cuda import is_available


class PiperProvider(Provider):
    def __init__(self, voice: str, name: str, volume = 1):
        super().__init__(name)

        self.voice = PiperVoice.load(voice, use_cuda= is_available())
        self.config = SynthesisConfig()
        self.config.volume = volume
        self.sample_rate = self.voice.config.sample_rate

    def Use(self, text: str, *args, **kwargs):
        result = self.voice.synthesize(text, self.config)
        return np.concatenate([x.audio_float_array for x in result])