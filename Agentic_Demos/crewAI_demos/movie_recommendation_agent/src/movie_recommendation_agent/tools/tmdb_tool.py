import os
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# 🔹 Input Schema
class MovieRecommendationInput(BaseModel):
    genre: str = Field(..., description="Genre of movies, e.g., action, comedy, drama, sci-fi, etc.")
    year: int | None = Field(None, description="Release year of movies (optional). Example: 2025.")

# 🔹 CrewAI Tool
class TMDBRecommendationTool(BaseTool):
    name: str = "tmdb_movie_recommendations"
    description: str = "Fetch top movie recommendations from TMDB based on genre and optional release year."
    args_schema: type[BaseModel] = MovieRecommendationInput

    def _run(self, genre: str, year: int | None = None) -> str:
        genre_map = {
            "action": 28,
            "comedy": 35,
            "drama": 18,
            "thriller": 53,
            "horror": 27,
            "sci-fi": 878,
            "animation": 16,
        }

        genre_id = genre_map.get(genre.lower(), None)
        if genre_id is None:
            return f"Genre '{genre}' not found in list."

        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "sort_by": "popularity.desc",
            "with_genres": genre_id,
            "include_adult": "false",  # safer default
            "language": "en-US",
            "page": 1,
        }

        if year:
            params["primary_release_year"] = year

        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("results", [])

        if not results:
            return f"No {genre} movies found for year {year if year else 'any year'}."

        recommendations = [
            f"🎬 {movie['title']} ({movie.get('release_date', 'N/A')[:4]})"
            for movie in results[:5]  # limit top 5
        ]
        return "\n".join(recommendations)
