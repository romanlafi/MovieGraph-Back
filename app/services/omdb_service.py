import os
from http import HTTPStatus

import httpx
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def fetch_movie_data(title: str) -> dict | None:
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    response = httpx.get(url)
    if response.status_code == HTTPStatus.OK:
        data = response.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": int(data.get("Year")) if data.get("Year") else None,
                "genres": data.get("Genre", "").split(", "),
                "imdb_id": data.get("imdbID"),
                "poster_url": data.get("Poster"),
                "rated": data.get("Rated"),
                "released": data.get("Released"),
                "runtime": data.get("Runtime"),
                "director": data.get("Director"),
                "box_office": data.get("BoxOffice"),
                "production": data.get("Production"),
                "website": data.get("Website"),
                "type": data.get("Type")
            }
    return None