class LLMWrapper:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def generate(self, prompt:str)-> str:
        output = self.pipeline(prompt)
        return output[0]['generated_text']