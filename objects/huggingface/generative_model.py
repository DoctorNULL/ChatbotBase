from engine import EngineObject, EnginePublic


class HuggingFaceGenerativeModel(EngineObject):
    def __str__(self):
        return f"Huggingface Generative Model {self.ProviderName}"

    def __init__(self, Provider: str, ListenVariable: str, ResponseVariable: str, MaxMemoryMessages = 10, tag= "", activation=True):
        super().__init__(tag, activation)

        self.model = None
        self.ListenVar = ListenVariable
        self.ResponseVar = ResponseVariable
        self.ProviderName = Provider

        self.MessageBase = None
        self.Memory = []
        self.MemoryLength = MaxMemoryMessages

    def OnCreate(self, Engine):
        super().OnCreate(Engine)
        self.model = self.GetProvider(self.ProviderName)
        self.MessageBase = self._engine.MessageBase

    def Update(self, data: EnginePublic):
        super().Update(data)
        
        text = data.FetchVariable(self.ListenVar)

        if text:
            self.Memory.append({"role": "user", "content": text})
            data.UpdateVariable(self.ListenVar, "")

            if len(self.Memory) >= self.MemoryLength:
                self.Memory.pop(0)

            prompt = [x for x in self.MessageBase]
            prompt.extend(self.Memory)

            prompt = self.model.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)

            out = self.model.Use(prompt)

            out = out.split("assistant\n")[1]

            out = out.replace("*", "")

            data.UpdateVariable(self.ResponseVar, out)
