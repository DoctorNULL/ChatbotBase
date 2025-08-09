from time import sleep

from engine import EngineBase, EngineConfig
from objects.mouth import PiperMouth
from provider import Mic, VoskModel, HuggingFaceModel, PiperProvider
from objects import EnglishEar, HuggingFaceGenerativeModel, VariableTracker

en = EngineBase(EngineConfig("Eva", "MiDO Mostafa", "Created to simulate Jarvis from Iron Man Films"
    , [
        VoskModel("EnglishEar", "EnglishEarModel"), # Base for English Speech Recognition
        HuggingFaceModel("InstructionBrain", "Qwen/Qwen2.5-0.5B-Instruct"), # Qwen Model for Generating Responses
        PiperProvider("en_US-voice.onnx", "Mouth"), # Speaker Provider to Say text
        Mic("Mic", index=1) # For Microphone Open
    ]))

en.RegisterObjects([
    EnglishEar("Mic", "EnglishEar", "Text", True),
    HuggingFaceGenerativeModel("InstructionBrain", "Text", "Response"),
    VariableTracker(["Text", "Response"], True, "Tracker 1"),
    PiperMouth("Mouth", ListenVar="Response")
])

en.Run()
sleep(120)
en.Stop()