# Decision Memory: Demo Walkthrough Guide

Follow these steps to demonstrate the end-to-end memory loop:

## STEP 1: Open Feedback
Navigate to `/feedback` and locate:
> `FB-1001`: "Search results are slow and irrelevant for large project datasets."

## STEP 2: Run Memory OFF vs Hindsight ON
1. Click **Analyze with Memory** with **Memory OFF**:
   - Observe the generic technical recommendation (e.g., "Consider UI or database adjustments").
2. Switch to **Hindsight ON**:
   - Observe historical evidence retrieved:
     - Feb 12, 2026 ADR: PostgreSQL search optimization selected.
     - Rejected Alternative: Elasticsearch rejected due to infrastructure complexity.
     - Apr 04, 2026 Outcome: Search latency decreased 42%.

## STEP 3: Ask AI Advisor (Search Migration Scenario)
Navigate to `/advisor` and query:
> *"Should we migrate search to Elasticsearch?"*

1. Click **Side-by-Side Impact Compare**:
   - **Without Memory**: Advises setting up Elasticsearch cluster based on standard architectural patterns.
   - **With Hindsight Memory**: Recalls original scale constraints, Elasticsearch rejection reason, and the 42% latency reduction achieved by tuning PostgreSQL. Recommends benchmarking against original constraints before adding secondary infrastructure.

## STEP 4: Record New Outcome & Verify Future Recall
1. Create a new engineering outcome or decision.
2. Verify that future queries immediately recall the newly retained experience.
