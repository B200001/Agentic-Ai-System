from tools.web_search import web_search
from tools.llm_tool import llm_summarize
from tools.retrieval_tool import retrieve_context


class ToolRouter:
    def __init__(self, llm, memory=None):
        self.llm = llm
        self.memory = memory


    def run(self, tool: str, task: str, context: dict):
        tool = tool.lower()

        if tool == "search":
            return web_search(task)

        elif tool == "llm":
            # LLM summarization / reasoning using context
            return llm_summarize(self.llm, task, context)

        elif tool == "retrieval":
            # Day 4 we’ll connect Qdrant RAG
            if self.memory is None:
                return {"type": "retrieval", "results": []}
            return retrieve_context(self.memory, task)

        elif tool == "critic":
            # Day 4 we’ll make critic score output
            return {"type": "critic", "data": "Critic is handled in Executor loop"}
        else:
            raise ValueError(f"Unknown tool: {tool}")
