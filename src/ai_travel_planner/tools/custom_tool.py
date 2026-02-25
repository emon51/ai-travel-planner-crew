import os
import requests
from crewai.tools import tool


@tool("SerperSearchTool")
def serper_search(query: str) -> str:
    """Search the web using Serper Dev API. Input should be a search query string."""
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return "Error: SERPER_API_KEY not set in environment."

    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": query, "num": 5},
    )

    if response.status_code != 200:
        return f"Search failed with status {response.status_code}: {response.text}"

    data = response.json()
    results = []
    for item in data.get("organic", []):
        results.append(f"- {item.get('title')}: {item.get('snippet')} ({item.get('link')})")

    return "\n".join(results) if results else "No results found."


@tool("BudgetCalculatorTool")
def budget_calculator(costs: str) -> str:
    """Calculate total travel costs. Input: comma-separated numbers e.g. '500,300,150,200'"""
    try:
        items = [float(x.strip()) for x in costs.split(",")]
        total = sum(items)
        breakdown = "\n".join([f"Item {i+1}: ${v:.2f}" for i, v in enumerate(items)])
        return f"{breakdown}\nTotal: ${total:.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"
