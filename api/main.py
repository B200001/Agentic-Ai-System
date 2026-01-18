from fastapi import FastAPI
from fastapi import Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os


from api.schemas import RunTaskRequest, RunTaskResponse

from llm.llm_loader import TinyLlamaChatLLM
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.critic import CriticAgent

from tools.tool_router import ToolRouter
from memory.qdrant_store import QdrantMemory

app = FastAPI(title="Agentic AI System", version="1.0")
# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# ✅ Initialize once (global)
llm = TinyLlamaChatLLM()
memory = QdrantMemory()

planner = PlannerAgent(llm)
critic = CriticAgent()

tool_router = ToolRouter(llm=llm, memory=memory)
executor = ExecutorAgent(tool_router=tool_router, critic_agent=critic, max_retries=2)

@app.get("/")
def home():
    file_path = os.path.join("static", "index.html")
    return FileResponse(file_path)



@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run-task", response_model=RunTaskResponse)
def run_task(req: RunTaskRequest):
    goal = req.goal

    try:
        plan = planner.create_plan(goal)
    except Exception:
        # ✅ fallback plan (guaranteed executable)
        plan = {
    "goal": goal,
    "subtasks": [
        {"id": 1, "task": goal, "tool": "search"},
        {"id": 2, "task": goal, "tool": "retrieval"},
        {"id": 3, "task": goal, "tool": "llm"}
    ]
}


    # Ensure retrieval step exists
    plan["subtasks"].insert(1, {"id": 99, "task": goal, "tool": "retrieval"})

    result = executor.execute(plan)

    return RunTaskResponse(
        goal=goal,
        plan=plan,
        final_output=result["final_output"],
        logs=result["logs"],
        memory_used=True
    )

    

@app.get("/memory/stats")
def memory_stats():
    return {
        "collection": memory.collection_name,
        "points_count": memory.count()
    }


@app.get("/memory/search")
def memory_search(q: str = Query(..., min_length=3), k: int = 5):
    results = memory.search(q, limit=k)
    return {
        "query": q,
        "top_k": k,
        "results": results
    }


@app.get("/memory/peek")
def memory_peek(k: int = 5):
    return {
        "top_k": k,
        "items": memory.peek(limit=k)
    }

