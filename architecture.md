# Architecture Diagram

## Flow
```
User Input (destination, dates, budget, preferences)
        │
        ▼
    main.py (entry point)
        │
        ▼
  AiTravelPlanner Crew (sequential process)
        │
        ├──▶ [1] Destination Researcher
        │         └── Tool: SerperSearchTool (web search)
        │         └── Output: Destination overview + highlights
        │
        ├──▶ [2] Budget Planner
        │         └── Tool: SerperSearchTool + BudgetCalculatorTool
        │         └── Output: Cost breakdown per category
        │
        ├──▶ [3] Itinerary Designer
        │         └── Tool: SerperSearchTool
        │         └── Context: research_task + budget_task
        │         └── Output: Day-wise itinerary
        │
        └──▶ [4] Validation Agent
                  └── Tool: BudgetCalculatorTool
                  └── Context: all previous tasks
                  └── Output: Validation summary + risks

Final Output: travel_plan_output.json
```
