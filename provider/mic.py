from .base import Provider
import pyaudio

class Mic(Provider):
    def __init__(self, name: str, rate: int = 16000, index= 0):
        super().__init__(name)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(rate, 1, pyaudio.paInt16, True,
                                    frames_per_buffer=8192, input_device_index=index)
        self.stream.start_stream()



    def Use(self, ReadRate: int = 4096, *args, **kwargs):
        try:
            return self.stream.read(ReadRate, exception_on_overflow=False)
        except Exception as e:
            return bytes()


    def Release(self):
        try:
            self.stream.stop_stream()
        except:
            pass

        self.stream.close()
        self.mic.terminate()