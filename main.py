from time import sleep

from engine import EngineBase, EngineConfig

en = EngineBase(EngineConfig("Eva"))

en.Run()
sleep(5)
en.Stop()