from abc import ABC, abstractmethod

class Provider(object):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def Use(self, *args, **kwargs):
        """
        Use of the Provider
        :param args: Positional Args
        :param kwargs: Key Word Args
        :return:
        """
        pass


    def Release(self):
        """
        Closes the provider
        :return:
        """
        pass