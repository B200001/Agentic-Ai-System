from llm.llm_loader import TinyLlamaChatLLM
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from tools.tool_router import ToolRouter

if __name__ == "__main__":
    # LLM
    llm = TinyLlamaChatLLM()

    # Planner
    planner = PlannerAgent(llm)

    # Tools
    tool_router = ToolRouter(llm)

    # Executor
    executor = ExecutorAgent(tool_router)

    goal = "Analyze recent AI trends and summarize key risks"
    plan = planner.create_plan(goal)

    result = executor.execute(plan)

    print("\n====================")
    print("✅ FINAL OUTPUT")
    print("====================\n")

    print(result["final_output"])

    print("\n====================")
    print("🧾 EXECUTION LOGS")
    print("====================\n")
    for log in result["logs"]:
        print(log)
