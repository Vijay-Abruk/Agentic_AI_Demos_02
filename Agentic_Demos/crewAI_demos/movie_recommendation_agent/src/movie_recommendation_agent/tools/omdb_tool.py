import os
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()  # Load OMDB_API_KEY from .env
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

class MovieToolInput(BaseModel):
    title: str = Field(..., description="Exact title of the movie to search for.")

class OMDBMovieTool(BaseTool):
    name: str = "omdb_movie_details"
    description: str = "Fetch details (genre, rating, plot) of a specified movie."
    args_schema: type[BaseModel] = MovieToolInput

    def _run(self, title: str) -> str:
        url = "http://www.omdbapi.com/"
        params = {"apikey": OMDB_API_KEY, "t": title}
        resp = requests.get(url, params=params)
        data = resp.json()

        if data.get("Response") == "False":
            return f"Movie '{title}' not found."

        return (
            f"🎬 {data.get('Title', 'N/A')} ({data.get('Year', 'N/A')})\n"
            f"⭐ IMDb: {data.get('imdbRating', 'N/A')}\n"
            f"🎭 Genre: {data.get('Genre', 'N/A')}\n"
            f"📝 Plot: {data.get('Plot', 'N/A')}"
        )
