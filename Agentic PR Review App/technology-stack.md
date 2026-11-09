┌──────────────────────────────────────────────────────────┐
│                    UI / Control Plane                    │
│                 Streamlit / Angular UI                   │
│                                                          │
│ Progress | Agent status | Time | Logs | HITL | Artifacts│
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                     FastAPI API Layer                    │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                     LangGraph Engine                     │
│                                                          │
│ State | Routing | Parallelism | Retry | HITL | Checkpoint│
└────────────────────────────┬─────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
       Agent Layer                     Tool Layer
              │                             │
              ▼                             ▼
        Ollama LLM                 Jira / Git / AST
        Local Models               NPM / Angular
                                  Playwright / Docker
              │
              ▼
       Guardrail Layer
              │
              ▼
       Cache / Artifact Layer
              │
              ▼
       SQLite / JSON / Files