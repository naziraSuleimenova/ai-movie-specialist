from langchain.tools import tool
import os
from dotenv import load_dotenv
import requests

load_dotenv()

omdb_api_key = os.getenv("OMDB_API_KEY")

@tool
def get_movie_information(title: str) -> dict:
  """Return full movie information
  Args:
    title: Exact movie title
  Returns:
    dict: Full movie information(Year, Plot, Genre, Rate etc)
  """
  try:
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={omdb_api_key}")
    return response.json()
  except:
    print("Could not load full movie information")
  

@tool
def get_movies(title: str) -> dict:
  """Return movies that match the title
  Args:
    title: Movie tile
  Returns:
    dict: List of movies that match given title
  """
  try:
    response = requests.get(f"http://www.omdbapi.com/?s={title}&apikey={omdb_api_key}")
    return response.json()
  except:
    print("Could not get movies")

@tool
def get_movie_plot(title: str) -> str:
  """Return movie full plot by exact title
  Args:
    title: Exact movie title
  Returns:
    str: Full movie plot
  """
  try:
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={omdb_api_key}")
    return response.json()["Plot"]
  except:
    print("Could not get movie plot")

