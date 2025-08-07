from abc import ABC
from .base import EnginePublic, EngineObject


class Component(ABC):

    def __init__(self, status: bool = True):
        self.object = None
        self.enabled = status

    def SetEnabledStatus(self, NewStatus: bool):
        self.enabled = NewStatus
        self.OnEnableStatusChange(self.enabled)

    def OnCreate(self, Parent: EngineObject):
        '''
        Called when the component is Registered inside the object
        :param Parent: Reference to the parent object
        '''
        self.object = Parent

    def Start(self):
        '''
        Start is called before the first update
        '''
        pass

    def Update(self, data: EnginePublic):
        '''
        Called on every event loop
        :param data: Data of the engine
        '''
        pass


    def OnEnableStatusChange(self, Status: bool):
        '''
        Called when the component enable status change
        :return:
        '''
        pass