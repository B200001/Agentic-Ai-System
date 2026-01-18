from llm.llm_loader import TinyLlamaChatLLM
from agents.planner import PlannerAgent

if __name__ == "__main__":
    llm = TinyLlamaChatLLM()
    planner = PlannerAgent(llm)

    goal = "Analyze recent AI trends and summarize key risks"
    plan = planner.create_plan(goal)

    print("\n✅ FINAL PLAN:\n")
    print(plan)
