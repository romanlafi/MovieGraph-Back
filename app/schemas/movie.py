from pydantic import BaseModel
from typing import Optional, List


class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    genres: Optional[List[str]] = []
    imdb_id: Optional[str] = None
    poster_url: Optional[str] = None
    rated: Optional[str] = None
    released: Optional[str] = None
    runtime: Optional[str] = None
    director: Optional[str] = None
    box_office: Optional[str] = None
    production: Optional[str] = None
    website: Optional[str] = None
    type: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: str

class MovieListResponse(BaseModel):
    imdb_id: str
    title: str
    poster_url: Optional[str] = None
    year: Optional[int] = None
    director: Optional[str] = None
    imdb_rating: Optional[float] = None
    type: Optional[str] = None

def movie_node_to_response(node) -> MovieResponse:
    return MovieResponse(
        id=str(node.id),
        title=node.get("title"),
        year=node.get("year"),
        genres=node.get("genres", []),
        imdb_id=node.get("imdb_id"),
        poster_url=node.get("poster_url"),
        rated=node.get("rated"),
        released=node.get("released"),
        runtime=node.get("runtime"),
        director=node.get("director"),
        box_office=node.get("box_office"),
        production=node.get("production"),
        website=node.get("website"),
        type=node.get("type")
    )

def movie_node_to_list_response(node) -> MovieListResponse:
    return MovieListResponse(
        imdb_id=node.get("imdb_id"),
        title=node["title"],
        poster_url=node.get("poster_url"),
        year=node.get("year"),
        director=node.get("director"),
        imdb_rating=node.get("imdb_rating"),
        type=node.get("type")
    )