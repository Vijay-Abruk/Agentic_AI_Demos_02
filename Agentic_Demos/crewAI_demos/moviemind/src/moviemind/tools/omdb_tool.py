from typing import Type, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os
import requests

class OMDbSearchInput(BaseModel):
    title: str = Field(..., description="Title of the movie")

class OMDbTool(BaseTool):
    name: str = "OMDb Plot Search Tool"
    description: str = "Fetches plot details, title, and IMDb rating for a specific movie using OMDb API."
    args_schema: Type[BaseModel] = OMDbSearchInput
    
    api_key: Optional[str] = None

    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv("OMDB_API_KEY")

    def _run(self, title: str) -> str:
        try:
            if not self.api_key:
                return "OMDb API key is missing."

            print(f"Searching for movie: {title}")
            
            # Step 1: Try exact search by title
            url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={title}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data.get("Response") == "True":
                    movie_title = data.get("Title", title)
                    rating = data.get("imdbRating", "N/A")
                    plot = data.get("Plot", "No plot available.")
                    return f"Movie: {movie_title} | IMDb: {rating}\nPlot: {plot}"
                
                # Step 2: If exact search fails, use 's' parameter (search)
                print(f"Exact title '{title}' not found, trying search...")
                search_url = f"http://www.omdbapi.com/?apikey={self.api_key}&s={title}"
                search_response = requests.get(search_url)
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    if search_data.get("Response") == "True" and search_data.get("Search"):
                        # Take the first search result
                        first_result = search_data["Search"][0]
                        exact_title = first_result["Title"]
                        
                        # Fetch full details for the first result
                        exact_url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={exact_title}"
                        exact_response = requests.get(exact_url)
                        
                        if exact_response.status_code == 200:
                            exact_data = exact_response.json()
                            if exact_data.get("Response") == "True":
                                movie_title = exact_data.get("Title", exact_title)
                                rating = exact_data.get("imdbRating", "N/A")
                                plot = exact_data.get("Plot", "No plot available.")
                                return f"Movie: {movie_title} | IMDb: {rating}\nPlot: {plot}"
                        
                        return f"Found movie: {exact_title} but couldn't fetch plot or rating."
                    
                    return f"No movies found with title containing '{title}'."
                
                return f"Movie '{title}' not found: {data.get('Error', 'Unknown error')}"
            
            return f"Error fetching movie: {response.status_code}"
        
        except Exception as e:
            return f"OMDbTool error: {e}"
