from .omdb_tool import get_movie_details
from google.adk.agents import Agent
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

root_agent = Agent(
    name="plot_details_agent",
    model="gemini-2.5-flash-lite",
    description="Agent to get the Plot details of the title along with genre and IMDB rating",
    instruction="Provide movie details in this exact format: Title, Year, Genre, IMDb Rating, Plot.",
    tools=[get_movie_details]
)