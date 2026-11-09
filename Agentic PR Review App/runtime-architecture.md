                       USER
                        │
                        ▼
                ┌──────────────┐
                │      UI      │
                │ Progress/HITL│
                └──────┬───────┘
                       │
                       ▼
                  FastAPI
                       │
                       ▼
                ┌──────────────┐
                │  LangGraph   │
                │ Orchestrator │
                └──────┬───────┘
                       │
       ┌───────────────┼─────────────────┐
       │               │                 │
       ▼               ▼                 ▼
    Agents          Guardrails        Cache
       │               │                 │
       ▼               ▼                 ▼
    LLM Router     Validators        SQLite
       │
       ▼
     Ollama
       │
       ▼
 Local Models