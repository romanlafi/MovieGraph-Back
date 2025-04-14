from fastapi import APIRouter

from app.schemas.movie import MovieResponse, MovieCreate
from app.services.movie_service import register_movie

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate):
    return register_movie(movie)
