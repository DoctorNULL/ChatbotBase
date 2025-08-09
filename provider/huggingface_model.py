from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

from provider import Provider


class HuggingFaceModel(Provider):
    def __init__(self, Name: str, Model: str, LLM= True):
        super().__init__(Name)

        self.model_name = Model

        if LLM:
            self.model = AutoModelForCausalLM.from_pretrained(Model)
        else:
            self.model = AutoModel.from_pretrained(Model)

        self.device = self.model.device

        self.tokenizer = AutoTokenizer.from_pretrained(Model)

    def Use(self, prompt, *args, **kwargs):

        model_inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=512
        )

        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]