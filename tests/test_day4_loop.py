from llm.llm_loader import TinyLlamaChatLLM
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.critic import CriticAgent
from tools.tool_router import ToolRouter

if __name__ == "__main__":
    llm = TinyLlamaChatLLM()

    planner = PlannerAgent(llm)
    tool_router = ToolRouter(llm)
    critic = CriticAgent()


    executor = ExecutorAgent(tool_router=tool_router, critic_agent=critic, max_retries=2)

    goal = "Analyze recent AI trends and summarize key risks"
    plan = planner.create_plan(goal)

    result = executor.execute(plan)

    print("\n====================")
    print("✅ FINAL OUTPUT")
    print("====================\n")
    print(result["final_output"])

    print("\n====================")
    print("🧾 LOGS")
    print("====================\n")
    for log in result["logs"]:
        print(log)
