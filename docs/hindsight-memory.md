# Hindsight Integration Guide

**Hindsight by Vectorize** is an open-source AI agent memory system that organizes information into a biomimetic structure—combining facts, entities, a knowledge graph, and temporal reasoning.

## Core Memory Primitives in Decision Memory

### 1. `retain`
Stores organizational experiences extracted from decisions, feedback, rejected alternatives, and outcomes.
- **Parameters**: `bank_id`, `content`, `metadata`
- **Usage**: Automatically triggered upon creating a Product Decision, Engineering ADR, Experiment Completion, or Outcome.

```python
hindsight_service.retain(
    content="Engineering Decision: PostgreSQL was selected for search optimization. Elasticsearch was evaluated but rejected due to operational complexity at current scale.",
    metadata={"memory_type": "ENGINEERING_DECISION", "technology": "PostgreSQL"}
)
```

### 2. `recall`
Retrieves historical memories using parallel search strategies (vector similarity, graph entity relationships, keyword matching, and temporal indexing).
- **Parameters**: `bank_id`, `query`, `top_k`
- **Usage**: Triggered by Decision Advisor before generating recommendations.

```python
memories = hindsight_service.recall(
    query="Should we migrate search to Elasticsearch?",
    top_k=5
)
```

### 3. `reflect`
Executes an autonomous agentic loop to search memory, analyze disposition, and synthesize reasoned conclusions based on historical knowledge.
- **Parameters**: `bank_id`, `query`
- **Usage**: Synthesizes complex cross-domain historical trends across product and engineering decisions.

```python
reflection = hindsight_service.reflect(
    query="What have we learned across all search relevance decisions?"
)
```

## Resilience & High Availability Fallback

If external Hindsight Cloud endpoint credentials are unset or unreachable, the application proxy seamlessly falls back to the integrated high-performance local experience store in PostgreSQL, ensuring 100% uptime while reporting transparent connection status.
