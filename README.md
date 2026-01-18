# Autonomous Agentic AI System (Planner → Executor → Critic + Memory/RAG)

An autonomous multi-agent AI system that takes a user goal, breaks it into steps, executes tools like web search and retrieval (RAG), and improves its final output using a critic feedback loop.

✅ Includes a FastAPI backend + Tailwind homepage UI to run tasks live.

---

# Autonomous Agentic AI System (Planner → Executor → Critic + Memory/RAG)

An autonomous multi-agent AI system that takes a user goal, breaks it into steps, executes tools like web search and retrieval (RAG), and improves its final output using a critic feedback loop.

✅ Includes a FastAPI backend + Tailwind homepage UI to run tasks live.

---

## 🚀 What This Project Does

Given a goal like:

> "Analyze recent AI trends and summarize key risks"

The system will:

1. **Plan** the task into subtasks (Planner Agent)
2. **Execute** each step using tools like search + retrieval (Executor Agent)
3. **Retrieve memory context** from Qdrant (RAG)
4. **Generate** a structured response using an open-source LLM
5. **Evaluate & retry** output based on Critic feedback

---

## 🧠 Architecture

**Planner → Executor → Critic → Memory (Qdrant + RAG)**

### ✅ System Design Diagram (High Level)

text
            ┌──────────────────────────┐
            │        User / UI         │
            │  (Postman / Web Form)    │
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │        FastAPI API        │
            │     POST /run-task        │
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │       Planner Agent       │
            │ Goal → JSON Plan/Subtasks │
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │      Executor Agent       │
            │ Runs steps + manages ctx  │
            └───────┬─────────┬────────┘
                    │         │
        ┌───────────▼───┐     ▼
        │ Search Tool     │  ┌─────────────────┐
        │ (ddgs web search│  │ Retrieval Tool   │
        └───────────┬────┘  │ (Qdrant RAG)     │
                    │       └─────────┬───────┘
                    │                 │
                    ▼                 ▼
          ┌──────────────────────────────┐
          │   Long-Term Memory (Qdrant)  │
          │ store + similarity retrieval │
          └──────────────────────────────┘
                    │
                    ▼
            ┌──────────────────────────┐
            │        LLM Tool           │
            │ Summarize + format output │
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │       Critic Agent        │
            │ Score + Retry if needed   │
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │       Final Output        │
            │ Summary + Key Risks       │
            └──────────────────────────┘


## 🚀 What This Project Does

Given a goal like:

> "Analyze recent AI trends and summarize key risks"

The system will:

1. **Plan** the task into subtasks (Planner Agent)
2. **Execute** each step using tools like search + retrieval (Executor Agent)
3. **Retrieve memory context** from Qdrant (RAG)
4. **Generate** a structured response using an open-source LLM
5. **Evaluate & retry** output based on Critic feedback

---

## 🧠 Architecture

**Planner → Executor → Critic → Memory (Qdrant + RAG)**

### Agents
- **Planner Agent**: Converts a goal into a JSON-based execution plan
- **Executor Agent**: Runs plan steps and routes to tools
- **Critic Agent**: Scores output quality and triggers retries for better results

### Tools
- **search**: DuckDuckGo web search (ddgs)
- **retrieval**: Qdrant similarity search (RAG)
- **llm**: Summarization + formatting
- **critic**: Rule-based evaluation

---

## 🌟 Key Features

- Multi-agent planning + execution workflow
- Tool routing with **normalization** to handle hallucinated tool names
- Long-term memory using **Qdrant Vector DB**
- RAG-based context injection for grounded responses
- Self-improving feedback loop using Critic + retries
- FastAPI service + Swagger docs
- Homepage UI (Tailwind) with a **Try API** form

---

## 🛠️ Tech Stack

- **Python**
- **HuggingFace Transformers**
- **TinyLlama (Open-source LLM)**
- **SentenceTransformers (Embeddings)**
- **Qdrant (Vector Database)**
- **FastAPI + Uvicorn**
- **Docker + Docker Compose**
- **HTML + Tailwind CSS (UI)**

---

## 📌 API Endpoints

- `GET /` → Homepage UI  
- `GET /docs` → Swagger API docs  
- `POST /run-task` → Run Planner → Executor → Critic pipeline  
- `GET /memory/stats` → Memory collection stats  
- `GET /memory/search?q=...&k=5` → Search stored memory  
- `GET /memory/peek?k=5` → Preview stored memory  

---

## ▶️ Run Locally

### 1) Start Qdrant
```bash
docker compose up -d
uvicorn api.main:app --reload
