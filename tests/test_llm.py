from llm.llm_loader import load_llm


if __name__== "__main__":
    llm = load_llm()

    prompt = """
    You are a planning AI.
    Break this task into steps:
    "Analyze AI trends in 2024"
    """

    response = llm(prompt)

    print(response[0]['generated_text'])