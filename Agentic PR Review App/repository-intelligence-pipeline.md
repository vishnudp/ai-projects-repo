Git Clone
   │
   ▼
Repository Hash
   │
   ├──── Cache HIT ──────► Existing Analysis
   │
   └──── Cache MISS
            │
            ▼
       File Scanner
            │
       ┌────┼─────────┐
       ▼    ▼         ▼
      AST  Imports   Git
       │    │         │
       └────┼─────────┘
            ▼
       Dependency Graph
            │
            ▼
        Index Files
            │
            ▼
       Semantic Search