from provider import Provider


class EngineConfig(object):
    def __init__(self, BotName: str, Providers=None):
        if Providers is None:
            Providers = []
        self.name = BotName
        self.providers = Providers