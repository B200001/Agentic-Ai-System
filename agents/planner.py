import json
import re
from agents.planner_prompt import PLANNER_SYSTEM_PROMPT


def normalize_tool_name(tool: str) -> str:
    tool = tool.lower()

    if "google" in tool or "bing" in tool or "news" in tool or "duckduckgo" in tool or "search" in tool:
        return "search"
    if "rag" in tool or "qdrant" in tool or "retriev" in tool:
        return "retrieval"
    if "llm" in tool or "summar" in tool or "generate" in tool:
        return "llm"
    if "critic" in tool or "validate" in tool or "review" in tool:
        return "critic"

    return tool


class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def _extract_json_anywhere(self, text: str) -> dict:
        # remove markdown fences
        text = text.replace("```json", "").replace("```", "").strip()

        # find first json object {...}
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("No JSON object found in output")

        json_text = match.group(0).strip()

        # common tinyllama mistakes
        json_text = json_text.replace("\'", "\"")  # fix single quotes

        return json.loads(json_text)
    def create_plan(self, user_goal: str) -> dict:
        user_prompt = f"""
    Goal: {user_goal}
    
    Return ONLY valid JSON with:
    goal + subtasks[{{
      id, task, tool (search/retrieval/llm/critic)
    }}]
    """
    
        for attempt in range(3):  # 3 tries
            raw_output = self.llm.generate(
                system_prompt=PLANNER_SYSTEM_PROMPT,
                user_prompt=user_prompt
            )
    
            try:
                plan = self._extract_json_anywhere(raw_output)
                return plan
            except Exception:
                user_prompt = f"""
    Goal: {user_goal}
    
    Your previous JSON was invalid.
    Return ONLY valid JSON now. No extra text.
    """
        raise ValueError("Planner failed to generate valid JSON after retries")

    



#     def create_plan(self, user_goal: str) -> dict:
#         user_prompt = f"""
# Goal: {user_goal}

# Rules:
# - Use ONLY these tools: search, retrieval, llm, critic
# - Keep subtasks <= 6
# - Output ONLY JSON
# """

#         raw_output = self.llm.generate(
#             system_prompt=PLANNER_SYSTEM_PROMPT,
#             user_prompt=user_prompt
#         )

#         print("\n===== RAW OUTPUT =====\n")
#         print(raw_output)
#         print("\n======================\n")

#         try:
#             plan = self._extract_json_anywhere(raw_output)
#         except Exception:
#             # retry once
#             raw_output = self.llm.generate(
#                 system_prompt=PLANNER_SYSTEM_PROMPT,
#                 user_prompt=f"Goal: {user_goal}\nReturn ONLY JSON. Do not write anything else."
#             )

#             print("\n===== RAW OUTPUT (RETRY) =====\n")
#             print(raw_output)
#             print("\n==============================\n")

#             plan = self._extract_json_anywhere(raw_output)

#         # Validate plan structure
#         if "goal" not in plan:
#             raise ValueError("Planner JSON missing 'goal'")
#         if "subtasks" not in plan or not isinstance(plan["subtasks"], list):
#             raise ValueError("Planner JSON missing/invalid 'subtasks'")
        
        

#         allowed_tools = {"search", "retrieval", "llm", "critic"}
#         for st in plan["subtasks"]:
#             st["tool"] = normalize_tool_name(st.get("tool", ""))
#         return plan
