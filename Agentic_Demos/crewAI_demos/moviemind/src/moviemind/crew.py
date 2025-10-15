from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.llm import LLM
from src.moviemind.tools.tmdb_tool import TMDbTool  # Fixed import path
from src.moviemind.tools.omdb_tool import OMDbTool   # Fixed import path
from dotenv import load_dotenv
from typing import List
import os

# Load environment variables
load_dotenv()


@CrewBase
class Moviemind():
    """Moviemind crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Debug: Check if API keys are loaded
        self.tmdb_api_key = os.getenv("TMDB_API_KEY")
        self.omdb_api_key = os.getenv("OMDB_API_KEY")
        
        print(f"TMDB_API_KEY available: {bool(self.tmdb_api_key)}")
        print(f"OMDB_API_KEY available: {bool(self.omdb_api_key)}")

    @agent
    def supervisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['supervisor_agent'],
            verbose=True,
            allow_delegation=True,
        )

    @agent
    def movie_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['MovieRecommender'],
            verbose=True,
            tools=[TMDbTool(api_key=self.tmdb_api_key)],
        )
    
    @agent
    def movie_plot_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['PlotFetcher'],
            verbose=True,
            tools=[OMDbTool(api_key=self.omdb_api_key)],
        )

    @task
    def Smart_Movie_Request_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Smart_Movie_Request_Task'],
            output_file='movie_response.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Moviemind crew"""
        return Crew(
            agents=[
                self.supervisor_agent(),
                self.movie_recommender(),
                self.movie_plot_analyst()
            ],
            tasks=[self.Smart_Movie_Request_Task()],  # Single intelligent task
            process=Process.hierarchical,
            manager_llm='gemini/gemini-2.0-flash',
            verbose=True,
        )