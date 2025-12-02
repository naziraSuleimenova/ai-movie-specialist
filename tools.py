from langchain.tools import tool
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

omdb_api_key = os.getenv("OMDB_API_KEY")

@tool
def get_movie_information(title: str) -> str:
  """Return full movie information
  Args:
    title: Exact movie title
  Returns:
    Full movie information
  """
  response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={omdb_api_key}")
  return response.json()
  

@tool
def get_movies(title: str) -> str:
  """Return movies that match the title
  Args:
    title: Movie tile
  Returns:
    Movies that match given title
  """
  response = requests.get(f"http://www.omdbapi.com/?s={title}&apikey={omdb_api_key}")
  return response.json()

@tool
def get_movie_plot(title: str) -> str:
  """Return movie full plot by exact title
  Args:
    title: Exact movie tile
  Returns:
    Full movie plot
  """
  response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={omdb_api_key}")
  return response.json()["Plot"]

