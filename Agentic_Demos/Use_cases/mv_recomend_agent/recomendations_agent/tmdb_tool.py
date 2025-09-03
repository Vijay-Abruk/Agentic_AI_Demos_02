import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure TMDB_API_KEY is loaded
os.environ["TMDB_API_KEY"] = os.getenv("TMDB_API_KEY")

def get_movie_recommendations(genre: str = "action", year: int = 2025) -> list[str] | str:
    """
    Fetches top movie recommendations from TMDB based on genre and an optional release year.

    Args:
        genre (str): The genre of movies to recommend (e.g., "action", "comedy", "drama").
                     Defaults to "action".
        year (int, optional): The primary release year to filter movies by.
                              Defaults to None, meaning no year filter is applied.

    Returns:
        list[str]: A list of formatted strings, each containing a movie title and its release date.
                   Example: ["Movie Title (YYYY-MM-DD)", "Another Movie (YYYY-MM-DD)"].
        str: An error message if the specified genre is not found or no movies are found for the criteria.
    """
    genre_map = {
        "action": 28,
        "comedy": 35,
        "drama": 18,
        "thriller": 53,
        "horror": 27,
        "sci-fi": 878,
        "animation": 16
    }

    genre_id = genre_map.get(genre.lower(), None)

    if genre_id is None:
        return f"Genre '{genre}' not found in list."

    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": os.environ["TMDB_API_KEY"],
        "sort_by": "popularity.desc",
        "with_genres": genre_id,
        "include_adult": "true", # Note: Setting this to true might return adult content.
                                 # Consider if this is the desired default behavior.
        "language": "en-US",
        "page": 1
    }

    if year:
        params["primary_release_year"] = year

    response = requests.get(url, params=params)
    data = response.json()

    results = data.get("results", [])

    if not results:
        return f"No {genre} movies found for year {year if year else 'any year'}."

    return [f"{movie['title']} ({movie.get('release_date', 'N/A')})" for movie in results]