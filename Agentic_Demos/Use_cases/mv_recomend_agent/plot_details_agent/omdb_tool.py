import requests
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OMDB_API_KEY"] = os.getenv("OMDB_API_KEY")

def get_movie_details(title: str) -> str:
    """
    Fetches details for a given movie title, including its plot, genre, and IMDb rating.

    Args:
        title (str): The exact title of the movie to search for.

    Returns:
        str: A formatted string containing the movie's title, year, IMDb rating, genre, and plot.
             Returns "Movie 'title' not found." if the movie is not found.
    """
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": os.environ["OMDB_API_KEY"],
        "t": title
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("Response") == "False":
        return f"Movie '{title}' not found."

    # Extract required details
    movie_title = data.get("Title", "Title not available.")
    year = data.get("Year", "Year not available.")
    genre = data.get("Genre", "Genre not available.")
    plot = data.get("Plot", "Plot details not available.")
    imdb_rating = data.get("imdbRating", "Rating not available.")

    return (
        f"🎬 {movie_title} ({year})\n"
        f"⭐ IMDb: {imdb_rating}\n"
        f"🎭 Genre: {genre}\n"
        f"📝 Plot: {plot}"
    )