import json
import logging
from ai_travel_planner.crew import AiTravelPlanner

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

    result = AiTravelPlanner().crew().kickoff(inputs=inputs)

    output = {
        "destination": inputs["destination"],
        "travel_dates": f"{inputs['start_date']} to {inputs['end_date']}",
        "budget": inputs["budget"],
        "travel_plan": str(result),
    }

    print("\n=== Travel Plan Output ===\n")
    print(output["travel_plan"])

    with open("travel_plan_output.json", "w") as f:
        json.dump(output, f, indent=2)
    log.info("Output saved to travel_plan_output.json")


if __name__ == "__main__":
    run()
