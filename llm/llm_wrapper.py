class LLMWrapper:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def generate(self, prompt: str) -> str:
        output = self.pipeline(prompt)

        # output format: [{'generated_text': '...'}]
        if isinstance(output, list) and len(output) > 0 and "generated_text" in output[0]:
            return output[0]["generated_text"]

        return str(output)
