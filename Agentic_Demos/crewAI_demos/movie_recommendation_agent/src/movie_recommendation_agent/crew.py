from crewai import Agent, Task, Crew, Process
from crewai.project import agent, task, crew
from .tools.omdb_tool import OMDBMovieTool
from .tools.tmdb_tool import TMDBRecommendationTool
from crewai.memory import LongTermMemory

@crew
class MovieCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # --- Agents ---
    @agent
    def supervisor(self) -> Agent:
        return Agent(
            config=self.agents_config["supervisor"],
            verbose=True
        )

    @agent
    def recommendation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["recommendation_agent"],
            tools=[TMDBRecommendationTool()],
            verbose=True
        )

    @agent
    def plot_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["plot_agent"],
            tools=[OMDBMovieTool()],
            verbose=True
        )

    # --- Tasks ---
    @task
    def recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config["recommendation_task"]
        )

    @task
    def plot_task(self) -> Task:
        return Task(
            config=self.tasks_config["plot_task"]
        )

    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,  # 👈 Supervisor routing
            manager_agent=self.supervisor(),
            verbose=True,
            memory=LongTermMemory(
            namespace="movie_research",
            type="vector",
            config={
                "path": "memory/movie_memory.db"  # local file storage
            }
        )
        )

