from provider import Provider


class EngineConfig(object):
    def __init__(self, BotName: str, CreatorName: str, CreationPurpose: str, Providers=None):

        if Providers is None:
            Providers = []

        self.name = BotName # The base name of the bot

        self.setup = [
            {"role": "system", "content": f"Your name is {BotName}, and created by {CreatorName}. You are a custom ai model."
                                          f" {CreationPurpose}"},
            {"role": "user", "content": f"Can you tell me that your name is {BotName}"},
        ] # Basic Setup for LLMs

        self.providers = Providers # Providers to take