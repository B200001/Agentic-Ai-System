from llm.llm_wrapper import LLMWrapper
from llm.llm_loader import load_llm



if __name__== "__main__":
    pipeline = load_llm()
    llm = LLMWrapper(pipeline)

    prompt = """
    You are a planning AI.
    Break this task into steps:
    "Analyze AI trends in 2024"
    """

    response = llm.generate(prompt)

    print(response)