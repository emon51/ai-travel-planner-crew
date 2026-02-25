# Mandatory Analysis

## Why Multi-Agent?
Each agent has a single responsibility — research, budgeting, itinerary, validation.
This separation improves accuracy, makes debugging easier, and allows parallel scaling.

## What if Serper Returns Incorrect Data?
The validation agent cross-checks outputs for consistency. Incorrect search results
will surface as logical conflicts in the itinerary or budget, which get flagged in
the validation summary.

## What if Budget is Unrealistic?
The budget planner uses the calculator tool to compute exact totals and explicitly
flags if estimated costs exceed the provided budget in its output.

## Hallucination Risks
LLMs may fabricate attraction names or costs. Serper grounds the researcher agent
in real web data. The validation agent adds a second layer of review to catch
inconsistencies.

## Token Usage
Sequential processing means each agent only receives its relevant context.
Task chaining via `context` field limits redundant token usage across agents.

## Scalability
New agents (e.g. weather, visa checker) can be added independently without
modifying existing agents or tasks. The sequential process can be switched to
hierarchical for parallel execution at scale.
