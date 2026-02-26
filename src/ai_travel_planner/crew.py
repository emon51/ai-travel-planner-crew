import logging
from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ai_travel_planner.tools.custom_tool import serper_search, budget_calculator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

llm = LLM(model="groq/llama-3.3-70b-versatile")


@CrewBase
class AiTravelPlanner:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def destination_researcher(self) -> Agent:
        log.info("Initializing Destination Researcher agent")
        return Agent(config=self.agents_config["destination_researcher"], tools=[serper_search], llm=llm, verbose=True)

    @agent
    def budget_planner(self) -> Agent:
        log.info("Initializing Budget Planner agent")
        return Agent(config=self.agents_config["budget_planner"], tools=[serper_search, budget_calculator], llm=llm, verbose=True)

    @agent
    def itinerary_designer(self) -> Agent:
        log.info("Initializing Itinerary Designer agent")
        return Agent(config=self.agents_config["itinerary_designer"], tools=[serper_search], llm=llm, verbose=True)

    @agent
    def validation_agent(self) -> Agent:
        log.info("Initializing Validation Agent")
        return Agent(config=self.agents_config["validation_agent"], tools=[budget_calculator], llm=llm, verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def budget_task(self) -> Task:
        return Task(config=self.tasks_config["budget_task"])

    @task
    def itinerary_task(self) -> Task:
        return Task(config=self.tasks_config["itinerary_task"])

    @task
    def validation_task(self) -> Task:
        return Task(config=self.tasks_config["validation_task"])

    @crew
    def crew(self) -> Crew:
        log.info("Assembling travel planner crew")
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
