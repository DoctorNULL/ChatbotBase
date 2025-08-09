from abc import abstractmethod
from threading import Thread

from provider import Provider
from .config import EngineConfig


class EnginePublic(object):
    def __init__(self, name: str):
        self.name = name
        self._storage = dict()

    def AddVariable(self, Name: str, Value: object):
        assert Name not in self._storage.keys(), f"{Name} already exists as a variable"

        self._storage[Name] = Value

    def UpdateVariable(self, Name: str, Value: object):
        self._storage[Name] = Value

    def FetchVariable(self, Name: str):
        if Name not in self._storage.keys():
            return None

        return self._storage[Name]

    def DeleteVariable(self, Name: str):
        self._storage.pop(Name)


class EngineObject(object):
    def __init__(self, tag: str = "", activation: bool = True):
        self._components = []
        self.tag = tag
        self._activation = activation
        self._engine = None

    @abstractmethod
    def __str__(self):
        return "Plain Object"

    def RegisterComponent(self, NewComponent):
        from engine import Component
        assert isinstance(NewComponent, Component), f"Object of type {type(NewComponent)} is Not a Component"

        NewComponent.OnCreate(self)
        self._components.append(NewComponent)
        return NewComponent

    def FindComponentOfType(self, Type: type):
        for component in self._components:
            if isinstance(component, Type):
                return component

        return None

    def GetProvider(self, name: str) -> Provider | None:
        assert self._engine, "Object not initialized"

        for provider in self._engine.providers:
            if provider.name == name:
                return provider

        return None


    def SetActivation(self, NewActivation: bool):
        self._activation = NewActivation
        self.OnActivationChange(self._activation)


    def FindObjectOfType(self, Type: type):
        for obj in self._engine.objects:
            if isinstance(obj, Type):
                return obj

        return None

    def FindObjectWithTag(self, Tag: str):
        for obj in self._engine.objects:
            if obj.tag == Tag:
                return obj

        return None


    def OnCreate(self, Engine):
        """
        Called when the Object is Registered to the engine
        """
        self._engine = Engine

    def Start(self):
        """
        Starts all components of the object
        Called before the first Update
        """

        for component in self._components:
            component.Start()

    def Update(self, data: EnginePublic):
        """
        Called in each iteration of the event loop
        :param data: Engine Public Data
        """

        for component in self._components:
            if component.enabled:
                component.Update(data)


    def OnActivationChange(self, Activation: bool):
        """
        Called when the object activation status change
        :param Activation: Current activation status
        """
        pass

    def Die(self):
        """
        Called when the Engine starts to stop
        """

        pass


class EngineBase(object):
    def __init__(self, config: EngineConfig):
        self.public = EnginePublic(config.name)
        self.MessageBase = config.setup
        self.providers = config.providers
        self.objects = []
        self._thread = None
        self.isWorking = False

    def RegisterObjects(self, Objects: list[EngineObject]):
        assert isinstance(Objects, list), f"Expected from {type(object)} to be a list"

        for obj in Objects:
            assert isinstance(obj, EngineObject), f"Expected {type(obj)} to be Engine Object"

            obj.OnCreate(self)
            self.objects.append(obj)

    def _Loop(self):

        while self.isWorking:
            for obj in self.objects:
                obj.Update(self.public)

    def Run(self):

        for obj in self.objects:
            obj.Start()

        self.isWorking = True
        self._thread = Thread(target=self._Loop)
        self._thread.start()

        print("Engine Started...")

    def Join(self):
        if self._thread:
            self._thread.join()

    def Stop(self):

        assert self._thread, "Engine is NOT working"

        self.isWorking = False

        for obj in self.objects:
            obj.Die()

        for provider in self.providers:
            provider.Release()

        print("Engine Stopped...")

