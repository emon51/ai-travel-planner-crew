import json
import logging
from crewai import Crew
from ai_travel_planner.crew import AiTravelPlanner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# Groq pricing for llama-3.3-70b-versatile (per 1M tokens)
COST_PER_1M_INPUT  = 0.59
COST_PER_1M_OUTPUT = 0.79


def get_user_input() -> dict:
    print("\n=== AI Travel Planner ===\n")
    destination = input("Destination: ").strip()
    start_date  = input("Start date (e.g. 2025-06-01): ").strip()
    end_date    = input("End date (e.g. 2025-06-07): ").strip()
    budget      = input("Total budget (e.g. $1500): ").strip()
    preferences = input("Preferences (optional, e.g. adventure, vegetarian): ").strip() or "none"
    return {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "preferences": preferences,
    }


def calc_token_stats(usage):
    """Calculate cost and average token stats from crew usage metrics."""
    prompt_tokens     = getattr(usage, "prompt_tokens", 0) or 0
    completion_tokens = getattr(usage, "completion_tokens", 0) or 0
    total_tokens      = getattr(usage, "total_tokens", 0) or (prompt_tokens + completion_tokens)
    api_calls         = getattr(usage, "successful_requests", 0) or 1

    input_cost  = (prompt_tokens / 1_000_000) * COST_PER_1M_INPUT
    output_cost = (completion_tokens / 1_000_000) * COST_PER_1M_OUTPUT
    total_cost  = input_cost + output_cost
    avg_tokens  = total_tokens / api_calls if api_calls else 0

    return {
        "total_tokens": total_tokens,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "api_calls": api_calls,
        "total_api_cost_usd": round(total_cost, 6),
        "avg_tokens_per_api_call": round(avg_tokens, 2),
    }


def run():
    inputs = get_user_input()
    log.info(f"Starting travel planner for: {inputs['destination']}")

    planner = AiTravelPlanner()
    crew: Crew = planner.crew()
    result = crew.kickoff(inputs=inputs)

    # Extract per-task outputs
    tasks = crew.tasks
    research_out   = str(tasks[0].output) if tasks[0].output else ""
    budget_out     = str(tasks[1].output) if tasks[1].output else ""
    itinerary_out  = str(tasks[2].output) if tasks[2].output else ""
    validation_out = str(tasks[3].output) if tasks[3].output else ""

    # Token & cost stats
    stats = calc_token_stats(result.token_usage)

    output = {
        "travel_plan": f"Travel Plan: {inputs['destination']}",
        "travel_dates": f"{inputs['start_date']} to {inputs['end_date']}",
        "destination_overview": research_out,
        "budget_breakdown": budget_out,
        "day_wise_itinerary": itinerary_out,
        "validation_summary": validation_out,
        "token_usage": stats,
    }

    print("\n=== Travel Plan Output ===\n")
    print(json.dumps(output, indent=2))

    # Save JSON
    with open("travel_plan_output.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("Output saved to travel_plan_output.json")

    # Auto-generate Output.md
    md = f"""# Travel Plan: {inputs['destination']}

**Travel Dates:** {inputs['start_date']} to {inputs['end_date']}
**Budget:** {inputs['budget']}

---

## Destination Overview
{research_out}

---

## Budget Breakdown
{budget_out}

---

## Day-wise Itinerary
{itinerary_out}

---

## Validation Summary
{validation_out}

---

## API & Token Usage Summary

| Metric                      | Value                          |
|-----------------------------|--------------------------------|
| Total Tokens                | {stats['total_tokens']}        |
| Prompt Tokens               | {stats['prompt_tokens']}       |
| Completion Tokens           | {stats['completion_tokens']}   |
| Total API Calls             | {stats['api_calls']}           |
| Total API Cost (USD)        | ${stats['total_api_cost_usd']} |
| Avg Tokens per API Call     | {stats['avg_tokens_per_api_call']} |
"""

    with open("Output.md", "w") as f:
        f.write(md)
    log.info("Output.md generated successfully")


if __name__ == "__main__":
    run()
