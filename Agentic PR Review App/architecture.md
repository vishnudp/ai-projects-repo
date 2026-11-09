USER
 │
 ▼
Requirement Intake
 │
 ▼
Requirement Analysis
 │
 ▼
Clarification
 │
 ▼
BRD Generation
 │
 ▼
BRD Validation
 │
 ▼
Human Approval
 │
 ▼
Product / Planning
 │
 ▼
Epic / Story / Task
 │
 ▼
Jira
 │
 ▼
Repository Intelligence
 │
 ├── Current Code
 ├── AST
 ├── Dependencies
 ├── Git History
 └── Jira History
 │
 ▼
Historical Impact Analysis
 │
 ▼
Architecture
 │
 ├── Security
 ├── API
 └── Integration
 │
 ▼
Frontend Agent
 │
 ▼
Code Changes
 │
 ▼
┌────────────────────────────────────────────┐
│             TESTING DOMAIN                 │
│                                            │
│ Strategy                                   │
│ Planning                                   │
│ Test Cases                                 │
│ Unit                                       │
│ Component                                  │
│ Integration                                │
│ E2E                                        │
│ Regression                                 │
│ Accessibility                              │
│ Security                                   │
│ Performance                                │
│ Quality Gate                               │
└───────────────────┬────────────────────────┘
                    │
                    ▼
              Review Agent
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
      FAIL                     PASS
        │                       │
        ▼                       ▼
 Frontend Agent              DevOps
        │                       │
        └───────► Re-test       ▼
                             Docker
                               │
                               ▼
                          Deployment
                               │
                               ▼
                          Monitoring
                               │
                               ▼
                            Release
                               │
                               ▼
                             Audit