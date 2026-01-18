from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

class TinyLlamaChatLLM:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=650,
                min_new_tokens = 350,
                do_sample=False,
                early_stopping = False
            )

        # Decode full
        decoded = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Best effort: return assistant portion (last response)
        # TinyLlama often includes "assistant" role marker implicitly
        if "assistant" in decoded.lower():
            return decoded.split("assistant")[-1].strip()

        return decoded.strip()
