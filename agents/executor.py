from tools.llm_tool import llm_summarize

class ExecutorAgent:
    def __init__(self, tool_router, critic_agent=None, max_retries=2):
        self.tool_router = tool_router
        self.critic_agent = critic_agent
        self.max_retries = max_retries

    def _normalize_tool(self, tool: str) -> str:
        t = tool.lower().strip()

        if any(x in t for x in ["google", "bing", "duckduckgo", "news", "search", "browser"]):
            return "search"

        if any(x in t for x in ["retrieval", "rag", "qdrant", "vector", "embed"]):
            return "retrieval"

        if any(x in t for x in ["llm", "summar", "generate", "write", "tensorflow", "pytorch"]):
            return "llm"

        if any(x in t for x in ["critic", "review", "validate", "score", "matplotlib", "plotly"]):
            return "critic"

        if any(x in t for x in ["pandas", "sklearn", "python", "analysis", "code"]):
            return "llm"

        return t

    def execute(self, plan: dict):
        logs = []
        context = {
            "search_results": [],
            "retrieved_docs": []
        }

        final_output = None

        # ------------ STEP EXECUTION ----------
        for step in plan["subtasks"]:
            tool_raw = step.get("tool", "")
            tool = self._normalize_tool(tool_raw)
            task = step.get("task", "")

            logs.append(f"➡️ Step {step.get('id')} tool={tool} (raw={tool_raw}) task={task}")

    # ✅ Handle LLM directly (skip tool_router)
            if tool == "llm":
                final_output = llm_summarize(
                    self.tool_router.llm,
                    task=plan["goal"],
                    context=context)["summary"]
                logs.append("✅ Result type: llm")
                continue

            result = self.tool_router.run(tool, task, context)
            logs.append(f"✅ Result type: {result.get('type')}")

            if result.get("type") == "search":
                results_list = result.get("results", [])
                context["search_results"] = results_list

                if not results_list:
                    final_output = "No reliable answer found because web search returned no results."
                    break
                
                if self.tool_router.memory and isinstance(results_list, list):
                    for item in results_list:
                        title = item.get("title", "")
                        body = item.get("body", "")
                        href = item.get("href", "")
                        text = f"{title}\n{body}\n{href}".strip()

                        if text:
                            self.tool_router.memory.add_text(
                                text,
                                metadata={"source": "web_search", "topic": plan.get("goal", "unknown")}
                            )

            if result.get("type") == "retrieval":
                context["retrieved_docs"] = result.get("results", [])


                if not final_output:
                    final_output = "No output generated."

        # ------------------ CRITIC + RETRY LOOP ---------------
        if self.critic_agent:
            for attempt in range(self.max_retries):
                evaluation = self.critic_agent.evaluate(plan["goal"], final_output)

                logs.append(f"🧠 Critic Score: {evaluation.get('score')} / 10")
                logs.append(f"🧠 Critic is_good: {evaluation.get('is_good')}")
                logs.append(f"🧠 Critic issues: {evaluation.get('issues')}")

                if evaluation.get("is_good") is True or evaluation.get("score", 0) >= 8:
                    logs.append("✅ Output accepted by Critic.")
                    break

                improvements = evaluation.get("improvements", [])
                critic_feedback = "\n".join(improvements) if improvements else "Improve clarity, structure, and completeness."
                logs.append(f"🔁 Retrying with Critic feedback: {critic_feedback}")

                retry_result = llm_summarize(
                    self.tool_router.llm,
                    task=plan["goal"],
                    context=context,
                    critic_feedback=critic_feedback
                )

                final_output = retry_result.get("summary", final_output)

        return {
            "goal": plan["goal"],
            "final_output": final_output,
            "logs": logs
        }
