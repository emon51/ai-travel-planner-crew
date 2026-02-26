import json
import logging
from crewai import Crew
from ai_travel_planner.crew import AiTravelPlanner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def get_user_input() -> dict:
    print("\n=== AI Travel Planner ===\n")
    destination = input("Destination: ").strip()
    start_date = input("Start date (e.g. 2025-06-01): ").strip()
    end_date = input("End date (e.g. 2025-06-07): ").strip()
    budget = input("Total budget (e.g. $1500): ").strip()
    preferences = input("Preferences (optional, e.g. adventure, vegetarian): ").strip() or "none"
    return {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "preferences": preferences,
    }


def run():
    inputs = get_user_input()
    log.info(f"Starting travel planner for: {inputs['destination']}")

    planner = AiTravelPlanner()
    crew: Crew = planner.crew()
    result = crew.kickoff(inputs=inputs)

    # Extract each task output individually
    tasks_output = crew.tasks
    research_out = str(tasks_output[0].output) if tasks_output[0].output else ""
    budget_out   = str(tasks_output[1].output) if tasks_output[1].output else ""
    itinerary_out = str(tasks_output[2].output) if tasks_output[2].output else ""
    validation_out = str(tasks_output[3].output) if tasks_output[3].output else ""

    output = {
        "travel_plan": f"Travel Plan: {inputs['destination']}",
        "travel_dates": f"{inputs['start_date']} to {inputs['end_date']}",
        "destination_overview": research_out,
        "budget_breakdown": budget_out,
        "day_wise_itinerary": itinerary_out,
        "validation_summary": validation_out,
    }

    print("\n=== Travel Plan Output ===\n")
    print(json.dumps(output, indent=2))

    with open("travel_plan_output.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("Output saved to travel_plan_output.json")


if __name__ == "__main__":
    run()
