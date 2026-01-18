from llm.llm_loader import TinyLlamaChatLLM
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.critic import CriticAgent
from tools.tool_router import ToolRouter
from memory.qdrant_store import QdrantMemory

if __name__ == "__main__":
    llm = TinyLlamaChatLLM()
    memory = QdrantMemory()

    planner = PlannerAgent(llm)
    critic = CriticAgent()

    tool_router = ToolRouter(llm=llm, memory=memory)
    executor = ExecutorAgent(tool_router=tool_router, critic_agent=critic, max_retries=2)

    goal = "Analyze recent AI trends and summarize key risks"
    plan = planner.create_plan(goal)

    # Add retrieval step manually (planner may not do it)
    plan["subtasks"].insert(2, {"id": 99, "task": goal, "tool": "retrieval"})

    result = executor.execute(plan)

    print("\n✅ FINAL OUTPUT:\n")
    print(result["final_output"])
