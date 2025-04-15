from fastapi import APIRouter, Depends, Query

from app.deps.auth import get_current_user
from app.schemas.movie import MovieListResponse
from app.services.movie_service import search_movies

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/search", response_model=list[MovieListResponse])
def search_movies_route(
    query: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    current_user=Depends(get_current_user)
):
    return search_movies(query=query, page=page, limit=limit)
