# System Architecture: Decision Memory

**Decision Memory** is an enterprise organizational memory system designed to connect customer feedback, product decisions, engineering decisions (ADRs), experiments, and observed outcomes using Hindsight by Vectorize.

## System Topology & Data Flow

```mermaid
flowchart TD
    User([User / Product Lead / Architect])
    
    subgraph Frontend ["Next.js 14 Web Frontend"]
        UI[App Shell & Navigation]
        Dash[Decision Dashboard]
        AdvConsole[AI Advisor Console]
        MemExp[Memory Explorer]
        EvPanel[Evidence Panel]
    end

    subgraph Backend ["FastAPI Application Backend"]
        API[REST OpenAPI Routes]
        AgentEngine[Decision Agent Engine]
        Analytics[Analytics Aggregator]
        MemoryManager[Decision Memory Manager]
    end

    subgraph Storage ["Durable Persistence Layer"]
        Postgres[(PostgreSQL Database)]
        Hindsight[(Hindsight Memory Bank)]
        Groq[Groq LLM Service]
    end

    User --> UI
    UI --> API
    API --> AgentEngine
    API --> MemoryManager
    API --> Analytics

    MemoryManager --> Postgres
    MemoryManager -->|retain experience| Hindsight

    AgentEngine -->|1. Query relational state| Postgres
    AgentEngine -->|2. Recall historical evidence| Hindsight
    AgentEngine -->|3. Reflect & synthesize| Hindsight
    AgentEngine -->|4. Grounded prompt| Groq

    Groq --> AgentEngine
    AgentEngine --> EvPanel
```

## Architectural Decoupling: PostgreSQL vs Hindsight

| Responsibility | PostgreSQL Datastore | Hindsight by Vectorize |
| :--- | :--- | :--- |
| **Data Nature** | Relational Application State | Durable Organizational Experience |
| **Entities Stored** | Customers, Feedbacks, Decisions, Experiments, Outcomes | Reasoning, Constraints, Rejected Alternatives, Lessons Learned |
| **Search Mechanism** | SQL Indexed Foreign Key Queries | Vector + Graph Traversal + Temporal Search |
| **Primitives** | INSERT / UPDATE / SELECT | retain / recall / reflect |
| **Availability** | Primary Application State | Resilient Proxy Fallback |

## Memory Loop Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Team as Product & Eng Team
    participant FB as Customer Feedback
    participant PD as Product Decision
    participant ED as Engineering ADR
    participant HS as Hindsight Bank
    participant Out as Measured Outcome
    participant Adv as Decision Advisor

    Team->>FB: Record "Search is slow & irrelevant"
    Team->>PD: Define "Improve search relevance"
    Team->>ED: Create ADR "Optimize PostgreSQL for Search"
    Note over ED: Rejected Elasticsearch due to operational complexity
    ED->>HS: Retain Experience (Why chosen, rejected options, constraints)
    
    Team->>Out: Measure Outcome (-42% Search Latency)
    Out->>HS: Retain Measured Outcome & Lesson
    
    Note over Team: 6 Months Later...
    Team->>Adv: "Should we migrate search to Elasticsearch?"
    Adv->>HS: Recall Historical Experiences
    HS-->>Adv: Return Feb 2026 ADR, Rejected Reason & Apr 2026 -42% Latency Outcome
    Adv-->>Team: Grounded Recommendation: "Do not migrate. Evaluate scale against Feb 2026 constraints."
```
