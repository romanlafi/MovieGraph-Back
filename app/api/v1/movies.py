from fastapi import APIRouter

from app.schemas.movie import MovieResponse, MovieCreate
from app.services.movie_service import register_movie

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate):
    node = register_movie(movie)
    return {
        "id": str(node.id),
        "title": node["title"],
        "year": node.get("year"),
        "genres": node.get("genres", []),
        "imdb_id": node.get("imdb_id"),
        "poster_url": node.get("poster_url")
    }