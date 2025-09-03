from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class MovieResearchProject:
    """Movie Research Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def movie_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['movie_researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='movie_report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # created by @agent
            tasks=self.tasks,   # created by @task
            process=Process.sequential,
            verbose=True,
            output_log_file=True
        )
