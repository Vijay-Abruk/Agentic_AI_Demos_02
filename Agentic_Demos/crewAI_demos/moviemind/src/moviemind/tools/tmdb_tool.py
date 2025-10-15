from typing import Type, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os
import requests

# Mapping user-friendly genre names to TMDb genres
TMDB_GENRE_MAP = {
    "action": "Action",
    "adventure": "Adventure",
    "animation": "Animation",
    "comedy": "Comedy",
    "crime": "Crime",
    "documentary": "Documentary",
    "drama": "Drama",
    "family": "Family",
    "fantasy": "Fantasy",
    "history": "History",
    "horror": "Horror",
    "music": "Music",
    "mystery": "Mystery",
    "romance": "Romance",
    "science fiction": "Science Fiction",
    "sci-fi": "Science Fiction",
    "tv movie": "TV Movie",
    "thriller": "Thriller",
    "war": "War",
    "western": "Western"
}

def normalize_genre(user_input: str) -> str:
    """Normalize user input into a TMDb genre name."""
    key = user_input.lower().strip()
    return TMDB_GENRE_MAP.get(key, user_input.title())


class TMDbSearchInput(BaseModel):
    genre: str = Field(..., description="Genre of the movies")
    year: str = Field(..., description="Release year of the movies (YYYY)")


class TMDbTool(BaseTool):
    name: str = "TMDb Top Rated Movie Search Tool"
    description: str = "Fetches top-rated movies of a given genre and year using TMDb API"
    args_schema: Type[BaseModel] = TMDbSearchInput

    api_key: Optional[str] = None

    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv("TMDB_API_KEY")
        print(f"TMDb API Key loaded: {bool(self.api_key)}")

    def _run(self, genre: str, year: str) -> str:
        """Fetch top TMDb-rated movies for a genre and year."""
        try:
            if not self.api_key:
                return "TMDb API key is missing."

            genre_name = normalize_genre(genre)
            print(f"Searching top-rated {genre_name} movies from {year}...")

            # Step 1: Get TMDb genre list
            genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={self.api_key}"
            genre_response = requests.get(genre_url)
            if genre_response.status_code != 200:
                return f"Error fetching genres: {genre_response.status_code}"

            genres = genre_response.json().get("genres", [])
            genre_id = next((g["id"] for g in genres if g["name"].lower() == genre_name.lower()), None)
            if not genre_id:
                return f"Genre '{genre_name}' not found."

            # Step 2: Discover movies by genre ID and release year
            # Sort by vote_average.desc and filter out low vote_count for reliability
            discover_url = (
                f"https://api.themoviedb.org/3/discover/movie"
                f"?api_key={self.api_key}"
                f"&with_genres={genre_id}"
                f"&primary_release_year={year}"
                f"&sort_by=vote_average.desc"
                f"&vote_count.gte=50"
            )
            discover_response = requests.get(discover_url)
            if discover_response.status_code != 200:
                return f"Error fetching movies: {discover_response.status_code}"

            movies = discover_response.json().get("results", [])
            if not movies:
                return f"No top-rated {genre_name} movies found from {year}."

            # Step 3: Get top 5 movie details
            movie_list = []
            for movie in movies[:5]:
                title = movie.get("title", "Unknown Title")
                release_date = movie.get("release_date", "Unknown")
                release_year = release_date.split("-")[0] if release_date != "Unknown" else "Unknown"
                rating = movie.get("vote_average", "N/A")
                movie_list.append(f"{title} ({release_year}) - ⭐ {rating}")

            return "\n".join(movie_list)

        except Exception as e:
            return f"TMDbTool error: {e}"
