from pydantic import BaseModel
from typing import Optional, List


class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    genres: Optional[List[str]] = []
    imdb_id: Optional[str] = None
    poster_url: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: str