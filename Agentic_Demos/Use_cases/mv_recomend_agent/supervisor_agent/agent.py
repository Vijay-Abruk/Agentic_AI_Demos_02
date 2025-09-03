from google.adk.agents import Agent
from .supervisor_tool import supervisor_router

root_agent = Agent(
    name="supervisor_agent",
    model="gemini-2.5-flash-lite",
    description="Supervisor agent that decides which movie agent to call.",
    instruction="Route user queries to either the movie recommendation agent or movie details agent.",
    tools=[supervisor_router]
)
