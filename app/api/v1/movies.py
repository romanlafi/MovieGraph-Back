from typing import List

from fastapi import APIRouter, Depends, Query

from app.deps.auth import get_current_user
from app.schemas.comment import CommentCreate, CommentResponse
from app.schemas.movie import MovieListResponse, MovieResponse
from app.services.comment_service import create_comment, list_comments
from app.services.movie_service import (
    search_movies,
    like_movie_by_imdb_id,
    unlike_movie_by_imdb,
    get_movies_liked_by_user,
    list_all_genres,
    get_movie_by_imdb,
    search_by_genre
)
from app.services.movie_service_async import search_movies_async

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/search", response_model=list[MovieListResponse])
def search_movies_route(
    query: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
):
    return search_movies(query=query, page=page, limit=limit)

@router.get("/search-async", response_model=List[MovieListResponse])
async def search_movies_async_route(
    query: str,
    page: int = 1,
    limit: int = 10,
):
    return await search_movies_async(query, page, limit)

@router.get("/by_genre", response_model=list[MovieListResponse])
def get_movies_by_genre(
    name: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50)
):
    return search_by_genre(name, page, limit)

@router.get("/", response_model=MovieResponse)
def get_movie(imdb_id: str):
    return get_movie_by_imdb(imdb_id)

@router.post("/like", status_code=200)
def like_movie(
        imdb_id: str = Query(...),
        current_user=Depends(get_current_user)
):
    like_movie_by_imdb_id(current_user["email"], imdb_id)

@router.delete("/like", status_code=200)
def unlike_movie(
    imdb_id: str = Query(...),
    current_user=Depends(get_current_user)
):
    unlike_movie_by_imdb(current_user["email"], imdb_id)

@router.get("/like", response_model=list[MovieListResponse])
def get_liked_movies(current_user=Depends(get_current_user)):
    return get_movies_liked_by_user(current_user["email"])

@router.post("/comment")
def comment_movie(
        movie_id: str = Query(...),
        comment: CommentCreate = Depends(CommentCreate),
        current_user=Depends(get_current_user)
):
    return create_comment(movie_id, current_user["email"], comment)

@router.get("/comments", response_model=list[CommentResponse])
def get_movie_comments(movie_id: str):
    return list_comments(movie_id)

@router.get("/genres", response_model=list[str])
def get_genres():
    return list_all_genres()