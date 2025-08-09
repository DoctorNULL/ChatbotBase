from time import sleep

from engine import EngineBase, EngineConfig
from provider import Mic, VoskModel
from objects import EnglishEar

en = EngineBase(EngineConfig("Eva", [
    VoskModel("EnglishEar", "EnglishEarModel"), # Base for English Speech Recognition
    Mic("Mic", index=0) # For Microphone Open
]))

en.RegisterObjects([
    EnglishEar("Mic", "EnglishEar")
])

en.Run()
sleep(120)
en.Stop()