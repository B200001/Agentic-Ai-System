def llm_summarize(llm, task: str, context: dict, critic_feedback: str = None):
    # limit context size (very important to avoid cut-off)
    search_data = context.get("search_results", [])[:5]
    retrieved_docs = context.get("retrieved_docs", [])[:5]

    # Make compact context text (do NOT dump full dicts)
    def compact_web(items):
        lines = []
        for i, it in enumerate(items, 1):
            title = it.get("title", "") if isinstance(it, dict) else ""
            body = it.get("body", "") if isinstance(it, dict) else ""
            href = it.get("href", "") if isinstance(it, dict) else ""
            lines.append(f"{i}. {title}\n{body}\nSource: {href}\n")
        return "\n".join(lines).strip()

    def compact_memory(items):
        lines = []
        for i, it in enumerate(items, 1):
            text = it.get("text", "") if isinstance(it, dict) else ""
            score = it.get("score", 0) if isinstance(it, dict) else 0
            # keep only first 300 chars
            text = text[:300].replace("\n", " ")
            lines.append(f"{i}. ({score:.2f}) {text}")
        return "\n".join(lines).strip()

    web_context = compact_web(search_data)
    memory_context = compact_memory(retrieved_docs)

    system_prompt = """
You are a professional research assistant.

IMPORTANT RULES:
- Do NOT repeat the prompt.
- Do NOT print raw context dumps.
- Output must contain ONLY the final answer.
- DO NOT list sources or URLs in the Summary.
- DO NOT copy/paste context lines.
- Write your OWN summarized answer.
- Output MUST be complete.
- Output MUST be ONLY these two sections:

Return in this exact format:

Summary:
<5-8 lines>

Key Risks:
- <bullet 1>
- <bullet 2>
- <bullet 3>
- <bullet 4>
- <bullet 5>
"""

    user_prompt = f"""
Goal: {task}

Memory Context:
{memory_context}

Web Context:
{web_context}
"""

    if critic_feedback:
        user_prompt += f"\nCritic Feedback:\n{critic_feedback}\n"

    output = llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)

    # ✅ clean common junk prefix
    bad_prefixes = ["|>", "<|assistant|>"]
    for bp in bad_prefixes:
        output = output.replace(bp, "").strip()

    return {"type": "llm", "summary": output.strip()}
