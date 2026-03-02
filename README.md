# AI Travel Planner — Multi-Agent CrewAI System

A multi-agent AI travel planner built with **CrewAI**, **Groq LLM**, and **Serper Dev API**. Given a destination, travel dates, budget and preferences — it autonomously researches, plans and validates a complete travel itinerary.

---

## Architecture
```
User Input (destination, dates, budget, preferences)
        │
        ▼
  AiTravelPlanner Crew (sequential process)
        │
        ├──▶ [1] Destination Researcher  → SerperSearchTool
        │         Searches web for attractions, culture, tips
        │
        ├──▶ [2] Budget Planner          → SerperSearchTool + BudgetCalculatorTool
        │         Estimates costs per category, verifies total
        │
        ├──▶ [3] Itinerary Designer      → SerperSearchTool
        │         Builds day-by-day plan (uses output of 1 & 2)
        │
        └──▶ [4] Validation Agent        → BudgetCalculatorTool
                  Reviews full plan for consistency & feasibility
                  (uses output of 1, 2 & 3)
        │
        ▼
  Output.md + travel_plan_output.json (auto-generated locally)
```

---

## Agents & Tools

| Agent | Tools Used | Responsibility |
|---|---|---|
| Destination Researcher | SerperSearchTool | Attractions, culture, travel tips |
| Budget Planner | SerperSearchTool, BudgetCalculatorTool | Cost breakdown per category |
| Itinerary Designer | SerperSearchTool | Conflict-free day-wise itinerary |
| Validation Agent | BudgetCalculatorTool | Budget alignment, risks, assumptions |

---

## Prerequisites

Before starting, make sure you have:

- **Python 3.10 – 3.13** → [Download](https://python.org/downloads)
- **Git** → [Download](https://git-scm.com)
- **Groq API key** (free) → [console.groq.com](https://console.groq.com)
- **Serper API key** (free) → [serper.dev](https://serper.dev)

---

## Setup instructions

### 1. Install `uv`

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After install, add to PATH if needed:
```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify:
```bash
uv --version
```

---

### 2. Install CrewAI CLI
```bash
uv tool install crewai
```

Verify:
```bash
crewai --version
```

---

### 3. Clone the Repository
```bash
git clone https://github.com/emon51/ai-travel-planner-crew.git
cd ai-travel-planner-crew
```

---

### 4. Install Dependencies
```bash
crewai install
```

This installs all dependencies defined in `pyproject.toml`:
```toml
dependencies = [
    "apscheduler>=3.11.2",
    "crewai-tools>=1.9.3",
    "crewai[google-genai,tools]==1.9.3",
    "fastapi>=0.133.1",
    "fastapi-sso>=0.21.0",
    "litellm>=1.75.3",
    "pydantic[email]>=2.11.10",
]
```

---

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```bash
cat > .env << 'ENVEOF'
MODEL=groq/llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
ENVEOF
```

Replace the placeholder values with your real API keys:
- Get Groq key: [console.groq.com](https://console.groq.com) → API Keys → Create
- Get Serper key: [serper.dev](https://serper.dev) → Dashboard → API Key


---

### 6. Run the Planner
```bash
crewai run
```

You will be prompted to enter:
```
Destination: Bangkok, Thailand
Start date (e.g. 2025-06-01): 2025-06-01
End date (e.g. 2025-06-07): 2025-06-07
Total budget (e.g. $1500): $1500
Preferences (optional, e.g. adventure, vegetarian): street food, temples
```

---

## Output

After a successful run, two files are auto-generated locally (not tracked in git):

**`travel_plan_output.json`** — structured JSON:
```json
{
  "travel_plan": "Travel Plan: Bangkok, Thailand",
  "travel_dates": "2025-06-01 to 2025-06-07",
  "destination_overview": "...",
  "budget_breakdown": "...",
  "day_wise_itinerary": "...",
  "validation_summary": "...",
  "token_usage": {
    "total_tokens": 3200,
    "prompt_tokens": 2800,
    "completion_tokens": 400,
    "api_calls": 6,
    "total_api_cost_usd": 0.002,
    "avg_tokens_per_api_call": 533.33
  }
}
```

**`Output.md`** — full markdown report with:
- Destination Overview
- Budget Breakdown
- Day-wise Itinerary
- Validation Summary (budget status, assumptions, risk factors)
- API & Token Usage Summary table

---

## Project Structure
```
ai-travel-planner-crew/           # Root directory
├── .env                          # API keys (not tracked)
├── .gitignore
├── pyproject.toml
├── analysis.md                   # Mandatory analysis section
├── architecture.md               # Architecture diagram
├── README.md
├── uv.lock
└── src/
    └── ai_travel_planner/
        ├── main.py               # Entry point, output generation
        ├── crew.py               # Crew + agent + task wiring
        ├── tools/
        │   └── custom_tool.py    # SerperSearchTool, BudgetCalculatorTool
        └── config/
            ├── agents.yaml       # Agent definitions
            └── tasks.yaml        # Task definitions with context chaining

```

---

## Assignment Rules Followed

- No hardcoded travel data
- No faked cost estimates
- Serper API mandatory for all web search (no other search tools)
- Minimum 4 agents enforced
- Multi-agent sequential architecture
- Structured JSON + Markdown output
- Execution flow logged throughout

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `uv: command not found` | Run `export PATH="$HOME/.local/bin:$PATH"` |
| `SERPER_API_KEY 403` | Check key is valid at serper.dev dashboard |
| `429 Rate limit` | Wait 1 minute and retry (free tier limit) |
| `No module named 'src'` | Always run via `crewai run`, not `python main.py` |
| `litellm not available` | Run `crewai install` to reinstall all dependencies |
