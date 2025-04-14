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
