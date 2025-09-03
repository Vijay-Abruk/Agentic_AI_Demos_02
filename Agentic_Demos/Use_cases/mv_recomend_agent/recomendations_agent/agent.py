from .tmdb_tool import get_movie_recommendations
from google.adk.agents import Agent
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

root_agent = Agent(
    name="recommendations_agent",
    model="gemini-2.5-flash-lite",
    description="Agent to get the top movies by genre and optionaly year using the provided tools",
    instruction="I can answer recommend you movies by your favourite genre and release year",
    tools=[get_movie_recommendations]
)



