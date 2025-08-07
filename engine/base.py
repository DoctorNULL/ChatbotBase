from threading import Thread


class EnginePublic(object):
    def __init__(self, name: str):
        self.name = name
        self._storage = dict()


class EngineObject(object):
    def __init__(self, tag: str = "", activation: bool = True):
        self._components = []
        self.tag = tag
        self._activation = activation
        self._engine = None

    def RegisterComponent(self, NewComponent):
        from engine import Component
        assert isinstance(NewComponent, Component), f"Object of type {type(NewComponent)} is Not a Component"

        NewComponent.OnCreate(self)
        self._components.append(NewComponent)

    def FindComponentOfType(self, Type: type):
        for component in self._components:
            if isinstance(component, Type):
                return component

        return None

    def SetActivation(self, NewActivation: bool):
        self._activation = NewActivation
        self.OnActivationChange(self._activation)


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
    def __init__(self, config):
        self.public = EnginePublic(config.name)
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

    def FindObjectOfType(self, Type: type):
        for obj in self.objects:
            if isinstance(obj, Type):
                return obj

        return None

    def FindObjectWithTag(self, Tag: str):
        for obj in self.objects:
            if obj.tag == Tag:
                return obj

        return None

    def Join(self):
        if self._thread:
            self._thread.join()

    def Stop(self):

        assert self._thread, "Engine is NOT working"

        self.isWorking = False

        for obj in self.objects:
            obj.Die()

        print("Engine Stopped...")

